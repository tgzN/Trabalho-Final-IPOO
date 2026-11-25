# -*- coding: utf-8 -*-
"""Secretaria: a classe que guarda todos os objetos e as regras do sistema.

O Menu só conversa com esta classe, nunca com as listas direto.
"""

from aluno import Aluno
from professor import Professor
from curso import Curso
from disciplina import Disciplina
from pessoa import Pessoa


class Secretaria:

    def __init__(self, nome_instituicao):
        self.__nome_instituicao = nome_instituicao
        self.__alunos = []
        self.__professores = []
        self.__cursos = []
        self.__disciplinas = []

    # ------------------------------------------------------------------
    # Propriedades (devolvem cópias das listas: ninguém mexe por fora)
    # ------------------------------------------------------------------

    @property
    def nome_instituicao(self):
        return self.__nome_instituicao

    @property
    def alunos(self):
        return list(self.__alunos)

    @property
    def professores(self):
        return list(self.__professores)

    @property
    def cursos(self):
        return list(self.__cursos)

    @property
    def disciplinas(self):
        return list(self.__disciplinas)

    # ==================================================================
    # ALUNOS
    # ==================================================================

    def cadastrar_aluno(self, nome, cpf, genero, data_nascimento):
        if self.__pessoa_com_cpf(cpf) is not None:
            raise ValueError("Já existe uma pessoa cadastrada com esse CPF.")
        aluno = Aluno(nome, cpf, genero, data_nascimento)
        self.__alunos.append(aluno)
        return aluno

    def buscar_aluno(self, matricula):
        matricula = str(matricula).strip()
        for aluno in self.__alunos:
            if aluno.matricula == matricula:
                return aluno
        return None

    def buscar_aluno_por_cpf(self, cpf):
        numeros = Pessoa.limpar_cpf(cpf)
        for aluno in self.__alunos:
            if aluno.cpf == numeros:
                return aluno
        return None

    def consultar_aluno(self, texto):
        """Procura o aluno pela matrícula ou pelo CPF (o que o usuário digitar)."""
        aluno = self.buscar_aluno(texto)
        if aluno is None:
            aluno = self.buscar_aluno_por_cpf(texto)
        if aluno is None:
            raise ValueError("Aluno não encontrado.")
        return aluno

    def alterar_aluno(self, matricula, nome="", genero="", data_nascimento=""):
        """Campos deixados em branco continuam com o valor atual."""
        aluno = self.consultar_aluno(matricula)
        if nome != "":
            aluno.nome = nome
        if genero != "":
            aluno.genero = genero
        if data_nascimento != "":
            aluno.data_nascimento = data_nascimento
        return aluno

    def alternar_status_aluno(self, matricula):
        aluno = self.consultar_aluno(matricula)
        if aluno.ativo:
            aluno.inativar()
        else:
            aluno.ativar()
        return aluno

    def excluir_aluno(self, matricula):
        aluno = self.consultar_aluno(matricula)
        self.__alunos.remove(aluno)
        return aluno

    def definir_curso_do_aluno(self, matricula, codigo_curso):
        aluno = self.consultar_aluno(matricula)
        if str(codigo_curso).strip() == "":
            aluno.definir_curso(None)
            return aluno
        curso = self.obter_curso(codigo_curso)
        aluno.definir_curso(curso)
        return aluno

    def matricular_aluno_em_disciplina(self, matricula, codigo_disciplina):
        """Regra da instituição: a disciplina precisa pertencer ao curso do aluno."""
        aluno = self.consultar_aluno(matricula)
        disciplina = self.obter_disciplina(codigo_disciplina)
        if aluno.curso is None:
            raise ValueError("Defina primeiro o curso do aluno.")
        if not aluno.curso.tem_disciplina(disciplina.codigo):
            raise ValueError("Essa disciplina não faz parte do curso do aluno.")
        aluno.matricular_em(disciplina)
        return disciplina

    def trancar_disciplina(self, matricula, codigo_disciplina):
        aluno = self.consultar_aluno(matricula)
        aluno.trancar(codigo_disciplina)
        return aluno

    def listar_alunos_por_status(self, ativo):
        encontrados = []
        for aluno in self.__alunos:
            if aluno.ativo == ativo:
                encontrados.append(aluno)
        return encontrados

    def alunos_do_curso(self, codigo_curso):
        curso = self.obter_curso(codigo_curso)
        encontrados = []
        for aluno in self.__alunos:
            if aluno.curso is not None and aluno.curso.codigo == curso.codigo:
                encontrados.append(aluno)
        return encontrados

    # ==================================================================
    # PROFESSORES
    # ==================================================================

    def cadastrar_professor(self, nome, cpf, genero, data_nascimento, codigo, titulacao):
        if self.__pessoa_com_cpf(cpf) is not None:
            raise ValueError("Já existe uma pessoa cadastrada com esse CPF.")
        if self.buscar_professor(codigo) is not None:
            raise ValueError("Já existe um professor com esse código.")
        professor = Professor(nome, cpf, genero, data_nascimento, codigo, titulacao)
        self.__professores.append(professor)
        return professor

    def buscar_professor(self, codigo):
        codigo = str(codigo).strip().upper()
        for professor in self.__professores:
            if professor.codigo == codigo:
                return professor
        return None

    def obter_professor(self, codigo):
        professor = self.buscar_professor(codigo)
        if professor is None:
            raise ValueError("Professor não encontrado.")
        return professor

    def alterar_professor(self, codigo, nome="", titulacao=""):
        professor = self.obter_professor(codigo)
        if nome != "":
            professor.nome = nome
        if titulacao != "":
            professor.titulacao = titulacao
        return professor

    def alternar_status_professor(self, codigo):
        professor = self.obter_professor(codigo)
        if professor.ativo:
            professor.inativar()
        else:
            professor.ativar()
        return professor

    def excluir_professor(self, codigo):
        professor = self.obter_professor(codigo)
        # antes de excluir, as disciplinas dele ficam sem professor
        for disciplina in self.__disciplinas:
            if disciplina.professor is not None and disciplina.professor.codigo == professor.codigo:
                disciplina.remover_professor()
        self.__professores.remove(professor)
        return professor

    def atribuir_disciplina_a_professor(self, codigo_professor, codigo_disciplina):
        professor = self.obter_professor(codigo_professor)
        disciplina = self.obter_disciplina(codigo_disciplina)
        if not professor.ativo:
            raise ValueError("Professor inativo não pode receber disciplinas.")
        professor.atribuir_disciplina(disciplina)
        disciplina.atribuir_professor(professor)
        return disciplina

    # ==================================================================
    # CURSOS
    # ==================================================================

    def cadastrar_curso(self, codigo, nome):
        if self.buscar_curso(codigo) is not None:
            raise ValueError("Já existe um curso com esse código.")
        curso = Curso(codigo, nome)
        self.__cursos.append(curso)
        return curso

    def buscar_curso(self, codigo):
        codigo = str(codigo).strip().upper()
        for curso in self.__cursos:
            if curso.codigo == codigo:
                return curso
        return None

    def obter_curso(self, codigo):
        curso = self.buscar_curso(codigo)
        if curso is None:
            raise ValueError("Curso não encontrado.")
        return curso

    def alterar_curso(self, codigo, nome):
        curso = self.obter_curso(codigo)
        curso.nome = nome
        return curso

    def excluir_curso(self, codigo):
        curso = self.obter_curso(codigo)
        if len(self.alunos_do_curso(curso.codigo)) > 0:
            raise ValueError("Não é possível excluir: existem alunos matriculados nesse curso.")
        self.__cursos.remove(curso)
        return curso

    def adicionar_disciplina_ao_curso(self, codigo_curso, codigo_disciplina):
        curso = self.obter_curso(codigo_curso)
        disciplina = self.obter_disciplina(codigo_disciplina)
        curso.adicionar_disciplina(disciplina)
        return disciplina

    def remover_disciplina_do_curso(self, codigo_curso, codigo_disciplina):
        curso = self.obter_curso(codigo_curso)
        for aluno in self.alunos_do_curso(curso.codigo):
            if aluno.buscar_matricula(codigo_disciplina) is not None:
                raise ValueError("Não é possível remover: há aluno do curso cursando essa disciplina.")
        curso.remover_disciplina(codigo_disciplina)
        return curso

    # ==================================================================
    # DISCIPLINAS
    # ==================================================================

    def cadastrar_disciplina(self, codigo, nome, carga_horaria):
        if self.buscar_disciplina(codigo) is not None:
            raise ValueError("Já existe uma disciplina com esse código.")
        disciplina = Disciplina(codigo, nome, carga_horaria)
        self.__disciplinas.append(disciplina)
        return disciplina

    def buscar_disciplina(self, codigo):
        codigo = str(codigo).strip().upper()
        for disciplina in self.__disciplinas:
            if disciplina.codigo == codigo:
                return disciplina
        return None

    def obter_disciplina(self, codigo):
        disciplina = self.buscar_disciplina(codigo)
        if disciplina is None:
            raise ValueError("Disciplina não encontrada.")
        return disciplina

    def alterar_disciplina(self, codigo, nome="", carga_horaria=""):
        disciplina = self.obter_disciplina(codigo)
        if nome != "":
            disciplina.nome = nome
        if str(carga_horaria) != "":
            disciplina.carga_horaria = carga_horaria
        return disciplina

    def excluir_disciplina(self, codigo):
        disciplina = self.obter_disciplina(codigo)
        for curso in self.__cursos:
            if curso.tem_disciplina(disciplina.codigo):
                raise ValueError("Não é possível excluir: a disciplina faz parte de um curso.")
        for aluno in self.__alunos:
            if aluno.buscar_matricula(disciplina.codigo) is not None:
                raise ValueError("Não é possível excluir: existem alunos cursando essa disciplina.")
        for professor in self.__professores:
            professor.remover_disciplina(disciplina.codigo)
        self.__disciplinas.remove(disciplina)
        return disciplina

    def media_da_disciplina(self, codigo):
        """Média da turma na disciplina (considera só quem já tem nota)."""
        disciplina = self.obter_disciplina(codigo)
        somatorio = 0.0
        quantidade = 0
        for aluno in self.__alunos:
            matricula = aluno.buscar_matricula(disciplina.codigo)
            if matricula is not None and len(matricula.notas) > 0:
                somatorio += matricula.media()
                quantidade += 1
        if quantidade == 0:
            return 0.0
        return round(somatorio / quantidade, 2)

    # ==================================================================
    # NOTAS
    # ==================================================================

    def lancar_nota(self, matricula, codigo_disciplina, nota):
        aluno = self.consultar_aluno(matricula)
        disciplina = self.obter_disciplina(codigo_disciplina)
        aluno.lancar_nota(disciplina.codigo, nota)
        return aluno

    def boletim_do_aluno(self, matricula):
        aluno = self.consultar_aluno(matricula)
        return aluno.boletim()

    # ==================================================================
    # RELATÓRIOS E APOIO
    # ==================================================================

    def listar_pessoas(self):
        """POLIMORFISMO: junta alunos e professores na mesma lista.

        Quem usar esta lista chama exibir_dados() sem saber (e sem
        precisar saber) se o objeto é um Aluno ou um Professor.
        """
        return self.__alunos + self.__professores

    def resumo(self):
        return {
            "alunos": len(self.__alunos),
            "ativos": len(self.listar_alunos_por_status(True)),
            "inativos": len(self.listar_alunos_por_status(False)),
            "professores": len(self.__professores),
            "cursos": len(self.__cursos),
            "disciplinas": len(self.__disciplinas),
        }

    def limpar(self):
        self.__alunos = []
        self.__professores = []
        self.__cursos = []
        self.__disciplinas = []
        Aluno.reiniciar_contador()

    def restaurar(self, cursos, disciplinas, professores, alunos):
        """Usado pelo Repositorio depois de ler o arquivo JSON."""
        self.__cursos = cursos
        self.__disciplinas = disciplinas
        self.__professores = professores
        self.__alunos = alunos

    def __pessoa_com_cpf(self, cpf):
        numeros = Pessoa.limpar_cpf(cpf)
        for pessoa in self.listar_pessoas():
            if pessoa.cpf == numeros:
                return pessoa
        return None

    def __str__(self):
        dados = self.resumo()
        return (f"{self.__nome_instituicao}: {dados['alunos']} aluno(s), "
                f"{dados['professores']} professor(es), {dados['cursos']} curso(s), "
                f"{dados['disciplinas']} disciplina(s)")
