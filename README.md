# Sistema de Secretaria Acadêmica

Trabalho final da disciplina **IPOO — Introdução à Programação Orientada a Objetos**.

- **Instituição atendida:** UDESC CEPLAN — São Bento do Sul (SC)
- **Grupo:** Bruno, Leandro, Guilherme e Tiago
- **Linguagem:** Python 3 (apenas biblioteca padrão: `json` e `os`)

## Como executar

```
python main.py
```

No menu principal, a opção **9 — Carregar dados de exemplo** preenche o sistema com
cursos, disciplinas, professores, alunos e notas para testar rapidamente.

## Classes

| Arquivo | Classe | Papel |
|---|---|---|
| `pessoa.py` | `Pessoa` | classe base: nome, CPF, gênero, nascimento e situação cadastral |
| `aluno.py` | `Aluno(Pessoa)` | matrícula automática, curso, disciplinas, média e situação |
| `professor.py` | `Professor(Pessoa)` | código, titulação e disciplinas que leciona |
| `curso.py` | `Curso` | é formado por disciplinas |
| `disciplina.py` | `Disciplina` | código, carga horária e professor responsável |
| `matricula.py` | `Matricula` | liga aluno e disciplina e guarda as notas |
| `secretaria.py` | `Secretaria` | cadastrar, listar, alterar, excluir e relatórios |
| `repositorio.py` | `Repositorio` | grava e lê os dados em `dados/secretaria.json` |
| `menu.py` | `Menu` | menu de opções no terminal |
| `main.py` | — | ponto de entrada do programa |

## Conceitos de orientação a objetos

- **Encapsulamento:** atributos privados (`__cpf`, `__nome`) com `@property` que valida antes de guardar.
- **Herança:** `Aluno` e `Professor` herdam de `Pessoa` e usam `super().__init__()`.
- **Polimorfismo:** `papel()` e `exibir_dados()` são sobrescritos; o relatório de pessoas percorre
  alunos e professores na mesma lista chamando o mesmo método.
- **Composição:** o aluno possui `Matricula`s; o curso é formado por `Disciplina`s.
- **Atributo de classe:** `Aluno._proximo_numero` gera as matrículas (2026001, 2026002...).
- **Método especial:** `__str__` em todas as classes de dados, usado nas listagens do menu.

O diagrama de classes está em [`diagrama_classes.md`](diagrama_classes.md).
