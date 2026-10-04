# Panduan Melanjutkan Modernisasi App (Digital Inventory)

Kerja dibagi dua, bergantian:
- **WEB** (claude.ai/code, repo `Arthuriant/smart_inventory`): hanya menulis/mengedit file
  (.pa.yaml dan .md). Tidak bisa connect, sync, atau compile ke Power Apps Studio.
- **TERMINAL** (laptop): pull hasil web, connect ke Studio, compile, perbaiki error, push.

Aturan utama: setiap sesi WEB harus diikuti sesi TERMINAL (compile) sebelum sesi WEB
berikutnya, supaya error tidak menumpuk. Kalau kuota terminal sedang tipis, maksimal dua
batch WEB boleh digabung dalam satu sesi TERMINAL.

## Status progress (WAJIB diupdate di akhir setiap sesi, web maupun terminal)
File ini menggantikan memory lokal, karena sesi web tidak bisa membaca memory laptop.

| Langkah | Tempat   | Model  | Isi                                                        | Status |
|---------|----------|--------|------------------------------------------------------------|--------|
| T0      | Terminal | Sonnet | Cek Studio vs file lokal (sync + diff), push               | selesai (digabung di T1) |
| W1      | Web      | Opus   | Tulis 12 brief yang belum ada + terapkan "Before builders" | selesai |
| T1      | Terminal | Sonnet | Pull, compile App/Sidebar/TopBar sampai bersih, push       | selesai |
| W2      | Web      | Sonnet | Build scr_dashboard, Log In, Register                      | selesai |
| T2      | Terminal | Sonnet | Pull, compile + fix W2, push                               | selesai |
| W3      | Web      | Sonnet | Build Template, Area, Add_area                             | selesai |
| T3      | Terminal | Sonnet | Pull, compile + fix W3, push                               | selesai |
| W4      | Web      | Sonnet | Build scr_user, scr_category, scr_frm_category             | belum  |
| T4      | Terminal | Sonnet | Pull, compile + fix W4, push                               | belum  |
| W5      | Web      | Sonnet | Build scr_item, scr_frm_item, scr_find_item                | belum  |
| T5      | Terminal | Sonnet | Pull, compile + fix W5, push                               | belum  |
| W6      | Web      | Opus   | Build scr_Transaction, scr_frm_Transaction, scr_consume    | belum  |
| T6      | Terminal | Opus   | Pull, compile + fix W6, cek logika stok, push              | belum  |
| W7      | Web      | Sonnet | Build scr_History + "After builders" + "Editor State"      | belum  |
| T7      | Terminal | Sonnet | Pull, compile final, validasi, push                        | belum  |

Catatan tambahan (diisi tiap sesi; tulis error yang belum beres atau keputusan penting):
- [W1, 2026-10-04] T0 dilewati, pengecekannya digabung ke T1: sebelum compile, lakukan dulu langkah T0
  (sync Studio ke folder baru, diff dengan app/, laporkan kalau ada perubahan dari Studio), baru compile.
- [W1] File yang ditulis web dan BELUM pernah di-compile: app/App.pa.yaml, app/Components/Sidebar.pa.yaml,
  app/Components/TopBar.pa.yaml (disalin verbatim dari "### Before builders" di canvas-app-plan.md; YAML-nya
  sudah dicek bisa di-parse). Setelah compile T1, jalankan describe_control untuk Sidebar dan TopBar (TopBar
  sekarang punya input `Subtitle`). Menu "Dashboard" di fxMenuItems sengaja masih ke scr_consume (diubah di W7).
  Screen lama masih memakai instance Sidebar/TopBar lama (lebar 180/975, tanpa Subtitle); error/peringatan
  layout di screen yang belum dibangun boleh diabaikan di T1.
- [W1] 12 brief baru: Area, Add_area, scr_user, scr_category, scr_frm_category, scr_item, scr_frm_item,
  scr_Transaction, scr_frm_Transaction, scr_consume, scr_find_item, scr_History (*.screen-plan.md).
  Cek konsistensi 16 brief (dengan skrip) terhadap Dispatch (target file, YAML key, prefix), tabel Cross-Screen
  (activemenu/TopBar/Subtitle), nama control di plan, Action Contracts, dan Mutation Field Ledger: semua cocok.
  Nama control baru unik dan memakai prefix screen masing-masing.
  Satu catatan kecil: brief scr_dashboard menamai control KPI Low/Today lewat pola `...KpiLow...` /
  `...KpiToday...` (contoh: txtDashKpiLowVal); builder W2 cukup mengikuti pola dari baris Items.
