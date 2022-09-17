from odoo import fields, models, api



class Pengembalian(models.Model):
    _name = 'tokokipin.pengembalian'
    _description = 'Description'


    name = fields.Char('nama')
    nama_pembeli = fields.Many2one(comodel_name="res.partner", string='Nama Pembeli')

    no_notaids = fields.One2many(
        comodel_name='tokokipin.penyewaandetail',
        inverse_name='nota_id',
        string='No Nota ids',
        required=False)

    tgl_penyewaan = fields.Datetime(
        string='Tanggal Penyewaan',
        required=False,
        default=fields.Datetime.now()
    )
    tgl_pengembalian = fields.Datetime(
        string='Tanggal Pengembalian',
        required=False,
        default=fields.Datetime.now()
    )
    detailpenjualan_ids = fields.One2many(comodel_name='tokokipin.pengembalian',
                                          inverse_name='no_penjualan',
                                          string='List Barang')


    status = fields.Selection(
        string='Status',
        selection=[('runing', 'Runig'),
                   ('ceking', 'Ceking'),
                   ('done', 'Done'),],
        required=False, )
    selesai_sewa = fields.Boolean(
        string='Sudah Selesai'
    )


    
    terlambat = fields.Integer(
        # compute='_compute_terlambat',
        string='Terlambat (Day)',
        required=False)

    denda = fields.Integer(
        # compute='_compute_denda',
        string='Denda 50K/hari',
        required=False)
    total_bayar = fields.Integer(compute='_compute_totalbayar', string='Total Bayar')

    # @api.depends('tgl_penyewaan,tgl_pengembalian')
    # def _compute_jml_hari(self):
    #     for i in self:
    #         if i.tgl_penyewaan and i.tgl_pengembalian:
    #             i.jml_hari = (i.tgl_pengembalian - i.tgl_penyewaan).days
    #         else:
    #             i.jml_hari = 0

    @api.model
    def _compute_tanggal(self):
        for record in self:
            tgl = self.env['tokokipin.selesaipakai'].search([('name', '=', record.id)]).mapped('tgl_pengembalian')
            if tgl:
                record.tanggal_pengembalian = tgl[0]
                record.selesai_pakai = False
            else:
                record.tanggal_pengembalian = 0
                record.selesai_pakai = False

    def write(self, vals):
        for rec in self:
            b = self.env['tokokipin.pengembalian'].search([('no_penjualan', '=', rec.id)])
            print(b)
            for data in b:
                print(str(data.kode_barang_ids.name) + " " + str(data.jml_hari))
        record = super(Pengembalian, self).write(vals)
        for rec in self:
            b = self.env['tokokipin.pengembalian'].search([('no_penjualan', '=', rec.id)])
            print(b)
            for data in b:
                print(str(data.kode_barang_ids.name) + " " + str(data.jml_hari))
        return record

    @api.depends('total_bayar')
    def _compute_totalbayar(self):
        for record in self:
            a = sum(self.env['tokokipin.pengembalian'].search(
                [('no_penjualan', '=', record.id)]).mapped('subtotal'))
            record.total_bayar = a
    # @api.depends('denda')
    # def _compute_denda(self):
    #     for record in self:
    #         record.denda = record.terlambat * record.harga_jual



    # status = fields.Selection(
    #     string='Status',
    #     selection=[('runing, Runing'), ('ceking', 'Ceking'), ('done', 'Done'),],
    #     required=False,)

    # @api.constrains('tgl_pengembalian')
    # def check_pengembalian(self):
    #     for rec in self:
    #         if rec.tgl_pengembalian == rec.tgl_pengembalian:
    #             raise ValidationError("Mau belanja {} berapa banyak sihh..".format(rec.tgl_pengembalian.name))
    #         elif (rec.tgl_pengembalian < rec.tgl_pengembalian):
    #             raise ValidationError(
    #                 'Stok {} tidak mencukupi, hanya tersedia {}'.format(rec.barang_id.name, rec.tgl_pengembalian.stok))

# class PengembalianDetail(models.Model):
#     _name = 'tokokipin.pengembaliandetail'
#     _description = 'Description pengembalian detail'
#     _rec_name = 'kode_barang_ids'

    # barang_id = fields.Many2one(comodel_name='tokokipin.barang', string='List Barang')
    # penjualan_id = fields.Many2one(comodel_name='tokokipin.penyewaan', string='Detail Penjualan')


    nota_id = fields.Char(
        string='Nota_id',
        required=False
    )
    no_penjualan = fields.Many2one(
        comodel_name='tokokipin.penyewaan',
        string='Kode penjualan',
        required=False
    )
    kode_barang_ids = fields.Many2one(
        comodel_name='tokokipin.barang',
        string='Kode_barang_ids',
        required=False
    )
    nama_barangpenjualan = fields.Char(
        compute="_compute_namabarang",
        string='Nama_barang',
        required=False
    )
    harga_jual = fields.Integer(
        compute="_compute_hargajual",
        string='Harge_jual',
        required=False
    )
    jml_hari = fields.Integer(
        string='jumlah hari',
        required=False
    )
    subtotal = fields.Integer(
        string='Subtotal',
        compute="_compute_subtotal",
        required=False
    )
    banyak_barang=fields.Integer(
        string='banyak barang',
        required=False
    )


    @api.model
    def create(self, vals):
        record = super(Pengembalian, self).create(vals)
        if record.jml_hari:
            self.env['tokokipin.barang'].search([('id', '=', record.kode_barang_ids.id)]).write({
                'stok': record.kode_barang_ids.stok - record.jml_hari})
            return record

    @api.depends('harga_jual')
    def _compute_hargajual(self):
        for a in self:
            a.harga_jual = a.kode_barang_ids.harga_jual

    @api.depends('subtotal')
    def _compute_subtotal(self):
        for record in self:
            record.subtotal = record.jml_hari * record.harga_jual * record.banyak_barang + record.denda

    @api.depends('nama_barangpenjualan')
    def _compute_namabarang(self):
        for a in self:
            a.nama_barangpenjualan = a.kode_barang_ids.nama_barang
