from odoo import fields, models, api


class Produk(models.Model):
    _name = 'tokokipin.produk'
    _description = 'Description produk'
    _rec_name = 'nama_produk'

    name = fields.Char()
    kode_spec = fields.Char(
        string='kode spec',
        required=False
    )
    kode_produk = fields.Char(
        string='Kode_produk',
        required=False)
    barang_ids = fields.One2many(
        comodel_name='tokokipin.barang',
        inverse_name='kode_produk',
        string='Kode_produk_ids',
        required=False)
    nama_produk = fields.Char(
        string='Nama_produk',
        required=False)

    jenisbarang_id = fields.Many2one(
        comodel_name='tokokipin.barang',
        string='jenis barang',
        required=False)