- [W1] Keputusan di brief:
  - Toolbar scr_consume pakai ikon reset 36 (shared), bukan 32 (angka budget di plan): 636 <= 832, tetap muat.
  - Kartu daftar scr_user tidak punya toolbar (tidak ada filter di aslinya), jadi tingginya 488.
  - Pilih baris di scr_Transaction / scr_History lewat tombol nomor (btnTrxLOpen / btnHistOpen). Mengklik
    control di dalam baris galeri otomatis memilih baris itu; OnSelect diisi aksi ringan (tutup strip konfirmasi
    / `false`).
  - Delete memakai `With({target: locSelectedRecord}, ...)` + `Errors(<source>)`: receipt hanya muncul kalau
    berhasil; kalau gagal (mis. kategori masih dipakai item) muncul Notify error.
- [W1] Yang perlu dicek saat compile:
  - Add_area: `elv_location_DataCard1.Default: =ThisItem.location` dipertahankan (tidak diubah). Receipt
    memakai `LastSubmit.'elv_location (cr8a3_elv_location)'.Name`, sama dengan kolom galeri Area.
  - Bug lama di luar scope (TIDAK diperbaiki, karena logika form harus tetap sama): di scr_frm_Transaction
    `DataCardValue4.Default` selalu membuat nomor baru, juga saat Edit, sehingga Edit transaksi ikut mengganti
    transaction_number-nya. Putuskan nanti apakah perlu diperbaiki (mis. `If(Form5.Mode = FormMode.New, <rumus>, Parent.Default)`).
- [T1, 2026-10-04] Cek T0 (digabung): Studio di-sync ke folder sementara di luar repo, lalu di-diff dengan app/ versi
  f62ebf2. 18 file .pa.yaml identik (hanya beda line ending; pakai `diff --strip-trailing-cr`). `_EditorState.pa.yaml`
  sengaja di-.gitignore dan sama dengan salinan lokal. Tidak ada perubahan dari Studio. Folder sementara sudah dihapus.
- [T1] Compile app/ (19 file; compile_canvas jalan langsung di app/ walau ada file .md): App.pa.yaml, Sidebar, dan TopBar
  BERSIH. Sisa 4 error + 2 warning, semuanya error baseline di screen lama yang belum dibangun ulang (daftar sama dengan
  canvas-app-requirements.md, kurang satu: error App.OnStart `elv_assigned_area` sudah beres lewat W1):
  - Log In: Button1 `Navigate(HomeAdmin)` dan ButtonUser `Navigate(HomeUser)`; Register: Subtitle2 `elv_assigned_area`.
    Hilang setelah W2/T2.
  - scr_user: warning `locSelectedRecord` Blank() di Button30_4 dan Button33_3. Hilang setelah W4/T4.
  Jangan diperbaiki di screen lama; biar builder yang menulis ulang. Selama diagnostik hanya 6 ini, compile dianggap bersih.
- [T1] describe_control setelah compile: Sidebar punya input `activemenu` (Text, Required); TopBar punya `ActiveMenu` dan
  `Subtitle` (Text, Required). Keduanya `Control: CanvasComponent` + `ComponentName`, tanpa Variant: cocok dengan semua
  brief. app/canvas-discovery-packet.md diupdate (TopBar + Subtitle).
- [T1] Efek samping di Studio (BUKAN edit dari Studio; jangan dianggap drift kalau sync lagi):
  - Sync ulang tidak sama persis dengan app/ karena Studio membuang properti bernilai default saat menulis YAML
    (GroupContainer/Gallery `FillPortions: =1` dan `AlignInContainer: Stretch`, teks/ikon/gambar `FillPortions: =0`, dst.).
    Sudah dicek: tidak ada nilai non-default yang hilang di Sidebar/TopBar, dan App.pa.yaml sama persis.
  - Instance TopBar di 13 screen lama di-reset Studio ke ukuran default komponen baru (Height 80 -> 64, Width
    `App.Width - 150` -> 912) dan mendapat `Subtitle: ""`. Di scr_category dan scr_frm_category, instance Sidebar/TopBar
    juga kehilangan isi `activemenu`/`ActiveMenu` (kosong; Sidebar Width 224). File di app/ TIDAK diubah (tetap sumber
    kebenaran); semua screen ini ditulis ulang di W2-W7 dan tiap builder mengisi input-nya sesuai brief.

