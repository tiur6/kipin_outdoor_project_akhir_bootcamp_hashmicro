from odoo import fields, models, api


class PenyewaanXlsx(models.AbstractModel):
    _name = 'report.tokokipin.report_penyewaan_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    tgl_lap = fields.Date.today()

    def generate_xlsx_report(self, workbook, data, penyewaan):
        sheet = workbook.add_worksheet('List Penyewaan')
        bold = workbook.add_format({'bold': True})
        sheet.write(0, 0, str(self.tgl_lap))
        sheet.write(1, 0, 'Nama Pembeli')
        sheet.write(1, 1, 'Tanggal Penyewaan')
        sheet.write(1, 2, 'Tanggal Pengembalian')
        sheet.write(1, 3, 'Subtotal')
        row = 2
        col = 0
        for obj in penyewaan:
            col = 0
            sheet.write(row, col, obj.name)
            sheet.write(row, col+1, obj.alamat)
            sheet.write(row, col+2, obj.no_telp)
            for xxx in obj.kode_barang_ids:
                sheet.write(row, col+3, xxx.name)
                col += 1
            row += 1
