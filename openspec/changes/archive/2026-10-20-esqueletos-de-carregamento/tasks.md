## 1. Componente

- [x] 1.1 `petbits/esqueletos.py`: `cartoes`, `linhas`, `perfil`, `fichas`, com `role="status"` e texto escondido
- [x] 1.2 `tests/test_esqueletos.py`: nenhuma página de carga mostra mais o spinner com "Carregando"

## 2. Telas

- [x] 2.1 Cliente: casa, agenda (lista e horários), loja, meus pedidos, perfil
- [x] 2.2 Histórico (equipe e tutor)
- [x] 2.3 Clínica: `_carregando` das listas e do painel

## 3. Verificação

- [x] 3.1 Testes locais passam
- [x] 3.2 No navegador: o esqueleto aparece na carga e o conteúdo entra no lugar dele
- [x] 3.3 `preparar_carga` no `on_load` de cada página, e `mostrar_carregando` na Loja e na Agenda (D5)
