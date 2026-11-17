# Multi-Agent Assessment — orquestração sequencial de agentes

Aplicação Streamlit que simula um ciclo completo de avaliação com três agentes LLM especializados: Professor, Estudante e Revisor.

> **Origem acadêmica:** refatoração do exercício “Sistema de Gestão Escolar com Agentes Autônomos” (Dia 04, Projeto 11) do repositório de materiais do curso de extensão. O exercício original definia três agentes CrewAI e três tarefas em sequência. Esta edição independente preserva os papéis e a ordem do fluxo, mas implementa a orquestração explicitamente com a API da OpenAI para tornar os hand-offs, validações e testes mais transparentes.

## O que demonstra

- decomposição de um processo em papéis especializados;
- orquestração sequencial com três chamadas de LLM;
- passagem controlada de contexto entre agentes;
- isolamento do gabarito: o agente Estudante recebe somente as questões;
- saída estruturada em JSON e validação de campos obrigatórios;
- correção com pontuação e feedback;
- relatório final em Markdown;
- testes automatizados com cliente LLM simulado, sem consumir API.

## Arquitetura

```text
Entrada: disciplina + tópico + dificuldade
                 |
                 v
       Agente 1 — Professor
       prova + gabarito (JSON)
                 |
         remove gabarito
                 |
                 v
       Agente 2 — Estudante
          respostas (JSON)
                 |
                 v
        Agente 3 — Revisor
     nota + correções + feedback
                 |
                 v
       Relatório estruturado
```

## Como executar

Requer Python 3.10 ou superior e uma chave própria da OpenAI.

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
# Linux/macOS: source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env  # Windows: copie o arquivo manualmente e preencha a chave
streamlit run app.py
```

Configure `OPENAI_API_KEY` e, opcionalmente, `OPENAI_MODEL` no `.env` ou informe a chave na barra lateral. Uma execução realiza três chamadas sequenciais ao modelo e pode gerar custos de API.

## Testes

Os testes usam um cliente simulado e verificam a ordem das três chamadas e o isolamento do gabarito. Notas para preparar uma apresentação técnica estão em `PORTFOLIO_NOTES.md`.

```bash
pytest -q
```

## Limitações e segurança

- As três etapas usam o mesmo modelo configurado, com prompts e responsabilidades diferentes; não são três modelos treinados de forma independente.
- A nota é proposta por um LLM e não deve ser usada como avaliação escolar oficial sem revisão humana.
- Não há autenticação, persistência de resultados, integração com sistemas acadêmicos ou deploy de produção.
- O modelo pode produzir erros; o relatório deve ser revisado por uma pessoa.
- Não informe dados pessoais de estudantes ou conteúdo confidencial.

## Créditos e escopo

Versão de portfólio refatorada com apoio de ferramentas de IA por Bruno Sena a partir do exercício acadêmico do curso de extensão. O código desta versão deve ser revisado e compreendido pelo autor antes de ser apresentado. Esta versão não é uma plataforma escolar implantada em produção.
