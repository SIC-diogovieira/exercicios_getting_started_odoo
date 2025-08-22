# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tags"
    _description = "Estate tutorial"
    _order = "name asc"

    name = fields.Char(required=True)
    tags_ids = fields.One2many('estate.property','property_tag_id', string='Propertys')
    color = fields.Integer("Color Index", default=0)

