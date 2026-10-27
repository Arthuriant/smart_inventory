"""Builds Bulk_Import_Template_Master.xlsx, the master copy used by the flow
"Smart Inventory - Bulk Import Template".

The master has empty list tables on the Lists sheet; the flow copies the master and fills
tblArea / tblCategory / tblRack with the current data of the requesting user's business line
(sent by the app), so the dropdowns in the downloaded template are always up to date.
Row 2 of each list table is a hidden empty row (a table needs one data row); data starts at row 3.

Usage: python build_template.py [output.xlsx]
"""
import os
import sys

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.worksheet.table import Table, TableStyleInfo

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "Bulk_Import_Template_Master.xlsx")
F = "Arial"
NAVY = "00126B"
HDR = PatternFill("solid", fgColor=NAVY)
thin = Side(style="thin", color="E2E6EF")
BOX = Border(left=thin, right=thin, top=thin, bottom=thin)
LAST = 500  # last list row the dropdowns look at
UOMS = ["EA", "M", "SET", "DR", "JT", "BOX", "L", "PR", "SX", "FT", "GAL", "KG", "BBL", "MT"]
HEADERS = ["Area", "Item name", "BPN", "SPN", "Category", "UOM", "Qty", "Min in area", "Rack"]
WIDTHS = [28, 30, 16, 14, 14, 9, 8, 12, 16]

wb = Workbook()

# ---------- Import ----------
ws = wb.active
ws.title = "Import"
for c, h in enumerate(HEADERS, 1):
    cell = ws.cell(row=1, column=c, value=h)
    cell.font = Font(name=F, bold=True, color="FFFFFF")
    cell.fill = HDR
    cell.alignment = Alignment(horizontal="center", vertical="center")
    ws.column_dimensions[cell.column_letter].width = WIDTHS[c - 1]
for r in range(2, 201):
    for c in range(1, 10):
        cell = ws.cell(row=r, column=c)
        cell.font = Font(name=F)
        cell.border = BOX
        if c in (7, 8):
            cell.number_format = "0"
ws.row_dimensions[1].height = 22
ws.freeze_panes = "A2"
t = Table(displayName="tblImport", ref="A1:I200")
t.tableStyleInfo = TableStyleInfo(name="TableStyleLight1", showRowStripes=False)
ws.add_table(t)

# ---------- Lists (filled by the flow) ----------
ls = wb.create_sheet("Lists")
# (table, first column, headers); one empty column between tables so they can grow independently
lists = [("tblArea", 1, ["Area"]), ("tblCategory", 3, ["Category code", "Category name"]),
         ("tblUom", 6, ["UOM"]), ("tblRack", 8, ["Rack", "Rack is in area"])]
for name, col, heads in lists:
    for i, h in enumerate(heads):
        cell = ls.cell(row=1, column=col + i, value=h)
        cell.font = Font(name=F, bold=True, color="FFFFFF")
        cell.fill = HDR
        ls.column_dimensions[cell.column_letter].width = 28 if h in ("Area", "Rack is in area") else 16
    last_row = 2 + (len(UOMS) if name == "tblUom" else 0)
    first = ls.cell(row=1, column=col).column_letter
    end = ls.cell(row=1, column=col + len(heads) - 1).column_letter
    tb = Table(displayName=name, ref=f"{first}1:{end}{last_row}")
    tb.tableStyleInfo = TableStyleInfo(name="TableStyleLight1", showRowStripes=False)
    ls.add_table(tb)
for i, u in enumerate(UOMS, 3):
    ls.cell(row=i, column=6, value=u).font = Font(name=F)
ls.row_dimensions[2].hidden = True
ls.cell(row=1, column=11, value="Filled automatically when the template is downloaded from the app. Do not edit.").font = \
    Font(name=F, italic=True, color="64707F")


def dv(formula, rng, title, msg):
    v = DataValidation(type="list", formula1=formula, allow_blank=True, showErrorMessage=True,
                       errorStyle="warning", errorTitle=title, error=msg)
    ws.add_data_validation(v)
    v.add(rng)


# Lists ranges go through INDIRECT: every row the flow adds to a Lists table inserts cells there, and Excel
# would shift a plain Lists!$A$3 reference down past the data (the dropdowns came out empty)
def lst(rng):
    return f'INDIRECT("Lists!{rng}")'


