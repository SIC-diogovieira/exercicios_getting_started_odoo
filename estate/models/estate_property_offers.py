# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offers"
    _description = "Estate tutorial"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection([("accepted", "Accepted"), ("refused", "Refused")], copy=False)
    partner_id = fields.Many2one('res.partner', string='Buyer')
    property_id = fields.Many2one('estate.property', string='Property')
    property_type_id = fields.Many2one(related="property_id.property_type_id")
    validity = fields.Integer(default=7)
    create_date = fields.Date(readonly=True)
    date_deadline = fields.Date(inverse="_inverse_date", compute="_compute_date")
    # offer_count = 1

    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)',
            'The Expected Price must be positive.'),
    ]

    def offer_accept(self):
        for record in self:
            if self.status == "accepted":
                raise ValidationError("The property only accept one offer")
            else:
                record.property_id.selling_price = record.price
                print(record.status)
                record.status = 'accepted'
                record.property_id.buyer = record.partner_id
                record.property_id.state = 'offer_a'

    def offer_refuse(self):
        for record in self:
            if record.status:
                record.status = 'refused'
                record.property_id.selling_price = ''
                record.property_id.buyer = ''
                record.property_id.state = 'offer_r'

    @api.constrains("price")
    def price_check(self):
        if self.property_id and self.property_id.offers_id:
            max_offer = max(self.property_id.offers_id.mapped("price"))
            print(max_offer)
            if self.price < max_offer:
                print(self.price)
                raise UserError('This price is lower than others')
            else:
                return self.price

    @api.depends("validity", "date_deadline", "create_date")
    def _compute_date(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + timedelta(days=record.validity)
            else:
                record.date_deadline = datetime.now() + timedelta(days=record.validity)

    def _inverse_date(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date - timedelta(days=record.validity)



