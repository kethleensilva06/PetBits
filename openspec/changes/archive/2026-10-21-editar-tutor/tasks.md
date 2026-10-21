## 1. Backend

- [x] 1.1 `equipe_tutor_update.xs`: prova de equipe, `pick`, CPF, e-mail na ficha e na conta, conta da equipe protegida
- [x] 1.2 Validar (`validar_xanoscript.mjs`, `verificar_equipe.py`) e publicar
- [x] 1.3 Provar no Xano com tutores de teste: CPF inválido, CPF de outro, e-mail de outra conta, tutor recusado, e uma alteração de verdade desfeita em seguida

## 2. Tela

- [x] 2.1 `xano.alterar_tutor`; `EquipeState.editar_tutor` e o diálogo servindo para criar e editar
- [x] 2.2 Botão Editar em cada tutor

## 3. Verificação

- [x] 3.1 Testes locais passam
- [x] 3.2 No navegador, como equipe (localhost)

Medido no Xano, com o tutor de teste 48 (Beatriz Rocha (teste), com conta):
conta de cliente recusada; CPF inválido recusado; CPF válido de outro tutor
recusado ("já está cadastrado para outro tutor"), sem mudar nada; e-mail de
outro tutor recusado; o próprio CPF com máscara aceito; telefone e e-mail novos
aceitos, com o e-mail de entrada da conta mudando junto, e o login com o e-mail
novo e a mesma senha funcionando; tudo desfeito em seguida. Na tela, como
Carla: Editar abriu o formulário preenchido, com o aviso do e-mail; o telefone
novo foi salvo e apareceu no cartão; desfeito pela API.

Achado na verificação: o formulário conferia o CPF antes de salvar, e há fichas
de teste com CPF inválido (a da Ana); na edição, o CPF só é conferido quando
muda.
