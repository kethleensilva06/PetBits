"""Estado e regras da página de Pets."""

from typing import Optional

import reflex as rx

from petbits import models
from petbits.states.conversores import para_data, para_input_data
from petbits.xano import XanoError


class PetState(rx.State):
    pets: list[dict] = []
    cliente_options: list[dict] = []
    search: str = ""
    load_error: str = ""

    show_dialog: bool = False
    editing_id: Optional[int] = None
    form_error: str = ""

    nome: str = ""
    especie: str = ""
    raca: str = ""
    data_nascimento: str = ""
    peso: str = ""
    observacoes: str = ""
    id_cliente: str = ""

    def set_search(self, value: str):
        self.search = value

    def set_show_dialog(self, value: bool):
        self.show_dialog = value

    def set_nome(self, value: str):
        self.nome = value

    def set_especie(self, value: str):
        self.especie = value

    def set_raca(self, value: str):
        self.raca = value

    def set_data_nascimento(self, value: str):
        self.data_nascimento = value

    def set_peso(self, value: str):
        self.peso = value

    def set_observacoes(self, value: str):
        self.observacoes = value

    def set_id_cliente(self, value: str):
        self.id_cliente = value

    @rx.var
    def filtered_pets(self) -> list[dict]:
        term = self.search.strip().lower()
        if not term:
            return self.pets
        return [
            p
            for p in self.pets
            if term in p["nome"].lower() or term in p["cliente_nome"].lower()
        ]

    async def load_pets(self):
        self.load_error = ""
        try:
            registros = await models.pets.listar()
            clientes = await models.clientes.listar()
        except XanoError as erro:
            self.pets = []
            self.cliente_options = []
            self.load_error = str(erro)
            return

        self.cliente_options = [
            {"id": c.get("id"), "nome": c.get("nome") or ""}
            for c in sorted(clientes, key=lambda c: (c.get("nome") or "").lower())
        ]
        clientes_by_id = {c["id"]: c["nome"] for c in self.cliente_options}

        self.pets = [
            {
                "id": p.get("id"),
                "nome": p.get("nome") or "",
                "especie": p.get("especie") or "",
                "raca": p.get("raca") or "-",
                "peso": p.get("peso"),
                "id_cliente": p.get("id_cliente"),
                "cliente_nome": clientes_by_id.get(
                    p.get("id_cliente"), "Cliente removido"
                ),
                "observacoes": p.get("observacoes") or "",
                "data_nascimento_input": para_input_data(p.get("data_nascimento")),
            }
            for p in sorted(registros, key=lambda p: (p.get("nome") or "").lower())
        ]

    def open_new(self):
        self.editing_id = None
        self.nome = ""
        self.especie = ""
        self.raca = ""
        self.data_nascimento = ""
        self.peso = ""
        self.observacoes = ""
        primeiro = self.cliente_options[0].get("id") if self.cliente_options else None
        self.id_cliente = str(primeiro) if primeiro is not None else ""
        self.form_error = ""
        self.show_dialog = True

    def open_edit(self, pet: dict):
        self.editing_id = pet["id"]
        self.nome = pet["nome"]
        self.especie = pet["especie"]
        self.raca = pet["raca"] if pet["raca"] != "-" else ""
        self.peso = str(pet["peso"]) if pet["peso"] is not None else ""
        self.id_cliente = str(pet["id_cliente"])
        self.observacoes = pet["observacoes"]
        self.data_nascimento = pet["data_nascimento_input"]
        self.form_error = ""
        self.show_dialog = True

    def close_dialog(self):
        self.show_dialog = False

    async def save(self):
        if not self.nome.strip() or not self.especie.strip() or not self.id_cliente:
            self.form_error = "Nome, espécie e tutor são obrigatórios."
            return
        try:
            peso_val = float(self.peso.replace(",", ".")) if self.peso.strip() else None
        except ValueError:
            self.form_error = "Peso inválido."
            return

        dados = {
            "id_cliente": int(self.id_cliente),
            "nome": self.nome.strip(),
            "especie": self.especie.strip(),
            "raca": self.raca.strip() or None,
            "data_nascimento": para_data(self.data_nascimento),
            "peso": peso_val,
            "observacoes": self.observacoes.strip() or None,
        }

        try:
            if self.editing_id is None:
                await models.pets.criar(dados)
            else:
                await models.pets.atualizar(self.editing_id, dados)
        except XanoError as erro:
            self.form_error = str(erro)
            return

        self.form_error = ""
        self.show_dialog = False
        await self.load_pets()

    async def delete(self, pet_id: int):
        try:
            await models.pets.remover(pet_id)
        except XanoError as erro:
            self.load_error = str(erro)
            return
        await self.load_pets()
