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
| T0      | Terminal | Sonnet | Cek Studio vs file lokal (sync + diff), push               | belum  |
| W1      | Web      | Opus   | Tulis 12 brief yang belum ada + terapkan "Before builders" | belum  |
| T1      | Terminal | Sonnet | Pull, compile App/Sidebar/TopBar sampai bersih, push       | belum  |
| W2      | Web      | Sonnet | Build scr_dashboard, Log In, Register                      | belum  |
| T2      | Terminal | Sonnet | Pull, compile + fix W2, push                               | belum  |
| W3      | Web      | Sonnet | Build Template, Area, Add_area                             | belum  |
| T3      | Terminal | Sonnet | Pull, compile + fix W3, push                               | belum  |
| W4      | Web      | Sonnet | Build scr_user, scr_category, scr_frm_category             | belum  |
| T4      | Terminal | Sonnet | Pull, compile + fix W4, push                               | belum  |
| W5      | Web      | Sonnet | Build scr_item, scr_frm_item, scr_find_item                | belum  |
| T5      | Terminal | Sonnet | Pull, compile + fix W5, push                               | belum  |
| W6      | Web      | Opus   | Build scr_Transaction, scr_frm_Transaction, scr_consume    | belum  |
| T6      | Terminal | Opus   | Pull, compile + fix W6, cek logika stok, push              | belum  |
| W7      | Web      | Sonnet | Build scr_History + "After builders" + "Editor State"      | belum  |
| T7      | Terminal | Sonnet | Pull, compile final, validasi, push                        | belum  |

Catatan tambahan (diisi tiap sesi; tulis error yang belum beres atau keputusan penting):
- (kosong)

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
