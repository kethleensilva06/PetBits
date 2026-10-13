// Quais funcoes de colaborador atendem uma categoria de servico (change
// `acabamentos`, D3). Era escrito duas vezes, em `agenda/ocupacao` e em
// `POST agendamentos`.
//
// Devolve `{a, b}`: clinica -> veterinario e clinico_geral; banho_tosa ->
// tosador nas duas posicoes. Duas posicoes fixas, e nao uma lista, porque os
// `where` que usam o resultado comparam por igualdade com cada valor -- a
// forma que o motor ja executa nesta conta.
function "PetBits/funcoes_da_categoria" {
  description = "Funcoes de colaborador que atendem uma categoria de servico"

  input {
    text categoria
  }

  stack {
    var $funcoes {
      value = {a: "tosador", b: "tosador"}
    }

    conditional {
      if ($input.categoria == "clinica") {
        var.update $funcoes {
          value = {a: "veterinario", b: "clinico_geral"}
        }
      }
    }
  }

  response = $funcoes
}
