"""O arquivo .ics do agendamento (change `agenda-guiada`)."""

import unittest
from datetime import date

from petbits import agenda
from petbits.calendario import ics

# 21/10/2026 às 15h em São Paulo = 18h UTC.
INICIO = agenda.inicio_do_dia_ms(date(2026, 10, 21)) + 15 * 3600 * 1000


class IcsTest(unittest.TestCase):
    def setUp(self):
        self.texto = ics(uid="agendamento-7@petbits", titulo="Consulta, para Mel",
                         inicio_ms=INICIO, fim_ms=INICIO + 30 * 60 * 1000,
                         descricao="Linha 1\nLinha 2; fim", agora_ms=INICIO)

    def test_crlf_e_envelope(self):
        self.assertTrue(self.texto.startswith("BEGIN:VCALENDAR\r\n"))
        self.assertTrue(self.texto.endswith("END:VCALENDAR\r\n"))
        self.assertNotIn("\n", self.texto.replace("\r\n", ""))

    def test_horarios_em_utc(self):
        self.assertIn("DTSTART:20261021T180000Z\r\n", self.texto)
        self.assertIn("DTEND:20261021T183000Z\r\n", self.texto)

    def test_texto_escapado(self):
        self.assertIn("SUMMARY:Consulta\\, para Mel\r\n", self.texto)
        self.assertIn("DESCRIPTION:Linha 1\\nLinha 2\\; fim\r\n", self.texto)


if __name__ == "__main__":
    unittest.main()
