"""O próximo agendamento na casa (change `proximo-agendamento-na-casa`)."""

import unittest
from datetime import date

from petbits import agenda
from petbits.proximo import dia_legivel, proximo_agendamento, separar_agendamentos

HORA = 3600 * 1000
# Agora: terça, 20/10/2026, 14h em São Paulo.
AGORA = agenda.inicio_do_dia_ms(date(2026, 10, 20)) + 14 * HORA
AMANHA_10 = agenda.inicio_do_dia_ms(date(2026, 10, 21)) + 10 * HORA


def ag(inicio, situacao="marcado", servico="Consulta clínica", pet="Mel"):
    return {"inicio": inicio, "fim": inicio + HORA // 2, "situacao": situacao,
            "servico_nome": servico, "pet_nome": pet, "profissional_nome": "Dra. Letícia",
            "profissional_funcao": "veterinario"}


class ProximoTest(unittest.TestCase):
    def test_o_mais_cedo_e_os_outros(self):
        p = proximo_agendamento([ag(AMANHA_10 + 48 * HORA, servico="Banho"), ag(AMANHA_10)],
                                AGORA)
        self.assertEqual(p["titulo"], "Consulta clínica · Mel")
        self.assertEqual(p["quando"], "Amanhã, 10:00")
        self.assertTrue(p["profissional"].startswith("Dra. Letícia"))
        self.assertEqual(p["outros"], "mais 1 agendamento")

    def test_cancelado_concluido_e_passado_nao_contam(self):
        registros = [ag(AMANHA_10, "cancelado"), ag(AGORA - 3 * HORA),
                     ag(AMANHA_10, "concluido")]
        self.assertEqual(proximo_agendamento(registros, AGORA), {})

    def test_em_andamento_agora(self):
        p = proximo_agendamento([ag(AGORA - HORA // 4, "em_andamento")], AGORA)
        self.assertTrue(p["em_andamento"])
        self.assertEqual(p["quando"], "Hoje, 13:45")

    def test_resposta_estranha(self):
        self.assertEqual(proximo_agendamento(None, AGORA), {})


class DiaLegivelTest(unittest.TestCase):
    def test_depois_de_amanha(self):
        self.assertEqual(dia_legivel(AMANHA_10 + 24 * HORA, AGORA), "Qui, 22 de outubro, 10:00")



class SepararTest(unittest.TestCase):
    """Próximos e anteriores (change `proximos-e-anteriores`)."""

    def test_separa_e_ordena(self):
        registros = [ag(AMANHA_10 + 48 * HORA, servico="Banho"), ag(AMANHA_10),
                     ag(AGORA - 24 * HORA, "concluido"), ag(AMANHA_10, "cancelado"),
                     ag(AGORA - 48 * HORA), ag(AGORA - 3 * 24 * HORA, "faltou")]
        proximos, anteriores = separar_agendamentos(registros, AGORA)
        self.assertEqual([p["servico_nome"] for p in proximos], ["Consulta clínica", "Banho"])
        self.assertEqual([a["situacao"] for a in anteriores],
                         ["cancelado", "concluido", "marcado", "faltou"])


if __name__ == "__main__":
    unittest.main()
