# -*- coding: utf-8 -*-
"""Trabalho final de IPOO - Sistema de Secretaria Acadêmica.

Para executar:  python main.py

Classes do projeto:
    Pessoa (base) -> Aluno, Professor      herança e polimorfismo
    Curso, Disciplina, Matricula           composição e associação
    Secretaria                             regras de negócio
    Repositorio                            gravação/leitura em JSON
    Menu                                   interface de texto
"""

from secretaria import Secretaria
from repositorio import Repositorio
from menu import Menu


def main():
    # criação dos objetos principais do programa
    secretaria = Secretaria("UDESC CEPLAN - São Bento do Sul")
    repositorio = Repositorio()

    # se já existe um arquivo salvo, os dados são carregados automaticamente
    if repositorio.existe():
        try:
            repositorio.carregar(secretaria)
            print(f"Dados carregados do arquivo: {secretaria}")
        except ValueError as erro:
            print(f"[AVISO] Nao foi possivel carregar o arquivo: {erro}")

    menu = Menu(secretaria, repositorio)
    menu.executar()


main()
