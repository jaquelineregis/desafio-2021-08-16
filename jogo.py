# -*- coding: utf-8 -*-
import json
import random


MAX_DE_CASAS_NO_TABULEIRO = 20
MAX_FACES_DO_DADO = 6
MAX_DE_RODADAS = 1000
VALOR_INICIAL_DO_TABULEIRO = 15
SIMULACOES = 300

IMPULSIVO = "IMPULSIVO"
EXIGENTE = "EXIGENTE"
CAUTELOSO = "CAUTELOSO"
ALEATORIO = "ALEATORIO"


class Jogador:
    saldo = 300
    posicao_anterior = 0
    posicao_atual = 0
    volta = 0
    turno = 0
    jogando = True
    propriedades = None

    def __init__(self, personalidade):
        self.personalidade = personalidade

    def comprar(self, numero_propriedade, valor_compra, valor_aluguel):
        self.checar_se_pode_continuar_jogando()
        if self.saldo < valor_compra:
            return False
        else:
            if self.compra_pela_personalidade(valor_compra, valor_aluguel):
                self.saldo -= valor_compra
                self.add_propriedade(numero_propriedade)
                return True
            else:
                return False

    def compra_pela_personalidade(self, valor_compra, valor_aluguel):
        if self.personalidade == IMPULSIVO:
            return True
        elif self.personalidade == EXIGENTE:
            return valor_aluguel > 50
        if self.personalidade == CAUTELOSO:
            return self.saldo - valor_compra >= 80
        if self.personalidade == ALEATORIO:
            return bool(random.randint(0, 1))

    def add_propriedade(self, numero_propriedade):
        if not self.propriedades:
            self.propriedades = []
        self.propriedades.append(numero_propriedade)

    def alugar(self, proprietario, valor_aluguel):
        if self.saldo < valor_aluguel:
            pagamento = self.saldo
        else:
            pagamento = valor_aluguel
        proprietario.recebe_aluguel(pagamento)
        self.saldo -= valor_aluguel
        self.checar_se_pode_continuar_jogando()

    def checar_se_pode_continuar_jogando(self):
        self.jogando = self.saldo >= 0

    def add_posicao_atual(self, numero_de_casas):
        self.posicao_anterior = self.posicao_atual

        self.posicao_atual += numero_de_casas
        if self.posicao_atual > MAX_DE_CASAS_NO_TABULEIRO:
            self.add_nova_volta()
            self.posicao_atual = self.posicao_atual - MAX_DE_CASAS_NO_TABULEIRO

    def joga_dado(self):
        numero_de_casas = random.randint(1, MAX_FACES_DO_DADO)
        self.add_posicao_atual(numero_de_casas)
        self.add_novo_turno()

    def add_nova_volta(self):
        self.volta += 1
        self.saldo += 100

    def add_novo_turno(self):
        self.turno += 1

    def remove_propriedades(self):
        self.propriedades = None

    def recebe_aluguel(self, valor_aluguel):
        self.saldo += valor_aluguel

    def tem_propriedade(self):
        return self.propriedades != None


class Propriedade:
    def __init__(self, valor_venda, valor_aluguel, posicao, proprietario=None):
        self.valor_venda = valor_venda
        self.valor_aluguel = valor_aluguel
        self.posicao = posicao
        self.proprietario = proprietario

    def adiciona_proprietario(self, jogador):
        self.proprietario = jogador

    def remove_proprietario(self):
        self.proprietario = None

    def tem_proprietario(self):
        return self.proprietario != None


def gerar_resultados(resultados):
    tvpp = resultados["total_de_vitorias_por_personalidade"]
    pvpp = dict(map(lambda item: (item[0], f"{(item[1]*100)/300:.2f}"), tvpp.items()))
    mtpp = int(resultados["media_de_turnos_por_partida"] / 300)
    resultados.update(
        {
            "media_de_turnos_por_partida": mtpp,
            "porcentagem_de_vitorias_por_personalidade": pvpp,
            "personalidade_com_maior_numeros_de_vitorias": max(
                tvpp, key=lambda k: tvpp[k]
            ),
        },
    )
    resultados.pop("total_de_vitorias_por_personalidade")
    return json.dumps(resultados, sort_keys=True, indent=4)


