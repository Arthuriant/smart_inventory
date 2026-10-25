# Smart Inventory – Power Automate (Bulk Import)

| File | Fungsi |
|---|---|
| `SmartInventoryFlows_1_1_0_0.zip` | Solution (unmanaged): 2 cloud flow + 2 connection reference. **Ini yang di-import.** |
| `Bulk_Import_Template_Master.xlsx` | File master template. Disimpan sekali di OneDrive (lihat Langkah 1). |
| `build_solution.py` / `build_template.py` | Sumber zip dan file master. Ubah di sini lalu jalankan ulang (`python build_solution.py`, `python build_template.py`). |

## Dua flow di solution ini

**Smart Inventory - Bulk Import Template** (tombol **Template** di Bulk Import)
1. App mengirim data terkini business line user (area, kategori, rak — teks JSON, input `listsJson`).
2. Flow menyalin `Apps/SmartInventory/Bulk_Import_Template_Master.xlsx`, mengisi tabel `tblArea`,
   `tblCategory`, `tblRack` di sheet *Lists* (dropdown Area/Category/Rack), membuat link (organisasi, view)
   dan mengirimnya ke app, yang langsung men-download file.
3. Salinan dihapus otomatis 15 menit kemudian.

**Smart Inventory - Bulk Import Read Excel** (tombol **Upload Excel** di Bulk Import)
1. App mengirim file .xlsx sebagai teks base64 (input `fileContent`).
2. Flow menyimpannya sementara, membaca tabel `tblImport`, mengembalikan baris sebagai teks (format paste),
   lalu menghapus file. App menjalankan **Check** seperti biasa.

Kedua flow hanya memakai konektor **standar** (OneDrive for Business, Excel Online Business) dan tidak menyentuh Dataverse.
Semua file ada di OneDrive **pemilik koneksi** (ARianto2): folder `Apps/SmartInventory` dan `Apps/SmartInventory/BulkImport`.

---

## Langkah 1 – OneDrive (sekali saja)

1. https://www.office.com > **OneDrive** > **My files** > `Apps` > `SmartInventory` (buat folder bila belum ada),
   dan di dalamnya folder `BulkImport`.
2. Upload `Bulk_Import_Template_Master.xlsx` ke **`Apps/SmartInventory`** (bukan ke BulkImport).
   Nama file harus persis `Bulk_Import_Template_Master.xlsx`.

## Langkah 2 – Import solution

1. https://make.powerapps.com > environment **ING | Well Construction - TLM** > **Solutions** > **Import solution**
   > pilih `SmartInventoryFlows_1_1_0_0.zip` > **Next** > pilih koneksi OneDrive & Excel yang sama seperti sebelumnya > **Import**.
2. Buka solution **Smart Inventory Flows**: pastikan **kedua** flow statusnya **On** (jika Off: buka flow > **Turn on**).

Drive OneDrive sudah tertanam di solution (milik ARianto2), jadi aksi Excel **tidak perlu diatur ulang**.
Jika pemilik flow diganti orang lain: di setiap aksi Excel (*List rows present in a table*, *Add area row*,
*Add category row*, *Add rack row*) pilih **Location** = OneDrive for Business dan **Document Library** = OneDrive, lalu Save
(atau ubah `DRIVE_ID` di `build_solution.py`).

## Langkah 3 – Hubungkan ke app

1. Power Apps Studio > panel **Power Automate** (menu kiri) > **Add flow** > pilih **Smart Inventory - Bulk Import Template**.
2. Pada flow **Smart Inventory - Bulk Import Read Excel**: **...** > **Refresh**.
3. **File > Save**. (Setelah itu Claude meng-compile tombol **Template** di screen Bulk Import.)

## Tes

- **Template**: klik di app > tunggu ±10–30 detik > file ter-download. Buka sheet *Import*, cek dropdown Area/Category/Rack.
- **Upload Excel**: isi template > upload > baris masuk ke kotak paste dan Check berjalan.
- Jika gagal: pesan di app berisi alasan; detail ada di **run history** flow (make.powerautomate.com > My flows > flow > run terakhir).

## Aturan template

- Jangan hapus/ganti nama tabel **`tblImport`** dan judul kolomnya: `Area | Item name | BPN | SPN | Category | UOM | Qty | Min in area | Rack`.
- Jangan ubah sheet **Lists** (diisi otomatis saat download).
- Baris kosong di dalam tabel diabaikan.
