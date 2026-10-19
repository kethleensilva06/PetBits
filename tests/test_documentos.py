"""CPF válido pelos dígitos verificadores (change `cpf-valido`)."""

import sys
import unittest
from pathlib import Path

from petbits.documentos import cpf_valido, so_digitos

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from criar_clientes_de_teste import cpf_ficticio  # noqa: E402


class CpfTest(unittest.TestCase):
    def test_validos_conhecidos(self):
        for cpf in ("529.982.247-25", "52998224725", "111.444.777-35", "390 533 447-05"):
            self.assertTrue(cpf_valido(cpf), cpf)

    def test_digito_verificador_errado(self):
        for cpf in ("123.456.789-00", "529.982.247-26", "52998224735"):
            self.assertFalse(cpf_valido(cpf), cpf)

    def test_onze_digitos_iguais(self):
        for d in "0123456789":
            self.assertFalse(cpf_valido(d * 11), d)

    def test_letras_tamanho_e_vazio(self):
        for cpf in ("1234567890a", "5299822472a", "5299822472", "529982247250", "", None):
            self.assertFalse(cpf_valido(cpf), cpf)

    def test_so_digitos_tira_so_a_pontuacao_do_backend(self):
        self.assertEqual(so_digitos("529.982.247-25"), "52998224725")
        self.assertEqual(so_digitos("529 982/247-25"), "52998224725")
        self.assertEqual(so_digitos("529,982"), "529,982")

    def test_gerador_dos_clientes_de_teste_gera_validos(self):
        for _ in range(200):
            self.assertTrue(cpf_valido(cpf_ficticio()))


if __name__ == "__main__":
    unittest.main()
