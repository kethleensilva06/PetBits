// O registro do que efetivamente aconteceu com o animal: o prontuario, no
// vocabulario da clinica (change `historico-clinico`, D1).
//
// NUNCA e alterado nem removido -- nao existe endpoint para isso. Corrigir e
// registrar outro atendimento com `retifica` apontando para este; o original
// continua no historico, e a tela o mostra como retificado.
//
// Os vinculos opcionais (`id_agendamento`, `retifica`) ficam 0 quando
// ausentes: e o que o Xano grava em coluna de vinculo omitida (medido neste
// projeto). "Sem retificacao" e `retifica == 0`.
table atendimento {
  auth = false

  schema {
    int id

    int id_pet {
      table = "pet"
    }

    // Quem atendeu: veterinario ou clinico geral, conferido no endpoint
    int id_colaborador {
      table = "colaborador"
    }

    // Quando o atendimento nasceu de um agendamento, que entao fica concluido
    int id_agendamento? {
      table = "agendamento"
    }

    // O atendimento que este corrige, quando e uma retificacao
    int retifica?

    timestamp data_atendimento

    text motivo? filters=trim
    text diagnostico filters=trim
    text tratamento? filters=trim
    decimal peso?
    timestamp retorno?

    // A conta que registrou, pelo token -- para diagnostico, nao para a tela
    int registrado_por? {
      table = "user"
    }

    timestamp created_at?=now
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "id_pet", op: "asc"}, {name: "data_atendimento", op: "desc"}]}
    {type: "btree", field: [{name: "id_colaborador", op: "asc"}]}
  ]
}
