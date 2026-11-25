# -*- coding: utf-8 -*-
"""Repositorio: grava e lê os dados da Secretaria em um arquivo JSON.

Cada classe sabe se transformar em dicionário (to_dict) e sabe voltar de
um dicionário (from_dict). Esta classe só cuida do arquivo e de religar
as ligações entre os objetos (aluno -> curso -> disciplinas -> professor).
"""

import json
import os

from aluno import Aluno
from professor import Professor
from curso import Curso
from disciplina import Disciplina


class Repositorio:

    # a pasta "dados" fica sempre junto dos arquivos .py do projeto
    PASTA_PROJETO = os.path.dirname(os.path.abspath(__file__))

    def __init__(self, nome_arquivo="secretaria.json"):
        self.__caminho = os.path.join(Repositorio.PASTA_PROJETO, "dados", nome_arquivo)

    @property
    def caminho(self):
        return self.__caminho

    def existe(self):
        return os.path.exists(self.__caminho)

    # ------------------------------------------------------------------
    # GRAVAR
    # ------------------------------------------------------------------

    def salvar(self, secretaria):
        dados = {
            "instituicao": secretaria.nome_instituicao,
            "cursos": self.__para_dicionarios(secretaria.cursos),
            "disciplinas": self.__para_dicionarios(secretaria.disciplinas),
            "professores": self.__para_dicionarios(secretaria.professores),
            "alunos": self.__para_dicionarios(secretaria.alunos),
        }
        pasta = os.path.dirname(self.__caminho)
        if not os.path.exists(pasta):
            os.makedirs(pasta)
        arquivo = open(self.__caminho, "w", encoding="utf-8")
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)
        arquivo.close()
        return self.__caminho

    def __para_dicionarios(self, objetos):
        lista = []
        for objeto in objetos:
            lista.append(objeto.to_dict())
        return lista

    # ------------------------------------------------------------------
    # LER
    # ------------------------------------------------------------------

    def carregar(self, secretaria):
        """Lê o arquivo, recria os objetos e devolve tudo para a secretaria."""
        dados = self.__ler_arquivo()

        # a secretaria e o contador de matriculas sao zerados antes de
        # recriar os objetos, para as matriculas lidas valerem de novo
        secretaria.limpar()

        professores = self.__recriar_professores(dados.get("professores", []))
        disciplinas = self.__recriar_disciplinas(dados.get("disciplinas", []), professores)
        cursos = self.__recriar_cursos(dados.get("cursos", []), disciplinas)
        alunos = self.__recriar_alunos(dados.get("alunos", []), cursos, disciplinas)

        secretaria.restaurar(cursos, disciplinas, professores, alunos)
        return secretaria

    def __ler_arquivo(self):
        if not self.existe():
            raise ValueError("Nenhum arquivo de dados foi salvo ainda.")
        arquivo = open(self.__caminho, "r", encoding="utf-8")
        try:
            return json.load(arquivo)
        except ValueError:
            raise ValueError("O arquivo de dados está corrompido.")
        finally:
            arquivo.close()

    def __recriar_professores(self, lista):
        professores = []
        for item in lista:
            professores.append(Professor.from_dict(item))
        return professores

    def __recriar_disciplinas(self, lista, professores):
        disciplinas = []
        for item in lista:
            disciplina = Disciplina.from_dict(item)
            professor = self.__buscar(professores, item["professor_codigo"])
            if professor is not None:
                disciplina.atribuir_professor(professor)
                professor.atribuir_disciplina(disciplina)
            disciplinas.append(disciplina)
        return disciplinas

    def __recriar_cursos(self, lista, disciplinas):
        cursos = []
        for item in lista:
            curso = Curso.from_dict(item)
            for codigo in item["disciplinas"]:
                disciplina = self.__buscar(disciplinas, codigo)
                if disciplina is not None:
                    curso.adicionar_disciplina(disciplina)
            cursos.append(curso)
        return cursos

    def __recriar_alunos(self, lista, cursos, disciplinas):
        alunos = []
        for item in lista:
            aluno = Aluno.from_dict(item)
            curso = self.__buscar(cursos, item["curso_codigo"])
            if curso is not None:
                aluno.definir_curso(curso)
            for registro in item["matriculas"]:
                disciplina = self.__buscar(disciplinas, registro["disciplina_codigo"])
                if disciplina is not None:
                    aluno.restaurar_matricula(disciplina, registro["notas"])
            alunos.append(aluno)
        return alunos

    def __buscar(self, objetos, codigo):
        """Procura em uma lista de objetos que tenham a propriedade codigo."""
        codigo = str(codigo).strip().upper()
        if codigo == "":
            return None
        for objeto in objetos:
            if objeto.codigo == codigo:
                return objeto
        return None
