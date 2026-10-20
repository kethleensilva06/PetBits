"""Publicação no Reflex Cloud sem segredo nem conta de teste (change
`publicacao-no-reflex-cloud`)."""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import publicar_no_reflex as p  # noqa: E402


def _projeto_falso(raiz: Path):
    for pasta in ("petbits", "assets", "xano", "tests", "docs"):
        (raiz / pasta).mkdir()
        (raiz / pasta / "x.py").write_text("x", encoding="utf-8")
    for arquivo in ("rxconfig.py", "requirements.txt", "contas-de-teste.local.txt",
                    "README.md"):
        (raiz / arquivo).write_text("x", encoding="utf-8")
    (raiz / ".env").write_text(
        "﻿XANO_BASE_URL=https://a\nXANO_AUTH_BASE_URL=https://b\nXANO_META_TOKEN=segredo\n",
        encoding="utf-8")


class PacoteTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.raiz = Path(self.tmp.name)
        _projeto_falso(self.raiz)

    def tearDown(self):
        self.tmp.cleanup()

    def test_so_o_permitido_vai(self):
        arquivos = {str(a).replace("\\", "/") for a in p.arquivos_do_pacote(self.raiz)}
        self.assertEqual(arquivos, {"petbits/x.py", "assets/x.py", "rxconfig.py",
                                    "requirements.txt"})

    def test_conta_de_teste_e_xano_ficam_de_fora(self):
        nomes = {x.name for x in p.excluidos(self.raiz)}
        self.assertTrue({"contas-de-teste.local.txt", "xano", "tests", "docs"} <= nomes)
        self.assertNotIn(".env", nomes)  # oculto: o próprio reflex deploy pula

    def test_trava(self):
        self.assertTrue(p.problemas([Path("contas-de-teste.local.txt")]))
        self.assertTrue(p.problemas([Path(".env")]))
        self.assertTrue(p.problemas([Path("xano/api/x.xs")]))
        self.assertEqual(p.problemas([Path("petbits/xano.py")]), [])


class VariaveisTest(unittest.TestCase):
    def test_so_as_duas_e_nunca_o_token(self):
        with tempfile.TemporaryDirectory() as tmp:
            raiz = Path(tmp)
            _projeto_falso(raiz)
            variaveis = p.ler_variaveis(raiz / ".env")
            cmd = p.comando(variaveis, raiz)
        self.assertEqual(set(variaveis), {"XANO_BASE_URL", "XANO_AUTH_BASE_URL"})
        texto = " ".join(cmd)
        self.assertNotIn("XANO_META_TOKEN", texto)
        self.assertNotIn("segredo", texto)
        self.assertNotIn("--envfile", texto)

    def test_valores_nao_aparecem_na_previa(self):
        cmd = ["reflex", "deploy", "--env", "XANO_BASE_URL=https://a"]
        self.assertNotIn("https://a", p._sem_valores(cmd))


class LimiteDoPrerenderTest(unittest.TestCase):
    """O limite de 10 s do prerender sobe para 60 s (D6)."""

    def test_ajusta_uma_vez(self):
        with tempfile.TemporaryDirectory() as tmp:
            arquivo = Path(tmp) / "vite.js"
            arquivo.write_text("const { a, maxRedirects = 0, timeout = 1e4 } = x;", encoding="utf-8")
            self.assertEqual(p.ajustar_limite_do_prerender(arquivo), "ajustado de 10 s para 60 s")
            self.assertIn("timeout = 6e4", arquivo.read_text(encoding="utf-8"))
            self.assertEqual(p.ajustar_limite_do_prerender(arquivo), "já em 60 s")

    def test_nao_mexe_no_que_nao_reconhece(self):
        with tempfile.TemporaryDirectory() as tmp:
            arquivo = Path(tmp) / "vite.js"
            arquivo.write_text("outra coisa", encoding="utf-8")
            self.assertIn("nada alterado", p.ajustar_limite_do_prerender(arquivo))
            self.assertEqual(arquivo.read_text(encoding="utf-8"), "outra coisa")

    def test_sem_ssr(self):
        self.assertIn("--no-ssr", p.comando({v: "x" for v in p.VARIAVEIS}))


if __name__ == "__main__":
    unittest.main()
