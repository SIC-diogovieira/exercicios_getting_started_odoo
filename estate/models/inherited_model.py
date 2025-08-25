from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class EstatePropertyInherited(models.Model):
    # _name = "inherited.model"
    _inherit = "res.users"

    property_ids = fields.One2many('estate.property', 'salesperson', string=' ')
