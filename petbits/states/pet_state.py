"""Estado e regras da página de Pets."""

from typing import Optional

import reflex as rx
from sqlmodel import select

from petbits.database import get_session
from petbits.models import Cliente, Pet
from petbits.states.conversores import para_data


class PetState(rx.State):
    pets: list[dict] = []
    cliente_options: list[Cliente] = []
    search: str = ""

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

    def load_pets(self):
        with get_session() as session:
            pets = session.exec(select(Pet).order_by(Pet.nome)).all()
            self.cliente_options = list(
                session.exec(select(Cliente).order_by(Cliente.nome)).all()
            )
            clientes_by_id = {c.id: c.nome for c in self.cliente_options}

        self.pets = [
            {
                "id": p.id,
                "nome": p.nome,
                "especie": p.especie,
                "raca": p.raca or "-",
                "peso": p.peso,
                "id_cliente": p.id_cliente,
                "cliente_nome": clientes_by_id.get(p.id_cliente, "Cliente removido"),
            }
            for p in pets
        ]

    def open_new(self):
        self.editing_id = None
        self.nome = ""
        self.especie = ""
        self.raca = ""
        self.data_nascimento = ""
        self.peso = ""
        self.observacoes = ""
        self.id_cliente = str(self.cliente_options[0].id) if self.cliente_options else ""
        self.form_error = ""
        self.show_dialog = True

    def open_edit(self, pet: dict):
        self.editing_id = pet["id"]
        self.nome = pet["nome"]
        self.especie = pet["especie"]
        self.raca = pet["raca"] if pet["raca"] != "-" else ""
        self.peso = str(pet["peso"]) if pet["peso"] is not None else ""
        self.id_cliente = str(pet["id_cliente"])
        with get_session() as session:
            full = session.get(Pet, pet["id"])
            self.observacoes = full.observacoes or "" if full else ""
            self.data_nascimento = (
                full.data_nascimento.isoformat()
                if full and full.data_nascimento
                else ""
            )
        self.form_error = ""
        self.show_dialog = True

    def close_dialog(self):
        self.show_dialog = False

    def save(self):
        if not self.nome.strip() or not self.especie.strip() or not self.id_cliente:
            self.form_error = "Nome, espécie e tutor são obrigatórios."
            return
        try:
            peso_val = float(self.peso.replace(",", ".")) if self.peso.strip() else None
        except ValueError:
            self.form_error = "Peso inválido."
            return

        with get_session() as session:
            if self.editing_id is None:
                session.add(
                    Pet(
                        id_cliente=int(self.id_cliente),
                        nome=self.nome.strip(),
                        especie=self.especie.strip(),
                        raca=self.raca.strip() or None,
                        data_nascimento=para_data(self.data_nascimento),
                        peso=peso_val,
                        observacoes=self.observacoes.strip() or None,
                    )
                )
            else:
                pet = session.get(Pet, self.editing_id)
                pet.id_cliente = int(self.id_cliente)
                pet.nome = self.nome.strip()
                pet.especie = self.especie.strip()
                pet.raca = self.raca.strip() or None
                pet.data_nascimento = para_data(self.data_nascimento)
                pet.peso = peso_val
                pet.observacoes = self.observacoes.strip() or None
                session.add(pet)
            session.commit()

        self.show_dialog = False
        self.load_pets()

    def delete(self, pet_id: int):
        with get_session() as session:
            pet = session.get(Pet, pet_id)
            if pet is not None:
                session.delete(pet)
                session.commit()
        self.load_pets()
