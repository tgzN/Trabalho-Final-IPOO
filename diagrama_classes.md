# Diagrama de classes — Sistema de Secretaria Acadêmica (IPOO)

```mermaid
classDiagram
    class Pessoa {
        -nome
        -cpf
        -genero
        -data_nascimento
        -ativo
        +ativar()
        +inativar()
        +status()
        +papel()
        +exibir_dados()
        +to_dict()
    }

    class Aluno {
        -matricula
        -curso
        -matriculas
        +gerar_matricula()
        +definir_curso(curso)
        +matricular_em(disciplina)
        +lancar_nota(codigo, nota)
        +media_geral()
        +situacao()
        +boletim()
        +papel()
        +exibir_dados()
    }

    class Professor {
        -codigo
        -titulacao
        -disciplinas
        +atribuir_disciplina(disciplina)
        +carga_horaria_total()
        +papel()
        +exibir_dados()
    }

    class Curso {
        -codigo
        -nome
        -disciplinas
        +adicionar_disciplina(d)
        +remover_disciplina(codigo)
        +carga_horaria_total()
    }

    class Disciplina {
        -codigo
        -nome
        -carga_horaria
        -professor
        +atribuir_professor(p)
        +nome_professor()
    }

    class Matricula {
        -aluno
        -disciplina
        -notas
        +lancar_nota(nota)
        +media()
        +situacao()
    }

    class Secretaria {
        -alunos
        -professores
        -cursos
        -disciplinas
        +cadastrar_aluno(...)
        +consultar_aluno(texto)
        +alterar_aluno(...)
        +excluir_aluno(matricula)
        +lancar_nota(...)
        +listar_pessoas()
        +resumo()
    }

    class Repositorio {
        -caminho
        +salvar(secretaria)
        +carregar(secretaria)
    }

    class Menu {
        -secretaria
        -repositorio
        +executar()
    }

    Pessoa <|-- Aluno : herança
    Pessoa <|-- Professor : herança

    Aluno "1" *-- "0..*" Matricula : possui
    Matricula "0..*" --> "1" Disciplina : refere-se a
    Curso "1" o-- "0..*" Disciplina : é formado por
    Aluno "0..*" --> "0..1" Curso : está matriculado em
    Disciplina "0..*" --> "0..1" Professor : é lecionada por

    Secretaria o-- Aluno
    Secretaria o-- Professor
    Secretaria o-- Curso
    Secretaria o-- Disciplina

    Menu --> Secretaria : usa
    Menu --> Repositorio : usa
    Repositorio ..> Secretaria : grava e lê
```

## Leitura rápida

| Relação | Significado |
|---|---|
| `Pessoa <|-- Aluno` | **Herança**: Aluno é uma Pessoa e reaproveita nome, CPF, gênero, data e situação cadastral. |
| `Pessoa <|-- Professor` | **Herança**: Professor também é uma Pessoa; ambos sobrescrevem `papel()` e `exibir_dados()` (**polimorfismo**). |
| `Aluno *-- Matricula` | **Composição**: as matrículas só existem dentro do aluno; se o aluno é excluído, elas vão com ele. |
| `Curso o-- Disciplina` | **Agregação**: o curso é formado por disciplinas que existem independentemente dele. |
| `Secretaria o-- ...` | A Secretaria **guarda** as listas de objetos e concentra as regras de negócio. |
| `Menu --> Secretaria` | O Menu (tela) não guarda dados: só pede as operações para a Secretaria. |
