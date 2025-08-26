# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate tutorial"
    _order = "id desc"

    # -----------------------------
    # Exercise: Basic Model Creation
    # -----------------------------
    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False,
        default=fields.Date.add(fields.Date.today(), months=3)
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_areas = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_orientation = fields.Selection([
        ("north", "North")
    ])
    garden_area = fields.Integer()
    active = fields.Boolean(default=True, string='Ativo')

    # -----------------------------
    # Exercise: States
    # -----------------------------
    state = fields.Selection([
        ("new", "New"),
        ("offer_r", "Offer Received"),
        ("offer_a", "Offer Accepted"),
        ("sold", "Sold"),
        ("canceled", "Canceled")
    ], default="new")

    # -----------------------------
    # Exercise: Relations
    # -----------------------------
    property_type_id = fields.Many2one('estate.property.type', string='Type')
    property_tag_id = fields.Many2many('estate.property.tags', string='Tags')
    salesperson = fields.Many2one('res.users', string='Salesperson')
    buyer = fields.Many2one('res.partner', string='Buyer', readonly=True, copy=False)
    offers_id = fields.One2many('estate.property.offers', 'property_id', string='Offers')

    # -----------------------------
    # Exercise: Computed Fields
    # -----------------------------
    total_area = fields.Float(compute="_compute_total")
    best_price = fields.Float(compute="_compute_best_price")

    # -----------------------------
    # Exercise: SQL Constraints
    # -----------------------------
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)',
         'The Expected Price must be positive.'),
    ]
    # outro exemplo possível:
    # status = fields.Selection([("accepted", "Accepted"), ("refused", "Refused")], copy=False)

    # -----------------------------
    # Exercise: Button Actions
    # -----------------------------
    def offer_received(self):
        """Change state when offer is received"""
        for record in self:
            record.state = 'offer_r'
        return self.state

    def property_cancel(self):
        """Cancel property"""
        for record in self:
            record.state = 'canceled'

    def property_sold(self):
        """Sell property (cannot sell canceled)"""
        for record in self:
            if record.state == 'canceled':
                raise UserError('Cancelled property cannot be sold')
            record.state = 'sold'

    # -----------------------------
    # Exercise: Deletion Constraint
    # -----------------------------
    @api.ondelete(at_uninstall=False)
    def prevent_delete(self):
        """Only allow delete if state is new or canceled"""
        if self.state not in ["new", "canceled"]:
            raise UserError('This property cannot be cancelled')

    # -----------------------------
    # Exercise: Create Override
    # -----------------------------
    @api.model_create_multi
    def create(self, vals_list):
        """If offers exist on creation, set state to offer received"""
        for vals in vals_list:
            if "offers_id" in vals:
                vals["state"] = "offer_r"
        res = super().create(vals_list)
        return res

    # -----------------------------
    # Exercise: Compute Methods
    # -----------------------------
    @api.depends("living_areas", "garden_area")
    def _compute_total(self):
        """Compute total area (living + garden)"""
        for record in self:
            record.total_area = record.living_areas + record.garden_area

    @api.depends("offers_id")
    def _compute_best_price(self):
        """Compute best price from all offers"""
        for record in self:
            prices = record.offers_id.mapped('price')
            record.best_price = max(prices) if prices else 0

    # -----------------------------
    # Exercise: Onchange
    # -----------------------------
    @api.onchange("garden")
    def _onchange_garden(self):
        """When garden is set, default orientation and area"""
        if self.garden:
            self.garden_orientation = 'north'
            self.garden_area = 10  # corrigido: inteiro, não string
        else:
            self.garden_orientation = False
            self.garden_area = 0

    # -----------------------------
    # Exercise: Python Constraint
    # -----------------------------
    # @api.constrains('offers_id')
    # def _check_selling_price(self):
    #     """Ensure selling price >= 90% of expected"""
    #     for record in self:
    #         if record.offers_id.price < 0.9 * record.expected_price:
    #             raise ValidationError(
    #                 "The Selling Price must be more than 90% of expected price"
    #             )
