// Allows the authenticated user to create an account. The user creating it, becomes the admin/owner of the account
query account verb=POST {
  api_group = "Members & Accounts"
  auth = "user"

  input {
    // The name of the new account.
    text name
  
    // A brief description of the new account (optional).
    text description?
  
    // The primary location of the new account (optional).
    text location?
  }

  stack {
    // Create a new account record in the database.
    db.add account {
      enforce_hidden_fields = false
      data = {
        name       : $input.name
        description: $input.description
        location   : $input.location
        created_at : "now"
      }
    } as $new_account
  
    // Link the user to the new account.
    //
    // PetBits: the original template also wrote `role: "admin"` here, which
    // made this a privilege escalation path -- any authenticated member could
    // sign up and then POST /account to become an administrator of the
    // veterinary clinic, in two requests and with no prior access. PetBits
    // decides authorization from `user.role` (see functions/pet_bits/ctx.xs),
    // so that line defeated the whole model. Roles are now granted only from
    // the Xano panel or through /admin/user_role, which requires an existing
    // admin.
    db.edit user {
      field_name = "id"
      field_value = $auth.id
      enforce_hidden_fields = false
      data = {account_id: $new_account.id}
    } as $updated_user
  
    // Log event for new account created
    function.run "Getting Started Template/create_event_log" {
      input = {
        user_id   : $updated_user.id
        account_id: $new_account.id
        action    : "new_account_created"
        metadata  : {}|set:"account":$new_account|set:"user":$updated_user
      }
    } as $event_log
  }

  response = {account: $new_account}
  tags = ["xano:quick-start"]
}