- [W2, 2026-10-04] Ditulis web, BELUM pernah di-compile: app/scr_dashboard.pa.yaml (BARU), app/Log In.pa.yaml,
  app/Register.pa.yaml (keduanya ditulis ulang total sesuai brief; semua control lama dihapus, termasuk Button1/ButtonUser
  HomeAdmin/HomeUser dan Subtitle2 elv_assigned_area, jadi 3 error baseline itu harusnya hilang di T2).
  Self-QA: YAML bisa di-parse, root tiap screen hanya con<P>Root, 55/12/18 control dengan nama unik (juga antar file),
  semua properti diawali `=`, nilai yang berisi `: ` di-quote, hanya control/properti dari discovery packet.
  Hal yang perlu diperhatikan di T2:
  - scr_dashboard BELUM ada di Editor State (ScreensOrder diatur di W7); Studio mungkin menaruhnya di urutan terakhir.
  - fxMenuItems "Dashboard" masih ke scr_consume (sesuai plan, diganti di W7). Log In -> scr_dashboard sudah aktif.
  - btnLoginEnter sengaja tanpa Width (AlignInContainer Stretch, LayoutMinWidth 0) supaya selebar kartu.
  - Caption KPI (txtDashKpi*Cap) Height 14 untuk Size 11 mengikuti budget brief (18 + 2 + 36 + 2 + 14 = 72); kalau
    teksnya terpotong di Studio, naikkan ke 16 dan conDashKpi*Txt ke 74.
  - Delegation warning di dashboard (`qty < dis_item_v2.min_qty`, kolom relasi) sudah diterima di brief.

- [T2, 2026-10-04] Compile app/ (20 file) setelah W2: 0 error. 3 error baseline Log In/Register (HomeAdmin, HomeUser,
  elv_assigned_area) hilang. scr_dashboard, Log In, Register bersih tanpa perbaikan, kecuali satu warning:
  `CountRows(dis_item_v2S)` di txtDashKpiItemsVal (Text dan AccessibleLabel) diganti `CountIf(dis_item_v2S, true)` karena
  warning "CountRows may return a cached value". Sisa diagnostik: 2 warning baseline `locSelectedRecord` Blank() di
  scr_user (Button30_4, Button33_3), hilang setelah W4/T4. Tidak ada drift dari Studio yang dicek di T2.
  Catatan: parameter compile_canvas bernama `directoryPath`. Caption KPI Height 14 belum dicek visual di Studio.
- [W3, 2026-10-04] Ditulis web, BELUM pernah di-compile: app/Template.pa.yaml, app/Area.pa.yaml, app/Add_area.pa.yaml
  (ditulis ulang sesuai brief). Self-QA: YAML bisa di-parse, root tiap screen hanya con<P>Root, 8/49/36 control,
  nama unik di semua 6 screen yang sudah dibangun, semua properti diawali `=`.
  - Area: Gallery8_12.Items, dropdown cascade (Items/ItemDisplayText/OnChange/DisplayMode) disalin dari file lama (token
    identik). Bug Delete diperbaiki: icoAreaLDelete menyimpan `locSelectedRecord: ThisItem`; btnAreaLConfirmDel
    `Remove(dis_areas, target)` + receipt gblReceipt "Area" (hanya kalau `Errors(dis_areas)` kosong). Overlay lama
    cntDeleteConfirm dan Button2/Button30_1/Button33_2 dihapus (Button2 -> btnAreaLAdd, OnSelect sama).
  - Add_area: subtree data card Form5_1 disalin apa adanya dari file lama; yang berubah hanya Width tiap card
    (4 card `=Parent.Width / 2`, elv_detail_DataCard2 `=Parent.Width`) dan properti level Form (Height 340, Fill, border,
    AlignInContainer/FillPortions/LayoutMin*, X/Y/Width dihapus, OnSuccess = receipt + 3 statement asli).
    `elv_location_DataCard1.Default: =ThisItem.location` tetap tidak diubah; cek apakah receipt
    `LastSubmit.'elv_location (cr8a3_elv_location)'.Name` compile.
  - Pelajaran T2 dipakai: tidak ada `CountRows(<tabel Dataverse>)` di W3.

