# Canvas App Shared Plan

## KOREKSI WAJIB (W4, setelah uji visual di Studio) - berlaku di atas semua aturan dan brief di bawah

Hasil W2/W3 compile bersih tetapi tampilannya rusak di Studio: TopBar hanya ~500 px, Sidebar hanya ~220 px tinggi,
baris galeri dan Form hitam, tombol Primary ungu (BasePaletteColor default). Aturan pengganti:

1. **Warna = literal `RGBA(...)`**, jangan pakai nama `clr*` di properti control (screen maupun komponen). Nilainya tetap
   sesuai tabel palet di bawah (clrNavy -> `RGBA(0, 18, 107, 1)`, dst.). Named formula `clr*` di App.Formulas boleh tetap
   ada, tapi tidak dipakai.
2. **Instance komponen di Shell**: `cmp<P>Sidebar` pakai `AlignInContainer: =AlignInContainer.Stretch` dan `Height: =640`
   (bukan `=Parent.Height`); `cmp<P>TopBar` pakai `AlignInContainer: =AlignInContainer.Stretch` dan `Width: =912`
   (bukan `=Parent.Width`). Ukuran instance komponen dari rumus `Parent.*` tidak diterapkan di dalam AutoLayout.
3. **Form yang dipertahankan**: ikuti gaya form asli yang dulu tampil benar: `Width: =Parent.Width`, `FillPortions: =0`,
   `Height` dari brief; JANGAN set `Fill`, `BorderThickness`, `AlignInContainer`, `LayoutMin*` di level Form.
4. Baris galeri: `Fill: =If(ThisItem.IsSelected, RGBA(232, 238, 252, 1), RGBA(255, 255, 255, 1))`; galeri
   `Fill: =RGBA(226, 230, 239, 1)`.
