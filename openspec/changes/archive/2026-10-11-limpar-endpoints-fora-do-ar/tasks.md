## 1. Limpeza

- [x] 1.1 Remover os cinco `.xs` de `apis/authentication/` que não estão no Xano (login, signup, e-mail de boas-vindas, magic link, pedido de link de troca de senha)
- [x] 1.2 Remover `apis/pet_bits/me_tutor_create.xs`
- [x] 1.3 Despublicar `POST me/tutor` no painel do Xano, feito por quem desenvolve — **Situação:** em 2026-10-11 o `GET me/tutor` foi apagado por engano primeiro e republicado do repositório com `publicar.py` (sem token responde 401); o `POST` estava no grupo de API `extra`, não no PetBits, e foi apagado de lá. `publicar.py --conferir`: nada do repositório falta no Xano; no Xano sobram só `equipe/animais POST` e `equipe/tutores POST` do grupo `extra`, em alinhamento com a Kethleen

## 2. Verificação

- [x] 2.1 `verificar_equipe.py` sem acusação e testes passando
- [x] 2.2 `openspec validate --strict` (lendo o Totals)
