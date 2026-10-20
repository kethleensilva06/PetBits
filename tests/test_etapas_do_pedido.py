"""As etapas do pedido (change `linha-do-tempo-do-pedido`)."""

import unittest

from petbits.etapas_do_pedido import etapas, finalizado


def resumo(lista):
    return [(e["rotulo"], "feita" if e["feita"] else ("atual" if e["atual"] else "-"))
            for e in lista]


class EtapasTest(unittest.TestCase):
    def test_recem_feito_online(self):
        self.assertEqual(resumo(etapas("pendente", "endereco", "online", None)), [
            ("Pedido recebido", "feita"), ("Aguardando pagamento", "atual"),
            ("Enviado", "-"), ("Entregue", "-")])

    def test_pago_para_entrega(self):
        self.assertEqual(resumo(etapas("pago", "endereco", "online", 1760000000000)), [
            ("Pedido recebido", "feita"), ("Pago", "feita"),
            ("Enviado", "atual"), ("Entregue", "-")])

    def test_pronto_antes_de_pagar(self):
        self.assertEqual(resumo(etapas("pronto_retirada", "retirada", "na_loja", 0)), [
            ("Pedido recebido", "feita"), ("Pagar na retirada", "-"),
            ("Pronto para retirada", "feita"), ("Retirado", "atual")])

    def test_entregue_nao_tem_atual(self):
        lista = etapas("entregue", "retirada", "na_loja", 1760000000000)
        self.assertTrue(all(e["feita"] for e in lista))
        self.assertFalse(any(e["atual"] for e in lista))

    def test_cancelado_e_desconhecido(self):
        self.assertEqual(etapas("cancelado", "retirada", "na_loja", None), [])
        self.assertEqual(etapas("", "retirada", "na_loja", None), [])



class FinalizadoTest(unittest.TestCase):
    def test_so_entregue_e_cancelado(self):
        self.assertEqual([s for s in ("pendente", "pago", "pronto_retirada", "enviado",
                                      "entregue", "cancelado") if finalizado(s)],
                         ["entregue", "cancelado"])


if __name__ == "__main__":
    unittest.main()
