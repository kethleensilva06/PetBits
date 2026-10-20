"""Horário e contato da clínica (change `horario-e-contato`)."""

import inspect
import unittest

from petbits import agenda, clinica
from petbits.pages import agenda as pagina_agenda
from petbits.pages import entrar
from petbits import visual


class HorarioTest(unittest.TestCase):
    def test_texto_bate_com_o_que_a_agenda_aceita(self):
        """"Segunda a sábado, das 8h às 18h" é o `EXPEDIENTE`: 0 a 5, de 8h a 18h."""
        self.assertEqual(sorted(agenda.EXPEDIENTE), [0, 1, 2, 3, 4, 5])
        self.assertTrue(all(v == (8 * 60, 18 * 60) for v in agenda.EXPEDIENTE.values()))
        self.assertIn("Segunda a sábado, das 8h às 18h", clinica.HORARIO)

    def test_email(self):
        self.assertEqual(clinica.EMAIL, "petbitsgroup@gmail.com")
        self.assertIn('href=f"mailto:{EMAIL}"', inspect.getsource(visual.horario_e_contato))

    def test_aparece_na_inicial_e_na_agenda(self):
        self.assertIn("horario_e_contato(", inspect.getsource(entrar.boas_vindas_page))
        self.assertIn("HORARIO_CURTO", inspect.getsource(pagina_agenda))

    def test_rodape_em_toda_tela_do_cliente(self):
        from petbits.pages import inicio, loja, perfil
        for pagina in (inicio.inicio_page, pagina_agenda.agenda_page, loja.loja_page,
                       loja.pedidos_page, perfil.perfil_page):
            self.assertIn("rodape_do_cliente()", inspect.getsource(pagina), pagina.__name__)


if __name__ == "__main__":
    unittest.main()
