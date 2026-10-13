"""Os rótulos de tela do sistema, num lugar só (change `acabamentos`, D2).

Valor gravado no Xano → texto que a pessoa lê. Sem Reflex, para os testes e
os scripts importarem. Os States mantêm os nomes antigos como apelidos para a
mudança não se espalhar.
"""

# Colaboradores (o enum `funcao` da tabela `colaborador`).
FUNCOES = ["gerente", "veterinario", "clinico_geral", "tosador", "atendente"]
FUNCAO_LEGIVEL = {
    "gerente": "Gerente",
    "veterinario": "Veterinário",
    "clinico_geral": "Clínico geral",
    "tosador": "Tosador",
    "atendente": "Atendente",
}

# Agenda.
CATEGORIAS_SERVICO = {"clinica": "Clínica", "banho_tosa": "Banho e tosa"}
SITUACOES_AGENDAMENTO = {
    "marcado": "Marcado",
    "em_andamento": "Em andamento",
    "concluido": "Concluído",
    "cancelado": "Cancelado",
}

# Loja.
CATEGORIAS_PRODUTO = {
    "racao": "Ração",
    "petisco": "Petisco",
    "brinquedo": "Brinquedo",
    "higiene": "Higiene",
    "acessorio": "Acessório",
    "medicamento": "Medicamento",
}
SITUACOES_PEDIDO = {
    "pendente": "Aguardando pagamento",
    "pago": "Pago",
    "pronto_retirada": "Pronto para retirada",
    "enviado": "Enviado",
    "entregue": "Entregue",
    "cancelado": "Cancelado",
}
ENTREGAS = {"retirada": "Retirada na clínica", "endereco": "Entrega no endereço"}
PAGAMENTOS = {"na_loja": "Pagamento na loja", "online": "Pago online (simulado)"}
ORIGENS = {"site": "Pela loja do site", "balcao": "Venda no balcão"}
