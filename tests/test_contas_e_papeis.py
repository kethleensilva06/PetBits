"""Contas de teste (spec `contas-de-teste`) e papéis (specs `acesso-da-equipe`
e `autenticacao`)."""

import tempfile
import unittest
from pathlib import Path

from petbits import contas_de_teste, xano

ARQUIVO = """Contas de teste. Linha de comentário com maiúscula vira bloco sem senha.

EQUIPE — Gerente
  e-mail: g@x.com
  senha: s1
Veterinária Ana
  email: v@x.com
  senha: s2
TUTOR — Cliente Um
  email: c1@x.com
  senha: c1
Cliente — Dois
  email: c2@x.com
  senha: c2
TUTOR — Sem senha
  email: z@x.com
  senha:
"""


class ContasDeTeste(unittest.TestCase):
    def setUp(self):
        self.original = contas_de_teste.ARQUIVO
        self.tmp = tempfile.TemporaryDirectory()
        contas_de_teste.ARQUIVO = Path(self.tmp.name) / "contas.txt"
        contas_de_teste.ARQUIVO.write_text(ARQUIVO, encoding="utf-8")

    def tearDown(self):
        contas_de_teste.ARQUIVO = self.original
        self.tmp.cleanup()

    def test_bloco_sem_senha_e_ignorado(self):
        emails = [c["email"] for c in contas_de_teste.ler()]
        self.assertNotIn("z@x.com", emails)
        self.assertEqual(len(emails), 4)

    def test_grupos_pelo_rotulo(self):
        self.assertEqual([c["email"] for c in contas_de_teste.do_grupo("equipe")],
                         ["g@x.com", "v@x.com"])
        self.assertEqual([c["email"] for c in contas_de_teste.do_grupo("clientes")],
                         ["c1@x.com", "c2@x.com"])

    def test_arquivo_ausente(self):
        contas_de_teste.ARQUIVO = Path(self.tmp.name) / "nao-existe.txt"
        self.assertEqual(contas_de_teste.ler(), [])


class Papeis(unittest.TestCase):
    def test_admin_e_staff_sao_equipe(self):
        for papel in ("admin", "staff"):
            self.assertTrue(xano.eh_equipe(papel))
            self.assertEqual(xano.rota_do_papel(papel), "/equipe")

    def test_member_e_tutor(self):
        self.assertTrue(xano.eh_tutor("member"))
        self.assertFalse(xano.eh_equipe("member"))
        self.assertEqual(xano.rota_do_papel("member"), "/inicio")

    def test_papel_vazio_ou_desconhecido_nao_e_equipe(self):
        for papel in ("", "gerente", "Admin"):
            self.assertFalse(xano.eh_equipe(papel))
            self.assertFalse(xano.papel_conhecido(papel))
            self.assertEqual(xano.papel_legivel(papel), "Sem perfil")


if __name__ == "__main__":
    unittest.main()
