"""Estado e regras da página de Produtos."""

from typing import Optional

import reflex as rx

from petbits import models
from petbits.states.conversores import formatar_moeda
from petbits.xano import XanoError


class ProdutoState(rx.State):
    produtos: list[dict] = []
    search: str = ""
    load_error: str = ""

    show_dialog: bool = False
    editing_id: Optional[int] = None
    form_error: str = ""

    nome: str = ""
    categoria: str = ""
    marca: str = ""
    unidade: str = ""
    preco_venda: str = "0.00"

    def set_search(self, value: str):
        self.search = value

    def set_show_dialog(self, value: bool):
        self.show_dialog = value

    def set_nome(self, value: str):
        self.nome = value

    def set_categoria(self, value: str):
        self.categoria = value

    def set_marca(self, value: str):
        self.marca = value

    def set_unidade(self, value: str):
        self.unidade = value

    def set_preco_venda(self, value: str):
        self.preco_venda = value

    @rx.var
    def filtered_produtos(self) -> list[dict]:
        term = self.search.strip().lower()
        if not term:
            return self.produtos
        return [
            p
            for p in self.produtos
            if term in p["nome"].lower() or term in p["categoria"].lower()
        ]

    async def load_produtos(self):
        self.load_error = ""
        try:
            registros = await models.produtos.listar()
        except XanoError as erro:
            self.produtos = []
            self.load_error = str(erro)
            return

        self.produtos = [
            {
                "id": p.get("id"),
                "nome": p.get("nome") or "",
                "categoria": p.get("categoria") or "-",
                "marca": p.get("marca") or "-",
                "unidade": p.get("unidade") or "-",
                "preco_venda": formatar_moeda(p.get("preco_venda")),
            }
            for p in sorted(registros, key=lambda p: (p.get("nome") or "").lower())
        ]

    def open_new(self):
        self.editing_id = None
        self.nome = ""
        self.categoria = ""
        self.marca = ""
        self.unidade = ""
        self.preco_venda = "0.00"
        self.form_error = ""
        self.show_dialog = True

    def open_edit(self, produto: dict):
        self.editing_id = produto["id"]
        self.nome = produto["nome"]
        self.categoria = produto["categoria"] if produto["categoria"] != "-" else ""
        self.marca = produto["marca"] if produto["marca"] != "-" else ""
        self.unidade = produto["unidade"] if produto["unidade"] != "-" else ""
        self.preco_venda = produto["preco_venda"]
        self.form_error = ""
        self.show_dialog = True

    def close_dialog(self):
        self.show_dialog = False

    async def save(self):
        if not self.nome.strip():
            self.form_error = "Nome é obrigatório."
            return
        try:
            preco = float(self.preco_venda.replace(",", "."))
        except ValueError:
            self.form_error = "Preço inválido."
            return
        if preco < 0:
            self.form_error = "Preço não pode ser negativo."
            return

        dados = {
            "nome": self.nome.strip(),
            "categoria": self.categoria.strip() or None,
            "marca": self.marca.strip() or None,
            "unidade": self.unidade.strip() or None,
            "preco_venda": preco,
        }

        try:
            if self.editing_id is None:
                await models.produtos.criar(dados)
            else:
                await models.produtos.atualizar(self.editing_id, dados)
        except XanoError as erro:
            self.form_error = str(erro)
            return

        self.form_error = ""
        self.show_dialog = False
        await self.load_produtos()

    async def delete(self, produto_id: int):
        try:
            await models.produtos.remover(produto_id)
        except XanoError as erro:
            self.load_error = str(erro)
            return
        await self.load_produtos()
