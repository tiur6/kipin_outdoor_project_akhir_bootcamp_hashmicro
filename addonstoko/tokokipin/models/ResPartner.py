from odoo import fields, models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'
    _description = 'New Description'

    is_direksi = fields.Boolean(string='Is Direksi')
    is_konsumen = fields.Boolean(string='Is Konsumen')
    id_member = fields.Char(
        string='Id Member',
        required=False,
        domain="[('is_konsumen', '=', True)]")
    poin = fields.Integer(string='Poin', domain="[('is_konsumen', '=', True)]")
    level = fields.Char(string='Level')