- [T3, 2026-10-04] Compile app/ (20 file) setelah W3: 0 error. Template, Area, Add_area bersih tanpa perbaikan
  (termasuk `elv_location_DataCard1.Default: =ThisItem.location` dan receipt `LastSubmit.'elv_location (cr8a3_elv_location)'.Name`
  di Add_area: compile). Sisa diagnostik: 2 warning baseline `locSelectedRecord` Blank() di scr_user (Button30_4, Button33_3),
  hilang setelah W4/T4. Tidak ada drift dari Studio yang dicek di T3; tidak ada file yang diubah selain dokumen status.
  Belum dicek visual di Studio (layout Area galeri/dropdown cascade, Add_area form).

---

## Persiapan sesi WEB
1. Buka https://claude.ai/code, pilih repo `Arthuriant/smart_inventory`, branch `main`.
2. Pilih model sesuai tabel.
3. Salin prompt WEB untuk langkah tersebut (lihat di bawah).
4. Di akhir sesi, pastikan perubahan sudah di-push ke `main`. Kalau web membuat branch
   atau PR terpisah, merge dulu ke `main` di GitHub sebelum sesi terminal.

## Persiapan sesi TERMINAL
1. Buka app di Power Apps Studio (mode edit), URL:
   https://make.powerapps.com/e/c2194d0b-89b3-ed3b-b65a-1db58a779659/canvas/?action=edit&app-id=%2Fproviders%2FMicrosoft.PowerApps%2Fapps%2F87f60c80-e3c1-45bf-ba27-93eb0c079759
2. Terminal:
   cd C:\Project\Powerapps
   git pull
   claude
3. Pilih model sesuai tabel: ketik /model
4. Salin prompt TERMINAL.
5. Jika kuota tinggal ~20%: ketik "stop di titik aman, update status di LANJUTAN-MODERNISASI.md, commit dan push".
6. Jangan edit app di Studio di luar sesi terminal (kalau terpaksa, sebutkan di prompt).

---

## Aturan bersama untuk semua sesi WEB (dibaca otomatis oleh tiap prompt web)
```
ATURAN SESI WEB:
- Kamu berjalan di Claude Code web. Tool Canvas Authoring MCP (connect, sync_canvas,
  compile_canvas, describe_control) TIDAK tersedia. Jangan mencoba connect, sync, atau compile.
- Plugin/skill canvas-apps mungkin tidak terpasang. Kalau tidak ada, kerjakan langsung dengan
  mengikuti app/canvas-app-plan.md, app/canvas-app-shared.md, app/canvas-discovery-packet.md,
  dan brief app/<screen>.screen-plan.md.
- Hanya pakai control, variant, dan properti yang tercantum di app/canvas-discovery-packet.md
  atau yang sudah ada di file .pa.yaml saat ini. Jangan mengarang nama properti.
- Satu screen = satu file app/<screen>.pa.yaml. Jangan sentuh file screen di luar daftar sesi ini.
- Lakukan self-QA manual sesuai checklist di brief dan canvas-app-shared.md (nama control unik,
  referensi ke control/data source/variabel valid, indentasi YAML benar).
- Akhiri dengan: update tabel "Status progress" dan "Catatan tambahan" di
  LANJUTAN-MODERNISASI.md (tandai "selesai, belum compile"), lalu commit dan push ke main.
```

---

## T0 (Terminal, Sonnet): cek awal, cukup sekali
```
Ini langkah T0 dari C:\Project\Powerapps\LANJUTAN-MODERNISASI.md. Gunakan skill canvas-apps:canvas-app.
1. Connect ke app (environment c2194d0b-89b3-ed3b-b65a-1db58a779659,
   app 87f60c80-e3c1-45bf-ba27-93eb0c079759, login ARianto2@slb.com).
2. Sync ke folder BARU (bukan app/, karena berisi file .md), lalu diff dengan
   C:\Project\Powerapps\app. Jika ada perubahan dari Studio, laporkan ke saya dulu.
3. Jika sama, hapus folder sync sementara. Update status T0 jadi "selesai", commit, push.
```

