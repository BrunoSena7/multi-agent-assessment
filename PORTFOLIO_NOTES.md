# Como apresentar o projeto em entrevista

## Contexto

Este projeto foi inspirado no exercício acadêmico “Sistema de Gestão Escolar com Agentes Autônomos”, que propunha três agentes CrewAI em sequência. A versão de portfólio preserva os três papéis, mas implementa a orquestração explicitamente com a API da OpenAI para controlar o contexto compartilhado e testar os contratos de entrada e saída.

## O que o fluxo faz

1. O agente Professor recebe disciplina, tópico e dificuldade e gera uma prova estruturada em JSON, incluindo o gabarito.
2. O orquestrador constrói uma nova entrada contendo somente enunciados e alternativas. O gabarito não é enviado ao agente Estudante.
3. O agente Estudante responde em JSON.
4. O agente Revisor recebe prova, gabarito e respostas e devolve correções e feedback.
5. O código valida campos, limita os pontos concedidos por questão e recalcula a nota final a partir das correções individuais, em vez de confiar no total produzido pelo LLM.

## Decisões técnicas que vale explicar

- **Orquestração sequencial:** cada etapa depende da saída estruturada da etapa anterior.
- **Contratos JSON:** facilita validar o formato e reduz ambiguidades entre agentes.
- **Separação de contexto:** o estudante não recebe o gabarito; isso reduz vazamento de informação no próprio fluxo.
- **Validação determinística:** o LLM sugere pontos por questão, mas o código limita os valores e recalcula a soma.
- **Testes com cliente simulado:** permitem verificar hand-offs e isolamento do gabarito sem consumir créditos de API.

## Limitações que devem ser reconhecidas

Os três agentes usam o mesmo modelo base com prompts diferentes. Não são modelos independentes nem agentes com memória persistente. A avaliação é uma sugestão do LLM e exige revisão humana em uso educacional real. O sistema não possui autenticação ou persistência.

## Perguntas de revisão antes de apresentar

- Por que o estudante não deve receber o gabarito?
- Por que pedir JSON em vez de texto livre?
- O que acontece quando o LLM retorna JSON inválido?
- Por que a nota é recalculada no código?
- Quais testes podem ser executados sem chamar o provedor?
- O que mudaria para suportar modelos diferentes por agente?
