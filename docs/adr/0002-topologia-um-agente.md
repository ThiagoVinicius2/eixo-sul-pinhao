> Contexto do formato ADR em `docs/adr/` (ver README do repo). Case educacional.

## ADR-0002 — Topologia: **um agente com ferramentas + regras no código** (não multi-agente)
**Status:** Aceito · *É a decisão mais importante do projeto.*

### Contexto
Quantos "cérebros de IA" o sistema tem? A tese do projeto é **"o modelo decide o que dizer; o código decide o que pode ser feito"**. O discovery mostrou uma jornada **curta e linear** (conversa → recomendação → proposta → aprovação humana), com pouquíssimos pontos onde a IA precisa "pensar sozinha".

*Analogia:* pense num caixa de banco simpático. Ele conversa e explica bem, mas **não consegue**, por mais que peçam bonito, liberar algo que o sistema não autoriza. A conversa é a IA; as regras do que pode/não pode ficam trancadas no código.

### Decisão
**Um único agente de IA** que conversa com o cliente e **chama ferramentas** (buscar catálogo, consultar preço, simular financiamento, montar rascunho, enfileirar para aprovação). Toda regra crítica — preço, desconto, disponibilidade, quem aprova — vive **em código determinístico dentro das ferramentas**, nunca no texto do prompt.

### Alternativas descartadas
- **Vários agentes se orquestrando** (um "vendedor", um "precificador", um "financeiro" conversando entre si). Parece moderno, mas: cada agente é mais uma chamada de IA = **mais custo** (o medo do Seu Nei da conta gigante), fica **mais difícil de auditar** ("qual dos robôs errou?") e a jornada é simples demais para justificar isso. Descartado por **custo e auditabilidade**.
- **Fluxo 100% roteirizado, sem IA** (só menus e regras). Elimina a alucinação, mas mata o valor: **é o site com filtro que já não funciona**. Descartado por perder a razão de existir do produto.
- **Framework pesado que "esconde" a lógica** do agente. Facilita começar, mas tira a regra de negócio da vista e dificulta cumprir o princípio "código decide o que pode ser feito". Descartado por **opacidade** (o Seu Nei não aceita "mágica").

### Consequências que aceitamos
- (+) Mais **barato**, mais **auditável** e mais **fácil de explicar** — bom para o portfólio e para o cliente.
- (+) Regras no código = **segurança de verdade** contra o "espertinho" que tenta enganar na conversa.
- (−) Um agente só pode ficar sobrecarregado **se o escopo crescer muito**. **Mitigação:** aceitamos isso agora; dividir em vários agentes vira uma decisão *futura*, quando (e se) a complexidade pedir.
