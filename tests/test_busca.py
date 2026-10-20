"""A busca das listas da clínica (change `busca-na-clinica`)."""

import unittest

from petbits.busca import filtrar

ANIMAIS = [
    {"nome": "Mel", "especie": "Cachorro", "raca": "Golden", "tutor": "Ana Ribeiro"},
    {"nome": "Mel", "especie": "Gato", "raca": "-", "tutor": "Bruno Lima"},
    {"nome": "Tomate", "especie": "Gato", "raca": "SRD", "tutor": "Ana Ribeiro"},
]
TUTORES = [
    {"nome": "Ana Ribeiro", "documento": "123.456.789-01", "telefone": "(11) 98888-7777"},
    {"nome": "José Conceição", "documento": "987.654.321-00", "telefone": "-"},
]
CAMPOS_ANIMAL = ("nome", "especie", "raca", "tutor")


class BuscaTest(unittest.TestCase):
    def test_vazio_devolve_tudo(self):
        self.assertEqual(filtrar(ANIMAIS, "  ", CAMPOS_ANIMAL), ANIMAIS)

    def test_todas_as_palavras(self):
        achados = filtrar(ANIMAIS, "ana mel", CAMPOS_ANIMAL)
        self.assertEqual([a["tutor"] for a in achados], ["Ana Ribeiro"])

    def test_sem_acento_nem_maiuscula(self):
        achados = filtrar(TUTORES, "JOSE conceicao", ("nome", "documento"))
        self.assertEqual(len(achados), 1)

    def test_cpf_e_telefone_so_pelos_numeros(self):
        campos, numericos = ("nome", "documento", "telefone"), ("documento", "telefone")
        self.assertEqual(filtrar(TUTORES, "12345678", campos, numericos)[0]["nome"],
                         "Ana Ribeiro")
        self.assertEqual(filtrar(TUTORES, "988887777", campos, numericos)[0]["nome"],
                         "Ana Ribeiro")
        self.assertEqual(filtrar(TUTORES, "123.456", campos, numericos)[0]["nome"],
                         "Ana Ribeiro")

    def test_cpf_gravado_sem_mascara(self):
        """Achado no navegador: o CPF vem do banco só com números, e "987.654"
        não achava nada."""
        crus = [{"nome": "Bruno Lima", "documento": "98765432100", "telefone": "11977776666"}]
        campos, numericos = ("nome", "documento", "telefone"), ("documento", "telefone")
        self.assertEqual(len(filtrar(crus, "987.654", campos, numericos)), 1)
        self.assertEqual(len(filtrar(crus, "(11) 97777", campos, numericos)), 1)

    def test_nada_encontrado(self):
        self.assertEqual(filtrar(ANIMAIS, "papagaio", CAMPOS_ANIMAL), [])


if __name__ == "__main__":
    unittest.main()
