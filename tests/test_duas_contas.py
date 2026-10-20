"""O teste das duas contas não grava nada (change `desligar-servico`, D4)."""

import unittest

import scripts.teste_duas_contas as roteiro


class SondasTest(unittest.TestCase):
    def test_toda_sonda_de_escrita_tem_nome_so_de_espacos(self):
        """Nome só de espaços passa pela entrada, o `trim` o esvazia, e a
        validação — que vem depois da prova de equipe — recusa: a equipe recebe
        400 e nada é gravado. Um nome de verdade criaria um registro a cada
        rodada; um vazio seria recusado antes da prova, para o cliente também."""
        escritas = [(m, c, corpo) for m, c, corpo in roteiro.SUPERFICIE_DA_EQUIPE
                    if m in ("POST", "PATCH", "PUT")]
        self.assertTrue(escritas)
        for metodo, caminho, corpo in escritas:
            self.assertIn("nome", corpo, f"{metodo} {caminho}")
            # Só espaços: "" seria recusado antes da prova (ver o roteiro).
            self.assertTrue(corpo["nome"] and not corpo["nome"].strip(), f"{metodo} {caminho}")


if __name__ == "__main__":
    unittest.main()
