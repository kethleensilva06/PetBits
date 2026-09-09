query "prontuario" verb=POST {
  api_group = "petbits"
  description = "Cria um registro em prontuario"
  input {
    int id_pet {
      description = "Pet atendido"
    }

    int id_funcionario {
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
    db.add "prontuario" {
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
