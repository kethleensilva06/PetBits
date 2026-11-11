"""Leituras guardadas por tempo, separadas por credencial (change
`telas-guardadas`)."""

import asyncio
import unittest
from unittest import mock

from petbits import guardados, xano


def rodar(coro):
    return asyncio.run(coro)


class Guardados(unittest.TestCase):
    def setUp(self):
        guardados._GUARDADOS.clear()
        # Importar o script de ponta a ponta (outro teste) desliga o guardado
        # no processo inteiro.
        ligar = mock.patch.object(guardados, "ligado", True)
        ligar.start()
        self.addCleanup(ligar.stop)
        self.chamadas = 0

        @guardados.guardado("animais", 60)
        async def ler(*, token):
            self.chamadas += 1
            return [{"dono": token, "n": self.chamadas}]

        @guardados.renova("animais")
        async def gravar(*, token):
            return None

        @guardados.renova("animais")
        async def gravar_com_falha(*, token):
            raise RuntimeError("caiu")

        self.ler, self.gravar, self.gravar_com_falha = ler, gravar, gravar_com_falha

    def test_segunda_leitura_vem_do_guardado(self):
        rodar(self.ler(token="a"))
        rodar(self.ler(token="a"))
        self.assertEqual(self.chamadas, 1)

    def test_credenciais_separadas(self):
        self.assertEqual(rodar(self.ler(token="a"))[0]["dono"], "a")
        self.assertEqual(rodar(self.ler(token="b"))[0]["dono"], "b")
        self.assertEqual(self.chamadas, 2)

    def test_tempo_vencido_busca_de_novo(self):
        with mock.patch("petbits.guardados.time.monotonic", return_value=1000.0):
            rodar(self.ler(token="a"))
        with mock.patch("petbits.guardados.time.monotonic", return_value=1061.0):
            rodar(self.ler(token="a"))
        self.assertEqual(self.chamadas, 2)

    def test_gravar_apaga_so_de_quem_gravou(self):
        rodar(self.ler(token="a"))
        rodar(self.ler(token="b"))
        rodar(self.gravar(token="a"))
        rodar(self.ler(token="a"))
        rodar(self.ler(token="b"))
        self.assertEqual(self.chamadas, 3)

    def test_gravacao_com_falha_tambem_apaga(self):
        rodar(self.ler(token="a"))
        with self.assertRaises(RuntimeError):
            rodar(self.gravar_com_falha(token="a"))
        rodar(self.ler(token="a"))
        self.assertEqual(self.chamadas, 2)

    def test_esquecer_tudo_da_credencial(self):
        rodar(self.ler(token="a"))
        guardados.esquecer("a")
        rodar(self.ler(token="a"))
        self.assertEqual(self.chamadas, 2)

    def test_devolve_copia(self):
        rodar(self.ler(token="a")).append("mexido")
        self.assertEqual(len(rodar(self.ler(token="a"))), 1)

    def test_sem_token_nao_guarda(self):
        rodar(self.ler(token=""))
        rodar(self.ler(token=""))
        self.assertEqual(self.chamadas, 2)

    def test_desligado_sempre_busca(self):
        with mock.patch.object(guardados, "ligado", False):
            rodar(self.ler(token="a"))
            rodar(self.ler(token="a"))
        self.assertEqual(self.chamadas, 2)

    def test_scripts_de_verificacao_desligam(self):
        from pathlib import Path
        raiz = Path(__file__).resolve().parent.parent / "scripts"
        for nome in ("verificar_ponta_a_ponta.py", "criar_clientes_de_teste.py",
                     "criar_produtos_de_exemplo.py"):
            self.assertIn("guardados.ligado = False",
                          (raiz / nome).read_text(encoding="utf-8"), nome)

    def test_varre_as_vencidas_acima_do_limite(self):
        with mock.patch.object(guardados, "LIMITE_DE_ENTRADAS", 2):
            with mock.patch("petbits.guardados.time.monotonic", return_value=0.0):
                rodar(self.ler(token="a"))
                rodar(self.ler(token="b"))
            with mock.patch("petbits.guardados.time.monotonic", return_value=100.0):
                rodar(self.ler(token="c"))
        self.assertEqual(set(guardados._GUARDADOS), {"c"})


class GruposDoXano(unittest.TestCase):
    """Os tempos e as invalidações do design (D3), no `xano.py` de verdade."""

    def setUp(self):
        guardados._GUARDADOS.clear()
        # Importar o script de ponta a ponta (outro teste) desliga o guardado
        # no processo inteiro.
        ligar = mock.patch.object(guardados, "ligado", True)
        ligar.start()
        self.addCleanup(ligar.stop)

    def test_casa_e_agenda_dividem_os_animais(self):
        pedidos = []

        async def falso(metodo, caminho, **kw):
            pedidos.append((metodo, caminho))
            return [] if metodo == "GET" else {"id": 1}

        with mock.patch.object(xano, "_requisitar", falso):
            rodar(xano.listar_animais(token="t"))
            rodar(xano.listar_animais(token="t"))
            self.assertEqual(pedidos.count(("GET", "/pet")), 1)
            rodar(xano.criar_animal({"nome": "Rex"}, token="t"))
            rodar(xano.listar_animais(token="t"))
            self.assertEqual(pedidos.count(("GET", "/pet")), 2)

    def test_ficha_com_token_na_posicao(self):
        pedidos = []

        async def falso(metodo, caminho, **kw):
            pedidos.append(caminho)
            return {"nome": "Ana"}

        with mock.patch.object(xano, "_requisitar", falso):
            rodar(xano.minha_ficha("t"))
            rodar(xano.minha_ficha("t"))
        self.assertEqual(pedidos.count("/me/tutor"), 1)

    def test_painel_e_agenda_da_clinica_sempre_na_hora(self):
        pedidos = []

        async def falso(metodo, caminho, **kw):
            pedidos.append(caminho)
            return {} if "painel" in caminho else []

        with mock.patch.object(xano, "_requisitar", falso):
            for _ in range(2):
                rodar(xano.painel_equipe(0, token="t"))
                rodar(xano.agenda_da_clinica(0, token="t"))
        self.assertEqual(len(pedidos), 4)


if __name__ == "__main__":
    unittest.main()
