## Decisions

### D1. Toda a equipe, não só a gerência

O cadastro de tutor de balcão já é da equipe (`equipe_tutor_create.xs`):
atender quem chega e corrigir o cadastro dele é o trabalho do atendente.
Manter o quadro de colaboradores continua sendo da gerência.

### D2. Só o que foi enviado muda

O padrão `pick` sobre o corpo cru, de `equipe_colaborador_update.xs`: campo
omitido não é campo apagado.

### D3. CPF com as regras do cadastro

Normalizado (sem pontos, traço, barra e espaço), 11 dígitos,
`PetBits/cpf_valido`, e não pode ser de OUTRO tutor (o próprio pode repetir).
A conferência é antes de gravar, pela mensagem; o índice único continua como
garantia.

### D4. O e-mail da ficha e o de entrada andam juntos

No cadastro pelo site, o mesmo e-mail vai para a conta (`user`) e para a ficha
(`tutor`), e o perfil do cliente mostra o da ficha. Se só a ficha mudasse, o
perfil mostraria um e-mail e o login pediria outro. Então, com `id_user` > 0,
o `user.email` muda junto, na mesma transação. Ficha sem conta (balcão) só
muda a ficha. O e-mail não pode estar em outro tutor nem em outra conta, e
ficha com conta não fica sem e-mail.

### D5. Conta da equipe não muda por aqui

Se a conta ligada à ficha não tiver papel `member` (conferido por igualdade,
regra do projeto), o e-mail é recusado: senão um atendente trocaria o e-mail
de entrada de uma conta da gerência pela aba Tutores.

### D6. A senha não muda

Trocar o e-mail não toca a senha. Quem não lembra a senha continua dependendo
da clínica, como hoje.
