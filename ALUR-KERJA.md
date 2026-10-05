# Alur Kerja Harian (setelah modernisasi selesai)

Modernisasi W1-T7 sudah selesai (riwayatnya ada di LANJUTAN-MODERNISASI.md, tidak perlu dibaca lagi kecuali butuh konteks).
Mulai sekarang setiap permintaan cukup dua langkah:

- **WEB** (claude.ai/code, repo `Arthuriant/smart_inventory`, branch `main`, model Opus): kerja berat. Membaca kode,
  menganalisis, menulis/mengedit file `.pa.yaml`. Tidak bisa compile.
- **TERMINAL** (laptop, `C:\Project\Powerapps`, model Sonnet): kerja ringan. Pull, compile, Save, push.
  Perbaikan di terminal hanya untuk error compile yang kecil dan jelas (salah ketik nama, properti tidak valid).
  Kalau perlu analisis atau desain ulang, terminal mencatat masalahnya di Log dan kembali ke WEB.

Setiap WEB yang mengubah `.pa.yaml` harus diikuti TERMINAL sebelum WEB berikutnya.

---

## Prompt WEB (salin, ganti bagian dalam kurung)

```
Baca ALUR-KERJA.md (bagian Aturan WEB dan Log) lalu kerjakan:
[tulis permintaan di sini, mis. "tombol Simpan di scr_frm_item tidak muncul, ini deskripsinya: ..."]
Patuhi Aturan WEB. Di akhir: tambah satu entri di Log, commit, push ke main.
```

## Prompt TERMINAL (salin apa adanya)

```
Baca ALUR-KERJA.md (bagian Aturan TERMINAL dan Log) lalu jalankan langkah terminal untuk entri Log terakhir
yang statusnya "belum compile". Gunakan skill canvas-apps:canvas-app hanya untuk connect/compile.
```

Kalau tidak ada perubahan file dan hanya mau bertanya/cek sesuatu di Studio, cukup tulis pertanyaannya biasa.

---

## Aturan WEB

- Tool Canvas Authoring MCP (connect, sync, compile, describe_control) TIDAK tersedia di web. Jangan mencoba.
- Konteks app: app/canvas-app-plan.md, app/canvas-app-shared.md, app/canvas-discovery-packet.md, dan
  app/<screen>.screen-plan.md. Hanya pakai control/properti yang ada di discovery packet atau di file .pa.yaml sekarang.
- Wajib ikuti "KOREKSI WAJIB" #1-#7 di app/canvas-app-shared.md (warna literal RGBA, instance komponen Stretch,
  form gaya asli, control yang dibuat ulang diberi nama baru, filter Dataverse dengan konstanta, tanpa ModernIcon dan
  container bersarang di baris galeri). **#8 TIDAK berlaku**: ganti ComboBox ke ModernCombobox sudah dicoba dan
  di-revert (merusak layout form). Jangan ubah tipe control di dalam form.
- Tabel hitam / dropdown form tidak bisa memilih = gejala "binding" Studio, BUKAN kesalahan YAML. Jangan ubah struktur
  YAML untuk gejala ini; tulis di Log agar user mengetik ulang rumus Fill / menghapus "Depends on" di Studio.
- Nama control unik di seluruh app. Kalau mengganti nama, ganti juga semua referensi lintas screen.
- Logika data (OnSuccess form, Patch stok Receive/Consume/Transfer) jangan diubah kecuali memang diminta.
- Self-QA sebelum commit: YAML bisa di-parse, nama control unik, semua properti diawali `=`, tanpa `clr*`, tanpa CR.
- Kalau info kurang (mis. "layout rusak" tanpa detail), tulis pertanyaan spesifik di Log dan jangan menebak.
- Akhiri dengan entri Log (format di bawah), commit, push ke main.

## Aturan TERMINAL

1. Studio terbuka dalam mode edit di SATU tab (URL di bawah). `git pull`.
2. Connect: environment `c2194d0b-89b3-ed3b-b65a-1db58a779659`, app `87f60c80-e3c1-45bf-ba27-93eb0c079759`,
   login `ARianto2@slb.com`.
3. `compile_canvas` dengan `directoryPath` = `C:\Project\Powerapps\app` (jangan `sync_canvas` ke app/; kalau perlu
   sync, pakai folder sementara lalu hapus).
4. Error kecil dan jelas: perbaiki lalu compile ulang. Error yang butuh analisis: jangan dikejar, catat di Log
   (nama control + properti + pesan error) untuk WEB.
5. Ingatkan user: tunggu Studio tampil (sering putih sebentar), JANGAN refresh, cek gejala "binding" di screen yang
   berubah, lalu File > Save.
6. Ubah status entri Log jadi "compile OK" (atau "compile gagal: ..."), commit, push. Jawab singkat.

URL Studio (mode edit):
https://make.powerapps.com/e/c2194d0b-89b3-ed3b-b65a-1db58a779659/canvas/?action=edit&app-id=%2Fproviders%2FMicrosoft.PowerApps%2Fapps%2F87f60c80-e3c1-45bf-ba27-93eb0c079759

---

## Log (entri terbaru di bawah)

Format: `- [tanggal, WEB/TERMINAL] file yang diubah | ringkasan | status: belum compile / compile OK / compile gagal: ... | cek manual di Studio: ...`

- [2026-10-05, TERMINAL] (tidak ada perubahan .pa.yaml) | Penutupan modernisasi: compile T7 bersih, sesi Studio sama
  dengan repo (beda hanya format tulis Studio). | status: compile OK | cek manual di Studio yang masih terbuka:
  gejala "binding" (Fill baris galeri, Depends on dropdown form), uji stok Receive 3 / Consume 2 / qty > stok,
  menu Dashboard, filter History, File > Save. Masalah terbuka: layout form scr_frm_item rusak (butuh deskripsi
  atau screenshot dari user: bagian mana yang salah, nama control di Tree view).
