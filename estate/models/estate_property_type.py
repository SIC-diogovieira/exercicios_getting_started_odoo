# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate tutorial"
    _order = "sequence,name"

    name = fields.Char(required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id', string='Properties')
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    property_id = fields.Many2one('estate.property', string='Property')
    offer_ids = fields.One2many('estate.property.offers', 'property_type_id')
    offers_count = fields.Integer(compute="_compute_offer_count")

    property_name = fields.Char(related="property_ids.name")
    state = fields.Selection(related="property_ids.state")
    expected_price = fields.Float(related="property_ids.expected_price")
    selling_price = fields.Float(related="property_ids.selling_price")
    best_price = fields.Float(related="property_ids.best_price")


    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'Types of house must be unique'),
    ]

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for rec in self:
            if rec.offer_ids:
                rec.offers_count = len(rec.offer_ids)
            else:
                rec.offers_count = 0