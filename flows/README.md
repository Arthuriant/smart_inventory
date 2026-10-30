# Smart Inventory – Power Automate (Bulk Import)

| File | Fungsi |
|---|---|
| `SmartInventoryFlows_1_4_0_0.zip` | Solution (unmanaged): 2 cloud flow + 3 connection reference (OneDrive, Excel, Dataverse). **Ini yang di-import.** |
| `FillTemplateLists.ts` | Office Script **SmartInventoryFillLists** yang dipanggil flow Template (sejak v1.4.0.0). Dibuat sekali di Excel Online (lihat Langkah 1b). |
| `Bulk_Import_Template_Master.xlsx` | File master template. Disimpan sekali di OneDrive (lihat Langkah 1). |
| `build_solution.py` / `build_template.py` | Sumber zip dan file master. Ubah di sini lalu jalankan ulang (`python build_solution.py`, `python build_template.py`). |

## Dua flow di solution ini

**Smart Inventory - Bulk Import Template** (tombol **Template** di Bulk Import)
1. App mengirim data terkini business line user (area, kategori — teks JSON, input `listsJson`).
   Sejak v1.2.0.0 rak dibaca flow sendiri dari Dataverse (`dis_racks` aktif yang areanya ada di daftar area dari app);
   daftar rak dari app diabaikan.
   Sejak v1.3.0.0 app juga mengirim nama item katalog (±100 nama per baris teks) ke tabel `tblCatalog`
   supaya kolom **Status** di sheet Import bisa mengecek baris dengan aturan yang sama seperti tombol Check di app.
2. Flow menyalin `Apps/SmartInventory/Bulk_Import_Template_Master.xlsx`, mengisi tabel `tblArea`,
   `tblCategory`, `tblRack`, `tblCatalog` di sheet *Lists* (sejak v1.4.0.0 sekaligus lewat satu Office Script, dulu satu
   panggilan per baris) (dropdown Area/Category/Rack), membuat link (organisasi, view)
   dan mengirimnya ke app, yang langsung men-download file.
3. Salinan dihapus otomatis 15 menit kemudian.

**Smart Inventory - Bulk Import Read Excel** (tombol **Upload Excel** di Bulk Import)
1. App mengirim file .xlsx sebagai teks base64 (input `fileContent`).
2. Flow menyimpannya sementara, membaca tabel `tblImport`, mengembalikan baris sebagai teks (format paste),
   lalu menghapus file. App menjalankan **Check** seperti biasa.

Kedua flow hanya memakai konektor **standar** (OneDrive for Business, Excel Online Business, Microsoft Dataverse).
Flow Template hanya **membaca** tabel `dis_racks`; tidak ada data Dataverse yang diubah.
Semua file ada di OneDrive **pemilik koneksi** (ARianto2): folder `Apps/SmartInventory` dan `Apps/SmartInventory/BulkImport`.

---

## Langkah 1 – OneDrive (sekali saja)

1. https://www.office.com > **OneDrive** > **My files** > `Apps` > `SmartInventory` (buat folder bila belum ada),
   dan di dalamnya folder `BulkImport`.
2. Upload `Bulk_Import_Template_Master.xlsx` ke **`Apps/SmartInventory`** (bukan ke BulkImport).
   Nama file harus persis `Bulk_Import_Template_Master.xlsx`.

## Langkah 1b – Office Script (sekali saja, sejak v1.4.0.0)

1. Buka file Excel apa saja di Excel Online (login ARianto2) > tab **Automate** > **New Script**.
2. Hapus isi editor, tempel seluruh isi `FillTemplateLists.ts`, beri nama **SmartInventoryFillLists**, **Save script**.
   Skrip tersimpan di OneDrive `Documents/Office Scripts/SmartInventoryFillLists.osts`.

## Langkah 2 – Import solution

1. https://make.powerapps.com > environment **ING | Well Construction - TLM** > **Solutions** > **Import solution**
   > pilih `SmartInventoryFlows_1_4_0_0.zip` > **Next** > pilih koneksi OneDrive & Excel yang sama seperti sebelumnya,
   dan untuk **Smart Inventory - Microsoft Dataverse** pilih/buat koneksi Dataverse (login ARianto2) > **Import**.
   Muncul pertanyaan upgrade: pilih **Upgrade** (default).
2. Sejak v1.4.0.0: buka flow **Smart Inventory - Bulk Import Template** > **Edit** > aksi **Fill_lists** (Run script) >
   **Script** pilih **SmartInventoryFillLists** > field **listsJson** isi dengan ekspresi `string(outputs('Compose_lists'))` >
   **Save**. (Id skrip berbeda per OneDrive, jadi tidak bisa tertanam di zip.)
3. Buka solution **Smart Inventory Flows**: pastikan **kedua** flow statusnya **On** (jika Off: buka flow > **Turn on**).

Drive OneDrive sudah tertanam di solution (milik ARianto2), jadi aksi Excel **tidak perlu diatur ulang**.
Jika pemilik flow diganti orang lain: di setiap aksi Excel (*List rows present in a table*, *Fill_lists*) pilih **Location** = OneDrive for Business dan **Document Library** = OneDrive, lalu Save
(atau ubah `DRIVE_ID` di `build_solution.py`).

## Langkah 3 – Hubungkan ke app

1. Power Apps Studio > panel **Power Automate** (menu kiri) > **Add flow** > pilih **Smart Inventory - Bulk Import Template**.
2. Pada flow **Smart Inventory - Bulk Import Read Excel**: **...** > **Refresh**.
3. **File > Save**. (Setelah itu Claude meng-compile tombol **Template** di screen Bulk Import.)

Update flow saja (app sudah terhubung): import zip versi baru, lalu di Studio flow **Smart Inventory - Bulk Import Template**
> **...** > **Refresh** dan **File > Save**. Input/output flow tidak berubah, jadi app tidak perlu di-compile.

## Tes

- **Template**: klik di app > tunggu > file terbuka di Excel Online (tab baru) > **File > Save As > Download a Copy**.
  Jangan download langsung dari link: isi baru masih di sesi Excel dan file di OneDrive baru ter-update beberapa menit kemudian. Buka sheet *Import*, cek dropdown Area/Category/Rack.
- **Upload Excel**: isi template > upload > baris masuk ke kotak paste dan Check berjalan.
- Jika gagal: pesan di app berisi alasan; detail ada di **run history** flow (make.powerautomate.com > My flows > flow > run terakhir).

## Aturan template

- Jangan hapus/ganti nama tabel **`tblImport`** dan judul kolomnya: `Area | Item name | BPN | SPN | Category | UOM | Qty | Min in area | Rack`.
- Jangan ubah sheet **Lists** (diisi otomatis saat download).
- Dropdown membaca sheet Lists lewat `INDIRECT(...)`: baris yang ditambahkan flow menggeser referensi biasa
  sehingga dropdown kosong (diperbaiki 2026-10-27; master lama di OneDrive harus diganti).
- Baris kosong di dalam tabel diabaikan.
- Kolom **Status** (K) dihitung rumus: aturan sama dengan Check di app (area, nama item wajib, qty/min, rack, item baru
  butuh Category+UOM, nama item sama 2x di satu area). Nama item = identitas barang; BPN/SPN boleh sama.
  Kolom L–M adalah kolom bantu tersembunyi. Status mencakup seluruh baris tabel (1000 baris siap, baris tempelan ikut). Upload hanya bila semua OK;
  app tetap memeriksa ulang saat upload. App tidak lagi punya kotak paste (hanya Template + Upload Excel).
