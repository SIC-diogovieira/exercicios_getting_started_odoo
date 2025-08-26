# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate tutorial"
    _order = "sequence,name"   # ordenação: primeiro pela sequência, depois pelo nome

    # -----------------------------
    # Exercise: Basic Model + Fields
    # -----------------------------
    name = fields.Char(required=True)

    # -----------------------------
    # Exercise: Relations
    # Ligação com propriedades deste tipo (One2many → estate.property.property_type_id)
    # -----------------------------
    property_ids = fields.One2many(
        'estate.property',
        'property_type_id',
        string='Properties'
    )

    # Sequência para organizar os tipos na UI
    sequence = fields.Integer(
        'Sequence',
        default=1,
        help="Used to order stages. Lower is better."
    )

    # Relação direta com uma propriedade (pouco usual, mas você incluiu aqui)
    property_id = fields.Many2one(
        'estate.property',
        string='Property'
    )

    # Ligação com ofertas associadas às propriedades deste tipo
    offer_ids = fields.One2many(
        'estate.property.offers',
        'property_type_id'
    )

    # -----------------------------
    # Exercise: Computed fields
    # Conta automaticamente quantas ofertas existem ligadas a este tipo
    # -----------------------------
    offers_count = fields.Integer(
        compute="_compute_offer_count"
    )

    # -----------------------------
    # Exercise: Related fields
    # Expondo informações de propriedades relacionadas diretamente no modelo de tipo.
    # CUIDADO: estas relações funcionam apenas para a *primeira* propriedade ligada,
    # o que pode causar comportamentos inesperados.
    # -----------------------------
    property_name = fields.Char(related="property_ids.name")
    state = fields.Selection(related="property_ids.state")
    expected_price = fields.Float(related="property_ids.expected_price")
    selling_price = fields.Float(related="property_ids.selling_price")
    best_price = fields.Float(related="property_ids.best_price")

    # -----------------------------
    # SQL Constraints
    # Garante que não existam tipos duplicados.
    # -----------------------------
    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'Types of house must be unique'),
    ]

    # -----------------------------
    # Compute Methods
    # -----------------------------
    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for rec in self:
            rec.offers_count = len(rec.offer_ids) if rec.offer_ids else 0
