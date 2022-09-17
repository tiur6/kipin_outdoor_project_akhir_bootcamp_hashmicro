from odoo import fields, models, api


class Penyewaan(models.Model):
    _name = 'tokokipin.penyewaan'
    # _inherit = 'res.partner'
    _description = 'Description'
    _rec_name = 'kode_pelanggan'

    status = fields.Selection(
        string='Status',
        selection=[('draft', 'Draft'),
                   ('runing', 'Runing'),
                   ('done', 'Done'),],
        required=False, )

    # status = fields.Selection(
    #     string='Status',
    #     selection=[('draft', 'Draft'),
    #                ('runing', 'Runing'),
    #                ('done', 'Done'),],
    #     required=False)


    nama_pembeli = fields.Many2one(comodel_name="res.partner", string='Nama Pembeli')
    # id_member = fields.Char(
    #     compute="_compute_id_member",
    #     string='Id_member',
    #     required=False)
    # @api.depends('nama')
    # def _compute_tagihan(self):
    #     for record in self:
    #         record.tagihan = record.name.subtotal

    no_notaids = fields.One2many(
        comodel_name='tokokipin.penyewaandetail',
        inverse_name='no_penjualan',
        string='No Penjualan ids',
        required=False)

    tgl_penyewaan = fields.Datetime(
        string='Tanggal Penyewaan',
        required=False,
        default=fields.Datetime.now()
    )

    tgl_pengembalian = fields.Datetime(
        string='Tanggal Pengembalian',
        # compute='_compute_tgl_pengembalian',
        required=False
    )
    jml_hari =fields.Integer(string='Jml_hari (Days)', required=False)

    state = fields.Selection(
        string='Status',
        selection=[('draft', 'Draft'),
                   ('confirm', 'Confirm'),
                   ('done', 'Done'),
                   ('cancelled', 'Cancelled'),
                   ],
        required=True, readonly=True, default='draft')

    @api.depends('nama_pembeli')
    def _compute_id_member(self):
        for rec in self:
            rec.id_member = rec.nama_pembeli.id_member

    def action_confirm(self):
        self.write({'state': 'confirm'})

    def action_done(self):
        self.write({'state': 'done'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})

    def action_draft(self):
        self.write({'state': 'draft'})

    # @api.depends('tgl_penyewaan', 'jml_hari')
    # def _compute_tgl_pengembalian(self):
    #     for record in self:
    #         record.tgl_pengembalian = record.tgl_penyewaan + timedelta(days=record.jml_hari)

    @api.depends('tgl_penyewaan,tgl_pengembalian')
    def _compute_jml_hari(self):
        for i in self:
            if i.tgl_penyewaan and i.tgl_pengembalian:
                i.jml_hari =(i.tgl_pengembalian - i.tgl_penyewaan).days
            else:
                i.jml_hari = 0

    # total_bayar = fields.Integer(
    #     string='Total_bayar',
    #     required=False
    # )
    total_bayar = fields.Integer(compute='_compute_totalbayar', string='Total Bayar')
    detailpenjualan_ids = fields.One2many(comodel_name='tokokipin.penyewaandetail',
                                          inverse_name='no_penjualan',
                                          string='List Barang')
    kode_pelanggan = fields.Char(
        # comodel_name='tokokipin.pelanggan',
        string='Kode Pelanggan',
        required=False
    )
    jk = fields.Selection(string='Jenis Kelamin',
                          selection=[('laki-laki', 'Laki-laki'),
                                     ('perempuan', 'Perempuan')],
                          required=True
                          )
    membership = fields.Boolean(string='Membership')
    nama_member = fields.Char(
        string='Nama_member',
        required=False
    )
    # pengguna = fields.Many2one(
    #     comodel_name='kipinmart.pengguna',
    #     string='Pengguna id',
    #     required=False
    # )
    harga_satuan=fields.Integer(
        string='harga satuan',
        required=False
    )
    satuan = fields.Char (compute= '_compute_satuan', string='satuan')
    selesai_sewa = fields.Boolean(
        string='Sudah Selesai'
    )

    @api.model
    def _compute_tanggal(self):
        for record in self:
            tgl = self.env['tokokipin.selesaipakai'].search([('name', '=', record.id)]).mapped('tgl_pengembalian')
            if tgl:
                record.tanggal_pengembalian = tgl[0]
                record.selesai_pakai = True
            else:
                record.tanggal_pengembalian = 0
                record.selesai_pakai = False

    # def confirm(self):
    #     for record in self:
    #         if record.tanggal_selesai:
    #             record.masuk_akunting = True
    #             self.env['wikulaundry.akunting'].create(
    #                 {'kredit': record.total_harga, 'name': record.name.display_name})
    #         else:
    #             raise ValidationError("Yang belum selesai dicuci tidak bisa masuk")


    # def unlink(self):
    #     if self.detailpenjualan_ids:
    #         a=[]
    #         for rec in self:
    #             a = self.env['tokokipin.penyewaandetail'].search([('no_penjualan','=',rec.id)])
    #             print(a)
    #         for i in a:
    #             print(str(i.barang_id.maen) +' ' + str(i.jumlah))
    #             i.barang_id.stok += i.jumlah
    #     record = super(PenyewaanDetail, self).unlink()

    def write(self, vals):
        for rec in self:
            a = self.env['tokokipin.penyewaandetail'].search([('no_penjualan','=', rec.id)])
            print(a)
            for data in a:
                print(str(data.kode_barang_ids.name)+" "+str(data.jml_hari))
        record= super (Penyewaan,self).write(vals)
        for rec in self :
            b=self.env['tokokipin.penyewaandetail'].search([('no_penjualan','=',rec.id)])
            print(b)
            for data in b:
                print(str(data.kode_barang_ids.name) + " " + str(data.jml_hari))
        return record

    @api.depends('total_bayar')
    def _compute_totalbayar(self):
        for record in self:
            a = sum(self.env['tokokipin.penyewaandetail'].search(
                [('no_penjualan', '=', record.id)]).mapped('subtotal'))
            record.total_bayar = a



class PenyewaanDetail(models.Model):
    _name = 'tokokipin.penyewaandetail'
    _description = 'Description penyewaan detail'
    _rec_name = 'kode_barang_ids'

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
        record = super(PenyewaanDetail, self).create(vals)
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
            record.subtotal = record.jml_hari * record.harga_jual * record.banyak_barang

    @api.depends('nama_barangpenjualan')
    def _compute_namabarang(self):
        for a in self:
            a.nama_barangpenjualan = a.kode_barang_ids.nama_barang
