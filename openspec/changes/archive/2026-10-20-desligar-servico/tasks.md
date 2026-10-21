## 1. Backend

- [x] 1.1 `bool ativo?=true` em `tables/servico.xs` (D1) — publicado primeiro sem padrão, o que desligou os serviços antigos (ver D1); corrigido em 20/10 com os três serviços religados e o padrão `true`
- [x] 1.2 Os seis endpoints de D2; validar; `--dry-run`; publicar — a prévia mostrou só `ADD_FIELD` em `servico` e os seis endpoints atualizados

## 2. Tela

- [x] 2.1 Selo e botão Desativar/Ativar em `/equipe/servicos` (D3)

## 3. Script

- [x] 3.1 Sondas de escrita com nome só de espaços em `scripts/teste_duas_contas.py` (D4) e `tests/test_duas_contas.py` — a primeira tentativa, com nome vazio, fazia o `POST` dar 400 também para o cliente; a rodada acusou, e a troca para "   " resolveu (D4)

## 4. Verificação

- [x] 4.1 Contra o Xano, como no design — **Feito em 20/10:** o `teste_duas_contas.py` deu "ok" nos 11 endpoints (cliente 403 em todos; equipe 200, 400 ou 404, nunca 403), e as listas de serviços e colaboradores ficaram idênticas antes e depois da rodada. A Vacinação (id 9), desativada pelo `PATCH`, manteve o nome, sumiu de `GET servicos` para a Ana, e o agendamento e a ocupação recusaram com "Este servico nao esta disponivel para agendamento."; reativada, voltou à lista do tutor.
      Foi esta prova que achou o defeito da D1: antes de desativar, a Ana já não via a Vacinação
- [x] 4.2 Navegador; desativar as duas "Sonda" — **Visto em 20/10 como Carla:** Banho e tosa, Consulta clinica e Vacinacao ativas com "Desativar"; as duas "Sonda" com o selo Inativo e "Ativar". Ativar uma pela tela a ligou, e Desativar a desligou de novo; as duas terminam inativas (os colaboradores "Sonda" já tinham sido desativados em 19/10)
- [x] 4.3 `unittest`, `verificar_equipe.py`, `openspec validate desligar-servico --strict`