dv(f"OFFSET({lst('$A$3')},0,0,MAX(1,COUNTA({lst(f'$A$3:$A${LAST}')})),1)", "A2:A200", "Area",
   "This area is not in your business line. The app will mark the row red.")
dv(f"OFFSET({lst('$C$3')},0,0,MAX(1,COUNTA({lst(f'$C$3:$C${LAST}')})),1)", "E2:E200", "Category",
   "Use a category code from the Lists sheet (the name also works).")
dv(lst(f"$F$3:$F${len(UOMS) + 2}"), "F2:F200", "UOM", "UOM must be one of the values in the Lists sheet.")
# only the racks of the row's area: the block in column H that starts at the first match of the area in column I
dv(f"OFFSET({lst('$H$2')},IFERROR(MATCH($A2,{lst(f'$I$3:$I${LAST}')},0),{LAST - 2}),0,"
   f"MAX(1,COUNTIF({lst(f'$I$3:$I${LAST}')},$A2)),1)",
   "I2:I200", "Rack", "This rack is not in the area of this row (see the Lists sheet).")
num = DataValidation(type="decimal", operator="greaterThanOrEqual", formula1="0", allow_blank=True,
                     showErrorMessage=True, errorTitle="Number", error="Enter a number of 0 or more.")
ws.add_data_validation(num)
num.add("G2:H200")

# ---------- Petunjuk ----------
gs = wb.create_sheet("Petunjuk", 0)
gs.column_dimensions["A"].width = 4
gs.column_dimensions["B"].width = 110
lines = [
    ("Bulk Import template - Smart Inventory", "title"),
    ("", None),
    ("Cara pakai", "h"),
    ("1. Isi sheet 'Import' mulai baris 2. Dropdown Area, Category, UOM dan Rack berisi data terkini business line Anda.", None),
    ("2. Simpan file, lalu di app: Transaction > Bulk Import > Upload Excel > Read file.", None),
    ("   (Atau: blok sel Area sampai Rack, Ctrl+C, lalu Ctrl+V ke kotak di app dan klik Check.)", None),
    ("3. Perbaiki baris yang merah, upload/paste lagi. Jika semua OK, klik Import.", None),
    ("", None),
    ("Kolom", "h"),
    ("Area (wajib): pilih dari dropdown (area business line Anda).", None),
    ("Item name / BPN: minimal salah satu. Barang dicocokkan lewat BPN; jika BPN kosong, lewat nama.", None),
    ("SPN: opsional, hanya untuk barang baru.", None),
    ("Category, UOM: hanya wajib untuk barang BARU (belum ada di katalog).", None),
    ("Qty: > 0 = dicatat sebagai Receive (1 transaksi per area). 0 / kosong = barang hanya ditambahkan ke area.", None),
    ("Min in area: minimum stok di area itu. Kosong = tidak mengubah min yang ada (barang baru: 0).", None),
    ("Rack: opsional. Dropdown hanya menampilkan rak milik Area di baris itu (isi Area dulu).", None),
    ("", None),
    ("Contoh baris", "h"),
    ("Container Filter | Filter Testing | | | | | 5 | 2 | Oil Filter   (barang lama, +5 stok, min 2, rak Oil Filter)", None),
    ("Storage Room | SAFETY GLOVES SIZE L | BPN-GLV-001 | SPN-778 | CNM | PR | 20 | 5 |   (barang baru)", None),
    ("", None),
    ("Catatan", "h"),
    ("Jangan hapus/ganti nama tabel 'tblImport' dan judul kolomnya; jangan ubah sheet 'Lists'.", None),
    ("Satu barang + area yang sama hanya boleh muncul sekali per import.", None),
    ("Download template baru dari app bila ada area/rak/kategori baru.", None),
]
for i, (text, kind) in enumerate(lines, 1):
    cell = gs.cell(row=i, column=2, value=text)
    cell.font = Font(name=F, bold=kind in ("title", "h"), size=14 if kind == "title" else 10 if kind is None else 11,
                     color=NAVY if kind else None)
    cell.alignment = Alignment(wrap_text=True, vertical="top")

wb.active = 1
wb.save(OUT)
print(OUT)
