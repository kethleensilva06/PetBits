query "prontuario/{id}" verb=PATCH {
  api_group = "petbits"
  description = "Substitui os campos de um registro de prontuario; envie o registro completo"
  input {
    int id {
      description = "Identificador do registro"
    }

    int id_pet? {
      description = "Pet atendido"
    }

    int id_funcionario? {
      description = "Responsavel pelo atendimento"
    }

    text diagnostico? filters=trim {
      description = "Diagnostico registrado"
    }

    text tratamento_realizado? filters=trim {
      description = "Tratamento realizado"
    }

    date proxima_consulta? {
      description = "Data da proxima consulta"
    }
  }
  stack {
    db.edit "prontuario" {
      field_name = "id"
      field_value = $input.id
      data = {
        id_pet: $input.id_pet,
        id_funcionario: $input.id_funcionario,
        diagnostico: $input.diagnostico,
        tratamento_realizado: $input.tratamento_realizado,
        proxima_consulta: $input.proxima_consulta
      }
    } as $registro
  }
  response = $registro
}
