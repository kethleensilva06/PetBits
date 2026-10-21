"""A linha do tempo do histórico (change `historico-clinico`)."""

import unittest

from petbits.historico import (data_local, dia_em_ms, evolucao_do_peso, linha_do_tempo,
                               proximo_retorno)

# 18/10/2026 00:00 em São Paulo = 03:00 UTC
MEIA_NOITE_SP = 1792292400000


class DatasTest(unittest.TestCase):
    def test_meia_noite_de_sao_paulo(self):
        self.assertEqual(dia_em_ms("2026-10-18"), MEIA_NOITE_SP)
        self.assertEqual(data_local(MEIA_NOITE_SP), "18/10/2026")

    def test_noite_de_sao_paulo_nao_vira_amanha(self):
        # 22h de 18/10 em São Paulo = 01:00 UTC de 19/10
        self.assertEqual(data_local(MEIA_NOITE_SP + 22 * 3600 * 1000), "18/10/2026")

    def test_vazios(self):
        self.assertEqual(data_local(0), "")
        self.assertEqual(data_local(None), "")
        self.assertIsNone(dia_em_ms(""))
        self.assertIsNone(dia_em_ms("ontem"))


class LinhaDoTempoTest(unittest.TestCase):
    REGISTROS = [
        {"id": 2, "retifica": 1, "data_atendimento": MEIA_NOITE_SP, "diagnostico": "Otite externa",
         "colaborador_nome": "Dr. Caio", "colaborador_funcao": "veterinario", "peso": 28.5},
        {"id": 1, "retifica": 0, "data_atendimento": MEIA_NOITE_SP, "diagnostico": "Otite",
         "colaborador_nome": "Dr. Caio", "colaborador_funcao": "veterinario", "peso": 0,
         "retorno": MEIA_NOITE_SP + 10 * 86400000},
    ]

    def test_retificacao_e_retificado(self):
        novo, antigo = linha_do_tempo(self.REGISTROS)
        self.assertTrue(novo["e_retificacao"])
        self.assertFalse(novo["retificado"])
        self.assertEqual(novo["retifica_data"], "18/10/2026")
        self.assertTrue(antigo["retificado"])
        self.assertFalse(antigo["e_retificacao"])

    def test_quem_peso_e_retorno(self):
        novo, antigo = linha_do_tempo(self.REGISTROS)
        self.assertEqual(novo["quem"], "Dr. Caio · Veterinário")
        self.assertEqual(novo["peso"], "28,5 kg")
        self.assertEqual(antigo["peso"], "")
        self.assertEqual(antigo["retorno"], "28/10/2026")

    def test_mesmo_dia_o_ultimo_registrado_primeiro(self):
        ids = [i["id"] for i in linha_do_tempo(list(reversed(self.REGISTROS)))]
        self.assertEqual(ids, [2, 1])

    def test_lista_vazia(self):
        self.assertEqual(linha_do_tempo([]), [])



class EvolucaoDoPesoTest(unittest.TestCase):
    """O quadro do peso (change `evolucao-do-peso`)."""

    DIA = 86400000

    def reg(self, id_, dias, peso, retifica=0):
        return {"id": id_, "data_atendimento": MEIA_NOITE_SP + dias * self.DIA, "peso": peso,
                "retifica": retifica}

    def test_engordou(self):
        e = evolucao_do_peso([self.reg(1, 0, 28.0), self.reg(2, 30, 28.5)])
        self.assertEqual(e["atual"], "28,5 kg")
        self.assertEqual(e["variacao"], f"+0,5 kg desde {data_local(MEIA_NOITE_SP)}")
        self.assertEqual([p["altura"] for p in e["pontos"]], ["35%", "100%"])

    def test_emagreceu_e_igual(self):
        self.assertTrue(evolucao_do_peso([self.reg(1, 0, 30), self.reg(2, 9, 29)])["variacao"]
                        .startswith("−1 kg desde"))
        self.assertTrue(evolucao_do_peso([self.reg(1, 0, 30), self.reg(2, 9, 30)])["variacao"]
                        .startswith("igual à pesagem"))

    def test_retificado_nao_conta(self):
        e = evolucao_do_peso([self.reg(1, 0, 28.0), self.reg(2, 30, 35.0),
                              self.reg(3, 30, 28.2, retifica=2)])
        self.assertEqual(e["atual"], "28,2 kg")
        self.assertEqual(len(e["pontos"]), 2)

    def test_sem_pesagem(self):
        self.assertEqual(evolucao_do_peso([self.reg(1, 0, None), self.reg(2, 1, 0)]), {})

    def test_ultimas_seis(self):
        e = evolucao_do_peso([self.reg(i, i, 20 + i) for i in range(1, 10)])
        self.assertEqual(len(e["pontos"]), 6)
        self.assertEqual(e["pontos"][-1]["peso"], "29 kg")



class ProximoRetornoTest(unittest.TestCase):
    """O retorno sugerido (change `agendar-retorno`)."""

    DIA = 86400000

    def reg(self, id_, dias, retorno_em_dias=None, retifica=0):
        return {"id": id_, "data_atendimento": MEIA_NOITE_SP + dias * self.DIA,
                "retorno": None if retorno_em_dias is None
                else MEIA_NOITE_SP + retorno_em_dias * self.DIA, "retifica": retifica}

    def agora(self, dias):
        return MEIA_NOITE_SP + dias * self.DIA + 10 * 3600 * 1000

    def test_o_mais_proximo(self):
        r = proximo_retorno([self.reg(1, 0, 20), self.reg(2, 5, 12)], self.agora(6))
        self.assertEqual(r, {"data": data_local(MEIA_NOITE_SP + 12 * self.DIA)})

    def test_retorno_hoje_conta_e_ontem_nao(self):
        self.assertTrue(proximo_retorno([self.reg(1, 0, 6)], self.agora(6)))
        self.assertEqual(proximo_retorno([self.reg(1, 0, 5)], self.agora(6)), {})

    def test_atendimento_depois_sem_retorno_nao_esconde(self):
        """Achado no navegador: a vacina sem retorno escondia o da consulta."""
        r = proximo_retorno([self.reg(1, 0, 20), self.reg(2, 5)], self.agora(6))
        self.assertEqual(r, {"data": data_local(MEIA_NOITE_SP + 20 * self.DIA)})

    def test_retificado_nao_conta(self):
        registros = [self.reg(1, 5, 9), self.reg(2, 5, 15, retifica=1)]
        self.assertEqual(proximo_retorno(registros, self.agora(6)),
                         {"data": data_local(MEIA_NOITE_SP + 15 * self.DIA)})

    def test_sem_registros(self):
        self.assertEqual(proximo_retorno([], self.agora(0)), {})


if __name__ == "__main__":
    unittest.main()
