// Resolve o contexto de autorizacao do usuario autenticado.
// Admin: 1 query. Member: 2 queries. Falha fechada nos dois casos.
function "PetBits/ctx" {
  description = "Devolve {user_id, role, is_admin, cliente_id} para o $auth.id recebido"

  input {
    // Sempre o $auth.id do endpoint que chamou
    int user_id
  }

  stack {
    // O token nao carrega o papel (extras = {} no auth/login do template),
    // entao o papel vem sempre do banco. O output explicito e obrigatorio:
    // role tem visibility = "private" na tabela user e so aparece quando
    // listado aqui.
    db.get user {
      field_name = "id"
      field_value = $input.user_id
      output = ["id", "role"]
    } as $user

    precondition ($user != null) {
      error_type = "accessdenied"
      error = "Usuario autenticado nao existe mais."
    }

    var $is_admin {
      value = $user.role == "admin"
    }

    var $cliente_id {
      value = null
    }

    // Admin nao tem ficha de cliente: nem consulta.
    conditional {
      if ($is_admin == false) {
        db.get cliente {
          field_name = "id_user"
          field_value = $user.id
          output = ["id"]
        } as $cliente

        // Sem ficha de cliente nenhum filtro de dono e possivel. Barrar aqui e
        // o que impede o caso perigoso: um filtro que ignora valor nulo
        // devolveria a tabela inteira para quem nao deveria ver nada.
        precondition ($cliente != null) {
          error_type = "accessdenied"
          error = "Este login nao esta vinculado a nenhum cadastro de cliente."
        }

        var.update $cliente_id {
          value = $cliente.id
        }
      }
    }

    var $ctx {
      value = {
        user_id   : $user.id
        role      : $user.role
        is_admin  : $is_admin
        cliente_id: $cliente_id
      }
    }
  }

  response = $ctx
}
