# Smart Inventory – Power Automate (Bulk Import upload)

Isi folder ini:

| File | Fungsi |
|---|---|
| `SmartInventoryFlows_1_0_0_2.zip` | Solution (unmanaged) berisi 1 cloud flow + 2 connection reference. Ini yang di-import. |
| `build_solution.py` | Sumber solution di atas. Ubah di sini lalu jalankan `python build_solution.py` untuk membuat zip baru. |
| `Bulk_Import_Template.xlsx` | Template Excel. Sheet **Import** berisi Excel Table **`tblImport`** yang dibaca flow. |

## Cara kerja flow "Smart Inventory - Bulk Import Read Excel"

1. App mengirim file .xlsx yang sudah diisi user sebagai teks *data URI* base64 (trigger **Power Apps (V2)**, input teks `fileContent`).
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
2. Menu kiri **Solutions** > **Import solution** > **Browse** > pilih `SmartInventoryFlows_1_0_0_2.zip` > **Next**.
3. Halaman **Connections**: untuk tiap connection reference pilih koneksi yang sudah ada, atau **+ New connection**:
   - *Smart Inventory - OneDrive for Business* → koneksi **OneDrive for Business** akun kamu.
   - *Smart Inventory - Excel Online (Business)* → koneksi **Excel Online (Business)** akun kamu.
4. **Import**, tunggu sampai muncul notifikasi sukses.
5. Buka solution **Smart Inventory Flows** > klik flow **Smart Inventory - Bulk Import Read Excel**.
   Jika statusnya **Off**: **Turn on**.

Jika import/turn on gagal dengan pesan tentang **data policy (DLP)**, berarti konektor OneDrive/Excel
diblokir di environment ini; minta admin Power Platform mengizinkan keduanya (kelompok *Business*).

## Langkah 2b – Pilih Drive di aksi Excel (wajib, sekali setelah import)

Drive ID OneDrive berbeda per akun, jadi tidak bisa dibawa di solution. Tanpa langkah ini flow gagal dengan
`WorkflowOperationParametersRuntimeMissingValue ... 'drive'`.

1. Buka flow > **Edit** > aksi **List rows present in a table**.
2. **Location**: *OneDrive for Business* · **Document Library**: *OneDrive*.
3. **File**: klik isian > **Expression (fx)** > `outputs('Create_file')?['body/Id']`.
4. **Table**: **Enter custom value** > `tblImport`.
5. **Save**.

## Update ke v1.0.0.2 (cek isi file + pesan error yang jelas)

Perubahan: flow mengecek dulu isi file dari app. Jika kosong/terlalu pendek, app menerima pesan
*"The app sent no file content. Received: '...'"* (berisi potongan yang diterima, untuk diagnosa).
Isi file boleh data URI (`data:...;base64,...`) atau base64 biasa. Pesan error lain kini menyertakan
alasan asli dari OneDrive/Excel. Input flow tetap sama (`fileContent`), jadi app tidak perlu diubah.

1. make.powerapps.com > **Solutions** > **Import solution** > pilih `SmartInventoryFlows_1_0_0_2.zip` > **Next**
   > **Import** (pilih koneksi yang sama seperti sebelumnya bila diminta).
2. Ulangi **Langkah 2b** (Drive di aksi *List rows present in a table* kosong lagi setelah import).
   Aksi itu sekarang ada di dalam blok **Check file content** > **True**.
3. Pastikan flow **On**. Di Studio: panel **Power Automate** > flow ini > **...** > **Refresh**, lalu **File > Save**.

## Update ke v1.0.0.1 (input File diganti teks)

Kontrol upload di app tidak punya tipe *Blob*, jadi file dikirim sebagai teks base64 (data URI).
Flow yang sudah ter-import (v1.0.0.0) cukup diubah manual, **tanpa import ulang** (pengaturan Drive tetap):

1. Buka flow > **Edit** > klik trigger **When Power Apps calls a flow (V2)**.
2. Hapus input **File** (ikon ... > Delete). Klik **+ Add an input** > **Text**, beri nama `fileContent`.
3. Klik aksi **Create file** > isian **File Content** > hapus isinya > **Expression (fx)** >
   `dataUriToBinary(triggerBody()?['text'])` > **Add/Update**.
4. **Save**.
5. Power Apps Studio > panel **Power Automate** > pada flow ini klik **...** > **Refresh**
   (jika tidak ada: hapus flow dari app lalu **Add flow** lagi). Lalu **File > Save**.

Alternatif: import `SmartInventoryFlows_1_0_0_2.zip` (upgrade), lalu ulangi **Langkah 2b** (Drive kosong lagi) dan langkah 5 di atas.

## Langkah 3 – Tes flow (tanpa app)

1. Di halaman flow: **Test** > **Manually** > **Test**.
2. Tes paling mudah sekarang lewat app (tombol **Upload Excel** di Bulk Import), karena input-nya teks base64.
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
