## 1. Código

- [x] 1.1 `exige_equipe.xs` aceita `admin` ou `staff` por igualdade (D1); validar com o parser oficial
- [x] 1.2 Publicar só `exige_equipe` pelo Xano CLI, com `--dry-run` antes
- [x] 1.3 `petbits/xano.py`: `PAPEIS_EQUIPE`, `eh_equipe`, `papel_conhecido`, `papel_legivel` (D1); verificar `admin`, `staff`, `member`, vazio e um valor desconhecido
- [x] 1.4 `tables/898256_user.xs` registra o enum do Xano (D2), sem publicar

## 2. Verificação

- [ ] 2.1 No navegador, com a sessão `staff` que já está aberta: a gerência abre e as listas da clínica carregam (o backend aceitou `staff`); `/` leva de volta à gerência
- [ ] 2.2 `openspec validate --strict` e `verificar_equipe.py` limpos — a guarda passa; o validate falha só na spec principal `autenticacao`, falha herdada que some no archive da `porta-de-entrada`