## W1 (Web, Opus): lengkapi brief + Before builders
```
Baca LANJUTAN-MODERNISASI.md (bagian Status dan ATURAN SESI WEB) lalu kerjakan langkah W1.
Patuhi semua poin ATURAN SESI WEB di file tersebut.

1. Tulis HANYA 12 brief yang belum ada, sebagai app/<screen>.screen-plan.md, dengan format dan
   tingkat detail yang sama seperti app/scr_dashboard.screen-plan.md dan app/Log In.screen-plan.md:
   Area, Add_area, scr_user, scr_category, scr_frm_category, scr_item, scr_frm_item,
   scr_Transaction, scr_frm_Transaction, scr_consume, scr_find_item, scr_History.
   Baca file .pa.yaml asli tiap screen sebagai dasar. Jangan tulis ulang canvas-app-plan.md,
   canvas-app-shared.md, atau 4 brief yang sudah ada.
2. Cek konsistensi 16 brief terhadap canvas-app-plan.md (bagian Dispatch, Action Contracts,
   Mutation Field Ledger) dan canvas-app-shared.md.
3. Terapkan "### Before builders" dari app/canvas-app-plan.md ke app/App.pa.yaml,
   app/Components/Sidebar.pa.yaml, app/Components/TopBar.pa.yaml (YAML final ada di plan).
4. JANGAN build screen. Update status, commit, push.
```

## T1..T7 (Terminal): compile setelah batch web
Ganti [N] dan daftar screen sesuai tabel. Untuk T6 pakai Opus.
```
Ini langkah T[N] dari C:\Project\Powerapps\LANJUTAN-MODERNISASI.md. Gunakan skill canvas-apps:canvas-app.
Saya sudah git pull. File berikut baru ditulis di sesi web dan BELUM pernah di-compile:
[daftar file dari langkah W sebelumnya].

1. Connect ke app (environment c2194d0b-89b3-ed3b-b65a-1db58a779659,
   app 87f60c80-e3c1-45bf-ba27-93eb0c079759, login ARianto2@slb.com).
2. Compile app/ dan perbaiki error sampai bersih. Error di screen yang memang belum dibangun
   boleh diabaikan. Pakai describe_control bila ada properti yang tidak valid.
3. Update status langkah W dan T ini jadi "selesai", isi Catatan tambahan, update memory
   canvas-modernize-progress, lalu commit dan push ke main. Beri ringkasan singkat.
```
Tambahan khusus T6: "Bandingkan Form5.OnSuccess sebelum dan sesudah; logika update stok
Receive/Consume/Transfer harus identik. Pastikan bug Consume sudah beres."
Tambahan khusus T7: "Jalankan ValidationWorkflow, compile final, lalu beri daftar hal yang
perlu saya cek manual di Studio."

## W2..W5, W7 (Web): build screen
Ganti [N] dan daftar screen sesuai tabel.
```
Baca LANJUTAN-MODERNISASI.md (bagian Status dan ATURAN SESI WEB) lalu kerjakan langkah W[N].
Patuhi semua poin ATURAN SESI WEB di file tersebut.

Pastikan langkah T sebelumnya sudah "selesai" di tabel status. Kalau belum, berhenti dan beri tahu saya.
Build screen berikut sesuai brief masing-masing (app/<screen>.screen-plan.md) dan
canvas-app-shared.md: [daftar screen dari tabel].
Khusus W7: setelah scr_History, terapkan juga "### After builders" dan
"## Editor State Changes" dari app/canvas-app-plan.md.
Update status, commit, push.
```

## W6 (Web, Opus): screen transaksi
```
Baca LANJUTAN-MODERNISASI.md (bagian Status dan ATURAN SESI WEB) lalu kerjakan langkah W6.
Patuhi semua poin ATURAN SESI WEB di file tersebut.

Pastikan T5 sudah "selesai". Build scr_Transaction, scr_frm_Transaction, scr_consume sesuai brief.
PENTING:
- Form5.OnSuccess (rewrite detail + update stok Receive/Consume/Transfer) harus sama persis
  dengan aslinya. Salin formula asli dulu ke Catatan tambahan, lalu bandingkan setelah edit.
- Perbaikan bug Consume: header berisi type Consume dan area_form; qty > stok diblokir.
Update status, commit, push.
```
