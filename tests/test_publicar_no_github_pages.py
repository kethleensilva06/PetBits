"""Publicação no GitHub Pages (change `site-no-github-pages`)."""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import publicar_no_github_pages as g  # noqa: E402


def _build_falso(raiz: Path, servidor: str = g.SERVIDOR) -> Path:
    build = raiz / "client"
    (build / "assets").mkdir(parents=True)
    (build / "assets" / "reflex-env-x.js").write_text(f"var e={{EVENT:`{servidor}`}}", encoding="utf-8")
    (build / "assets" / "app.js").write_text("x", encoding="utf-8")
    (build / "assets" / "app.js.gz").write_text("x", encoding="utf-8")
    (build / "fotos").mkdir()
    (build / "fotos" / "banner.webp").write_text("x", encoding="utf-8")
    (build / "404.html").write_text("x", encoding="utf-8")
    (build / "PetBits.html").write_text("x", encoding="utf-8")
    (build / "PetBits" / "loja").mkdir(parents=True)
    (build / "PetBits" / "index.html").write_text("raiz", encoding="utf-8")
    (build / "PetBits" / "loja.html").write_text("loja", encoding="utf-8")
    return build


class PagesTest(unittest.TestCase):
    def test_monta_com_as_paginas_na_raiz(self):
        with tempfile.TemporaryDirectory() as tmp:
            build = _build_falso(Path(tmp))
            destino = Path(tmp) / "pages"
            destino.mkdir()
            g.montar(destino, build)
            nomes = {str(p.relative_to(destino)).replace("\\", "/") for p in destino.rglob("*")
                     if p.is_file()}
        self.assertIn("index.html", nomes)
        self.assertIn("loja.html", nomes)
        self.assertIn("assets/app.js", nomes)
        self.assertIn(".nojekyll", nomes)
        self.assertNotIn("assets/app.js.gz", nomes)
        self.assertNotIn("PetBits.html", nomes)

    def test_confere_o_servidor(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(g.conferir_build(_build_falso(Path(tmp))), [])
        with tempfile.TemporaryDirectory() as tmp:
            faltas = g.conferir_build(_build_falso(Path(tmp), servidor="http://localhost:8000"))
        self.assertTrue(any("servidor" in f for f in faltas))


if __name__ == "__main__":
    unittest.main()
