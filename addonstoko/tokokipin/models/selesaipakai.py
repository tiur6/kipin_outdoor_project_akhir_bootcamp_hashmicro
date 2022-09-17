from odoo import fields, models, api


class Selesaipakai(models.Model):
    _name = 'tokokipin.selesaipakai'
    _description = 'Description'


    name = fields.Many2one(
        comodel_name='tokokipin.penyewaan',
        string='Customer',
        # domain="[('tgl_pengembalian','=',False)]",
    )

    tgl_penyewaan = fields.Char(
        compute='_compute_tgl_masuk',
        string='Tanggal Masuk')

    @api.depends('name')
    def _compute_tgl_pengembalian(self):
        for record in self:
            record.tgl_penyewaan = record.name.tanggal_penyewaan

    tgl_pengembalian = fields.Datetime(
        string='Tanggal Selesai',
        default=fields.Datetime.now())

    tagihan = fields.Integer(
        compute='_compute_tagihan',
        string='Total Pembayaran',
        store=True
    )

    @api.depends('name')
    def _compute_tagihan(self):
        for record in self:
            record.tagihan = record.name.subtotal
