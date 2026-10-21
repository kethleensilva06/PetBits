"""A página não encontrada (change `pagina-nao-encontrada`)."""

import inspect
import unittest
from pathlib import Path

from petbits.pages import nao_encontrada

RAIZ = Path(__file__).resolve().parent.parent


class NaoEncontradaTest(unittest.TestCase):
    def test_foto_existe_e_tem_credito(self):
        arquivo = nao_encontrada.FOTO[0].removeprefix("/fotos/")
        self.assertTrue((RAIZ / "assets/fotos" / arquivo).is_file())
        self.assertIn(f"`{arquivo}`", (RAIZ / "assets/fotos/CREDITOS.md").read_text(encoding="utf-8"))

    def test_caminhos_de_volta(self):
        fonte = inspect.getsource(nao_encontrada.nao_encontrada_page)
        self.assertIn("Ir ao início", fonte)
        self.assertIn("history.back()", fonte)

    def test_rota_404(self):
        fonte = (RAIZ / "petbits/petbits.py").read_text(encoding="utf-8")
        self.assertIn('route="404"', fonte)


if __name__ == "__main__":
    unittest.main()
