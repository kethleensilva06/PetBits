"""Caminhos de situação de um pedido (spec `pedidos`, change `pedidos-da-equipe`).

A tabela abaixo é a da spec, escrita à parte de `petbits/pedidos.py` de
propósito: se alguém mudar uma das duas, as 72 combinações deixam de bater.
A mesma tabela está em `apis/pet_bits/equipe_pedido_situacao.xs`, que é quem
decide de verdade.
"""

import unittest

from petbits.pedidos import ROTULOS_ACAO, proximas

SITUACOES = ["pendente", "pago", "pronto_retirada", "enviado", "entregue", "cancelado"]
ENTREGAS = ["retirada", "endereco"]


def permitido_pela_spec(atual, entrega, nova):
    if atual in ("pendente", "pago"):
        if nova == "cancelado":
            return True
        if nova == "pago" and atual == "pendente":
            return True
        if nova == "pronto_retirada" and entrega == "retirada":
            return True
        if nova == "enviado" and entrega == "endereco":
            return True
    if atual == "pronto_retirada" and nova in ("entregue", "cancelado"):
        return True
    if atual == "enviado" and nova == "entregue":
        return True
    return False


class Caminhos(unittest.TestCase):
    def test_todas_as_72_combinacoes_batem_com_a_spec(self):
        for atual in SITUACOES:
            for entrega in ENTREGAS:
                for nova in SITUACOES:
                    with self.subTest(atual=atual, entrega=entrega, nova=nova):
                        self.assertEqual(nova in proximas(atual, entrega),
                                         permitido_pela_spec(atual, entrega, nova))

    def test_entregue_e_cancelado_nao_mudam_mais(self):
        for entrega in ENTREGAS:
            self.assertEqual(proximas("entregue", entrega), [])
            self.assertEqual(proximas("cancelado", entrega), [])

    def test_pronto_para_retirada_so_em_retirada(self):
        self.assertIn("pronto_retirada", proximas("pago", "retirada"))
        self.assertNotIn("pronto_retirada", proximas("pago", "endereco"))

    def test_todo_caminho_tem_rotulo_de_botao(self):
        for atual in SITUACOES:
            for entrega in ENTREGAS:
                for nova in proximas(atual, entrega):
                    self.assertIn(nova, ROTULOS_ACAO)


if __name__ == "__main__":
    unittest.main()
