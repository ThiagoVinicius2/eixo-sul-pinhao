"""Loop fino do agente.

Orquestra a conversa: recebe a mensagem, chama o LLM, executa as ferramentas já
validadas e devolve a resposta. NÃO contém regra de negócio — regra vive em
`tools/` e `guardrails/`.
"""
