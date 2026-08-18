# Discovery — Eixo Sul / "Pinhão"

> Documento de descoberta que antecede os ADRs e SPECs. Objetivo: decidir, etapa por etapa, **onde a linguagem natural gera valor, onde gera risco, o que é irreversível e onde o cliente precisa de garantia absoluta** (número do banco), e não de resposta plausível. Case fictício, fins educacionais — ver disclaimer no PRD.

## Como lemos cada etapa (as quatro lentes)
1. **Valor × Risco** — a linguagem natural aqui ajuda ou ameaça?
2. **Pior caso** — o que acontece de pior se o modelo errar?
3. **Irreversibilidade / aprovação** — dá pra desfazer? Quem aprova antes?
4. **Garantia absoluta** — precisa vir determinístico do banco/regra, ou basta resposta plausível?

---

## Mapa da jornada do Seu Valdir (autônomo comprando 1 caminhão)

| # | Etapa | L1 · Valor × Risco | L2 · Pior caso se errar | L3 · Irreversível? / Aprova | L4 · Precisa garantia absoluta? |
|---|---|---|---|---|---|
| 1 | Abertura / acolhimento | **Valor** | Tom ruim; cliente sai. Baixo custo. | Não | Não |
| 2 | Descoberta da operação (carga, rota, km/mês, relevo, orçamento) | **Valor máximo** — é o trunfo | Entende errado a necessidade → recomenda errado lá na frente | Não | Não (mas registrar o que foi coletado) |
| 3 | Recomendação de configuração | **Valor com trilho** | Recomenda modelo que não existe/ não serve | Não (revisável) | **Parcial**: o modelo só pode escolher **entre itens que a ferramenta de catálogo retornou** — nunca inventar modelo/spec |
| 4 | Preço / estoque / prazo | **Risco puro** | Alucina preço/estoque → cliente decide em cima de mentira | Não, mas propaga erro | **Sim** — 100% do banco |
| 5 | Simulação de financiamento (entrada, parcela, taxa) | **Risco puro** | Parcela errada; falsa expectativa; dano de imagem | Não | **Sim** — cálculo determinístico em código, nunca o LLM fazendo conta |
| 6 | Montagem da proposta comercial (documento) | **Risco** | Junta preço+spec errados num papel com a marca da loja | Reversível **enquanto rascunho** | **Sim** — números vêm das etapas 4/5, o LLM só redige o texto |
| 7 | Aprovação humana interna | **Controle** (fora do LLM) | — (aqui o modelo não decide) | É **o portão** | Autorização de quem aprova mora no **código** |
| 8 | Envio / liberação da proposta ao cliente | **Irreversível** | Documento com erro vai pro cliente; sem volta | **Sim** — só após aprovação humana | Sim |
| 9 | Pós-venda (peças, manutenção, telemetria) | — | — | — | *Fora da v1* |

---

## Decisões travadas (a minha recomendação)

**D1 — A fronteira "valor vira risco" fica entre a etapa 4 e a 3, mas com um trilho na 3.**
A recomendação (3) continua sendo do LLM, porque é aí que mora a mágica consultiva — **mas ele só escolhe entre as opções que a ferramenta de catálogo devolveu.** Ele não inventa modelo, não inventa spec. Assim a etapa 3 é valor sem virar alucinação. Da etapa 4 em diante (preço/prazo/financiamento/documento) é **risco puro**: nada sai da cabeça do robô.

**D2 — O único passo irreversível na v1 é o envio da proposta (8), e ele exige aprovação humana (7).**
Regra geral que vai pra código: **todo documento que sai para o cliente passa por um humano.** É o portão do Seu Nei.

**D3 — Garantia absoluta (determinístico, nunca LLM):** preço, estoque, prazo, combinações de spec válidas, cálculo de parcela e limites de desconto. Quem pode aprovar também é regra de código, não de prompt.

**D4 — Decisões de escopo (escopo é decisão de risco, não preguiça):**
- **Fora da v1:** avaliação do usado na troca (*trade-in* — é uma avaliação de valor, arriscada e não deve ser do LLM), **análise de crédito real** (a v1 faz só **simulação** de financiamento, rotulada como estimativa, em ambiente de teste), test drive/visita, ônibus e construção, pós-venda.
- Motivo: cada um desses agrega um risco novo (avaliação, crédito, agenda) que não precisa estar na primeira fatia vertical para provar a tese "conversa consultiva → proposta com humano no meio".

**D5 — O desconto é regra, não conversa.** O Pinhão nunca "concede" desconto na conversa. Existe uma faixa fixa em código; acima dela, só com aprovação humana. Isso mata o medo do "espertinho que engana o robô".

---

## O que isso já define para os próximos documentos
- **Ferramentas (tools) mínimas da v1:** `buscar_catalogo`, `consultar_preco_estoque_prazo`, `simular_financiamento`, `montar_rascunho_proposta`, `enfileirar_para_aprovacao`. Toda regra de negócio vive aqui, não no prompt.
- **Estados do fluxo:** descoberta → recomendação → proposta (rascunho) → **aguardando aprovação** → liberada / recusada.
- **O que sempre é logado (auditoria/custo):** cada turno, cada chamada de ferramenta (entrada/saída), tokens e custo por conversa.

## Perguntas que sobram para virar ADR
- [ ] **Stack:** linguagem, banco, provedor de LLM.
- [ ] **Quantos agentes:** um agente com ferramentas, ou orquestrador + especialistas?
- [ ] **Como garantir grounding:** o modelo responde só a partir do retorno das tools (sem memória paramétrica de catálogo) — como impomos isso no código?
- [ ] **Onde mora a aprovação humana:** fila simples no banco + tela interna? canal separado?

---

## Recomendação de stack e agentes (para o ADR-0001)
Minha sugestão, já pensando na plateia da Jornada de Dados e em "código decide o que pode ser feito":
- **Python** (ecossistema de agentes/LLM mais maduro e familiar ao público).
- **Um único agente com ferramentas + guardrails determinísticos**, e **não** um enxame de agentes. Mais barato, mais fácil de auditar e de explicar — e o desafio premia arquitetura *explicada*, não complexa.
- **Loop de tool-calling explícito** (agente "fino") em vez de um framework pesado que esconde a lógica: mantém a regra de negócio visível no seu código.
- **Banco:** Postgres (ou SQLite na v1 para simplicidade) como fonte única de verdade do catálogo.
- **Provedor de LLM:** manter uma camada fina que permita trocar de modelo (barato para roteio/tarefa fácil, caro só quando precisa) — isso é o controle de custo virando arquitetura.

Cada uma dessas vira um ADR com a alternativa descartada e a consequência aceita.
