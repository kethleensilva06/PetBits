// CPF valido pelos digitos verificadores (change `cpf-valido`, D1).
//
// Recebe o documento JA normalizado (so digitos, sem ponto, traco nem
// espaco). Devolve true ou false; quem chama decide a recusa. Uma funcao so,
// chamada pelo cadastro publico e pelo de balcao: duas copias do calculo
// divergem na primeira correcao.
//
// Confere a forma, nao a pessoa: um CPF valido de outra pessoa passa. Saber
// a quem o numero pertence exigiria consultar a Receita, fora do escopo.
function "PetBits/cpf_valido" {
  description = "Confere os dois digitos verificadores de um CPF (modulo 11)"

  input {
    text documento
  }

  stack {
    var $valido {
      value = false
    }

    // A contagem de 11 sozinha aceitaria letras.
    var $so_digitos {
      value = "/^[0-9]{11}$/"|regex_matches:$input.documento
    }

    // 111.111.111-11 passa no calculo, mas nao e CPF: recusado por convencao.
    var $p {
      value = $input.documento|substr:0:1
    }

    var $repetido {
      value = $input.documento == ($p ~ $p ~ $p ~ $p ~ $p ~ $p ~ $p ~ $p ~ $p ~ $p ~ $p)
    }

    conditional {
      if ($so_digitos == true && $repetido == false) {
        // Primeiro digito: os 9 primeiros com pesos 10..2.
        var $soma1 {
          value = 0
        }

        for (9) {
          each as $i {
            math.add $soma1 {
              value = ($input.documento|substr:$i:1|to_int) * (10 - $i)
            }
          }
        }

        var $dv1 {
          value = ($soma1 * 10)|modulus:11
        }

        conditional {
          if ($dv1 == 10) {
            var.update $dv1 {
              value = 0
            }
          }
        }

        // Segundo digito: os 10 primeiros com pesos 11..2.
        var $soma2 {
          value = 0
        }

        for (10) {
          each as $j {
            math.add $soma2 {
              value = ($input.documento|substr:$j:1|to_int) * (11 - $j)
            }
          }
        }

        var $dv2 {
          value = ($soma2 * 10)|modulus:11
        }

        conditional {
          if ($dv2 == 10) {
            var.update $dv2 {
              value = 0
            }
          }
        }

        var.update $valido {
          value = ($dv1 == ($input.documento|substr:9:1|to_int)) && ($dv2 == ($input.documento|substr:10:1|to_int))
        }
      }
    }
  }

  response = $valido
}
