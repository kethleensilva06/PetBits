## 1. Backend

- [x] 1.1 `image? foto` em `tables/colaborador.xs` (D5)
- [x] 1.2 `equipe_meu_perfil_get.xs` (`GET equipe/meu-perfil`): prova de equipe, ficha pelo e-mail da conta (D1, D2)
- [x] 1.3 `equipe_meu_perfil_update.xs` (`PATCH equipe/meu-perfil`): nome e telefone, nome também na conta (D3)
- [x] 1.4 `equipe_meu_perfil_foto.xs` (`POST equipe/meu-perfil/foto`) (D5) — a ficha é conferida antes de guardar o arquivo
- [x] 1.5 `me_tutor_update.xs` muda também o nome da conta (D4)
- [x] 1.6 Validar, `--dry-run` e publicar — a prévia mostrou só `ADD_FIELD` em `colaborador`, os três endpoints novos e o `me/tutor PATCH` atualizado

## 2. Reflex

- [x] 2.1 Cliente HTTP em `petbits/xano.py`
- [x] 2.2 `/equipe/perfil` com `PerfilEquipeState`: dados, campos travados, senha, foto, aviso sem ficha — o comum dos dois perfis foi para um mixin (`_PerfilBase`), e os blocos de `pages/perfil.py` recebem o State; o perfil do tutor continua igual
- [x] 2.3 Avatar no topo da clínica levando ao perfil; foto da equipe na entrada (D6); `sair` limpa

## 3. Verificação

- [x] 3.1 Contra o Xano: as provas do design — **Feito em 19/10:** Bianca (atendente, com ficha) leu a ficha; `PATCH` com telefone, `funcao: "gerente"`, `ativo: false` e outro e-mail mudou só o telefone (na lista da gerência continuou atendente e ativa), e o telefone voltou ao original; nome em branco → 400; nome novo apareceu em `auth/me` e voltou ao original; Carla (sem ficha) recebeu `ficha: null`, e o `PATCH` e a foto deram 403 com o aviso de procurar a gerência; Ana (tutora) recebeu 403 no `GET` e no `PATCH`; foto WebP da Bianca aceita com URL, PDF → 400; Ana mudou o nome pelo `PATCH me/tutor` e `auth/me` passou a dizer o nome novo — o defeito da D4 —, e voltou ao original
- [x] 3.2 Navegador: perfil da equipe com e sem ficha; claro, escuro e celular — **Visto em 19/10:** como Bianca, a foto veio para o topo na entrada; tocar no avatar abriu `/equipe/perfil` com nome e telefone livres e função (Atendente), e-mail e "Na clínica desde 12/02/2024" travados; telefone salvo, igual depois de recarregar, e devolvido; foto trocada pela tela (o avatar do topo mudou junto); PDF recusado com o motivo; senha atual errada recusada. Como Carla, o perfil mostrou o aviso de que não há ficha e só a troca de senha, com as iniciais no avatar; no celular e no escuro, sem rolagem lateral
- [x] 3.3 `unittest`, `verificar_equipe.py`, `openspec validate perfil-do-colaborador --strict` — **83 testes, OK**; `verificar_equipe.py`: 24 endpoints de equipe, os três novos entre eles, nenhuma acusação
