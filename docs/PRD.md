# Case & PRD — Eixo Sul / "Pinhão"

> **Disclaimer (colar no README e no card do projeto):** Projeto **educacional e independente**, sem qualquer vínculo, afiliação ou endosso da **AB Volvo / Volvo Group**. A Volvo aparece aqui apenas como **referência real que inspirou o domínio** (venda consultiva de veículos pesados). Empresa, personagens, produto e todos os dados de catálogo, preço, estoque e prazo são **fictícios e ilustrativos**. Marcas citadas pertencem aos seus respectivos donos. Não há dinheiro real nem documento com validade fiscal: pagamentos usam ambiente de teste e documentos são simulações.

> **Como usar este arquivo:** o que está entre `[colchetes]` é decisão sua. Renomeie o negócio, o produto ou as personas se quiser — a Regra nº 1 do desafio pede um case com nome próprio, então o importante é que os nomes sejam **seus** e apareçam de forma consistente em toda a documentação e no código.

---

# Parte 1 — O Case (com nome e sobrenome)

## O negócio — **Eixo Sul**
Concessionária **fictícia** da família Bevilácqua, de caminhões e ônibus em **Curitiba/PR**, fundada em 1984, hoje de segunda geração. Vende veículos pesados **inspirados no portfólio real da Volvo** (linhas VM, FM, FMX, FH/FH16 e chassis de ônibus) para transportadores da região Sul. É um negócio de **venda consultiva**: ninguém entra na loja pedindo "um FH 540 6x2 com I-Shift" — entra dizendo "preciso rodar grão pro Paraná inteiro sem quebrar o caminhão". Traduzir necessidade em configuração é o serviço.

*(Volvo = inspiração/benchmark do domínio; a concessionária e tudo mais é fictício — ver disclaimer.)*

## O cliente que te contratou — **Ademir "Seu Nei" Bevilácqua**, 60
Dono de segunda geração, vendedor da velha guarda. Fechou negócio a vida inteira apertando mão e conhecendo a operação do cliente. Está perdendo venda porque o site tem filtro e categoria, e o transportador "não sabe traduzir o que quer em filtro, desiste e vai embora". Quer um atendimento que **converse de verdade**, mas desconfia de tecnologia: *"não aceito um sistema que funciona por mágica"*. Os medos dele são o coração dos requisitos (ver Parte 2). É o Seu Nei que vai aparecer nos seus ADRs: *"descartamos X porque o Seu Nei exige aprovar toda proposta antes de sair"*.

## O produto que você está construindo — **Pinhão**
O consultor digital de vendas da Eixo Sul. *(Nome fácil de trocar — alternativas: "Baú", "RodaCerta". "Pinhão" é o ícone do Paraná e dá cara regional.)*

- **Personalidade:** consultor de frota experiente. Direto, sem juridiquês nem tecnês, fala a língua do transportador ("PBT", "entre-eixos", "consumo", "parcela"). Curioso sobre a operação antes de recomendar. Nunca empurra o mais caro; recomenda o que serve.
- **O que ele faz:** entende a necessidade → recomenda a configuração certa → monta um **rascunho de proposta comercial** → simula financiamento → entrega para um humano aprovar antes de qualquer coisa "sem volta".
- **O que ele nunca faz sozinho:** afirmar preço/estoque/prazo de cabeça, dar desconto fora da regra, ou emitir proposta/documento sem aprovação humana.

## Quem é atendido (personas)
1. **Seu Valdir — autônomo/pequeno frotista.** 1 a 3 caminhões. Fala 100% por necessidade, sensível a parcela e consumo. *(Persona da fatia vertical da v1.)*
2. **Juliana — gestora de frota de transportadora média.** Compra em lote, decide por **TCO e uptime**, quer contrato de manutenção e telemetria. *(v2.)*
3. **Cooperativa/viação urbana — comprador de chassis de ônibus** (linha urbana/BRT). *(fora da v1.)*
4. **Construtora/locadora — precisa de FMX para obra.** *(fora da v1.)*

---

# Parte 2 — PRD (esqueleto para você preencher)

## 1. Problema
O site atual da Eixo Sul filtra por categoria e modelo, mas o cliente de veículo pesado **chega por necessidade, não por nome**. Ele não sabe traduzir "rodar grão em longa distância com baixo consumo" em "FH 6x2 D13 500cv". Resultado: abandono no funil e perda de venda consultiva — justamente o que a concessionária faz melhor no presencial.

