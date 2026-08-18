# Pinhão — agente de vendas da Eixo Sul

Agente de atendimento e vendas consultivas para uma concessionária **fictícia** de caminhões em
Curitiba/PR. O Pinhão conversa com o cliente, entende a necessidade (mesmo quando ele não sabe
o nome do produto), recomenda a configuração certa, monta a proposta e leva à venda — com um
humano aprovando o que é irreversível.

> **Disclaimer.** Projeto **educacional e independente**, sem qualquer vínculo, afiliação ou
> endosso da **AB Volvo / Volvo Group**. A Volvo é apenas referência real que inspirou o
> domínio. Empresa, personagens e todos os dados de catálogo, preço, estoque e prazo são
> **fictícios e ilustrativos**. Não há dinheiro real (pagamento em ambiente de teste) nem
> documento com validade fiscal (simulações). Marcas citadas pertencem aos seus donos.

## Princípio que costura tudo
**O modelo de linguagem decide o que dizer. O código decide o que pode ser feito.**

## Como rodar (para a equipe)
Pré-requisitos: Python 3.11+ e `make`.
```
cp .env.example .env     # preencha as chaves (LLM e banco)
make setup               # instala dependências
make seed                # popula o banco com o catálogo fictício
make run                 # sobe o agente localmente
```
Para desenvolver: `make test` roda os testes e `make lint` roda ruff + mypy.

## Documentação
Comece por aqui, nesta ordem:
- `docs/PRD.md` — o case (Eixo Sul, Seu Nei, personas) e o produto: problema, escopo, métricas.
- `docs/DISCOVERY.md` — a jornada mapeada, onde a IA gera valor × risco, decisões de escopo.
- `docs/ARCHITECTURE.md` — o desenho do sistema e o que acontece quando algo falha.
- `docs/adr/` — as decisões de arquitetura, cada uma com alternativa descartada.
- `docs/HARNESS.md` — como este repo é construído com um agente de código.
- `CLAUDE.md` — o contexto e os limites que o agente de código deve respeitar.

## Estado do projeto
Discovery e documentação prontos; arquitetura definida; implementação da primeira fatia
vertical (um cliente comprando um caminhão, do "oi" à proposta aprovada) em andamento.