def jogar():
    resultados = {
        "total_de_partidas_terminadas_em_time_out": 0,
        "media_de_turnos_por_partida": 0,
        "total_de_vitorias_por_personalidade": {
            IMPULSIVO: 0,
            EXIGENTE: 0,
            CAUTELOSO: 0,
            ALEATORIO: 0,
        },
        "personalidade_com_maior_numeros_de_vitorias": "",
    }

    simulacao = 1
    while simulacao <= SIMULACOES:
        jogadores = [
            Jogador(IMPULSIVO),
            Jogador(EXIGENTE),
            Jogador(CAUTELOSO),
            Jogador(ALEATORIO),
        ]
        jogadores = random.sample(jogadores, len(jogadores))
        perdedores = []

        tabuleiro = {}
        for numero in range(1, MAX_DE_CASAS_NO_TABULEIRO + 1):
            tabuleiro[numero] = Propriedade(
                VALOR_INICIAL_DO_TABULEIRO * numero,
                int((VALOR_INICIAL_DO_TABULEIRO * numero) / 2),
                numero,
            )

        rodadas = 1
        vencedor = False
        while rodadas < MAX_DE_RODADAS:
            for jgdr in jogadores:

                jgdr.joga_dado()
                ppdd = tabuleiro.get(jgdr.posicao_atual)
                if ppdd.tem_proprietario():
                    if ppdd.proprietario != jgdr:
                        jgdr.alugar(ppdd.proprietario, ppdd.valor_aluguel)
                else:
                    jgdr_comprou = jgdr.comprar(
                        ppdd.posicao, ppdd.valor_venda, ppdd.valor_aluguel
                    )
                    if jgdr_comprou:
                        ppdd.adiciona_proprietario(jgdr)

                if not jgdr.jogando:
                    if jgdr.tem_propriedade():
                        for posicao_ppdd in jgdr.propriedades:
                            tabuleiro.get(posicao_ppdd).remove_proprietario()
                        jgdr.remove_propriedades()
                        jogadores.remove(jgdr)
                        perdedores.append(jgdr)

                if len(jogadores) == 1:
                    vencedor = True
                    break

            if vencedor and len(jogadores):

                maior_turno = max([j.turno for j in [*jogadores, *perdedores]])
                resultados.update(
                    {
                        "media_de_turnos_por_partida": resultados[
                            "media_de_turnos_por_partida"
                        ]
                        + maior_turno
                    },
                )
                resultados["total_de_vitorias_por_personalidade"].update(
                    {
                        jogadores[0].personalidade: resultados[
                            "total_de_vitorias_por_personalidade"
                        ][jogadores[0].personalidade]
                        + 1
                    },
                )
                break

            rodadas += 1

        if rodadas == MAX_DE_RODADAS:
            if len(jogadores) > 1:
                vencedor = sorted(jogadores, key=lambda j: (-j.saldo, j.turno))[0]

            maior_turno = max([j.turno for j in [*jogadores, *perdedores]])
            resultados.update(
                {
                    "total_de_partidas_terminadas_em_time_out": resultados[
                        "total_de_partidas_terminadas_em_time_out"
                    ]
                    + 1,
                    "media_de_turnos_por_partida": resultados[
                        "media_de_turnos_por_partida"
                    ]
                    + maior_turno,
                },
            )
            resultados["total_de_vitorias_por_personalidade"].update(
                {
                    vencedor.personalidade: resultados[
                        "total_de_vitorias_por_personalidade"
                    ][vencedor.personalidade]
                    + 1
                },
            )

        simulacao += 1

    return gerar_resultados(resultados)


resultados = jogar()
print(resultados)
