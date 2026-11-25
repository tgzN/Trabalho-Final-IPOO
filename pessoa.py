# -*- coding: utf-8 -*-
"""Classe base do sistema: o que toda pessoa cadastrada tem em comum.

Aluno e Professor HERDAM desta classe e sobrescrevem os métodos
papel() e exibir_dados() (polimorfismo).
"""


class Pessoa:

    # atributo de classe: tabela de apoio (código guardado -> texto na tela)
    GENEROS = {"M": "Masculino", "F": "Feminino", "O": "Outro"}

    def __init__(self, nome, cpf, genero, data_nascimento, ativo=True):
        # usamos as propriedades (e não os atributos direto) para que as
        # validações também aconteçam no momento do cadastro
        self.nome = nome
        self.cpf = cpf
        self.genero = genero
        self.data_nascimento = data_nascimento
        self.__ativo = bool(ativo)

    # ------------------------------------------------------------------
    # ENCAPSULAMENTO
    # Os atributos são privados (começam com __) e só podem ser lidos ou
    # alterados pelas propriedades abaixo, que validam o valor recebido.
    # ------------------------------------------------------------------

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, valor):
        texto = str(valor).strip()
        if len(texto) < 3:
            raise ValueError("O nome deve ter pelo menos 3 caracteres.")
        self.__nome = texto.title()

    @property
    def cpf(self):
        return self.__cpf

    @cpf.setter
    def cpf(self, valor):
        numeros = Pessoa.limpar_cpf(valor)
        if len(numeros) != 11:
            raise ValueError("O CPF deve conter 11 números.")
        self.__cpf = numeros

    @property
    def cpf_formatado(self):
        """CPF no formato 000.000.000-00 (só para mostrar na tela)."""
        return f"{self.__cpf[0:3]}.{self.__cpf[3:6]}.{self.__cpf[6:9]}-{self.__cpf[9:11]}"

    @property
    def genero(self):
        return self.__genero

    @genero.setter
    def genero(self, valor):
        codigo = str(valor).strip().upper()
        if codigo not in Pessoa.GENEROS:
            raise ValueError("Gênero inválido. Use M (masculino), F (feminino) ou O (outro).")
        self.__genero = codigo

    @property
    def genero_descricao(self):
        return Pessoa.GENEROS[self.__genero]

    @property
    def data_nascimento(self):
        return self.__data_nascimento

    @data_nascimento.setter
    def data_nascimento(self, valor):
        texto = str(valor).strip()
        partes = texto.split("/")
        if len(partes) != 3:
            raise ValueError("A data deve estar no formato dd/mm/aaaa.")
        dia, mes, ano = partes
        if not (dia.isdigit() and mes.isdigit() and ano.isdigit()):
            raise ValueError("A data deve conter apenas números e barras.")
        if len(ano) != 4:
            raise ValueError("O ano deve ter 4 números.")
        if int(dia) < 1 or int(dia) > 31:
            raise ValueError("Dia inválido.")
        if int(mes) < 1 or int(mes) > 12:
            raise ValueError("Mês inválido.")
        self.__data_nascimento = f"{int(dia):02d}/{int(mes):02d}/{ano}"

    @property
    def ativo(self):
        return self.__ativo

    def ativar(self):
        self.__ativo = True

    def inativar(self):
        self.__ativo = False

    def status(self):
        if self.__ativo:
            return "Ativo"
        return "Inativo"

    @staticmethod
    def limpar_cpf(valor):
        """Devolve somente os números digitados (aceita 000.000.000-00)."""
        numeros = ""
        for caractere in str(valor):
            if caractere.isdigit():
                numeros += caractere
        return numeros

    # ------------------------------------------------------------------
    # POLIMORFISMO
    # Pessoa não sabe responder estas duas perguntas: cada classe filha
    # responde do seu jeito. Chamar aqui gera erro de propósito.
    # ------------------------------------------------------------------

    def papel(self):
        raise NotImplementedError("Cada classe filha deve informar o seu papel.")

    def exibir_dados(self):
        raise NotImplementedError("Cada classe filha deve exibir os seus dados.")

    def dados_basicos(self):
        """Linhas comuns a qualquer pessoa, reaproveitadas pelas filhas."""
        return [
            f"{'Nome':<18}: {self.nome}",
            f"{'CPF':<18}: {self.cpf_formatado}",
            f"{'Gênero':<18}: {self.genero_descricao}",
            f"{'Nascimento':<18}: {self.data_nascimento}",
            f"{'Cadastro':<18}: {self.status()}",
        ]

    def to_dict(self):
        """Transforma o objeto em dicionário para gravar no arquivo JSON."""
        return {
            "nome": self.nome,
            "cpf": self.cpf,
            "genero": self.genero,
            "data_nascimento": self.data_nascimento,
            "ativo": self.ativo,
        }

    def __str__(self):
        return f"{self.nome} ({self.cpf_formatado})"