## 2. Para quem
- **Usuário final:** o comprador de veículo pesado (persona 1 na v1: Seu Valdir).
- **Usuário interno:** o vendedor/aprovador da Eixo Sul (o "humano no meio" que aprova proposta).
- **Patrocinador:** Seu Nei (dono).

## 3. Objetivos e métricas de sucesso *(escolha as suas metas numéricas)*
| Métrica | Como medir | Meta v1 |
|---|---|---|
| Grounding (zero alucinação de catálogo) | % de respostas com preço/estoque/prazo que batem com o banco, medido por suíte de avaliação | `[100%]` |
| Conversão em proposta | conversas → rascunho de proposta gerado | `[meta]` |
| Aprovação sem retrabalho | propostas aprovadas pelo humano sem correção | `[meta]` |
| Custo de IA por atendimento | tokens × preço, logado por conversa | `[R$ x/conversa]` |
| Tempo até proposta | 1ª mensagem → rascunho pronto | `[meta]` |
| Escalonamento correto | casos fora do escopo passados a humano sem "inventar" | `[meta]` |

## 4. Escopo da v1 — o que ENTRA
- **Uma persona** (Seu Valdir) comprando **um caminhão**.
- Conversa em linguagem natural que faz **discovery da operação** (carga, rota, km/mês, topografia, orçamento).
- **Recomendação** de configuração a partir do catálogo.
- **Todo dado de catálogo (preço, estoque, prazo, spec) vem de ferramenta que consulta o banco** — nunca do modelo.
- **Rascunho de proposta comercial** (documento simulado, sem validade fiscal).
- **Simulação de financiamento** (estilo VFS, ambiente de teste, sem dinheiro real).
- **Portão de aprovação humana** antes de a proposta "sair".
- **Trilha de auditoria + tracing** de cada turno e chamada de ferramenta.
- **Contador de custo de IA** por conversa.

## 5. Fora de escopo da v1 — o que FICA de fora *(escopo é decisão de risco)*
- Ônibus, construção (FMX/CE) e motores (Penta).
- Personas 2–4 (frota em lote, cooperativa, construtora).
- Pagamento real e emissão fiscal real.
- Negociação de desconto além das regras fixas.
- Integração com CRM/ERP, pós-venda, contrato de manutenção, telemetria.
- Voz, multi-idioma, multi-loja.

## 6. Requisitos derivados dos medos do Seu Nei (medo → requisito)
| Medo do Seu Nei | Vira requisito de engenharia |
|---|---|
| "O robô inventar coisas sobre meus produtos" | Nenhum dado de catálogo do modelo; **grounding** via tool no banco. |
| "Alguém espertinho enganar o robô" | Defesa a **prompt injection**; regra e autorização no **código**, não no prompt. |
| "Sair documento sem alguém olhar" | **Human-in-the-loop**: aprovação obrigatória antes de ação irreversível. |
| "A conta da IA vir gigante" | **Observabilidade de custo**: tokens/conversa, teto, modelo barato p/ tarefa fácil. |
| "Dado do cliente vazar" | **Proteção de PII**: mínimo necessário ao LLM, mascaramento, mínimo privilégio. |
| "Entender o que aconteceu" | **Tracing + log estruturado** e trilha de auditoria da conversa. |
| "Minha equipe conseguir rodar" | **Reprodutibilidade**: docs, containerização, onboarding. |

## 7. Princípio arquitetural (a frase que costura tudo)
> **O modelo decide o que dizer. O código decide o que pode ser feito.**

Regra de negócio (preço, desconto, disponibilidade, quem pode aprovar) mora em **código determinístico e nas ferramentas**, não no texto do prompt. O LLM **propõe**; o código (e, no passo irreversível, um humano) **dispõe**.

## 8. Jornada da fatia vertical (o happy path da v1)
`Oi` → discovery da operação → recomendação fundamentada no catálogo → cliente aceita → **rascunho de proposta + simulação de financiamento** → **fila de aprovação humana** → proposta liberada → fim. Cada passo com log/trace; o passo em **negrito** é o irreversível que exige humano.

## 9. Perguntas em aberto (discovery — responder antes dos ADRs)
- [ ] Onde exatamente a linguagem natural gera **valor** e onde gera **risco** nesta jornada?
- [ ] Qual o pior caso se o modelo errar em cada etapa?
- [ ] Além da proposta, algo mais é irreversível? Quem aprova?
- [ ] Onde o cliente precisa de **garantia absoluta** (não de resposta plausível)?
- [ ] Stack: `[Python? Node? qual banco? qual provedor de LLM?]` → vira ADR.
- [ ] Quantos agentes? `[1 agente com ferramentas? ou orquestrador + especialistas?]` → vira ADR.