5. **JANGAN pertahankan nama control lama** (koreksi W4b; menggantikan semua kalimat "keep name" / "(kept)" di brief).
   Control yang namanya dipakai ulang di struktur baru tampil dengan properti default di Studio (form "isn't connected
   to any data", galeri hitam ukuran default, dropdown/tombol kotak polos). Beri nama baru ber-prefix: form -> `frm<P>`,
   galeri -> `gal<P>...`, input -> `inp<P>...` / `dd<P>...` / `cmb<P>...` / `num<P>...`, tombol -> `btn<P>...`. Data card dan
   SEMUA anak card di dalam form: nama lama + `_<P>` (mis. `DataCardValue58_AreaF`), dan ganti juga referensinya di
   dalam form (Update, Y, dst.). Logika/rumus tetap sama, hanya namanya. Update semua referensi lintas screen di file
   yang sudah dibangun (mis. W6: `Form5` -> `frmTrxF` berarti `btnDashNewTrx.OnSelect` di scr_dashboard ikut diganti;
   W5: `Form5_3`/`Gallery8_6` dipakai scr_item + scr_frm_item).
6. **Filter Dataverse**: sisi kanan perbandingan harus konstanta. `qty < dis_item_v2.min_qty` di Filter atas tabel
   ditolak server; pakai named formula `nfLowStock` (App.Formulas, dihitung lokal dengan AddColumns) atau bandingkan per
   baris (`ThisItem.qty < ThisItem.dis_item_v2.min_qty` di galeri boleh).
7. **Baris galeri TANPA GroupContainer bersarang** (koreksi W5b). Semua galeri yang barisnya berisi container AutoLayout
   lain (grup ikon aksi, tumpukan teks 2-3 baris) tampil hitam/rusak di Studio; galeri dengan isi baris langsung
   (teks, badge, ikon) tampil benar. Ikon Edit/Hapus langsung jadi anak `con<P>Row` (32 + gap 8 + 32 = kolom AKSI 72).
   Teks bertingkat ditulis dalam SATU ModernText dengan `Char(10)` dan `Wrap: =true`.


## Aesthetic Direction

Refined industrial dashboard: SLB navy brand rail, cool-grey page, crisp white cards with 12px radius and a light
shadow, dense but airy tables with hairline row dividers, semantic Fluent badges for status/type/role. One accent
(navy) for primary actions; red only for destructive actions; green only for success evidence.

All colours are App-level named formulas (defined in App.Formulas before builders run). Use the names, not raw RGBA:

| Name | Value | Use |
| --- | --- | --- |
| clrNavy | RGBA(0, 18, 107, 1) | Sidebar, primary buttons (`BasePaletteColor`), active segment |
| clrAccent | RGBA(56, 96, 178, 1) | Edit icons, links, KPI icon tint base |
| clrBg | RGBA(244, 246, 250, 1) | Screen Fill, root, main column, body |
| clrSurface | RGBA(255, 255, 255, 1) | Cards, TopBar, gallery rows |
| clrBorder | RGBA(226, 230, 239, 1) | Card borders, gallery row dividers (Gallery Fill) |
| clrHeaderBg | RGBA(241, 244, 250, 1) | Table header rows, segmented control track |
| clrRowSelected | RGBA(232, 238, 252, 1) | Selected gallery row |
| clrText | RGBA(31, 41, 55, 1) | Primary text |
| clrTextMuted | RGBA(100, 112, 130, 1) | Secondary text, labels, column headers |
| clrDanger / clrDangerTint | RGBA(196, 43, 28, 1) / RGBA(253, 237, 236, 1) | Delete icon & button / confirm strip |
| clrSuccess / clrSuccessTint | RGBA(16, 124, 65, 1) / RGBA(232, 246, 238, 1) | Receipt icon / receipt strip |
| clrWarning / clrWarningTint | RGBA(188, 118, 0, 1) / RGBA(255, 246, 225, 1) | Low-stock KPI tile |

Typography: `Font: =Font.'Segoe UI'` on every ModernText / ModernButton you add.

## Visual Contract

- Type roles (ModernText `Size` / `FontWeight`): page title is in TopBar (18 Bold). Card title 16 Semibold clrText
  (Height 24). Body / table cell 13 Normal clrText (Height 20). Identity cell 13 Semibold. Secondary line 12 clrTextMuted
  (Height 18). Field label & column header 11 Semibold clrTextMuted (Height 16 / 18). KPI value 28 Bold (Height 36).
  Every ModernText sets all four `Padding*: =0` (except where a brief says otherwise), `Wrap: =false` for single-line
  text, and an explicit `Height` >= Size x 1.5.
- Spacing scale: 2, 4, 8, 12, 16, 20, 24. Body padding 24 L/R/B, 20 top; body gap 16; card padding 16; toolbar gap 8.
- Surfaces: card = Fill clrSurface, BorderColor clrBorder, BorderStyle Solid, BorderThickness 1, DropShadow Light,
  Radius 12 (all four). Strips (confirm / receipt) = Radius 10, DropShadow None, BorderThickness 1.
- Actions: Primary = `Appearance: =ButtonAppearance.Primary`, `BasePaletteColor: =clrNavy`, Height 36, Size 13,
  Radius 8, `Layout: =ButtonLayout.IconBefore` with a Fluent `Icon`. Secondary = `ButtonAppearance.Secondary`,
  `Color: =clrText`. Destructive = Primary with `BasePaletteColor: =clrDanger`. Disabled = `DisplayMode.Disabled`
  (Fluent renders the disabled look). Every ModernButton sets `Width` and `LayoutMinWidth` equal to that width, and
  `LayoutMinHeight: =0`, because its AutoLayout defaults are 280 x 64.
- Row actions: two `ModernIcon` 32 x 32 (`Icon: ="Edit"` IconColor clrAccent; `Icon: ="Delete"` IconColor clrDanger),
  `Padding*: =6`, Radius 6, `Tooltip` + `AccessibleLabel` naming the row identity. Action column width 72 (32 + 8 + 32).
- Density: fixed desktop only; one composition. No phone/tablet branches.

## Layout Strategy

Fixed desktop (approved). Minimum supported canvas = the app's current 1136 x 640; wider canvases stretch through
`FillPortions` / `Parent.Width`. There is one layout branch, so no breakpoints and no layout variables. All budgets in
the briefs are computed at 1136 x 640:

- Sidebar 224 + Main 912. TopBar 64. Body padding 24/24/24 + top 20 -> body inner width 864, inner height 532.
- Card inner width = 864 - 32 = 832. Gallery row inner width = 832 - 2 (TemplatePadding 1 x 2) - 24 (row padding) = 806.
- The body (`con<P>Body`) is the only scroll container. Its direct children use `FillPortions: =0` + explicit `Height`.
- Do not nest scroll containers; galleries scroll themselves inside a fixed `Height`.
- Never use ManualLayout, X/Y positioning, or hard-coded container widths > 400 (Sidebar 224 is the only fixed rail).
- Every GroupContainer sets `LayoutMinWidth: =0` and `LayoutMinHeight: =0`, `DropShadow` explicitly, and all four
  `Radius*` explicitly. Every AutoLayout child sets `AlignInContainer` and `FillPortions`.
- Modern inputs (ModernTextInput / ModernDropdown / ModernNumberInput / ModernDatePicker / ModernCombobox) default
  to LayoutMinWidth 560 and LayoutMinHeight 64 inside AutoLayout: always set `LayoutMinWidth: =0`,
  `LayoutMinHeight: =0`, `Height: =36`.
- Canvas component instances default LayoutMinWidth/LayoutMinHeight 640: always set them as in the Shell pattern.

### Pattern - Screen shell (instantiate under your prefix `<P>`; values are fixed)

Screen `Properties`: `Fill: =clrBg`, `LoadingSpinnerColor: =clrAccent`. The screen `Children:` list contains ONLY
`con<P>Root`.

```yaml
- con<P>Root:
    Control: GroupContainer
    Variant: AutoLayout
    Properties:
      DropShadow: =DropShadow.None
      Fill: =clrBg
      Height: =Parent.Height
      LayoutAlignItems: =LayoutAlignItems.Stretch
      LayoutDirection: =LayoutDirection.Horizontal
      LayoutGap: =0
      LayoutMinHeight: =0
      LayoutMinWidth: =0
      RadiusBottomLeft: =0
      RadiusBottomRight: =0
      RadiusTopLeft: =0
      RadiusTopRight: =0
      Width: =Parent.Width
    Children:
      - cmp<P>Sidebar:
          Control: CanvasComponent
          ComponentName: Sidebar
          Properties:
            activemenu: ="<exact fxMenuItems TextValue from brief>"
            AlignInContainer: =AlignInContainer.Start
            FillPortions: =0
            Height: =Parent.Height
            LayoutMinHeight: =0
            LayoutMinWidth: =224
            Width: =224
      - con<P>Main:
          Control: GroupContainer
          Variant: AutoLayout
          Properties:
            AlignInContainer: =AlignInContainer.Stretch
            DropShadow: =DropShadow.None
            Fill: =clrBg
            FillPortions: =1
            LayoutAlignItems: =LayoutAlignItems.Stretch
            LayoutDirection: =LayoutDirection.Vertical
            LayoutGap: =0
            LayoutMinHeight: =0
            LayoutMinWidth: =0
            RadiusBottomLeft: =0
            RadiusBottomRight: =0
            RadiusTopLeft: =0
            RadiusTopRight: =0
          Children:
            - cmp<P>TopBar:
                Control: CanvasComponent
                ComponentName: TopBar
                Properties:
                  ActiveMenu: ="<title from brief>"
                  Subtitle: ="<subtitle from brief>"
                  AlignInContainer: =AlignInContainer.Start
                  FillPortions: =0
                  Height: =64
                  LayoutMinHeight: =64
                  LayoutMinWidth: =0
                  Width: =Parent.Width
            - con<P>Body:
                Control: GroupContainer
                Variant: AutoLayout
                Properties:
                  AlignInContainer: =AlignInContainer.Stretch
                  DropShadow: =DropShadow.None
                  Fill: =clrBg
                  FillPortions: =1
                  LayoutAlignItems: =LayoutAlignItems.Stretch
                  LayoutDirection: =LayoutDirection.Vertical
                  LayoutGap: =16
                  LayoutMinHeight: =0
                  LayoutMinWidth: =0
                  LayoutOverflowY: =LayoutOverflow.Scroll
                  PaddingBottom: =24
                  PaddingLeft: =24
                  PaddingRight: =24
                  PaddingTop: =20
                  RadiusBottomLeft: =0
                  RadiusBottomRight: =0
                  RadiusTopLeft: =0
                  RadiusTopRight: =0
                Children:
                  # screen-specific sections, each FillPortions 0 + explicit Height
```

### Pattern - Card

`con<P><Name>Card`: GroupContainer AutoLayout Vertical; Fill clrSurface; BorderColor clrBorder; BorderStyle Solid;
BorderThickness 1; DropShadow Light; Radius 12 x4; Padding 16 x4; LayoutGap 12 (unless brief says otherwise);
LayoutAlignItems Stretch; AlignInContainer Stretch; FillPortions 0; Height from brief.

Card title: ModernText Size 16 Semibold clrText Height 24 Wrap false.

### Pattern - Toolbar with labelled fields

`con<P>Toolbar`: AutoLayout Horizontal, Height 56, LayoutGap 8, LayoutAlignItems End, Fill RGBA(0,0,0,0),
DropShadow None, Radius 0 x4, FillPortions 0, AlignInContainer Stretch.
Each filter = field group `con<P><X>Fld`: AutoLayout Vertical, LayoutGap 4, Height 56, LayoutAlignItems Stretch,
AlignInContainer End, FillPortions 0 + `Width` (or FillPortions 1 for the search field), containing:
1. `txt<P><X>Lbl` ModernText, Size 11, Semibold, clrTextMuted, Height 16, FillPortions 0, Wrap false, paddings 0.
2. the input, Height 36, FillPortions 0, AlignInContainer Stretch, LayoutMinWidth 0, LayoutMinHeight 0,
   `Appearance: =Appearance.Outline`, Size 13, Radius 8 x4 (TextInput/Dropdown support Radius*).
Toolbar buttons / icons: AlignInContainer End, FillPortions 0. Reset icon = ModernIcon `Icon: ="ArrowReset"`
36 x 36, IconColor clrTextMuted, Tooltip "Reset filter".

### Pattern - Table header + gallery rows

- Header `con<P>Head`: AutoLayout Horizontal, Height 36, Fill clrHeaderBg, Radius 8 x4, PaddingLeft/Right 13
  (12 + 1 to align with TemplatePadding), LayoutGap 8, LayoutAlignItems Center, FillPortions 0. Header cells are
  ModernText Size 11 Semibold clrTextMuted Height 18 Wrap false, UPPERCASE text, AlignInContainer Center, with the
  SAME `FillPortions`/`Width` as the matching row cell.
- Gallery: `Variant: Vertical`, explicit numeric `Height` (brief), `TemplateSize` (brief), `TemplatePadding: =1`,
  `Fill: =clrBorder` (hairline dividers), BorderThickness 0, ShowScrollbar true, TabIndex 0, AccessibleLabel,
  FillPortions 0, AlignInContainer Stretch, LayoutMinWidth 0, LayoutMinHeight 0. Never set OnSelect on a Gallery.
  Never derive Height from CountRows.
- Exactly ONE direct child `con<P>Row`: AutoLayout Horizontal, `Width: =Parent.TemplateWidth`,
  `Height: =Parent.TemplateHeight`, `Fill: =If(ThisItem.IsSelected, clrRowSelected, clrSurface)`, PaddingLeft/Right 12,
  LayoutGap 8, LayoutAlignItems Center, DropShadow None, Radius 0 x4. Row cells: ModernText Size 13 clrText Height 20
  Wrap false paddings 0 AlignInContainer Center, `LayoutMinWidth: =0`, with FillPortions or fixed Width per brief.
  Only the shell uses `Parent.TemplateWidth/Height`.
- Empty state `txt<P>Empty`: ModernText Size 13 clrTextMuted Align Center, Height = the gallery Height, placed right
  after the gallery; `Visible` = `IsEmpty(<same Items expression>)` and the gallery `Visible` = `!IsEmpty(...)`
  (same slot, so the card height budget is unchanged). Never use `Self.AllItems` for empty state.

### Pattern - Delete confirmation strip (state-driven, nested in the body above the list card)

`con<P>Confirm`: AutoLayout Horizontal, Height 56, Fill clrDangerTint, BorderColor RGBA(240, 180, 176, 1),
BorderThickness 1, Radius 10 x4, PaddingLeft 16, PaddingRight 12, LayoutGap 12, LayoutAlignItems Center,
DropShadow None, FillPortions 0, AlignInContainer Stretch, `Visible:` per brief. Children:
`ico<P>ConfirmIco` (ModernIcon "Warning" 24 x 24, IconColor clrDanger), `txt<P>ConfirmMsg` (ModernText FillPortions 1,
Size 13 Semibold clrText Height 20 Wrap false, text per brief), `btn<P>ConfirmDel` (Destructive, Text "Hapus",
Icon "Delete", Width 104), `btn<P>ConfirmCancel` (Secondary, Text "Batal", Icon "Dismiss", Width 96).

### Pattern - Receipt strip (mutation evidence)

`con<P>Receipt`: AutoLayout Horizontal, Height 80, Fill clrSuccessTint, BorderColor RGBA(180, 222, 196, 1),
BorderThickness 1, Radius 10 x4, PaddingLeft 16, PaddingRight 12, PaddingTop 10, PaddingBottom 10, LayoutGap 12,
LayoutAlignItems Center, DropShadow None, FillPortions 0, AlignInContainer Stretch,
`Visible: =gblReceipt.Screen = "<key from brief>"`. Children:
1. `ico<P>RcIco` ModernIcon "CheckmarkCircle" 24 x 24 IconColor clrSuccess, AlignInContainer Center.
2. `con<P>RcText` AutoLayout Vertical, FillPortions 1, Height 58, LayoutGap 2, LayoutAlignItems Stretch,
   LayoutJustifyContent Center, AlignInContainer Center:
   - `txt<P>RcTitle` ModernText `Text: =gblReceipt.Action & " - " & gblReceipt.Title`, Size 13 Bold clrText,
     Height 20, Wrap false.
   - `txt<P>RcDetail` ModernText `Text: =gblReceipt.Detail`, Size 12 clrTextMuted, Height 36, Wrap true (2 lines).
3. `ico<P>RcClose` ModernIcon "Dismiss" 32 x 32, IconColor clrTextMuted, Padding 6 x4, Tooltip "Tutup",
   `OnSelect: '=Set(gblReceipt, {Screen: "", Action: "", Title: "", Detail: ""})'`.

### Pattern - Segmented type filter (Trx list, History)

Field group `con<P>TypeFld` (Width 360, label "TIPE") containing `con<P>TypeSeg`: AutoLayout Horizontal, Height 36,
Fill clrHeaderBg, Radius 8 x4, Padding 2 x4, LayoutGap 4, LayoutAlignItems Center, DropShadow None. Four
ModernButtons Height 32, FillPortions 0, Size 13, Radius 6 x4, Layout TextOnly:
"Semua" W 72, "Receive" W 84, "Consume" W 92, "Transfer" W 88 (2 + 72 + 4 + 84 + 4 + 92 + 4 + 88 + 2 = 352 <= 360).
Active button: `Appearance: =ButtonAppearance.Primary`, `BasePaletteColor: =clrNavy`, `Color: =RGBA(255, 255, 255, 1)`;
inactive: `Appearance: =ButtonAppearance.Subtle`, `Color: =clrText`. Write both as one `If(...)` per property.

### Pattern - Form screen

Body children: `con<P>FormCard` (Card pattern: title text + the existing Form) then `con<P>Actions` (AutoLayout
Horizontal, Height 44, LayoutJustifyContent End, LayoutAlignItems Center, LayoutGap 12, Fill transparent,
DropShadow None) with Secondary "Kembali" (Icon "ArrowLeft", W 120) then Primary save button (Icon "Save", W 160).
Existing Form: keep `Control: Form`, `Variant: Modern`, `Layout: Vertical`, name, DataSource, Item, DataField/Update,
DefaultMode and every data card + child; set `AlignInContainer: =AlignInContainer.Stretch`, `FillPortions: =0`,
`Height` (brief), `Fill: =clrSurface`, `BorderThickness: =0`, `NumberOfColumns: =2`; delete `X`, `Y`, `Width`.
On data cards change only `Width` (half cards `=Parent.Width / 2`, full cards `=Parent.Width`); do not add or remove
cards or card children, do not change Update / DataField / Default / variants.

## Named State

| Name | Kind | Owner | Meaning |
| --- | --- | --- | --- |
| nfMe | App named formula | App | Current user's dis_users row |
| clr* | App named formulas | App | Palette (above) |
| fxMenuItems | App named formula | App | Sidebar items `{TextValue, Icon, NavigateScreen}` |
| imyrole, imyid, imyarea, imyemail, iroleview | App vars/collection (OnStart) | App | Legacy compatibility, read-only for screens |
| gblReceipt | Global record `{Screen, Action, Title, Detail}` (all Text) | Set by form OnSuccess / delete handlers | Receipt strip content; `Screen` keys: "Area", "User", "Category", "Item", "Transaction". Always set all four fields. Clear with `{Screen: "", Action: "", Title: "", Detail: ""}` |
| gblFormMode | Global text "Add"/"Update" | Area / Add_area | Existing; preserved |
| colTempDetails | Collection `{Urutan, Id, name, description, Qty}` | scr_Transaction / scr_frm_Transaction / scr_dashboard | Existing cart; preserved |
| colConsumeReceipt | Collection `{StockId, ItemName, Operation, OldQty, Amount, ExpectedQty, ActualQty}` | scr_consume | Consume receipt lines |
| locSelectedRecord | Context var (per screen) | list screens | Row targeted by Delete (and Edit on scr_user) - always `ThisItem` |
| locShowDeleteConfirm / locShowDeleteConfirm_1 / locShowUserPopUp | Context vars | list screens | Existing names, preserved |
| locTrxType / locHistType | Context vars | scr_Transaction / scr_History | Type segment state: `Blank()` = all, else `'type (dis_trx_headers)'.<Member>` |
| locConsHeader, locShowConsReceipt | Context vars | scr_consume | Consume receipt header |

Option-set literals: `'type (dis_trx_headers)'.Receive`, `.Consume`, `.Transfer`; `dis_role.administrator`;
`'status (dis_item_v2S)'` values are compared via `Text(ThisItem.status) = "Active"`.

## Control Naming

`<type><Prefix><Purpose>`: `con` GroupContainer, `cmp` component instance, `txt` ModernText, `btn` ModernButton,
`ico` ModernIcon, `bdg` Badge, `gal` Gallery, `img` Image, `inp` text input, `dd` dropdown, `num` number input.
Prefixes (unique, never a prefix of another): Dash, Login, Reg, Tpl, AreaL, AreaF, UsrL, CatL, CatF, ItmL, ItmF,
TrxL, TrxF, Cons, Find, Hist. Components own `Sb` (Sidebar) and `Tb` (TopBar) - never use them on screens.
Existing functional controls listed in each brief KEEP their current names (cross-screen references depend on them);
every NEW control uses the screen prefix. Patterns above are instantiated under each screen's own prefix.

## Cross-Screen Contracts

Sidebar `activemenu` (must equal fxMenuItems.TextValue) and TopBar values:

| Screen | activemenu | TopBar ActiveMenu | TopBar Subtitle |
| --- | --- | --- | --- |
| scr_dashboard | "Dashboard" | "Dashboard" | "Ringkasan stok dan transaksi hari ini" |
| Template | "" | "Template" | "Kerangka halaman baru" |
| Area | "Area" | "Area" | "Kelola area penyimpanan" |
| Add_area | "Area" | `=If(gblFormMode = "Add", "Tambah Area", "Edit Area")` | "Lengkapi data area" |
| scr_user | "User" | "User" | "Kelola pengguna dan peran" |
| scr_category | "Category Item" | "Category Item" | "Kelola kategori item" |
| scr_frm_category | "Category Item" | `=If(frm_catFrm_category.Mode = FormMode.Edit, "Edit Kategori", "Tambah Kategori")` | "Lengkapi data kategori" |
| scr_item | "Item" | "Item" | "Master data item" |
| scr_frm_item | "Item" | `=If(Form5_3.Mode = FormMode.Edit, "Edit Item", "Tambah Item")` | "Lengkapi data item" |
| scr_Transaction | "Transaction" | "Transaction" | "Daftar transaksi dan detail item" |
| scr_frm_Transaction | "Transaction" | `=If(Form5.Mode = FormMode.Edit, "Edit Transaksi", "Transaksi Baru")` | "Header transaksi dan keranjang item" |
| scr_consume | "Consume" | "Consume" | "Pakai barang dari stok area" |
| scr_find_item | "Find Item" | "Find Item" | "Cari stok item per lokasi" |
| scr_History | "History" | "History" | "Riwayat transaksi" |

Log In and Register have no shell (welcome layouts). Cross-screen controls that must keep their names: Form5_1 +
Gallery8_12 (Area/Add_area), Form4 + Gallery8_13 (scr_user), frm_catFrm_category + gal_cat_list (scr_category /
scr_frm_category), Form5_3 + Gallery8_6 (scr_item / scr_frm_item), Form5 + Gallery8_1 (scr_Transaction /
scr_frm_Transaction / scr_dashboard). Navigation between screens uses ModernButton/ModernIcon `OnSelect` with
`Navigate(...)`; never ModernTabList.

## YAML Conventions

- Every property value starts with `=`; multi-line formulas use `|-` with `=` on the first content line.
- Any value containing `: ` (captions like `"Area: "`, record literals `{Screen: ""}`) must be single-quoted
  (`'=...'`) or written as a `|-` block. Prefer `|-` for anything longer than one line.
- Enum literals: `='BadgeCanvas.Appearance'.Tint`, `='BadgeCanvas.Shape'.Rounded`,
  `='BadgeCanvas.ThemeColor'.Success`, `=ButtonAppearance.Primary`, `=Appearance.Outline`, `=DecimalPrecision.'0'`,
  `=Font.'Segoe UI'`, `=LayoutOverflow.Scroll`. Never a bare member.
- `Control: GroupContainer` always has `Variant: AutoLayout`; `Control: Gallery` always has `Variant: Vertical`.
- Canvas components: `Control: CanvasComponent` + `ComponentName: Sidebar|TopBar`, no Variant. Set both TopBar inputs
  (`ActiveMenu`, `Subtitle`).
- Badges always set `Content`, `FontSize: =12`, `FontWeight: =FontWeight.Semibold`, `Shape: ='BadgeCanvas.Shape'.Rounded`,
  `Appearance: ='BadgeCanvas.Appearance'.Tint`, `Height: =24`, `Width`, `FillPortions: =0`; do not set `FontColor`
  on Tint badges (the variant owns the contrast).
- Never `Set`/`UpdateContext` a variable to `Blank()` unless it is typed by another assignment in the app.
- Do not add `X`/`Y` anywhere except preserved TypedDataCard grid positions and preserved data-card children.
