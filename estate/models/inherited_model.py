from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class EstatePropertyInherited(models.Model):
    # -----------------------------
    # Exercise: Inheritance
    # Herdamos o modelo "res.users" para adicionar novos campos.
    # -----------------------------
    _inherit = "res.users"

    # -----------------------------
    # Exercise: Relations
    # Criamos uma relação One2many para saber quais propriedades
    # estão atribuídas a cada vendedor (usuário do sistema).
    # Ligação → estate.property.salesperson
    # -----------------------------
    property_ids = fields.One2many(
        'estate.property',
        'salesperson',
        string='Properties'
    )
