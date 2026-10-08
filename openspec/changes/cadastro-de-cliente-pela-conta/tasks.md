## 1. Xano

- [x] 1.1 `apis/pet_bits/me_tutor_create.xs` (`POST me/tutor`): D1, D2, D3; validar com o parser oficial
- [x] 1.2 Publicar só este arquivo pelo Xano CLI, com `--dry-run` antes; verificar sem token que responde 401

## 2. Reflex

- [x] 2.1 `xano.criar_minha_ficha` e `PetState`: `sem_ficha` calculado com `GET me/tutor` só para conta que não é de tutor (D4)
- [ ] 2.2 Na tela inicial do cliente, conta sem ficha vê o formulário "Complete seu cadastro de cliente" no lugar de "Nenhum animal cadastrado"; ao concluir, a tela recarrega já como cliente

## 3. Verificação

- [ ] 3.1 Percurso: conta de equipe pela aba Cliente completa o cadastro e cadastra um animal (feito por quem tem o CPF)
- [ ] 3.2 Segunda tentativa na mesma conta, por requisição direta, recusada
- [ ] 3.3 `openspec validate --strict` e `verificar_equipe.py` limpos
