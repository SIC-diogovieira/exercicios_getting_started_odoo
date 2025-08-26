# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offers"
    _description = "Estate tutorial"
    _order = "price desc"

    # -----------------------------
    # Exercise: Basic Fields
    # -----------------------------
    price = fields.Float()
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")],
        copy=False
    )
    partner_id = fields.Many2one('res.partner', string='Buyer')
    property_id = fields.Many2one('estate.property', string='Property')

    # -----------------------------
    # Exercise: Related Field
    # -----------------------------
    property_type_id = fields.Many2one(
        related="property_id.property_type_id"
    )

    # -----------------------------
    # Exercise: Validity + Dates
    # -----------------------------
    validity = fields.Integer(default=7)
    create_date = fields.Date(readonly=True)
    date_deadline = fields.Date(
        inverse="_inverse_date",
        compute="_compute_date"
    )

    # -----------------------------
    # Exercise: SQL Constraint
    # -----------------------------
    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)',
            'The offer price must be positive.'),
    ]

    # -----------------------------
    # Exercise: Offer Actions
    # -----------------------------
    def offer_accept(self):
        """Accept an offer, only one allowed per property"""
        for record in self:
            if record.status == "accepted":
                raise ValidationError("The property only accepts one offer")
            record.property_id.selling_price = record.price
            record.status = 'accepted'
            record.property_id.buyer = record.partner_id
            record.property_id.state = 'offer_a'

    def offer_refuse(self):
        """Refuse an offer"""
        for record in self:
            if record.status:
                record.status = 'refused'
                # limpar campos no imóvel
                record.property_id.selling_price = 0
                record.property_id.buyer = False
                record.property_id.state = 'offer_r'

    # -----------------------------
    # Exercise: Python Constraint
    # -----------------------------
    @api.constrains("price")
    def price_check(self):
        """Ensure new offer is not lower than existing ones"""
        for record in self:
            if record.property_id and record.property_id.offers_id:
                max_offer = max(record.property_id.offers_id.mapped("price"))
                if record.price < max_offer:
                    raise UserError('This price is lower than other offers')

    # -----------------------------
    # Exercise: Compute + Inverse
    # -----------------------------
    @api.depends("validity", "date_deadline", "create_date")
    def _compute_date(self):
        """Compute deadline = create_date + validity days"""
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + timedelta(days=record.validity)
            else:
                record.date_deadline = datetime.now() + timedelta(days=record.validity)

    def _inverse_date(self):
        """Allow changing deadline manually (recalculate validity)"""
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date - timedelta(days=record.validity)
