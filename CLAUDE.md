# CLAUDE.md — contexto do projeto para o agente de código

Este arquivo é lido pelo agente de código (Claude Code) antes de trabalhar. Ele diz o que
você **precisa saber para não quebrar este projeto**. Leia até o fim antes de editar código.

> Projeto **educacional e independente**, sem vínculo com a AB Volvo / Volvo Group. Dados,
> empresa e personagens são fictícios. Ver `README.md` para o disclaimer completo.

---

## 1. O que é este projeto (em uma frase)
Um agente de vendas consultivas ("Pinhão") para uma concessionária fictícia de caminhões
("Eixo Sul"): conversa, entende a necessidade, recomenda, monta proposta e leva à venda —
com o humano aprovando o que é irreversível.

## 2. A regra de ouro (não negociável)
> **O modelo de linguagem decide o que dizer. O código decide o que pode ser feito.**

Implicações práticas, que valem para todo commit:
- Regra de negócio (preço, desconto, disponibilidade, prazo, quem aprova) vive em **código**
  (`src/pinhao/tools/` e `src/pinhao/guardrails/`), **nunca** no texto de um prompt.
- O LLM **propõe** ações; o código **valida e executa**. Se o LLM "pedir" algo fora da regra,
  o código recusa — não o prompt pedindo "por favor não faça isso".

## 3. Regras invioláveis (se você for quebrar uma delas, PARE e abra um PR pequeno pedindo revisão humana)
1. **Nada de fato de catálogo saindo do modelo.** Preço, estoque, prazo e specs sempre vêm de
   uma ferramenta que consulta o banco (`src/pinhao/db/`). O LLM nunca "sabe" esses números.
2. **Nenhuma ação irreversível sem aprovação humana.** Enviar proposta/documento ao cliente só
   depois de passar pela fila de aprovação. A porta de aprovação não se contorna por atalho.
3. **Sem dinheiro real e sem documento fiscal real.** Pagamento só em ambiente de teste
   (sandbox); documentos são simulações rotuladas como tal.
4. **PII protegida.** Não logar dados sensíveis do cliente em texto puro; mascarar antes de ir
   para o LLM e antes de gravar log. Segredos só em variáveis de ambiente (`.env`), nunca no
   código nem no prompt.
5. **Tudo observável.** Cada turno e cada chamada de ferramenta registram entrada, saída e
   custo em tokens. Não remova nem "otimize" o tracing sem revisão.
6. **Desconto é regra, não conversa.** Existe uma faixa fixa em código; acima dela, exige
   aprovação humana. O LLM nunca concede desconto por conta própria.

## 4. Onde as coisas vivem
```
docs/            documentação (leia antes de decidir): PRD, DISCOVERY, ARCHITECTURE, adr/
src/pinhao/
  agent/         loop fino do agente — orquestra, NÃO contém regra de negócio
  tools/         ferramentas = regra de negócio em código (preço, financiamento, proposta...)
  guardrails/    barreiras determinísticas: entrada (PII, injection) e saída (validação, limites)
  db/            acesso ao banco = fonte única da verdade do catálogo e do estado
  llm/           camada fina do provedor de LLM (troca de modelo por custo); NÃO decide regra
  observability/ tracing, logs estruturados e custo por conversa
tests/           testes; todo comportamento de tool/guardrail precisa de teste
data/seed/       catálogo fictício para popular o banco
```
Decisões de arquitetura estão em `docs/adr/`. Se sua mudança contraria um ADR, ela precisa de
um ADR novo — não contrarie um em silêncio.

## 5. Convenções de código
- **Python** com *type hints* em tudo. `mypy` precisa passar.
- Formatação e lint com `ruff` (format + check). Sem exceções não justificadas.
- Uma ferramenta = uma função com validação explícita da entrada e retorno tipado. Ela é a
  fronteira de segurança; trate-a como tal.
- Nomes e mensagens ao usuário em **português**.

## 6. Comandos
```
make setup      # instala dependências
make seed       # popula o banco com o catálogo fictício
make test       # roda os testes
make lint       # ruff + mypy
make run        # sobe o agente localmente
```
(Se o alvo não existir ainda, crie-o de forma mínima e coerente com este arquivo.)

## 7. Definição de pronto (o código é revisado assim)
- `main` é protegida. Toda mudança entra por **pull request**.
- O CI (`.github/workflows/ci.yml`) roda lint, type-check, testes e varredura de segredo, e
  **bloqueia** o merge se algo falhar.
- Um humano lê o diff. Mudanças em `tools/`, `guardrails/`, no fluxo de aprovação ou em
  pagamento recebem **revisão redobrada**.

## 8. O que você (agente) NÃO decide sozinho — escale para um humano
- Mudar o **escopo** (o que entra/sai da v1 está no PRD).
- Alterar a **porta de aprovação humana** ou qualquer caminho que torne uma ação irreversível.
- Tocar em **pagamento** ou em emissão de documento.
- Relaxar um **guardrail** ou uma regra inviolável da seção 3.
- Editar um **ADR** ou o **PRD**.
Nesses casos: faça o mínimo, deixe claro no PR o que precisa de decisão humana, e pare.
