> Contexto do formato ADR em `docs/adr/` (ver README do repo). Case educacional.

## ADR-0001 — Linguagem e runtime: **Python**
**Status:** Aceito

### Contexto
Precisamos de uma linguagem para escrever o assistente (Pinhão), as ferramentas que ele chama e a ligação com o banco. Dois fatores pesam: o ecossistema de IA/dados e a facilidade de **outra pessoa da equipe do Seu Nei continuar** o projeto (um dos desejos do cliente).

### Decisão
Usar **Python**.

### Alternativas descartadas
- **Node.js / TypeScript** — ótimo ecossistema e tipagem forte, mas a maior parte dos exemplos, bibliotecas e da familiaridade do público (e do autor) em IA/dados está em Python. Descartado por afinidade e curva de continuidade.
- **Go / Rust** — mais rápidos e robustos, mas o ferramental de LLM é menos maduro e a curva é íngreme. Para uma primeira versão, é potência que não vamos usar. Descartado por *overkill*.

### Consequências que aceitamos
- (+) Ecossistema maduro de LLM e dados; fácil de contratar/continuar.
- (−) Runtime mais lento e tipagem opcional. **Mitigação:** usar *type hints* e um verificador de tipos (mypy/pyright) para o projeto não virar bagunça.
