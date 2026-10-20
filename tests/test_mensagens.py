"""Acento nas recusas do backend (change `acabamentos-de-tela`, D1)."""

import re
import unittest
from pathlib import Path

from petbits.mensagens import _PALAVRAS, acentuar

RAIZ = Path(__file__).resolve().parent.parent


def mensagens_do_backend() -> set[str]:
    achadas = set()
    for pasta in ("apis", "functions"):
        for arquivo in (RAIZ / pasta).rglob("*.xs"):
            achadas |= set(re.findall(r'error = "([^"]*)"', arquivo.read_text(encoding="utf-8")))
    return achadas


class AcentuarTest(unittest.TestCase):
    def test_exemplos(self):
        casos = {
            "A senha atual nao confere.": "A senha atual não confere.",
            "CPF invalido. Confira os numeros.": "CPF inválido. Confira os números.",
            "Esta conta nao tem ficha de tutor.": "Esta conta não tem ficha de tutor.",
            "Este horario nao esta mais disponivel. Escolha outro.":
                "Este horário não está mais disponível. Escolha outro.",
            "O cadastro de tutor desta conta esta incompleto.":
                "O cadastro de tutor desta conta está incompleto.",
            "Um dos produtos nao esta mais a venda: ": "Um dos produtos não está mais à venda: ",
            "Sem permissao para esta area.": "Sem permissão para esta área.",
            "Esta conta ja esta vinculada a um cadastro de tutor.":
                "Esta conta já está vinculada a um cadastro de tutor.",
            "Esta mudanca de situacao nao e permitida para o pedido.":
                "Esta mudança de situação não é permitida para o pedido.",
            "A nova senha e a confirmacao nao conferem.":
                "A nova senha e a confirmação não conferem.",
            "So um agendamento marcado pode ter falta registrada.":
                "Só um agendamento marcado pode ter falta registrada.",
            "Este agendamento ja foi cancelado, concluido ou teve falta.":
                "Este agendamento já foi cancelado, concluído ou teve falta.",
            "O horario deste agendamento ainda nao chegou.":
                "O horário deste agendamento ainda não chegou.",
            "Nao ha uma ficha de colaborador com o seu e-mail. Procure a gerencia.":
                "Não há uma ficha de colaborador com o seu e-mail. Procure a gerência.",
            "Ha mais de uma ficha com o seu e-mail. Procure a gerencia.":
                "Há mais de uma ficha com o seu e-mail. Procure a gerência.",
            "Informe de quem e o animal.": "Informe de quem é o animal.",
            "Sessao invalida.": "Sessão inválida.",
            "Passwords do not match!": "As senhas não conferem.",
        }
        for sem, com in casos.items():
            self.assertEqual(acentuar(sem), com, sem)

    def test_desconhecida_passa_como_veio(self):
        for texto in ("", "Algo deu errado.", "O Xano respondeu 500: erro"):
            self.assertEqual(acentuar(texto), texto)

    def test_nenhuma_mensagem_do_backend_fica_sem_acento(self):
        """Toda mensagem dos `.xs`, acentuada, não tem mais palavra da tabela."""
        mensagens = mensagens_do_backend()
        self.assertGreater(len(mensagens), 50)
        sem_acento = re.compile(r"\b(" + "|".join(_PALAVRAS) + r")\b", re.IGNORECASE)
        for mensagem in mensagens:
            self.assertIsNone(sem_acento.search(acentuar(mensagem)), mensagem)


if __name__ == "__main__":
    unittest.main()
