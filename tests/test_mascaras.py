"""Máscaras de CPF e telefone (change `acabamentos-de-tela`, D5)."""

import unittest

from petbits import mascaras
from petbits.documentos import cpf_valido, so_digitos
from petbits.states.loja_state import filtrar_produtos


class CpfTest(unittest.TestCase):
    def test_completo_e_pela_metade(self):
        casos = {"12345678909": "123.456.789-09", "123.456.789-09": "123.456.789-09",
                 "1234": "123.4", "123456": "123.456", "1234567890": "123.456.789-0",
                 "": "", "abc": "", "123456789099999": "123.456.789-09"}
        for entrada, saida in casos.items():
            self.assertEqual(mascaras.cpf(entrada), saida, entrada)

    def test_mascara_nao_atrapalha_a_conferencia(self):
        self.assertTrue(cpf_valido(mascaras.cpf("52998224725")))
        self.assertEqual(so_digitos(mascaras.cpf("52998224725")), "52998224725")


class TelefoneTest(unittest.TestCase):
    def test_celular_fixo_e_pela_metade(self):
        casos = {"11988887777": "(11) 98888-7777", "1133334444": "(11) 3333-4444",
                 "(11) 98888-7777": "(11) 98888-7777", "1": "(1", "11": "(11",
                 "119": "(11) 9", "119888": "(11) 9888", "1198888": "(11) 9888-8",
                 "": "", "11988887777123": "(11) 98888-7777"}
        for entrada, saida in casos.items():
            self.assertEqual(mascaras.telefone(entrada), saida, entrada)


class FiltroDaLojaTest(unittest.TestCase):
    PRODUTOS = [
        {"nome": "Ração cães adultos 10 kg", "categoria": "Ração"},
        {"nome": "Bolinha com guizo", "categoria": "Brinquedo"},
        {"nome": "Corda para morder", "categoria": "Brinquedo"},
    ]

    def test_busca_sem_acento(self):
        achados = filtrar_produtos(self.PRODUTOS, "racao", "")
        self.assertEqual([p["nome"] for p in achados], ["Ração cães adultos 10 kg"])

    def test_filtro_por_categoria(self):
        self.assertEqual(len(filtrar_produtos(self.PRODUTOS, "", "Brinquedo")), 2)

    def test_busca_e_filtro_juntos_e_nada(self):
        self.assertEqual(len(filtrar_produtos(self.PRODUTOS, "corda", "Brinquedo")), 1)
        self.assertEqual(filtrar_produtos(self.PRODUTOS, "xyz", ""), [])
        self.assertEqual(len(filtrar_produtos(self.PRODUTOS, "", "")), 3)


if __name__ == "__main__":
    unittest.main()
