from odoo import fields, models, api


class Pelanggan(models.Model):
    _name = 'tokokipin.pelanggan'
    _description = 'Description pelanggan'
    _rec_name = 'kode_pelanggan'

    kode_pelanggan = fields.Char(
        string='Kode_pelanggan',
        required=False)
    pelanggan_ids = fields.One2many(
        comodel_name='tokokipin.penyewaan',
        inverse_name='kode_pelanggan',
        string='Kode_pelanggan IDs',
        required=False)
    nama_pelanggan = fields.Char(
        string='Nama_pelanggan',
        required=False)
    alamat = fields.Char(
        string='Alamat',
        required=False)
    no_tlpn = fields.Char(
        string='No_telepon',
        required=False)
    nama_pelanggan = fields.Many2one(comodel_name="res.partner", string='Nama Pembeli')
