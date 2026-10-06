# Alur Kerja Harian (full terminal)

Modernisasi W1-T7 sudah selesai (riwayatnya ada di LANJUTAN-MODERNISASI.md, tidak perlu dibaca lagi kecuali butuh konteks).
Mulai 2026-10-06 semua pekerjaan dilakukan di **TERMINAL** (Claude Code di laptop, `C:\Project\Powerapps`):
membaca kode, menganalisis, mengedit `.pa.yaml`, compile, sampai commit dan push. Pembagian WEB/TERMINAL yang lama
tidak berlaku lagi.

---

## Prompt (salin, ganti bagian dalam kurung)

```
Baca ALUR-KERJA.md (Aturan dan Log) lalu kerjakan:
[tulis permintaan di sini, mis. "tombol Simpan di scr_frm_item tidak muncul, ini deskripsinya: ..."]
```

Kalau tidak ada perubahan file dan hanya mau bertanya/cek sesuatu di Studio, cukup tulis pertanyaannya biasa.

---

## Aturan

### Persiapan
1. Studio terbuka dalam mode edit di SATU tab (URL di bawah). `git pull`.
2. Connect: environment `c2194d0b-89b3-ed3b-b65a-1db58a779659`, app `87f60c80-e3c1-45bf-ba27-93eb0c079759`,
   login `ARianto2@slb.com`.
3. Sebelum mengedit: `sync_canvas` ke folder sementara baru (mis. scratchpad `studio`, JANGAN ke app/) dan bandingkan
   dengan app/ (`diff -r --strip-trailing-cr`). Kalau user mengubah sesuatu manual di Studio, salin dulu file itu ke
   app/ supaya tidak tertimpa.

### Mengedit
- Konteks app: app/canvas-app-plan.md, app/canvas-app-shared.md, app/canvas-discovery-packet.md, dan
  app/<screen>.screen-plan.md. Kalau ragu soal control/properti, cek dengan `describe_control`.
- Wajib ikuti "KOREKSI WAJIB" #1-#7 di app/canvas-app-shared.md (warna literal RGBA, instance komponen Stretch,
  form gaya asli, control yang dibuat ulang diberi nama baru, filter Dataverse dengan konstanta, tanpa ModernIcon dan
  container bersarang di baris galeri). **#8 TIDAK berlaku**: ganti ComboBox ke ModernCombobox sudah dicoba dan
  di-revert (merusak layout form). Jangan ubah tipe control di dalam form.
- Tabel hitam / dropdown form tidak bisa memilih = gejala "binding" Studio, BUKAN kesalahan YAML. Jangan ubah struktur
  YAML untuk gejala ini; minta user mengetik ulang rumus Fill / menghapus "Depends on" di Studio.
- Nama control unik di seluruh app. Kalau mengganti nama, ganti juga semua referensi lintas screen.
- Jangan pakai `Select(Parent)` di control dalam container baris galeri. ModernText tidak punya `Tooltip`.
- Logika data (OnSuccess form, Patch stok Receive/Consume/Transfer) jangan diubah kecuali memang diminta.
- Kalau info kurang (mis. "layout rusak" tanpa detail), tanya user dulu, jangan menebak.

