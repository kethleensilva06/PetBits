## 1. Busca

- [x] 1.1 `petbits/busca.py`: `filtrar`, com testes em `tests/test_busca.py`
- [x] 1.2 `EquipeState`: `busca`, as três listas visíveis, busca zerada em `preparar_carga`
- [x] 1.3 Campo de busca e "nada encontrado" nas três telas

## 2. Verificação

- [x] 2.1 Testes locais passam
- [x] 2.2 No navegador, como equipe: buscar por nome, por CPF, por tutor; nada encontrado; nenhuma requisição ao digitar
- [x] 2.3 Achado na verificação: o CPF vem do banco só com números, e "987.654" não achava nada. Número digitado com pontuação passou a ser comparado pelos dígitos (teste `test_cpf_gravado_sem_mascara`)
