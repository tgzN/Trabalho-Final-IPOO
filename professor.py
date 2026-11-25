# -*- coding: utf-8 -*-
"""Professor é uma Pessoa (HERANÇA)."""

from pessoa import Pessoa


class Professor(Pessoa):

    TITULACOES = ["Graduado", "Especialista", "Mestre", "Doutor"]

    def __init__(self, nome, cpf, genero, data_nascimento, codigo, titulacao, ativo=True):
        # super() chama o construtor da classe base para aproveitar
        # as validações de nome, CPF, gênero e data
        super().__init__(nome, cpf, genero, data_nascimento, ativo)
        self.codigo = codigo
        self.titulacao = titulacao
        self.__disciplinas = []

    @property
    def codigo(self):
        return self.__codigo

    @codigo.setter
    def codigo(self, valor):
        texto = str(valor).strip().upper()
        if len(texto) < 2:
            raise ValueError("O código do professor deve ter pelo menos 2 caracteres.")
        self.__codigo = texto

    @property
    def titulacao(self):
        return self.__titulacao

    @titulacao.setter
    def titulacao(self, valor):
        texto = str(valor).strip().title()
        if texto not in Professor.TITULACOES:
            opcoes = ", ".join(Professor.TITULACOES)
            raise ValueError(f"Titulação inválida. Use uma destas: {opcoes}.")
        self.__titulacao = texto

    @property
    def disciplinas(self):
        return list(self.__disciplinas)

    def atribuir_disciplina(self, disciplina):
        for item in self.__disciplinas:
            if item.codigo == disciplina.codigo:
                raise ValueError("Este professor já leciona essa disciplina.")
        self.__disciplinas.append(disciplina)

    def remover_disciplina(self, codigo):
        codigo = str(codigo).strip().upper()
        for item in self.__disciplinas:
            if item.codigo == codigo:
                self.__disciplinas.remove(item)
                return True
        return False

    def carga_horaria_total(self):
        total = 0
        for disciplina in self.__disciplinas:
            total += disciplina.carga_horaria
        return total

    # ------------------------------------------------------------------
    # POLIMORFISMO: mesmos nomes de método da classe Pessoa,
    # com o comportamento próprio do professor.
    # ------------------------------------------------------------------

    def papel(self):
        return "Professor"

    def exibir_dados(self):
        print("-" * 56)
        print(f"{self.papel().upper()} - {self.nome}")
        for linha in self.dados_basicos():
            print(f"  {linha}")
        print(f"  {'Código':<18}: {self.codigo}")
        print(f"  {'Titulação':<18}: {self.titulacao}")
        print(f"  {'Disciplinas':<18}: {self.disciplinas_texto()}")
        print(f"  {'Carga horária':<18}: {self.carga_horaria_total()} horas")

    def disciplinas_texto(self):
        if len(self.__disciplinas) == 0:
            return "nenhuma disciplina atribuída"
        nomes = []
        for disciplina in self.__disciplinas:
            nomes.append(disciplina.nome)
        return ", ".join(nomes)

    def to_dict(self):
        dados = super().to_dict()
        dados["codigo"] = self.codigo
        dados["titulacao"] = self.titulacao
        return dados

    @classmethod
    def from_dict(cls, dados):
        return cls(dados["nome"], dados["cpf"], dados["genero"],
                   dados["data_nascimento"], dados["codigo"],
                   dados["titulacao"], dados["ativo"])

    def __str__(self):
        return f"[{self.codigo}] {self.nome} - {self.titulacao} ({self.status()})"
