# -*- coding: utf-8 -*-
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

    def __str__(self) -> str:
        return f"Jogador({self.personalidade}, {self.saldo}, {self.volta}, {self.posicao_anterior}, {self.posicao_atual}, {self.propriedades}, {self.jogando})"

    def comprar(self, numero_propriedade, valor_compra, valor_aluguel):
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
        if self.saldo < 0:
            self.jogando = False

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

    @property
    def tem_propriedade(self):
        return self.propriedades != None


class Propriedade:
    def __init__(self, valor_venda, valor_aluguel, posicao, proprietario=None):
        self.valor_venda = valor_venda
        self.valor_aluguel = valor_aluguel
        self.posicao = posicao
        self.proprietario = proprietario

    def __str__(self) -> str:
        return f"Propriedade({self.valor_venda}, {self.valor_aluguel}, {self.posicao}, {self.proprietario})"

    def adiciona_proprietario(self, jogador):
        self.proprietario = jogador

    def remove_proprietario(self):
        self.proprietario = None

    def tem_proprietario(self):
        return self.proprietario != None


resultados = {
    "time_out": 0,
    "turnos_por_partida": 0,
    "vitorias_por_personalidade": {
        IMPULSIVO: 0,
        EXIGENTE: 0,
        CAUTELOSO: 0,
        ALEATORIO: 0,
    },
}

simulacao = 1
while simulacao <= SIMULACOES:
    j1 = Jogador(IMPULSIVO)
    j2 = Jogador(EXIGENTE)
    j3 = Jogador(CAUTELOSO)
    j4 = Jogador(ALEATORIO)

    jogadores = [j1, j2, j3, j4]
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
                if jgdr.tem_propriedade:
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
                {"turnos_por_partida": resultados["turnos_por_partida"] + maior_turno},
            )
            resultados["vitorias_por_personalidade"].update(
                {
                    jogadores[0].personalidade: resultados[
                        "vitorias_por_personalidade"
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
                "time_out": resultados["time_out"] + 1,
                "turnos_por_partida": resultados["turnos_por_partida"] + maior_turno,
            },
        )
        resultados["vitorias_por_personalidade"].update(
            {
                vencedor.personalidade: resultados["vitorias_por_personalidade"][
                    vencedor.personalidade
                ]
                + 1
            },
        )

    simulacao += 1


print(resultados)
