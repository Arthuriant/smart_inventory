# Smart Inventory – Power Automate (Bulk Import upload)

Isi folder ini:

| File | Fungsi |
|---|---|
| `SmartInventoryFlows_1_0_0_0.zip` | Solution (unmanaged) berisi 1 cloud flow + 2 connection reference. Ini yang di-import. |
| `build_solution.py` | Sumber solution di atas. Ubah di sini lalu jalankan `python build_solution.py` untuk membuat zip baru. |
| `Bulk_Import_Template.xlsx` | Template Excel. Sheet **Import** berisi Excel Table **`tblImport`** yang dibaca flow. |

## Cara kerja flow "Smart Inventory - Bulk Import Read Excel"

1. App mengirim file .xlsx yang sudah diisi user (trigger **Power Apps (V2)**, input `File`).
2. File disimpan sementara di OneDrive pemilik koneksi: `/Apps/SmartInventory/BulkImport/<guid>.xlsx`.
3. **Excel Online (Business) – List rows present in a table** membaca tabel `tblImport`.
4. Setiap baris diubah menjadi teks dipisah tab, **format yang sama dengan copy-paste dari Excel**.
5. Flow menjawab ke app: `rows` (teks) atau `error` (pesan), lalu menghapus file sementara.

App memasukkan `rows` ke kotak paste lalu menjalankan **Check** yang sudah ada, jadi semua aturan
(area per BL, rak per area, barang baru, dll.) tetap di app. Flow **tidak** menyentuh Dataverse,
jadi hanya butuh konektor **standar** (OneDrive for Business + Excel Online Business).

---

## Langkah 1 – Siapkan folder OneDrive (sekali saja)

Flow menyimpan file sementara di OneDrive **akun yang dipakai untuk koneksi** (kamu).

1. Buka https://www.office.com, login dengan akun SLB (ARianto2@slb.com), lalu buka **OneDrive**.
2. Di **My files**, buka folder **Apps** (jika belum ada: **+ Add new > Folder**, beri nama `Apps`).
3. Di dalam `Apps`, buat folder `SmartInventory`.
4. Di dalam `SmartInventory`, buat folder `BulkImport`.
   Hasil akhirnya: `My files > Apps > SmartInventory > BulkImport`.
5. (Opsional) Simpan juga `Bulk_Import_Template.xlsx` di `Apps > SmartInventory` sebagai master template
   untuk dibagikan ke user (klik kanan file > **Share** / **Copy link**).

> File di `BulkImport` langsung dihapus flow setelah dibaca. Jika ada yang tertinggal (flow gagal di tengah), aman dihapus manual.

## Langkah 2 – Import solution

1. Buka https://make.powerapps.com, pilih environment **ING | Well Construction - TLM** (kanan atas).
2. Menu kiri **Solutions** > **Import solution** > **Browse** > pilih `SmartInventoryFlows_1_0_0_0.zip` > **Next**.
3. Halaman **Connections**: untuk tiap connection reference pilih koneksi yang sudah ada, atau **+ New connection**:
   - *Smart Inventory - OneDrive for Business* → koneksi **OneDrive for Business** akun kamu.
   - *Smart Inventory - Excel Online (Business)* → koneksi **Excel Online (Business)** akun kamu.
4. **Import**, tunggu sampai muncul notifikasi sukses.
5. Buka solution **Smart Inventory Flows** > klik flow **Smart Inventory - Bulk Import Read Excel**.
   Jika statusnya **Off**: **Turn on**.

Jika import/turn on gagal dengan pesan tentang **data policy (DLP)**, berarti konektor OneDrive/Excel
diblokir di environment ini; minta admin Power Platform mengizinkan keduanya (kelompok *Business*).

## Langkah 3 – Tes flow (tanpa app)

1. Di halaman flow: **Test** > **Manually** > **Test**.
2. Upload `Bulk_Import_Template.xlsx` (masih berisi 5 baris contoh) > **Run flow**.
3. Buka run-nya: aksi **Respond to app rows** harus berisi 5 baris teks (kolom dipisah tab).
   Cek juga file di `BulkImport` sudah terhapus.

## Langkah 4 – Hubungkan ke app (nanti, saat fitur upload diaktifkan)

1. Power Apps Studio > ikon **Power Automate** (menu kiri) > **Add flow** > pilih
   **Smart Inventory - Bulk Import Read Excel**.
2. Beri tahu Claude: tombol **Upload Excel** di screen Bulk Import akan memanggil
   `<nama flow>.Run({file: {contentBytes: ..., name: ...}})` (nama persisnya terlihat di Studio setelah Add flow), mengisi kotak paste
   dengan hasil `rows`, lalu menjalankan Check otomatis. (Kontrol upload file perlu ditambahkan di Studio
   karena Power Apps hanya menyediakan kontrol *Attachments* di dalam form.)

## Aturan template supaya bisa dibaca flow

- Jangan hapus/ganti nama tabel **`tblImport`** (Table Design > Table Name).
- Jangan ubah judul kolom: `Area | Item name | BPN | SPN | Category | UOM | Qty | Min in area | Rack`.
- Baris kosong di dalam tabel tidak masalah (diabaikan oleh app).
