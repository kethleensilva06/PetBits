"""Tradução do caminho do repositório para o do Xano CLI (spec `publicacao`).

Usa arquivos de verdade do repositório: se alguém mudar a forma de declarar
um endpoint, o teste mostra que o script deixaria de achar o par.
"""

import sys
import unittest
from pathlib import Path

PROJETO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJETO / "scripts"))

from publicar import caminho_cli, grupo_cli  # noqa: E402


def ler(relativo: str) -> str:
    return (PROJETO / relativo).read_text(encoding="utf-8")


class Caminhos(unittest.TestCase):
    def test_tabela(self):
        self.assertEqual(caminho_cli(ler("tables/produto.xs")), "table/produto.xs")

    def test_tabela_com_numero_no_arquivo(self):
        self.assertEqual(caminho_cli(ler("tables/898256_user.xs")), "table/user.xs")

    def test_funcao(self):
        self.assertEqual(caminho_cli(ler("functions/pet_bits/exige_equipe.xs")),
                         "function/pet_bits/exige_equipe.xs")

    def test_endpoint_simples(self):
        self.assertEqual(caminho_cli(ler("apis/pet_bits/pedido_create.xs")),
                         "api/pet_bits/pedidos_POST.xs")

    def test_endpoint_com_parametro(self):
        self.assertEqual(caminho_cli(ler("apis/pet_bits/equipe_pedido_situacao.xs")),
                         "api/pet_bits/equipe/pedidos/pedido_id/situacao_POST.xs")

    def test_grupo_de_api(self):
        self.assertEqual(caminho_cli(ler("apis/pet_bits/api_group.xs")), "api/pet_bits/pet_bits.xs")
        self.assertEqual(caminho_cli(ler("apis/event_logs/api_group.xs")),
                         "api/event_logs/event_logs.xs")

    def test_nomes_de_grupo(self):
        self.assertEqual(grupo_cli("PetBits"), "pet_bits")
        self.assertEqual(grupo_cli("Quick Start"), "quick_start")
        self.assertEqual(grupo_cli("Authentication"), "authentication")


if __name__ == "__main__":
    unittest.main()
