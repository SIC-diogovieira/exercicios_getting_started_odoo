# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from datetime import datetime, timedelta


class EstateProperty(models.Model):
    _name = "estate.property.offers"
    _description = "Estate tutorial"

    price = fields.Float()
    status = fields.Selection([("accepted", "Accepted"), ("refused", "Refused")], copy=False)
    partner_id = fields.Many2one('res.partner', string='Buyer')
    property_id = fields.Many2one('estate.property', string='Property')
    validity = fields.Integer(default=7)
    create_date = fields.Date(readonly=True)
    date_deadline = fields.Date(inverse="_inverse_date", compute="_compute_date")
    accept = fields.Boolean()
    refuse = fields.Boolean()

    def offer_accept(self):
        for record in self:
            record.accept = True
            if record.accept and record.status == False:
                record.property_id.selling_price = record.price
                record.status = 'accepted'
                record.property_id.buyer = record.partner_id

    def offer_refuse(self):
        for record in self:
            record.refuse = True
            print(record.status)
            if record.refuse and record.status != '':
                record.status = 'refused'
                record.property_id.selling_price = ''
                record.property_id.buyer = ''

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

