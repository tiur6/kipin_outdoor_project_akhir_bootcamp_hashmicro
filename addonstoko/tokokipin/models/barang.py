from odoo import fields, models, api


class Barang(models.Model):
    _name = 'tokokipin.barang'
    _description = 'Description'
    _rec_name = 'kode_barang'

    name = fields.Char()

    kode_barang = fields.Char(
        string='Kode_barang',
        required=False)

    kode_produk = fields.Many2one(
        comodel_name='tokokipin.produk',
        string='Kode_produk',
        required=False)

    keterangan_produk = fields.Char(
        string='Nama Produk',
        compute="_compute_produk",
        required=False)

    nama_barang = fields.Char(
        string='Nama_barang',
        required=False
    )
    satuan = fields.Selection(
        string='Satuan',
        selection=[('unit', 'Unit'),
                   ('dus', 'Dus'),
                   ('lusin', 'Lusin'),
                   ('meter', 'Meter'), ],
        required=False,
    )
    harga_beli = fields.Integer(
        string='Harga_beli',
        required=False)
    harga_jual = fields.Integer(
        string='Harga Sewa/hari',
        required=False)

    stok = fields.Integer(
        string='Stok',
        required=False)

    jenisbarang_ids = fields.One2many(
        comodel_name='tokokipin.produk',
        inverse_name='jenisbarang_id',
        string='jenis barang',
        required=False)

    @api.depends('kode_produk')
    def _compute_produk(self):
        for a in self:
            a.keterangan_produk = a.kode_produk.nama_produk