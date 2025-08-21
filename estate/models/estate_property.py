# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate tutorial"

    name = fields.Char(required=True)
    description = fields.Text()
    property_type_id = fields.Many2one('estate.property.type', string='Type')
    property_tag_id = fields.Many2many('estate.property.tags', string='Tags')
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_areas = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_orientation = fields.Selection([("north", "North")])
    garden_area = fields.Integer()
    active = fields.Boolean(default=True, label='Ativo')
    state = fields.Selection([("new", "New"), ("offer_r", "Offer Received"), ("offer_a", "Offer Accepted"), ("sold", "Sold"), ("canceled", "Canceled")])
    salesperson = fields.Many2one('res.users', string='Salesperson')
    buyer = fields.Many2one('res.partner', string='Buyer', readonly=True, copy=False)
    offers_id = fields.One2many('estate.property.offers', 'property_id', string='Offers')
    total_area = fields.Float(compute="_compute_total")
    best_price = fields.Float(compute="_compute_best_price")

    def property_cancel(self):
        for record in self:
            if record.state == 'canceled':
                record.state = 'canceled'
            else:
                record.state = 'canceled'

    def property_sold(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError('Cancelled property cannot be sold')
            else:
                record.state = 'sold'

    @api.depends("living_areas", "garden_area")
    def _compute_total(self):
        for record in self:
            record.total_area = record.living_areas + record.garden_area

    @api.depends("offers_id")
    def _compute_best_price(self):
        for best in self:
           prices = best.offers_id.mapped('price')
           best.best_price = max(prices) if prices else 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_orientation = 'north'
            self.garden_area = "10"
        else:
            self.garden_orientation = False
            self.garden_area = ''

