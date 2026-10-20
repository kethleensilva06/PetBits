"""Os passos e o resumo da tela de agendar (change `agenda-guiada`)."""

import unittest
from datetime import date

from petbits import agenda
from petbits.agenda_guiada import FALTA, linhas_do_resumo, passos

CONSULTA = {"nome": "Consulta", "duracao": 30, "preco": "R$ 120,00"}
QUINZE = agenda.inicio_do_dia_ms(date(2026, 10, 21)) + 15 * 3600 * 1000


def atual(lista):
    return next(p["rotulo"] for p in lista if p["atual"])


class PassosTest(unittest.TestCase):
    def test_comeco(self):
        lista = passos("", "", 0)
        self.assertEqual(atual(lista), "Serviço")
        self.assertFalse(any(p["feito"] for p in lista))

    def test_faltando_o_horario(self):
        lista = passos("3", "7", 0)
        self.assertEqual([p["feito"] for p in lista], [True, True, False, False])
        self.assertEqual(atual(lista), "Horário")

    def test_tudo_escolhido(self):
        self.assertEqual(atual(passos("3", "7", QUINZE)), "Confirmar")

    def test_animal_antes_do_servico(self):
        """Escolher o animal primeiro não pula o serviço."""
        self.assertEqual(atual(passos("", "7", 0)), "Serviço")


class ResumoTest(unittest.TestCase):
    def test_nada_escolhido(self):
        self.assertTrue(all(l["valor"] == FALTA for l in linhas_do_resumo({}, "", 0, "")))

    def test_servico_e_animal(self):
        linhas = {l["rotulo"]: l["valor"] for l in linhas_do_resumo(CONSULTA, "Mel", 0, "")}
        self.assertEqual(linhas, {"Serviço": "Consulta", "Duração": "30 min",
                                  "Preço": "R$ 120,00", "Animal": "Mel", "Quando": FALTA})

    def test_quando(self):
        dia = linhas_do_resumo(CONSULTA, "Mel", 0, "quarta, 21 de outubro")[-1]["valor"]
        self.assertEqual(dia, "quarta, 21 de outubro, horário a escolher")
        hora = linhas_do_resumo(CONSULTA, "Mel", QUINZE, "")[-1]["valor"]
        self.assertTrue(hora.endswith("às 15:00"), hora)


if __name__ == "__main__":
    unittest.main()
