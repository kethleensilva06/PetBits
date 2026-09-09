"""Tabelas do PetBits no Xano.

O banco de dados fica hospedado no Xano. Este módulo é o único lugar que
descreve as tabelas do projeto e expõe um acessor para cada uma delas.

Os registros circulam pelo projeto como dicionários JSON, exatamente como o
Xano os devolve — sempre com `id` e `created_at`, que ele gera sozinho.

Para criar essas tabelas no painel do Xano, siga `docs/xano-setup.md`.
"""

from petbits.xano import TabelaXano

# Valores aceitos nos campos de domínio fechado. O Xano não impõe CHECK
# constraints como o SQL Server, então estas listas alimentam os selects da
# interface e a validação feita nos States.
CARGOS_FUNCIONARIO = ["veterinario", "tosador", "atendente"]
STATUS_PEDIDO = ["pendente", "pago", "enviado", "entregue"]
STATUS_AGENDAMENTO = ["agendado", "em_andamento", "concluido", "cancelado"]

# Tutor responsável pelos pets.
# nome (text), cpf (text), email (text), telefone (text), endereco (text),
# data_cadastro (timestamp)
clientes = TabelaXano("cliente")

# Colaborador da clínica.
# nome (text), cpf (text), cargo (text), telefone (text), email (text),
# data_contratacao (date)
funcionarios = TabelaXano("funcionario")

# Item vendável do petshop.
# nome (text), categoria (text), marca (text), unidade (text),
# preco_venda (decimal)
produtos = TabelaXano("produto")

# Serviço prestado pela clínica.
# nome_servico (text), descricao (text), preco (decimal),
# duracao_estimada (int)
servicos = TabelaXano("servico")

# Animal de estimação, vinculado a um cliente.
# id_cliente (int), nome (text), especie (text), raca (text),
# data_nascimento (date), peso (decimal), observacoes (text)
pets = TabelaXano("pet")

# Pedido de compra de produtos feito por um cliente.
# id_cliente (int), data_pedido (timestamp), status (text),
# valor_total (decimal)
pedidos = TabelaXano("pedido")

# Horário marcado para um pet realizar um serviço com um funcionário.
# id_pet (int), id_servico (int), id_funcionario (int), data_hora (timestamp),
# status (text), observacoes (text)
agendamentos = TabelaXano("agendamento")

# Item (produto + quantidade) que compõe um pedido.
# id_pedido (int), id_produto (int), quantidade (int),
# valor_unitario (decimal), valor_total (decimal)
itens_pedido = TabelaXano("itens_pedido")

# Registro de atendimento clínico de um pet.
# id_pet (int), id_funcionario (int), data_atendimento (timestamp),
# diagnostico (text), tratamento_realizado (text), proxima_consulta (date)
prontuarios = TabelaXano("prontuario")