### Compile
1. JANGAN compile langsung `app/`. Compile mengirim SEMUA file ke Studio; teks repo bisa beda format dengan Studio,
   jadi setiap screen dibangun ulang dan tabel yang sudah dibetulkan user jadi hitam lagi (gejala "binding"). Caranya:
   a. Pakai folder sementara hasil sync (langkah Persiapan #3).
   b. Salin ke folder itu HANYA file `.pa.yaml` yang diubah.
   c. `compile_canvas` dengan `directoryPath` = folder sementara itu.
   d. Error compile: perbaiki di app/, salin ulang, compile lagi sampai bersih.
   e. Hapus folder sementara setelah selesai.
2. Ingatkan user: tunggu Studio tampil (sering putih sebentar), JANGAN refresh, cek gejala "binding" di screen yang
   berubah, lalu File > Save.

### Penutup
- Tambah satu entri di Log, commit, push ke main. Jawab singkat.

URL Studio (mode edit):
https://make.powerapps.com/e/c2194d0b-89b3-ed3b-b65a-1db58a779659/canvas/?action=edit&app-id=%2Fproviders%2FMicrosoft.PowerApps%2Fapps%2F87f60c80-e3c1-45bf-ba27-93eb0c079759

---

---

## Log (entri terbaru di bawah)

Format: `- [tanggal] file yang diubah | ringkasan | status: belum compile / compile OK / compile gagal: ... | cek manual di Studio: ...`

- [2026-10-05, TERMINAL] (tidak ada perubahan .pa.yaml) | Penutupan modernisasi: compile T7 bersih, sesi Studio sama
  dengan repo (beda hanya format tulis Studio). | status: compile OK | cek manual di Studio yang masih terbuka:
  gejala "binding" (Fill baris galeri, Depends on dropdown form), uji stok Receive 3 / Consume 2 / qty > stok,
  menu Dashboard, filter History, File > Save. Masalah terbuka: layout form scr_frm_item rusak (butuh deskripsi
  atau screenshot dari user: bagian mana yang salah, nama control di Tree view).
- [2026-10-05, WEB] app/scr_consume.pa.yaml, app/scr_consume.screen-plan.md | Consume pakai foto: thumbnail
  `imgConsItem` 56x56 (dis_item_v2.Image) di tiap baris + header "FOTO", baris 72; filter Geounit/Location/Area
  otomatis terisi dari Assigned_area user (Default ddConsGeo/ddConsLoc/ddConsArea); qty terkunci untuk stok 0; tombol
  `btnConsClear` "Kosongkan" di footer. Logika Patch Consume tidak diubah. | status: compile OK (lihat entri TERMINAL di bawah) | cek manual di
  Studio: foto muncul di baris (item tanpa foto = kotak abu), baris tidak hitam; buka screen sebagai user yang punya
  Assigned_area -> 3 dropdown langsung terisi dan tombol Consume aktif setelah isi qty; ganti Geounit -> Location/Area
  ikut kosong; tombol Kosongkan dan setelah Consume qty kembali 0 (kalau qty tidak kembali 0, catat di Log).
- [2026-10-05, TERMINAL] app/scr_consume.pa.yaml | Compile entri WEB Consume foto: 1 error
  `imgConsItem.OnSelect = Select(Parent)` (Parent = GroupContainer conConsRow, tanpa OnSelect). Diperbaiki: OnSelect
  dihapus (foto hanya tampilan). Catatan untuk WEB: jangan pakai Select(Parent) di control dalam container baris
  galeri. | status: compile OK | cek manual di Studio: sama dengan entri WEB di atas, lalu File > Save.
- [2026-10-05, TERMINAL] app/scr_consume.pa.yaml, app/scr_consume.screen-plan.md, ALUR-KERJA.md | (1) Sebab tabel
  hitam lagi: compile `app/` mengirim semua 20 file, semuanya beda format dengan Studio, jadi Studio membangun ulang
  semua screen (termasuk Area yang sudah dibetulkan user). Aturan TERMINAL #3 diganti: sync Studio ke folder
  sementara, salin hanya file yang berubah, compile folder itu. (2) Consume jadi grid kartu ala online shop: galCons
  WrapCount 4, kartu 346 tinggi (foto 176 penuh lebar kartu, nama 2 baris, badge "Stok n uom", BPN · area, qty,
  peringatan), header kolom conConsHead dihapus, galeri 720 tinggi (2 baris kartu), conConsCard 876. Nama control
  dan logika Consume/Kosongkan tidak berubah; kartu ber-border biru kalau qty > 0. | status: compile OK (cara baru)
  | cek manual di Studio: Area tetap normal; kartu Consume tidak hitam (kalau hitam: ketik ulang Fill conConsRow),
  foto besar, isi qty -> border biru, Consume & Kosongkan jalan; lalu File > Save.
- [2026-10-05, TERMINAL] semua app/*.pa.yaml (+ Components) | Repo disamakan dengan Studio setelah user membetulkan
  dropdown ("Depends on") dan warna hitam (ketik ulang Fill) secara manual: hasil `sync_canvas` disalin ke app/.
  Mulai sekarang file di app/ memakai format tulis Studio (properti default tidak ditulis, rumus panjang jadi string
  satu baris dengan \n). Itu normal; WEB tetap boleh menulis gaya biasa. | status: compile OK (repo = sesi Studio)
  | cek manual di Studio: pastikan sudah File > Save.
- [2026-10-06] ALUR-KERJA.md | Alur kerja diganti jadi full terminal (tidak ada lagi pembagian WEB/TERMINAL). Sync
  Studio dicek: app/ sudah identik dengan sesi Studio. | status: tidak ada perubahan .pa.yaml | cek manual di Studio: -
- [2026-10-06] app/scr_consume.pa.yaml | Kotak qty Consume diperbesar: numConsQty tinggi 32 -> 48, huruf 13 -> 16;
  foto imgConsItem 176 -> 160 supaya tinggi kartu (346) dan grid 2 baris tetap. | status: compile OK | cek manual di
  Studio: kartu Consume tidak hitam (kalau hitam: ketik ulang Fill conConsRow), qty lebih besar, lalu File > Save.
- [2026-10-06] app/scr_consume.pa.yaml | Panel bukti "Consume tersimpan" (conConsReceipt + galConsReceipt) dihapus,
  beserta colConsumeReceipt / locConsHeader / locShowConsReceipt di btnConsSubmit. Simpan header, detail, dan
  pengurangan stok tidak berubah; toast hijau tetap ada. | status: compile OK | cek manual di Studio: Consume 1 item ->
  tidak ada panel bukti, stok berkurang, qty kembali 0; kartu tidak hitam; lalu File > Save.
- [2026-10-06] app/scr_find_item.pa.yaml | Tombol "Detail" (btnFindDetail, ModernButton Subtle + ikon Info) di kolom
  baru AKSI tiap baris galFind; menekannya membuka overlay conFindDetOverlay (locFindDetail = baris stok,
  locShowFindDetail) berisi foto, nama, badge stok/status, deskripsi, BPN/SPN/Kategori/UOM/Min. stok dan
  Geounit/Location/Area/Stok/Diperbarui; tutup lewat X atau tombol Tutup, direset di OnVisible. | status: compile OK |
  cek manual di Studio: baris galFind tidak hitam (gejala "binding"), klik Detail -> panel muncul di tengah dengan
  data yang benar, Tutup berfungsi; lalu File > Save.
- [2026-10-06] 16 screen + Components/Sidebar + Components/TopBar (semua kecuali App.pa.yaml) | Standarisasi bahasa
  Inggris: semua teks UI (label, judul, placeholder, tombol, AccessibleLabel/Tooltip, Notify, isi gblReceipt) dari
  Indonesia ke Inggris lewat peta terjemahan string literal; locale tanggal "id-ID" -> "en-US" (TopBar, Dashboard).
  Komentar // di rumus tidak diubah. Log In.pa.yaml lebih dulu disalin dari Studio (teks tagline yang diubah user).
  Nama control, kolom, dan logika tidak berubah. | status: compile OK | cek manual di Studio: karena semua screen
  dikirim ulang, gejala "binding" bisa muncul di SEMUA galeri/dropdown form (ketik ulang Fill baris, hapus
  "Depends on"); cek teks yang terpotong karena lebih panjang; lalu File > Save.
- [2026-10-06] app/scr_user.pa.yaml | Multi-area per user: pemilih `cmbUsrLAreas` (ModernCombobox SelectMultiple, di
  luar form, Items dis_areas, default = relasi N:N 'dis_areas (cr8a3_elv_dis_user_elv_dis_area_elv_dis_area)') di
  panel Edit User (tinggi 400). frmUsrL.OnSuccess menyamakan relasi N:N dengan pilihan (Unrelate yang dibuang, Relate
  yang baru; Primary area/Assigned_area selalu ikut), lalu Refresh(dis_users). Card Assigned_area diberi label
  "Primary area"; kolom daftar jadi AREAS (Concat semua area, fallback Assigned_area). Belum ada pembatasan akses
  (RBAC) - ini fondasinya. | status: compile OK | cek manual di Studio: baris galUsrL tidak hitam, dropdown form tidak
  kosong ("Depends on"), Edit user -> pilih 2-3 area -> Save -> kolom AREAS tampil semua; buang satu area -> Save ->
  hilang; lalu File > Save.
- [2026-10-06] app/App.pa.yaml, app/scr_consume.pa.yaml, app/scr_find_item.pa.yaml, app/scr_frm_Transaction.pa.yaml,
  app/scr_Transaction.pa.yaml | RBAC Administrator vs User (role selain administrator = user). App.Formulas baru:
  nfIsAdmin, nfMyAreas (relasi N:N user-area), nfHomeArea (Primary area, fallback area pertama), nfMyAreaIds,
  nfMyLocIds, nfMyGeoIds. fxMenuItems diberi kolom AdminOnly dan disaring: user tidak melihat Category Item, Item, Area,
  User. Consume & Find Item: dropdown Geounit/Location/Area user hanya berisi miliknya; Geounit & Location otomatis
  terisi dari nfHomeArea dan terkunci (kalau area user tersebar di >1 location/geounit, dropdown itu tetap bisa dipilih
  tapi hanya opsi miliknya); galeri stok user hanya area miliknya. Transaction form: From hanya area user; To hanya
  area user kalau tipe Receive (Transfer tetap boleh ke area mana saja). Tombol Delete transaksi hanya untuk admin.
  Admin tidak berubah. Catatan: Navigate di OnVisible ditolak compiler, jadi pembatasan screen admin lewat menu saja
  (tidak ada link lain ke screen admin dari screen user). | status: compile OK | cek manual di Studio: galeri Consume /
  Find / Transaction tidak hitam, dropdown form Transaction tidak kosong ("Depends on"); uji sebagai user: menu hanya 5,
  Geounit/Location terisi & abu-abu, Area hanya area yang di-assign; lalu File > Save.
- [2026-10-06] app/scr_geoloc.pa.yaml (baru), app/App.pa.yaml | Screen baru "Geounit & Location" (scr_geoloc, prefix Gl,
  menu admin-only, ikon Globe, di atas Area): kartu kiri = tabel Geounit (SHORT, LONG NAME, Edit/Delete/Show), kartu
  kanan = Location dari geounit yang dipilih di kiri (galGlLoc filter galGlGeo.Selected). Tambah/edit lewat panel inline
  di atas tabel (Patch, tanpa Form): geounit = short + long name (cek duplikat short name), location = nama + dropdown
  geounit (bisa pindah geounit). Delete pakai bar konfirmasi; geounit ditolak kalau masih punya location / dipakai area,
  location ditolak kalau masih dipakai area. Receipt hijau gblReceipt.Screen = "GeoLoc". | status: compile OK (screen
  terverifikasi ada di sesi Studio) | cek manual di Studio: baris galeri tidak hitam (ketik ulang Fill conGlGeoRow /
  conGlLocRow), klik geounit -> kanan ganti, Add/Edit/Delete kedua sisi, ikon menu muncul; lalu File > Save.
- [2026-10-06] app/App.pa.yaml, app/scr_consume.pa.yaml, app/scr_find_item.pa.yaml, app/Area.pa.yaml,
  app/Add_area.pa.yaml, app/scr_geoloc.pa.yaml | Fix dropdown Geounit/Location/Area kosong sejak RBAC. Penyebab (dicek
  di Dataverse via pac): dis_areas punya 2 lookup lokasi - `location` (elv_location, terisi 24/27 area, data lama) dan
  'elv_location (cr8a3_elv_location)' (terisi 4/27, area baru) - dan app hanya memakai yang kedua, sehingga
  nfMyLocIds/nfMyGeoIds berisi blank. Data Dataverse TIDAK diubah (keputusan user); logika saja: lokasi efektif =
  Coalesce(location, cr8a3) (nfHomeLoc baru, nfMyLocIds/nfMyGeoIds buang blank), filter area per lokasi =
  location match Or (IsBlank(location) And cr8a3 match), dropdown RBAC jadi If(nfIsAdmin, semua, Filter(...)).
  Add_area kini menulis ke `location`. Lokasi CIB belum punya geounit (dibiarkan, data). | status: compile OK, 35
  warning delegasi di filter dis_areas (IsBlank lookup; aman selama dis_areas < 500 baris) | cek manual di Studio:
  dropdown Consume/Find/Area tidak kosong ("Depends on"), galeri tidak hitam; lalu File > Save.
