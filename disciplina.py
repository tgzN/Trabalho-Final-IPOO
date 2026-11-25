# -*- coding: utf-8 -*-
"""Disciplina (matéria) oferecida pela instituição."""


class Disciplina:

    def __init__(self, codigo, nome, carga_horaria):
        self.codigo = codigo
        self.nome = nome
        self.carga_horaria = carga_horaria
        self.__professor = None

    @property
    def codigo(self):
        return self.__codigo

    @codigo.setter
    def codigo(self, valor):
        texto = str(valor).strip().upper()
        if len(texto) < 2:
            raise ValueError("O código da disciplina deve ter pelo menos 2 caracteres.")
        self.__codigo = texto

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, valor):
        texto = str(valor).strip()
        if len(texto) < 3:
            raise ValueError("O nome da disciplina deve ter pelo menos 3 caracteres.")
        self.__nome = texto

    @property
    def carga_horaria(self):
        return self.__carga_horaria

    @carga_horaria.setter
    def carga_horaria(self, valor):
        if not str(valor).isdigit():
            raise ValueError("A carga horária deve ser um número inteiro de horas.")
        horas = int(valor)
        if horas < 10 or horas > 400:
            raise ValueError("A carga horária deve ficar entre 10 e 400 horas.")
        self.__carga_horaria = horas

    @property
    def professor(self):
        return self.__professor

    def atribuir_professor(self, professor):
        self.__professor = professor

    def remover_professor(self):
        self.__professor = None

    def nome_professor(self):
        if self.__professor is None:
            return "sem professor"
        return self.__professor.nome

    def to_dict(self):
        if self.__professor is None:
            codigo_professor = ""
        else:
            codigo_professor = self.__professor.codigo
        return {
            "codigo": self.codigo,
            "nome": self.nome,
            "carga_horaria": self.carga_horaria,
            "professor_codigo": codigo_professor,
        }

    @classmethod
    def from_dict(cls, dados):
        return cls(dados["codigo"], dados["nome"], dados["carga_horaria"])

    def __str__(self):
        return (f"[{self.codigo}] {self.nome} - {self.carga_horaria}h "
                f"- Professor: {self.nome_professor()}")
