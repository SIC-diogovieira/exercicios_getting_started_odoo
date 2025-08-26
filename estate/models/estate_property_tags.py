# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tags"
    _description = "Estate tutorial"
    _order = "name asc"

    # -----------------------------
    # Exercise: Basic Model + Fields
    # -----------------------------
    name = fields.Char(required=True)

    # -----------------------------
    # Exercise: Relations (Many2many/One2many)
    # Aqui criamos a ligação inversa para visualizar propriedades com esta tag.
    # OBS: no tutorial, normalmente o relacionamento é Many2many no estate.property
    #     (property_tag_id), mas você também adicionou este One2many aqui.
    # -----------------------------
    tags_ids = fields.One2many(
        'estate.property',
        'property_tag_id',
        string='Properties'
    )

    # -----------------------------
    # Exercise: Color Helper
    # -----------------------------
    color = fields.Integer("Color Index", default=0)
