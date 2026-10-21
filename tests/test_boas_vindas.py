"""A página inicial com fotos (change `boas-vindas-com-fotos`)."""

import inspect
import unittest
from pathlib import Path

from petbits.pages import entrar

RAIZ = Path(__file__).resolve().parent.parent


class FotosTest(unittest.TestCase):
    def test_toda_foto_existe_e_tem_credito(self):
        creditos = (RAIZ / "assets/fotos/CREDITOS.md").read_text(encoding="utf-8")
        fotos = [entrar.FOTO_DA_CAPA] + [s[:2] for s in entrar.SERVICOS_DA_CLINICA]
        for caminho, alt in fotos:
            arquivo = caminho.removeprefix("/fotos/")
            self.assertTrue((RAIZ / "assets/fotos" / arquivo).is_file(), arquivo)
            self.assertIn(f"`{arquivo}`", creditos, arquivo)
            self.assertTrue(alt.strip(), arquivo)

    def test_tres_servicos(self):
        self.assertEqual([s[3] for s in entrar.SERVICOS_DA_CLINICA],
                         ["Clínica", "Banho e tosa", "Petshop"])


class CaminhosTest(unittest.TestCase):
    def test_os_tres_caminhos_continuam(self):
        fonte = inspect.getsource(entrar.boas_vindas_page)
        for destino in ('"/entrar/cliente"', '"/entrar/equipe"', '"/cadastro"'):
            self.assertIn(destino, fonte)


if __name__ == "__main__":
    unittest.main()
