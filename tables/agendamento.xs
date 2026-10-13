// O compromisso: um animal, um servico, um colaborador, um intervalo.
//
// E onde mora a regra mais delicada do sistema (modelo de dominio): dois
// agendamentos nao cancelados do mesmo colaborador nao podem se cruzar. Quem
// garante e o `POST agendamentos`, dentro de uma transacao com trava
// (design.md da change `agendamento`, D4) -- nada nesta declaracao impede.
//
// `fim` e GRAVADO, e nao calculado na consulta (D1). Com inicio e fim na
// linha, "cruza o intervalo" e uma condicao de banco, e o intervalo de um
// agendamento antigo nao muda quando a equipe altera a duracao do servico.
//
// Nenhuma coluna aponta para tutor: o tutor do agendamento e o tutor do
// animal, e guarda-lo aqui criaria duas fontes para o mesmo fato.
table agendamento {
  auth = false

  schema {
    int id

    // Animal atendido. Vem de um animal do tutor do token, conferido no POST.
    int id_pet {
      table = "pet"
    }

    // Servico. Define a duracao (copiada para `fim`) e a funcao exigida.
    int id_servico {
      table = "servico"
    }

    // Profissional escolhido pelo sistema, nunca pelo cliente.
    int id_colaborador {
      table = "colaborador"
    }

    // Instantes em ms UTC. A grade de 30 minutos e o expediente sao
    // conferidos no fuso de Sao Paulo no POST (D3).
    timestamp inicio
    timestamp fim

    // D7: so `marcado` e `cancelado` sao usados nesta change; os outros dois
    // ficam para a change de historico clinico.
    enum situacao?=marcado {
      values = ["marcado", "em_andamento", "concluido", "cancelado"]
    }

    // Observacoes do tutor para a clinica
    text observacoes? filters=trim

    // Quando foi cancelado. Cancelar nao apaga (modelo de dominio).
    timestamp cancelado_em?

    timestamp created_at?=now
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "id_colaborador", op: "asc"}, {name: "inicio", op: "asc"}]}
    {type: "btree", field: [{name: "id_pet", op: "asc"}]}
    {type: "btree", field: [{name: "inicio", op: "asc"}]}
  ]
}
