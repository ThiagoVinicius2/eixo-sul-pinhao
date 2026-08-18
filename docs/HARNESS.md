# Harness do agente de código

Este projeto é construído **com** um agente de código, e isso é explícito. Esta página
responde: qual harness, o que foi automatizado, o que ficou deliberadamente fora do alcance do
agente, e como o que ele escreve é revisado.

## Qual harness e por quê
**Claude Code.** Motivos:
- Lê o `CLAUDE.md` na raiz automaticamente, então o contexto e os limites do projeto viajam
  junto com cada tarefa — que é exatamente o que este desafio quer treinar.
- Trabalha no terminal / app, com acesso a arquivos e comandos, o que combina com um fluxo de
  **doc-primeiro** (os documentos em `docs/` guiam o código).
- Casa com a revisão por **pull request**: o agente propõe o diff, o humano decide.

Alternativas consideradas: **Cursor** (ótimo no editor, mas queríamos o contexto num arquivo
versionado e um fluxo de terminal/PR), **Aider** e **Codex CLI** (bons, mas a integração do
`CLAUDE.md` + skills fechou a escolha). Não é "o único certo" — é o explicado.

## O que foi automatizado PARA o agente
- **Arquivo de contexto (`CLAUDE.md`).** A regra de ouro, as regras invioláveis e o mapa do
  repo, para o agente não improvisar limites.
- **Comandos (`make setup/seed/test/lint/run`).** Um jeito único de rodar, para o agente (e a
  equipe) não inventar caminho.
- **Validações que bloqueiam (CI + hooks).** `ruff` (lint/format), `mypy` (tipos), `pytest`
  (testes) e varredura de segredo. Rodam no CI e barram o merge; um *pre-commit* roda o básico
  antes de cada commit.
- **`main` protegida.** Nada entra direto; só por PR que passou no CI.

## O que deliberadamente NÃO foi deixado na mão do agente
- **Aprovar propostas.** Isso é humano, por definição do produto.
- **Mudar escopo, ADRs ou PRD.** São decisões de produto/arquitetura.
- **Mexer na porta de aprovação, em pagamento ou em emissão de documento** sem revisão humana
  redobrada.
- **Relaxar guardrails.** As barreiras de segurança não são "otimização" que o agente decide
  sozinho.

Esses limites estão escritos no `CLAUDE.md` (seções 3 e 8) para o agente vê-los, e reforçados
no CI e na proteção de branch para o caso de ele tentar mesmo assim — porque, coerente com a
regra de ouro, **o código decide o que pode ser feito**, não a boa vontade do agente.

## Como o que o agente escreve é revisado
1. O agente abre um **PR** com um diff pequeno e uma descrição do que mudou.
2. O **CI** roda e bloqueia se lint, tipos, testes ou segredo falharem.
3. Um **humano lê o diff**, com atenção redobrada em `tools/`, `guardrails/`, aprovação e
   pagamento.
4. Só então faz merge na `main`.
