# -*- coding: utf-8 -*-
"""Aluno é uma Pessoa (HERANÇA) e possui várias Matriculas (COMPOSIÇÃO)."""

from pessoa import Pessoa
from matricula import Matricula


class Aluno(Pessoa):

    # atributos de CLASSE: valem para todos os alunos e servem para
    # gerar a matrícula automaticamente (2026001, 2026002, ...)
    ANO_BASE = 2026
    _proximo_numero = 1

    def __init__(self, nome, cpf, genero, data_nascimento, matricula=None, ativo=True):
        super().__init__(nome, cpf, genero, data_nascimento, ativo)
        if matricula is None:
            self.__matricula = Aluno.gerar_matricula()
        else:
            self.__matricula = str(matricula).strip()
            Aluno.reservar_matricula(self.__matricula)
        self.__curso = None
        self.__matriculas = []

    # ------------------------------------------------------------------
    # Métodos de classe: trabalham com o contador, não com um aluno
    # ------------------------------------------------------------------

    @classmethod
    def gerar_matricula(cls):
        numero = str(cls._proximo_numero).zfill(3)
        cls._proximo_numero += 1
        return f"{cls.ANO_BASE}{numero}"

    @classmethod
    def reservar_matricula(cls, matricula):
        """Evita que uma matrícula lida do arquivo seja gerada novamente."""
        final = str(matricula)[4:]
        if final.isdigit() and int(final) >= cls._proximo_numero:
            cls._proximo_numero = int(final) + 1

    @classmethod
    def reiniciar_contador(cls):
        cls._proximo_numero = 1

    # ------------------------------------------------------------------
    # Encapsulamento
    # ------------------------------------------------------------------

    @property
    def matricula(self):
        # só leitura: a matrícula nunca muda depois do cadastro
        return self.__matricula

    @property
    def curso(self):
        return self.__curso

    @property
    def matriculas(self):
        return list(self.__matriculas)

    def definir_curso(self, curso):
        """Matricula o aluno em um curso (ou retira, passando None)."""
        self.__curso = curso

    def nome_curso(self):
        if self.__curso is None:
            return "sem curso"
        return f"{self.__curso.codigo} - {self.__curso.nome}"

    # ------------------------------------------------------------------
    # Disciplinas e notas
    # ------------------------------------------------------------------

    def buscar_matricula(self, codigo_disciplina):
        codigo = str(codigo_disciplina).strip().upper()
        for matricula in self.__matriculas:
            if matricula.disciplina.codigo == codigo:
                return matricula
        return None

    def matricular_em(self, disciplina):
        if self.buscar_matricula(disciplina.codigo) is not None:
            raise ValueError("O aluno já está matriculado nessa disciplina.")
        if not self.ativo:
            raise ValueError("Aluno inativo não pode se matricular em disciplinas.")
        nova = Matricula(self, disciplina)
        self.__matriculas.append(nova)
        return nova

    def trancar(self, codigo_disciplina):
        matricula = self.buscar_matricula(codigo_disciplina)
        if matricula is None:
            raise ValueError("O aluno não está matriculado nessa disciplina.")
        self.__matriculas.remove(matricula)

    def lancar_nota(self, codigo_disciplina, nota):
        matricula = self.buscar_matricula(codigo_disciplina)
        if matricula is None:
            raise ValueError("O aluno não está matriculado nessa disciplina.")
        matricula.lancar_nota(nota)

    def media_geral(self):
        """Média das médias das disciplinas que já têm nota lançada."""
        somatorio = 0.0
        quantidade = 0
        for matricula in self.__matriculas:
            if len(matricula.notas) > 0:
                somatorio += matricula.media()
                quantidade += 1
        if quantidade == 0:
            return 0.0
        return round(somatorio / quantidade, 2)

    def situacao(self):
        if len(self.__matriculas) == 0:
            return "Sem disciplinas"
        media = self.media_geral()
        if media == 0.0:
            return "Cursando"
        if media >= Matricula.MEDIA_APROVACAO:
            return "Aprovado"
        if media >= Matricula.MEDIA_RECUPERACAO:
            return "Recuperação"
        return "Reprovado"

    def boletim(self):
        """Devolve as linhas do boletim (uma por disciplina)."""
        linhas = []
        for matricula in self.__matriculas:
            linhas.append(str(matricula))
        return linhas

    def restaurar_matricula(self, disciplina, notas):
        """Recria uma matricula lida do arquivo (usado pelo Repositorio)."""
        nova = Matricula(self, disciplina)
        for nota in notas:
            nova.lancar_nota(nota)
        self.__matriculas.append(nova)
        return nova

    # ------------------------------------------------------------------
    # POLIMORFISMO: sobrescreve os métodos da classe Pessoa
    # ------------------------------------------------------------------

    def papel(self):
        return "Aluno"

    def exibir_dados(self):
        print("-" * 56)
        print(f"{self.papel().upper()} - {self.nome}")
        for linha in self.dados_basicos():
            print(f"  {linha}")
        rotulo_matricula = "Matrícula"
        print(f"  {rotulo_matricula:<18}: {self.matricula}")
        print(f"  {'Curso':<18}: {self.nome_curso()}")
        print(f"  {'Disciplinas':<18}: {len(self.matriculas)}")
        print(f"  {'Média geral':<18}: {self.media_geral():.2f}")
        print(f"  {'Situação':<18}: {self.situacao()}")

    def to_dict(self):
        dados = super().to_dict()
        dados["matricula"] = self.matricula
        if self.__curso is None:
            dados["curso_codigo"] = ""
        else:
            dados["curso_codigo"] = self.__curso.codigo
        lista = []
        for matricula in self.__matriculas:
            lista.append(matricula.to_dict())
        dados["matriculas"] = lista
        return dados

    @classmethod
    def from_dict(cls, dados):
        """Cria o aluno sem as ligações (curso/disciplinas religados depois)."""
        return cls(dados["nome"], dados["cpf"], dados["genero"],
                   dados["data_nascimento"], dados["matricula"], dados["ativo"])

    def __str__(self):
        return f"[{self.matricula}] {self.nome} - {self.nome_curso()} ({self.status()})"
