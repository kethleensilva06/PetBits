"""A conferência da foto antes de enviar (change `perfil-e-fotos`, D2)."""

import unittest

from petbits.fotos_enviadas import LIMITE_EM_BYTES, FotoRecusada, extensao_da_foto, url_da_foto


class ExtensaoTest(unittest.TestCase):
    def test_aceita_as_tres(self):
        for nome, esperada in (("mel.JPG", "jpg"), ("x.jpeg", "jpeg"), ("a.b.png", "png"),
                               ("foto.webp", "webp")):
            self.assertEqual(extensao_da_foto(nome, 1000), esperada)

    def test_recusa_o_que_nao_e_imagem(self):
        for nome in ("nota.pdf", "foto.gif", "sem_extensao", "", None):
            with self.assertRaises(FotoRecusada):
                extensao_da_foto(nome, 1000)

    def test_tamanho(self):
        self.assertEqual(extensao_da_foto("ok.png", LIMITE_EM_BYTES), "png")
        with self.assertRaises(FotoRecusada):
            extensao_da_foto("grande.png", LIMITE_EM_BYTES + 1)
        with self.assertRaises(FotoRecusada):
            extensao_da_foto("vazia.png", 0)


class UrlTest(unittest.TestCase):
    def test_url_da_resposta_do_xano(self):
        self.assertEqual(url_da_foto({"url": "https://x/vault/a.webp", "path": "/vault/a.webp"}),
                         "https://x/vault/a.webp")

    def test_sem_foto(self):
        for foto in (None, "", {}, []):
            self.assertEqual(url_da_foto(foto), "")


if __name__ == "__main__":
    unittest.main()
