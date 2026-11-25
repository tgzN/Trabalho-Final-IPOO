# -*- coding: utf-8 -*-
"""Menu: a interface de texto do sistema (tudo que o usuário vê e digita).

Esta classe não guarda dados: ela apenas conversa com a Secretaria e com
o Repositorio. Assim as regras ficam separadas da tela.
"""

from professor import Professor
from dados_exemplo import popular


class Menu:

    LARGURA = 58

    def __init__(self, secretaria, repositorio):
        self.__secretaria = secretaria
        self.__repositorio = repositorio

    # ==================================================================
    # MENU PRINCIPAL
    # ==================================================================

    def executar(self):
        try:
            self.__menu_principal()
        except (EOFError, KeyboardInterrupt):
            print("\n\nSistema encerrado.")

    def __menu_principal(self):
        while True:
            self.__titulo(self.__secretaria.nome_instituicao)
            print("SECRETARIA ACADÊMICA".center(Menu.LARGURA))
            print("-" * Menu.LARGURA)
            print(" 1 - Alunos")
            print(" 2 - Professores")
            print(" 3 - Cursos")
            print(" 4 - Disciplinas")
            print(" 5 - Notas e boletim")
            print(" 6 - Relatórios")
            print(" 7 - Salvar dados em arquivo")
            print(" 8 - Carregar dados do arquivo")
            print(" 9 - Carregar dados de exemplo")
            print(" 0 - Sair")
            print("-" * Menu.LARGURA)
            opcao = self.__ler_texto("Opção: ", False)
            try:
                if opcao == "1":
                    self.__menu_alunos()
                elif opcao == "2":
                    self.__menu_professores()
                elif opcao == "3":
                    self.__menu_cursos()
                elif opcao == "4":
                    self.__menu_disciplinas()
                elif opcao == "5":
                    self.__menu_notas()
                elif opcao == "6":
                    self.__menu_relatorios()
                elif opcao == "7":
                    self.__salvar()
                    self.__pausar()
                elif opcao == "8":
                    self.__carregar()
                    self.__pausar()
                elif opcao == "9":
                    self.__carregar_exemplo()
                    self.__pausar()
                elif opcao == "0":
                    self.__sair()
                    return
                else:
                    print("\nOpção inválida.")
                    self.__pausar()
            except ValueError as erro:
                print(f"\n[ERRO] {erro}")
                self.__pausar()

    def __sair(self):
        resposta = self.__ler_texto("\nDeseja salvar os dados antes de sair? (S/N): ", False)
        if resposta.upper().startswith("S"):
            try:
                self.__salvar()
            except ValueError as erro:
                print(f"\n[ERRO] {erro}")
        print("\nSistema encerrado. Obrigado!")

    # ==================================================================
    # ALUNOS
    # ==================================================================

    def __menu_alunos(self):
        while True:
            self.__titulo("ALUNOS")
            print(" 1 - Cadastrar aluno")
            print(" 2 - Listar alunos")
            print(" 3 - Consultar aluno (matrícula ou CPF)")
            print(" 4 - Alterar dados do aluno")
            print(" 5 - Ativar / inativar aluno")
            print(" 6 - Definir curso do aluno")
            print(" 7 - Matricular aluno em disciplina")
            print(" 8 - Trancar disciplina do aluno")
            print(" 9 - Excluir aluno")
            print(" 0 - Voltar")
            print("-" * Menu.LARGURA)
            opcao = self.__ler_texto("Opção: ", False)
            if opcao == "0":
                return
            try:
                if opcao == "1":
                    self.__cadastrar_aluno()
                elif opcao == "2":
                    self.__listar_alunos()
                elif opcao == "3":
                    self.__consultar_aluno()
                elif opcao == "4":
                    self.__alterar_aluno()
                elif opcao == "5":
                    self.__status_aluno()
                elif opcao == "6":
                    self.__definir_curso_do_aluno()
                elif opcao == "7":
                    self.__matricular_aluno()
                elif opcao == "8":
                    self.__trancar_disciplina()
                elif opcao == "9":
                    self.__excluir_aluno()
                else:
                    print("\nOpção inválida.")
            except ValueError as erro:
                print(f"\n[ERRO] {erro}")
            self.__pausar()

    def __cadastrar_aluno(self):
        self.__titulo("CADASTRO DE ALUNO")
        nome = self.__ler_texto("Nome completo: ")
        cpf = self.__ler_texto("CPF (somente números): ")
        genero = self.__ler_texto("Gênero (M/F/O): ")
        nascimento = self.__ler_texto("Data de nascimento (dd/mm/aaaa): ")
        aluno = self.__secretaria.cadastrar_aluno(nome, cpf, genero, nascimento)
        print(f"\nAluno cadastrado com sucesso! Matrícula gerada: {aluno.matricula}")

    def __listar_alunos(self):
        self.__titulo("LISTA DE ALUNOS")
        self.__listar(self.__secretaria.alunos)

    def __consultar_aluno(self):
        self.__titulo("CONSULTA DE ALUNO")
        texto = self.__ler_texto("Matrícula ou CPF: ")
        aluno = self.__secretaria.consultar_aluno(texto)
        print()
        aluno.exibir_dados()
        if len(aluno.matriculas) > 0:
            print("\n  Boletim:")
            for linha in aluno.boletim():
                print(f"    {linha}")

    def __alterar_aluno(self):
        self.__titulo("ALTERAR ALUNO")
        texto = self.__ler_texto("Matrícula ou CPF: ")
        aluno = self.__secretaria.consultar_aluno(texto)
        print(f"\nAlterando: {aluno}")
        print("(deixe em branco para manter o valor atual)")
        nome = self.__ler_texto(f"Nome [{aluno.nome}]: ", False)
        genero = self.__ler_texto(f"Gênero M/F/O [{aluno.genero}]: ", False)
        nascimento = self.__ler_texto(f"Nascimento [{aluno.data_nascimento}]: ", False)
        self.__secretaria.alterar_aluno(aluno.matricula, nome, genero, nascimento)
        print("\nDados alterados com sucesso!")

    def __status_aluno(self):
        self.__titulo("ATIVAR / INATIVAR ALUNO")
        texto = self.__ler_texto("Matrícula ou CPF: ")
        aluno = self.__secretaria.alternar_status_aluno(texto)
        print(f"\n{aluno.nome} agora está: {aluno.status()}")

    def __definir_curso_do_aluno(self):
        self.__titulo("DEFINIR CURSO DO ALUNO")
        self.__listar(self.__secretaria.cursos)
        texto = self.__ler_texto("\nMatrícula ou CPF do aluno: ")
        codigo = self.__ler_texto("Código do curso (em branco = retirar do curso): ", False)
        aluno = self.__secretaria.definir_curso_do_aluno(texto, codigo)
        print(f"\n{aluno.nome} -> {aluno.nome_curso()}")

    def __matricular_aluno(self):
        self.__titulo("MATRICULAR ALUNO EM DISCIPLINA")
        texto = self.__ler_texto("Matrícula ou CPF do aluno: ")
        aluno = self.__secretaria.consultar_aluno(texto)
        if aluno.curso is None:
            raise ValueError("Defina primeiro o curso do aluno.")
        print(f"\nDisciplinas do curso {aluno.curso.nome}:")
        self.__listar(aluno.curso.disciplinas)
        codigo = self.__ler_texto("\nCódigo da disciplina: ")
        disciplina = self.__secretaria.matricular_aluno_em_disciplina(aluno.matricula, codigo)
        print(f"\n{aluno.nome} foi matriculado em {disciplina.nome}.")

    def __trancar_disciplina(self):
        self.__titulo("TRANCAR DISCIPLINA")
        texto = self.__ler_texto("Matrícula ou CPF do aluno: ")
        aluno = self.__secretaria.consultar_aluno(texto)
        self.__listar(aluno.matriculas)
        codigo = self.__ler_texto("\nCódigo da disciplina a trancar: ")
        self.__secretaria.trancar_disciplina(aluno.matricula, codigo)
        print("\nDisciplina trancada (as notas dela foram removidas).")

    def __excluir_aluno(self):
        self.__titulo("EXCLUIR ALUNO")
        texto = self.__ler_texto("Matrícula ou CPF: ")
        aluno = self.__secretaria.consultar_aluno(texto)
        print(f"\n{aluno}")
        resposta = self.__ler_texto("Confirma a exclusão? (S/N): ", False)
        if resposta.upper().startswith("S"):
            self.__secretaria.excluir_aluno(aluno.matricula)
            print("\nAluno excluído.")
        else:
            print("\nExclusão cancelada.")

    # ==================================================================
    # PROFESSORES
    # ==================================================================

    def __menu_professores(self):
        while True:
            self.__titulo("PROFESSORES")
            print(" 1 - Cadastrar professor")
            print(" 2 - Listar professores")
            print(" 3 - Consultar professor")
            print(" 4 - Alterar dados do professor")
            print(" 5 - Atribuir disciplina ao professor")
            print(" 6 - Ativar / inativar professor")
            print(" 7 - Excluir professor")
            print(" 0 - Voltar")
            print("-" * Menu.LARGURA)
            opcao = self.__ler_texto("Opção: ", False)
            if opcao == "0":
                return
            try:
                if opcao == "1":
                    self.__cadastrar_professor()
                elif opcao == "2":
                    self.__titulo("LISTA DE PROFESSORES")
                    self.__listar(self.__secretaria.professores)
                elif opcao == "3":
                    codigo = self.__ler_texto("Código do professor: ")
                    print()
                    self.__secretaria.obter_professor(codigo).exibir_dados()
                elif opcao == "4":
                    self.__alterar_professor()
                elif opcao == "5":
                    self.__atribuir_disciplina()
                elif opcao == "6":
                    codigo = self.__ler_texto("Código do professor: ")
                    professor = self.__secretaria.alternar_status_professor(codigo)
                    print(f"\n{professor.nome} agora está: {professor.status()}")
                elif opcao == "7":
                    self.__excluir_professor()
                else:
                    print("\nOpção inválida.")
            except ValueError as erro:
                print(f"\n[ERRO] {erro}")
            self.__pausar()

    def __cadastrar_professor(self):
        self.__titulo("CADASTRO DE PROFESSOR")
        nome = self.__ler_texto("Nome completo: ")
        cpf = self.__ler_texto("CPF (somente números): ")
        genero = self.__ler_texto("Gênero (M/F/O): ")
        nascimento = self.__ler_texto("Data de nascimento (dd/mm/aaaa): ")
        codigo = self.__ler_texto("Código do professor (ex.: P01): ")
        print(f"Titulações: {', '.join(Professor.TITULACOES)}")
        titulacao = self.__ler_texto("Titulação: ")
        professor = self.__secretaria.cadastrar_professor(nome, cpf, genero, nascimento,
                                                          codigo, titulacao)
        print(f"\nProfessor cadastrado: {professor}")

    def __alterar_professor(self):
        self.__titulo("ALTERAR PROFESSOR")
        codigo = self.__ler_texto("Código do professor: ")
        professor = self.__secretaria.obter_professor(codigo)
        print(f"\nAlterando: {professor}")
        print("(deixe em branco para manter o valor atual)")
        nome = self.__ler_texto(f"Nome [{professor.nome}]: ", False)
        titulacao = self.__ler_texto(f"Titulação [{professor.titulacao}]: ", False)
        self.__secretaria.alterar_professor(codigo, nome, titulacao)
        print("\nDados alterados com sucesso!")

    def __atribuir_disciplina(self):
        self.__titulo("ATRIBUIR DISCIPLINA AO PROFESSOR")
        self.__listar(self.__secretaria.disciplinas)
        codigo_professor = self.__ler_texto("\nCódigo do professor: ")
        codigo_disciplina = self.__ler_texto("Código da disciplina: ")
        disciplina = self.__secretaria.atribuir_disciplina_a_professor(codigo_professor,
                                                                      codigo_disciplina)
        print(f"\nDisciplina atribuída: {disciplina}")

    def __excluir_professor(self):
        self.__titulo("EXCLUIR PROFESSOR")
        codigo = self.__ler_texto("Código do professor: ")
        professor = self.__secretaria.obter_professor(codigo)
        print(f"\n{professor}")
        resposta = self.__ler_texto("Confirma a exclusão? (S/N): ", False)
        if resposta.upper().startswith("S"):
            self.__secretaria.excluir_professor(codigo)
            print("\nProfessor excluído (as disciplinas dele ficaram sem professor).")
        else:
            print("\nExclusão cancelada.")

    # ==================================================================
    # CURSOS
    # ==================================================================

    def __menu_cursos(self):
        while True:
            self.__titulo("CURSOS")
            print(" 1 - Cadastrar curso")
            print(" 2 - Listar cursos")
            print(" 3 - Consultar curso (com disciplinas)")
            print(" 4 - Alterar nome do curso")
            print(" 5 - Adicionar disciplina ao curso")
            print(" 6 - Remover disciplina do curso")
            print(" 7 - Excluir curso")
            print(" 0 - Voltar")
            print("-" * Menu.LARGURA)
            opcao = self.__ler_texto("Opção: ", False)
            if opcao == "0":
                return
            try:
                if opcao == "1":
                    codigo = self.__ler_texto("Código do curso (ex.: TI): ")
                    nome = self.__ler_texto("Nome do curso: ")
                    curso = self.__secretaria.cadastrar_curso(codigo, nome)
                    print(f"\nCurso cadastrado: {curso}")
                elif opcao == "2":
                    self.__titulo("LISTA DE CURSOS")
                    self.__listar(self.__secretaria.cursos)
                elif opcao == "3":
                    self.__consultar_curso()
                elif opcao == "4":
                    codigo = self.__ler_texto("Código do curso: ")
                    nome = self.__ler_texto("Novo nome: ")
                    curso = self.__secretaria.alterar_curso(codigo, nome)
                    print(f"\nCurso alterado: {curso}")
                elif opcao == "5":
                    self.__listar(self.__secretaria.disciplinas)
                    codigo = self.__ler_texto("\nCódigo do curso: ")
                    codigo_disciplina = self.__ler_texto("Código da disciplina: ")
                    self.__secretaria.adicionar_disciplina_ao_curso(codigo, codigo_disciplina)
                    print("\nDisciplina adicionada ao curso.")
                elif opcao == "6":
                    codigo = self.__ler_texto("Código do curso: ")
                    codigo_disciplina = self.__ler_texto("Código da disciplina: ")
                    self.__secretaria.remover_disciplina_do_curso(codigo, codigo_disciplina)
                    print("\nDisciplina removida do curso.")
                elif opcao == "7":
                    codigo = self.__ler_texto("Código do curso: ")
                    self.__secretaria.excluir_curso(codigo)
                    print("\nCurso excluído.")
                else:
                    print("\nOpção inválida.")
            except ValueError as erro:
                print(f"\n[ERRO] {erro}")
            self.__pausar()

    def __consultar_curso(self):
        codigo = self.__ler_texto("Código do curso: ")
        curso = self.__secretaria.obter_curso(codigo)
        self.__titulo(f"CURSO {curso.codigo} - {curso.nome}")
        print(f"Carga horária total: {curso.carga_horaria_total()} horas")
        print("\nDisciplinas:")
        self.__listar(curso.disciplinas)
        alunos = self.__secretaria.alunos_do_curso(curso.codigo)
        print(f"\nAlunos matriculados no curso: {len(alunos)}")
        self.__listar(alunos)

    # ==================================================================
    # DISCIPLINAS
    # ==================================================================

    def __menu_disciplinas(self):
        while True:
            self.__titulo("DISCIPLINAS")
            print(" 1 - Cadastrar disciplina")
            print(" 2 - Listar disciplinas")
            print(" 3 - Alterar disciplina")
            print(" 4 - Atribuir professor à disciplina")
            print(" 5 - Excluir disciplina")
            print(" 0 - Voltar")
            print("-" * Menu.LARGURA)
            opcao = self.__ler_texto("Opção: ", False)
            if opcao == "0":
                return
            try:
                if opcao == "1":
                    codigo = self.__ler_texto("Código da disciplina (ex.: POO): ")
                    nome = self.__ler_texto("Nome da disciplina: ")
                    carga = self.__ler_texto("Carga horária (horas): ")
                    disciplina = self.__secretaria.cadastrar_disciplina(codigo, nome, carga)
                    print(f"\nDisciplina cadastrada: {disciplina}")
                elif opcao == "2":
                    self.__titulo("LISTA DE DISCIPLINAS")
                    self.__listar(self.__secretaria.disciplinas)
                elif opcao == "3":
                    self.__alterar_disciplina()
                elif opcao == "4":
                    self.__atribuir_disciplina()
                elif opcao == "5":
                    codigo = self.__ler_texto("Código da disciplina: ")
                    self.__secretaria.excluir_disciplina(codigo)
                    print("\nDisciplina excluída.")
                else:
                    print("\nOpção inválida.")
            except ValueError as erro:
                print(f"\n[ERRO] {erro}")
            self.__pausar()

    def __alterar_disciplina(self):
        self.__titulo("ALTERAR DISCIPLINA")
        codigo = self.__ler_texto("Código da disciplina: ")
        disciplina = self.__secretaria.obter_disciplina(codigo)
        print(f"\nAlterando: {disciplina}")
        print("(deixe em branco para manter o valor atual)")
        nome = self.__ler_texto(f"Nome [{disciplina.nome}]: ", False)
        carga = self.__ler_texto(f"Carga horária [{disciplina.carga_horaria}]: ", False)
        self.__secretaria.alterar_disciplina(codigo, nome, carga)
        print("\nDisciplina alterada com sucesso!")

    # ==================================================================
    # NOTAS
    # ==================================================================

    def __menu_notas(self):
        while True:
            self.__titulo("NOTAS E BOLETIM")
            print(" 1 - Lançar nota")
            print(" 2 - Ver boletim do aluno")
            print(" 3 - Média da turma por disciplina")
            print(" 0 - Voltar")
            print("-" * Menu.LARGURA)
            opcao = self.__ler_texto("Opção: ", False)
            if opcao == "0":
                return
            try:
                if opcao == "1":
                    self.__lancar_nota()
                elif opcao == "2":
                    self.__ver_boletim()
                elif opcao == "3":
                    codigo = self.__ler_texto("Código da disciplina: ")
                    disciplina = self.__secretaria.obter_disciplina(codigo)
                    media = self.__secretaria.media_da_disciplina(codigo)
                    print(f"\nMédia da turma em {disciplina.nome}: {media:.2f}")
                else:
                    print("\nOpção inválida.")
            except ValueError as erro:
                print(f"\n[ERRO] {erro}")
            self.__pausar()

    def __lancar_nota(self):
        self.__titulo("LANÇAR NOTA")
        texto = self.__ler_texto("Matrícula ou CPF do aluno: ")
        aluno = self.__secretaria.consultar_aluno(texto)
        if len(aluno.matriculas) == 0:
            raise ValueError("Este aluno não está matriculado em nenhuma disciplina.")
        print(f"\nDisciplinas de {aluno.nome}:")
        self.__listar(aluno.matriculas)
        codigo = self.__ler_texto("\nCódigo da disciplina: ")
        nota = self.__ler_texto("Nota (0 a 10): ")
        self.__secretaria.lancar_nota(aluno.matricula, codigo, nota)
        matricula = aluno.buscar_matricula(codigo)
        print(f"\nNota lançada! {matricula}")

    def __ver_boletim(self):
        texto = self.__ler_texto("Matrícula ou CPF do aluno: ")
        aluno = self.__secretaria.consultar_aluno(texto)
        self.__titulo(f"BOLETIM - {aluno.nome}")
        print(f"Matrícula: {aluno.matricula}   |   Curso: {aluno.nome_curso()}")
        print("-" * Menu.LARGURA)
        linhas = aluno.boletim()
        if len(linhas) == 0:
            print("O aluno não está matriculado em disciplinas.")
            return
        for linha in linhas:
            print(linha)
        print("-" * Menu.LARGURA)
        print(f"Média geral: {aluno.media_geral():.2f}   |   Situação: {aluno.situacao()}")

    # ==================================================================
    # RELATÓRIOS
    # ==================================================================

    def __menu_relatorios(self):
        while True:
            self.__titulo("RELATÓRIOS")
            print(" 1 - Todas as pessoas (alunos + professores)")
            print(" 2 - Alunos ativos")
            print(" 3 - Alunos inativos")
            print(" 4 - Alunos por curso")
            print(" 5 - Resumo geral da instituição")
            print(" 0 - Voltar")
            print("-" * Menu.LARGURA)
            opcao = self.__ler_texto("Opção: ", False)
            if opcao == "0":
                return
            try:
                if opcao == "1":
                    self.__relatorio_pessoas()
                elif opcao == "2":
                    self.__titulo("ALUNOS ATIVOS")
                    self.__listar(self.__secretaria.listar_alunos_por_status(True))
                elif opcao == "3":
                    self.__titulo("ALUNOS INATIVOS")
                    self.__listar(self.__secretaria.listar_alunos_por_status(False))
                elif opcao == "4":
                    self.__listar(self.__secretaria.cursos)
                    codigo = self.__ler_texto("\nCódigo do curso: ")
                    self.__titulo(f"ALUNOS DO CURSO {codigo.upper()}")
                    self.__listar(self.__secretaria.alunos_do_curso(codigo))
                elif opcao == "5":
                    self.__resumo_geral()
                else:
                    print("\nOpção inválida.")
            except ValueError as erro:
                print(f"\n[ERRO] {erro}")
            self.__pausar()

    def __relatorio_pessoas(self):
        self.__titulo("TODAS AS PESSOAS CADASTRADAS")
        pessoas = self.__secretaria.listar_pessoas()
        if len(pessoas) == 0:
            print("Nenhuma pessoa cadastrada.")
            return
        # POLIMORFISMO: a mesma chamada exibir_dados() serve para
        # objetos Aluno e objetos Professor
        for pessoa in pessoas:
            pessoa.exibir_dados()
        print("-" * Menu.LARGURA)
        print(f"Total: {len(pessoas)} pessoa(s).")

    def __resumo_geral(self):
        dados = self.__secretaria.resumo()
        self.__titulo("RESUMO GERAL")
        print(f"{'Alunos cadastrados':<24}: {dados['alunos']}")
        print(f"{'  - ativos':<24}: {dados['ativos']}")
        print(f"{'  - inativos':<24}: {dados['inativos']}")
        print(f"{'Professores':<24}: {dados['professores']}")
        print(f"{'Cursos':<24}: {dados['cursos']}")
        print(f"{'Disciplinas':<24}: {dados['disciplinas']}")

    # ==================================================================
    # ARQUIVO
    # ==================================================================

    def __salvar(self):
        caminho = self.__repositorio.salvar(self.__secretaria)
        print(f"\nDados salvos em: {caminho}")

    def __carregar(self):
        resposta = self.__ler_texto("Os dados em memória serão substituídos. Continuar? (S/N): ",
                                    False)
        if not resposta.upper().startswith("S"):
            print("\nOperação cancelada.")
            return
        self.__repositorio.carregar(self.__secretaria)
        print(f"\nDados carregados! {self.__secretaria}")

    def __carregar_exemplo(self):
        resposta = self.__ler_texto("Os dados em memória serão substituídos. Continuar? (S/N): ",
                                    False)
        if not resposta.upper().startswith("S"):
            print("\nOperação cancelada.")
            return
        popular(self.__secretaria)
        print(f"\nDados de exemplo carregados! {self.__secretaria}")

    # ==================================================================
    # MÉTODOS DE APOIO DA TELA
    # ==================================================================

    def __titulo(self, texto):
        print()
        print("=" * Menu.LARGURA)
        print(texto.center(Menu.LARGURA))
        print("=" * Menu.LARGURA)

    def __listar(self, objetos):
        """Mostra qualquer lista de objetos usando o __str__ de cada um."""
        if len(objetos) == 0:
            print("Nenhum registro encontrado.")
            return
        numero = 1
        for objeto in objetos:
            print(f"{numero:>3} - {objeto}")
            numero += 1

    def __ler_texto(self, rotulo, obrigatorio=True):
        valor = input(rotulo).strip()
        if obrigatorio and valor == "":
            raise ValueError("Este campo é obrigatório.")
        return valor

    def __pausar(self):
        input("\nPressione ENTER para continuar...")
