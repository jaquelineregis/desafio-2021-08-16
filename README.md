# desafio-2021-08-16

[![Github Badge](https://img.shields.io/badge/-Github-000?style=flat-square&logo=Github&logoColor=white&link=https://github.com/jaquelineregis)](https://github.com/jaquelineregis)
[![Gitlab Badge](https://img.shields.io/badge/-Gitlab-000?style=flat-square&logo=Gitlab&logoColor=white&link=https://gitlab.com/jaquelineregis)](https://gitlab.com/jaquelineregis)
[![Linkedin Badge](https://img.shields.io/badge/-LinkedIn-blue?style=flat-square&logo=Linkedin&logoColor=white&link=https://www.linkedin.com/in/jaquelineregis/)](https://www.linkedin.com/in/jaquelineregis/)



# Tecnologias
Projeto criado com:
* Python versão 3.8.2



# Funcionalidades extras
- [ ] Funcionamento do teste integrado a uma API com Flask ou Django;
- [ ] Containerização (por exemplo Docker, CoreOS rkt, OpenVZ, containerd);
- [x] Orientação a Objeto, Clean code e Padrão de Projetos;
- [ ] Testes Unitários;
- [x] Documentação e instrução como executar o código;
- [ ] Deploy em Nuvem (Azure ou AWS).

# Runner
```
$ cd ./desafio-2021-08-16
$ python3 jogo.py
```

# Retorno
```json
{
    "media_de_turnos_por_partida": 96,
    "personalidade_com_maior_numeros_de_vitorias": "EXIGENTE",
    "porcentagem_de_vitorias_por_personalidade": {
        "ALEATORIO": "21.33",
        "CAUTELOSO": "22.67",
        "EXIGENTE": "28.67",
        "IMPULSIVO": "27.33"
    },
    "total_de_partidas_terminadas_em_time_out": 15
}
```