// Devolve a ficha de cliente do usuario autenticado
query "me/cliente" verb=GET {
  api_group = "PetBits"
  description = "A propria ficha do tutor logado. Admin nao tem ficha e recebe null."
  auth = "user"

  input {
  }

  stack {
    function.run "PetBits/ctx" {
      input = {user_id: $auth.id}
    } as $ctx

    // O caminho e "me/cliente" e nao "cliente/{algo}" de proposito: um prefixo
    // estatico nao colide com GET /cliente/{cliente_id}, cujo parametro e int.
    conditional {
      if ($ctx.is_admin) {
        var $registro {
          value = null
        }
      }
      else {
        db.get cliente {
          field_name = "id"
          field_value = $ctx.cliente_id
        } as $registro
      }
    }
  }

  response = $registro
}
