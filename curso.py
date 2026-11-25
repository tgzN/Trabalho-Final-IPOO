# -*- coding: utf-8 -*-
"""Curso é formado por várias Disciplinas (COMPOSIÇÃO)."""


class Curso:

    def __init__(self, codigo, nome):
        self.codigo = codigo
        self.nome = nome
        self.__disciplinas = []

    @property
    def codigo(self):
        return self.__codigo

    @codigo.setter
    def codigo(self, valor):
        texto = str(valor).strip().upper()
        if len(texto) < 2:
            raise ValueError("O código do curso deve ter pelo menos 2 caracteres.")
        self.__codigo = texto

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, valor):
        texto = str(valor).strip()
        if len(texto) < 3:
            raise ValueError("O nome do curso deve ter pelo menos 3 caracteres.")
        self.__nome = texto

    @property
    def disciplinas(self):
        return list(self.__disciplinas)

    def tem_disciplina(self, codigo):
        codigo = str(codigo).strip().upper()
        for disciplina in self.__disciplinas:
            if disciplina.codigo == codigo:
                return True
        return False

    def adicionar_disciplina(self, disciplina):
        if self.tem_disciplina(disciplina.codigo):
            raise ValueError("Essa disciplina já faz parte do curso.")
        self.__disciplinas.append(disciplina)

    def remover_disciplina(self, codigo):
        codigo = str(codigo).strip().upper()
        for disciplina in self.__disciplinas:
            if disciplina.codigo == codigo:
                self.__disciplinas.remove(disciplina)
                return True
        raise ValueError("Essa disciplina não faz parte do curso.")

    def carga_horaria_total(self):
        total = 0
        for disciplina in self.__disciplinas:
            total += disciplina.carga_horaria
        return total

    def to_dict(self):
        codigos = []
        for disciplina in self.__disciplinas:
            codigos.append(disciplina.codigo)
        return {
            "codigo": self.codigo,
            "nome": self.nome,
            "disciplinas": codigos,
        }

    @classmethod
    def from_dict(cls, dados):
        return cls(dados["codigo"], dados["nome"])

    def __str__(self):
        return (f"[{self.codigo}] {self.nome} - {len(self.disciplinas)} disciplina(s) "
                f"- {self.carga_horaria_total()}h")
