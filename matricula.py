# -*- coding: utf-8 -*-
"""Liga um Aluno a uma Disciplina e guarda as notas dessa disciplina.

É um exemplo de ASSOCIAÇÃO: o objeto Matricula não é um aluno nem uma
disciplina, ele guarda a ligação entre os dois.
"""


class Matricula:

    # atributos de classe: as regras de aprovação da instituição
    MEDIA_APROVACAO = 7.0
    MEDIA_RECUPERACAO = 5.0
    MAXIMO_NOTAS = 3

    def __init__(self, aluno, disciplina):
        self.__aluno = aluno
        self.__disciplina = disciplina
        self.__notas = []

    @property
    def aluno(self):
        return self.__aluno

    @property
    def disciplina(self):
        return self.__disciplina

    @property
    def notas(self):
        # devolve uma copia da lista para ninguem alterar as notas por fora
        return list(self.__notas)

    def lancar_nota(self, nota):
        """Adiciona uma avaliação (0 a 10) nesta disciplina."""
        try:
            valor = float(str(nota).replace(",", "."))
        except ValueError:
            raise ValueError("A nota deve ser um número (exemplo: 8.5).")
        if valor < 0 or valor > 10:
            raise ValueError("A nota deve estar entre 0 e 10.")
        if len(self.__notas) >= Matricula.MAXIMO_NOTAS:
            raise ValueError(f"Esta disciplina já possui {Matricula.MAXIMO_NOTAS} notas lançadas.")
        self.__notas.append(round(valor, 2))

    def remover_ultima_nota(self):
        if len(self.__notas) == 0:
            raise ValueError("Não há nota para remover.")
        return self.__notas.pop()

    def media(self):
        if len(self.__notas) == 0:
            return 0.0
        return round(sum(self.__notas) / len(self.__notas), 2)

    def situacao(self):
        if len(self.__notas) == 0:
            return "Cursando"
        media = self.media()
        if media >= Matricula.MEDIA_APROVACAO:
            return "Aprovado"
        if media >= Matricula.MEDIA_RECUPERACAO:
            return "Recuperação"
        return "Reprovado"

    def notas_texto(self):
        if len(self.__notas) == 0:
            return "sem notas"
        textos = []
        for nota in self.__notas:
            textos.append(f"{nota:.2f}")
        return " / ".join(textos)

    def to_dict(self):
        return {
            "disciplina_codigo": self.__disciplina.codigo,
            "notas": self.notas,
        }

    def __str__(self):
        return (f"{self.__disciplina.codigo} - {self.__disciplina.nome} | "
                f"notas: {self.notas_texto()} | média: {self.media():.2f} | {self.situacao()}")
