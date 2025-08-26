from odoo import api, fields, models, Command
from odoo.exceptions import AccessError, UserError


class EstatePropertyAccount(models.Model):
    # -----------------------------
    # Exercise: Addons Integration
    # Integração com o módulo de Contabilidade (account).
    # Herdamos o modelo estate.property.
    # -----------------------------
    _inherit = "estate.property"

    def property_sold(self):
        # Chamamos a versão original do método property_sold
        res = super().property_sold()

        # -----------------------------
        # Exercise: Accounting
        # Criamos uma fatura ao vender o imóvel
        # -----------------------------

        # Buscar o diário de vendas (necessário para criar a fatura)
        journal = self.env['account.journal'].search([('type', '=', 'sale')], limit=1)
        if not journal:
            raise UserError("Nenhum diário de vendas encontrado. Configure um diário de vendas em Contabilidade.")

        # Criar fatura ligada ao comprador (buyer)
        self.env['account.move'].create({
            'partner_id': self.buyer.id,          # cliente (comprador)
            'move_type': 'out_invoice',           # tipo de documento: fatura de saída
            'journal_id': journal.id,             # diário de vendas obrigatório
            'invoice_line_ids': [
                # linha da fatura → preço da propriedade
                Command.create({
                    'name': "Property",
                    'quantity': 1,
                    'price_unit': self.offers_id.price,
                }),
                # linha da fatura → comissão de 6%
                Command.create({
                    'name': "6% Fees",
                    'quantity': 1,
                    'price_unit': self.selling_price * 0.06,
                }),
                # linha da fatura → taxa administrativa fixa
                Command.create({
                    'name': "Administrative Fee",
                    'quantity': 1,
                    'price_unit': 100.0,
                }),
            ]
        })

        return res
