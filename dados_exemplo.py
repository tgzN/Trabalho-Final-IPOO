# -*- coding: utf-8 -*-
"""Dados de exemplo para a demonstração do trabalho.

A função popular() apaga o que estiver na memória e cria cursos,
disciplinas, professores e alunos já com notas lançadas, usando
apenas os métodos públicos da Secretaria.
"""


def popular(secretaria):
    secretaria.limpar()

    # ----------------------------- disciplinas -----------------------------
    secretaria.cadastrar_disciplina("POO", "Programação Orientada a Objetos", 72)
    secretaria.cadastrar_disciplina("BDA", "Banco de Dados", 72)
    secretaria.cadastrar_disciplina("RED", "Redes de Computadores", 54)
    secretaria.cadastrar_disciplina("PRO", "Pesquisa Operacional", 72)
    secretaria.cadastrar_disciplina("GPR", "Gestão da Produção", 54)

    # ------------------------------- cursos --------------------------------
    secretaria.cadastrar_curso("SIN", "Sistemas de Informação")
    secretaria.adicionar_disciplina_ao_curso("SIN", "POO")
    secretaria.adicionar_disciplina_ao_curso("SIN", "BDA")
    secretaria.adicionar_disciplina_ao_curso("SIN", "RED")

    secretaria.cadastrar_curso("EPS", "Engenharia de Produção e Sistemas")
    secretaria.adicionar_disciplina_ao_curso("EPS", "PRO")
    secretaria.adicionar_disciplina_ao_curso("EPS", "GPR")

    # ----------------------------- professores -----------------------------
    secretaria.cadastrar_professor("Marcos Antônio Ferreira", "11122233344", "M",
                                   "14/05/1980", "P01", "Mestre")
    secretaria.cadastrar_professor("Helena Prado Camargo", "22233344455", "F",
                                   "02/09/1975", "P02", "Doutor")
    secretaria.cadastrar_professor("Rafael Boeing", "33344455566", "M",
                                   "23/11/1988", "P03", "Especialista")

    secretaria.atribuir_disciplina_a_professor("P01", "POO")
    secretaria.atribuir_disciplina_a_professor("P01", "RED")
    secretaria.atribuir_disciplina_a_professor("P02", "BDA")
    secretaria.atribuir_disciplina_a_professor("P03", "PRO")
    secretaria.atribuir_disciplina_a_professor("P03", "GPR")

    # -------------------------------- alunos -------------------------------
    ana = secretaria.cadastrar_aluno("Ana Paula Schneider", "98765432100", "F", "12/03/2005")
    vitor = secretaria.cadastrar_aluno("Vitor Grossl", "87654321099", "M", "27/07/2004")
    carla = secretaria.cadastrar_aluno("Carla Mayer", "76543210988", "F", "05/11/2006")
    diego = secretaria.cadastrar_aluno("Diego Ramos", "65432109877", "M", "19/01/2003")
    eduarda = secretaria.cadastrar_aluno("Eduarda Lima", "54321098766", "O", "30/09/2005")

    secretaria.definir_curso_do_aluno(ana.matricula, "SIN")
    secretaria.definir_curso_do_aluno(vitor.matricula, "SIN")
    secretaria.definir_curso_do_aluno(carla.matricula, "EPS")
    secretaria.definir_curso_do_aluno(diego.matricula, "EPS")

    # --------------------- matrículas nas disciplinas ----------------------
    secretaria.matricular_aluno_em_disciplina(ana.matricula, "POO")
    secretaria.matricular_aluno_em_disciplina(ana.matricula, "BDA")
    secretaria.matricular_aluno_em_disciplina(ana.matricula, "RED")
    secretaria.matricular_aluno_em_disciplina(vitor.matricula, "POO")
    secretaria.matricular_aluno_em_disciplina(vitor.matricula, "BDA")
    secretaria.matricular_aluno_em_disciplina(carla.matricula, "PRO")
    secretaria.matricular_aluno_em_disciplina(carla.matricula, "GPR")
    secretaria.matricular_aluno_em_disciplina(diego.matricula, "PRO")

    # ------------------------------- notas ---------------------------------
    secretaria.lancar_nota(ana.matricula, "POO", 9.0)
    secretaria.lancar_nota(ana.matricula, "POO", 8.5)
    secretaria.lancar_nota(ana.matricula, "BDA", 7.5)
    secretaria.lancar_nota(ana.matricula, "RED", 10.0)

    secretaria.lancar_nota(vitor.matricula, "POO", 6.0)
    secretaria.lancar_nota(vitor.matricula, "POO", 5.5)
    secretaria.lancar_nota(vitor.matricula, "BDA", 4.0)

    secretaria.lancar_nota(carla.matricula, "PRO", 8.0)
    secretaria.lancar_nota(carla.matricula, "GPR", 9.5)
    # Diego ainda não tem nota: aparece como "Cursando"

    # Eduarda trancou a matrícula na instituição
    secretaria.alternar_status_aluno(eduarda.matricula)

    return secretaria
