"""Horários livres e prazo de cancelamento (spec `agendamentos`).

Cada teste é um cenário da spec, com o mesmo nome. As regras daqui só
SUGEREM horários — quem decide é o `POST agendamentos` no Xano —, mas a tela
oferecer o que o backend recusaria é defeito do mesmo jeito.
"""

import unittest
from datetime import date

from petbits.agenda import (
    DIA_MS,
    horarios_livres,
    hora,
    inicio_do_dia_ms,
    mes_vizinho,
    pode_cancelar,
    semanas_do_mes,
)

SEGUNDA = date(2026, 10, 12)
SABADO = date(2026, 10, 17)
DOMINGO = date(2026, 10, 18)
ANTES = inicio_do_dia_ms(date(2026, 10, 8))  # "agora", antes de todos os dias acima


def ms(dia, h, m=0):
    return inicio_do_dia_ms(dia) + (h * 60 + m) * 60_000


def horas(lista):
    return [hora(x) for x in lista]


class HorariosLivres(unittest.TestCase):
    def test_dia_util_sem_agendamentos(self):
        livres = horas(horarios_livres(SEGUNDA, 30, [1], [], ANTES))
        self.assertEqual(livres[0], "08:00")
        self.assertEqual(livres[-1], "17:30")
        self.assertEqual(len(livres), 20)

    def test_o_fim_do_atendimento_precisa_caber_no_expediente(self):
        livres = horas(horarios_livres(SABADO, 90, [1], [], ANTES))
        self.assertEqual(livres[-1], "10:30")

    def test_domingo(self):
        self.assertEqual(horarios_livres(DOMINGO, 30, [1], [], ANTES), [])

    def test_profissional_ocupado_em_parte_do_intervalo(self):
        ocupado = [{"id_colaborador": 7, "inicio": ms(SEGUNDA, 9), "fim": ms(SEGUNDA, 10, 30)}]
        livres = horas(horarios_livres(SEGUNDA, 60, [7], ocupado, ANTES))
        for cruza in ("08:30", "09:00", "09:30", "10:00"):
            self.assertNotIn(cruza, livres)
        self.assertIn("08:00", livres)  # termina às 9h00: encosta, não cruza
        self.assertIn("10:30", livres)  # começa no fim do ocupado

    def test_outro_profissional_livre_cobre_o_horario(self):
        ocupado = [{"id_colaborador": 7, "inicio": ms(SEGUNDA, 9), "fim": ms(SEGUNDA, 10, 30)}]
        self.assertIn("09:00", horas(horarios_livres(SEGUNDA, 60, [7, 8], ocupado, ANTES)))

    def test_nenhum_profissional_da_funcao(self):
        self.assertEqual(horarios_livres(SEGUNDA, 30, [], [], ANTES), [])

    def test_horario_no_passado_nao_e_oferecido(self):
        livres = horas(horarios_livres(SEGUNDA, 30, [1], [], ms(SEGUNDA, 10)))
        self.assertEqual(livres[0], "10:30")

    def test_grade_de_30_minutos_vale_no_fuso_de_sao_paulo(self):
        self.assertEqual(inicio_do_dia_ms(SEGUNDA) % DIA_MS, 3 * 3600 * 1000)
        self.assertEqual(ms(SEGUNDA, 8, 30) % 1_800_000, 0)


class Cancelamento(unittest.TestCase):
    def test_cancelamento_dentro_do_prazo(self):
        self.assertTrue(pode_cancelar(ms(SEGUNDA, 9), ms(SEGUNDA, 9) - 2 * DIA_MS))

    def test_exatamente_24_horas_ainda_pode(self):
        self.assertTrue(pode_cancelar(ms(SEGUNDA, 9), ms(SEGUNDA, 9) - DIA_MS))

    def test_menos_de_24_horas(self):
        self.assertFalse(pode_cancelar(ms(SEGUNDA, 9), ms(SEGUNDA, 4)))


class Calendario(unittest.TestCase):
    def test_outubro_de_2026_comeca_na_quinta(self):
        primeira = semanas_do_mes(2026, 10)[0]
        self.assertEqual(primeira[:3], [None, None, None])
        self.assertEqual(primeira[3], date(2026, 10, 1))

    def test_virada_de_ano(self):
        self.assertEqual(mes_vizinho(2026, 12, 1), (2027, 1))
        self.assertEqual(mes_vizinho(2027, 1, -1), (2026, 12))


if __name__ == "__main__":
    unittest.main()
