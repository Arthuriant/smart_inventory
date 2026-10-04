# Panduan Melanjutkan Modernisasi App (Digital Inventory)

## Persiapan SETIAP sesi
1. Buka app di Power Apps Studio (mode edit), URL:
   https://make.powerapps.com/e/c2194d0b-89b3-ed3b-b65a-1db58a779659/canvas/?action=edit&app-id=%2Fproviders%2FMicrosoft.PowerApps%2Fapps%2F87f60c80-e3c1-45bf-ba27-93eb0c079759
2. Terminal:
   cd C:\Project\Powerapps
   claude
3. Pilih model sesuai tabel di bawah: ketik /model
4. Salin prompt sesi tersebut.
5. Jika kuota tinggal ~20%: ketik "stop di titik aman dan update memory".
6. Jangan edit app di Studio di antara sesi (kalau terpaksa, sebutkan di prompt).

| Sesi | Model  | Isi |
|------|--------|-----|
| 1    | Opus   | Lengkapi 12 brief + App/Sidebar/TopBar |
| 2    | Sonnet | scr_dashboard, Log In, Register |
| 3    | Sonnet | Template, Area, Add_area |
| 4    | Sonnet | scr_user, scr_category, scr_frm_category |
| 5    | Sonnet | scr_item, scr_frm_item, scr_find_item |
| 6    | Opus   | scr_Transaction, scr_frm_Transaction, scr_consume (logika stok) |
| 7    | Sonnet | scr_History + perubahan akhir + validasi akhir |

---

## SESI 1 (Opus)
```
Lanjutkan modernisasi canvas app sesuai memory canvas-modernize-progress dan file
C:\Project\Powerapps\LANJUTAN-MODERNISASI.md. Ini SESI 1. Gunakan skill canvas-apps:canvas-app.

1. Connect ulang ke app (environment c2194d0b-89b3-ed3b-b65a-1db58a779659,
   app 87f60c80-e3c1-45bf-ba27-93eb0c079759, login ARianto2@slb.com).
2. Sync ke folder BARU (bukan app/, karena berisi file .md), lalu diff dengan
   C:\Project\Powerapps\app. Jika ada perubahan dari Studio, laporkan ke saya dulu.
3. Jalankan planner HANYA untuk 12 brief yang belum ada (Area, Add_area, scr_user,
   scr_category, scr_frm_category, scr_item, scr_frm_item, scr_Transaction,
   scr_frm_Transaction, scr_consume, scr_find_item, scr_History). Jangan tulis ulang
   canvas-app-plan.md, canvas-app-shared.md, atau 4 brief yang sudah ada.
4. Lakukan pengecekan pre-dispatch sesuai skill untuk semua 16 brief.
5. Terapkan "### Before builders" dari canvas-app-plan.md (App.pa.yaml, Sidebar, TopBar),
   lalu compile sampai tidak ada error level App.
6. JANGAN jalankan builder screen di sesi ini. Berhenti, update memory, dan beri
   ringkasan singkat.
```

## SESI 2 (Sonnet)
```
Lanjutkan modernisasi canvas app sesuai memory canvas-modernize-progress dan
C:\Project\Powerapps\LANJUTAN-MODERNISASI.md. Ini SESI 2. Gunakan skill canvas-apps:canvas-app
(Planned Build Handoff).

Connect ulang ke app. Jalankan builder (maksimal 3 sekaligus) untuk: scr_dashboard,
Log In, Register. Cek laporan QA tiap builder sesuai skill, lalu compile sampai bersih.
Error compile di screen yang belum dibangun boleh diabaikan bila memang menunggu sesi berikutnya.
Berhenti setelah itu, update memory (screen mana yang selesai), dan beri ringkasan singkat.
```

## SESI 3 / 4 / 5 (Sonnet), ganti nomor sesi dan daftar screen
```
Lanjutkan modernisasi canvas app sesuai memory canvas-modernize-progress dan
C:\Project\Powerapps\LANJUTAN-MODERNISASI.md. Ini SESI [3/4/5]. Gunakan skill
canvas-apps:canvas-app (Planned Build Handoff).

Connect ulang ke app. Jalankan builder untuk: [daftar 3 screen dari tabel].
Cek laporan QA tiap builder, compile sampai bersih, lalu berhenti, update memory,
dan beri ringkasan singkat.
```

## SESI 6 (Opus)
```
Lanjutkan modernisasi canvas app sesuai memory canvas-modernize-progress dan
C:\Project\Powerapps\LANJUTAN-MODERNISASI.md. Ini SESI 6. Gunakan skill
canvas-apps:canvas-app (Planned Build Handoff).

Connect ulang ke app. Jalankan builder untuk: scr_Transaction, scr_frm_Transaction,
scr_consume. PENTING:
- Form5.OnSuccess (rewrite detail + update stok Receive/Consume/Transfer) harus sama
  persis dengan aslinya. Bandingkan formula sebelum dan sesudah.
- Perbaikan bug Consume: header berisi type Consume dan area_form; qty > stok diblokir.
Cek laporan QA, compile sampai bersih, lalu berhenti, update memory, dan beri ringkasan.
```

## SESI 7 (Sonnet), penutup
```
Lanjutkan modernisasi canvas app sesuai memory canvas-modernize-progress dan
C:\Project\Powerapps\LANJUTAN-MODERNISASI.md. Ini SESI 7 (terakhir). Gunakan skill
canvas-apps:canvas-app.

Connect ulang ke app. Jalankan builder untuk scr_History. Lalu terapkan
"### After builders" dan "## Editor State Changes" dari canvas-app-plan.md, jalankan
ValidationWorkflow, dan compile final sampai bersih. Beri ringkasan semua perubahan
dan apa yang perlu saya cek manual di Studio.
```
