> Contexto do formato ADR em `docs/adr/` (ver README do repo). Case educacional.

## ADR-0003 — Dados: **um banco como fonte única de verdade** (Postgres; SQLite na v1)
**Status:** Aceito

### Contexto
Preço, estoque e prazo precisam de **garantia absoluta** — o cliente não pode decidir em cima de um número que a IA "achou". Precisamos de um lugar único e confiável para esses dados, **fora** do alcance do modelo.

### Decisão
Um **banco relacional** como fonte única de verdade do catálogo e do estado das conversas/aprovações. Alvo: **Postgres**. Na v1, **SQLite** é aceitável para rodar simples na máquina de qualquer um da equipe.

### Alternativas descartadas
- **Guardar o catálogo num arquivo (JSON) junto do código.** Fácil, mas a "verdade" fica espalhada, sem trilha de mudança, e mistura dado com código. Descartado por **rastreabilidade**.
- **Banco de "documentos" (NoSQL).** Flexível, mas o catálogo é estruturado (modelo, spec, preço, estoque) e um banco relacional dá **integridade** melhor. Descartado por **encaixe**.
- **Usar busca por similaridade (RAG/vetores) como fonte de preço.** RAG é ótimo para *texto* (descrição, manual), mas **péssimo para número exato**: preço precisa de consulta exata, não de "resposta parecida". Descartado **para dados críticos** — RAG pode entrar depois só para descrições.

### Consequências que aceitamos
- (+) **Garantia absoluta** e integridade dos números; separação limpa entre "dado" e "modelo"; trilha de auditoria natural.
- (−) Exige um pouco mais de preparo (migrações e um script para popular o catálogo fictício) do que um arquivo solto. **Mitigação:** um *seed* simples com o catálogo de exemplo resolve.

---

## O que estas decisões destravam
Com linguagem, topologia e dados definidos, o próximo passo é o **desenho da arquitetura**: um diagrama mostrando o agente, as ferramentas, o banco, onde entra o humano (aprovação) e o que acontece quando algo falha. Depois disso, montamos o **repositório e o arquivo de contexto do agente de código** (`CLAUDE.md`/`AGENTS.md`) e só então começamos a programar a primeira fatia vertical.
