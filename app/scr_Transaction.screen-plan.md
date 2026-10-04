# Screen Plan: Transaction

## Assignment

- Action: Modify (rewrite layout; keep YAML key and the functional controls listed below)
- Target file: `C:\Project\Powerapps\app\scr_Transaction.pa.yaml`
- YAML key: scr_Transaction
- Control name prefix: TrxL

Read `C:\Project\Powerapps\app\canvas-app-shared.md` first (Shell, Card, Toolbar, Table, Segmented type filter,
Confirm, Receipt).

## Current State

`con_Main_trans` shell (Sidebar "Transaction", TopBar "Transaction") -> `Container8`:
- Header list `Container13`: toolbar `Container15` (Dropdown2 type `Choices(dis_trx_headers.type)`, inp_search_1,
  spacer, Button31 "Add Transaction"), Label header `Container20`, ManualLayout `Container10_1` with `Gallery8_1`
  (rows Text1_2 number, Text1_3 date, Type_1 type, Type_4 area_to.Name, Type_5 note, Button15_2 "Update", spacer,
  Button15_3 "Delete").
- Spacer `Container25`.
- Detail `Container13_1`: toolbar `Container15_1` (Dropdown2_1 category, inp_search_2 never wired), Label header
  `Container20_1`, ManualLayout `Container10_2` with `Gallery8_3` (rows Text1_4..Type_8).

Preserved logic (copy verbatim):
- Button31 `OnSelect: =Clear(colTempDetails); NewForm(Form5); Navigate(scr_frm_Transaction);`.
- Button15_2 OnSelect (Edit; becomes `icoTrxLEdit.OnSelect`, copy the full text from the current file, including
  comments):
  ```
  =Clear(colTempDetails);

  ForAll(
      Filter(dis_trx_details, header_id.dis_trx_header = ThisItem.dis_trx_header),
      Collect(
          colTempDetails,
          {
              Urutan: CountRows(colTempDetails) + 1,
              Id: ThisRecord.item.dis_item_v2,
              name: ThisRecord.item.name,
              description: ThisRecord.item.description,
              Qty: ThisRecord.qty
          }
      )
  );

  // 3. Buka form dalam mode Edit dan pindah halaman
  EditForm(Form5);
  Navigate(scr_frm_Transaction);
  ```
- Button15_3 cascade delete: `RemoveIf(dis_trx_details, header_id.dis_trx_header = ThisItem.dis_trx_header); Remove(dis_trx_headers, ThisItem); Notify(...)`
  (immediate, no confirmation - fixed below; stock is NOT reversed and stays that way).
- Gallery8_3 Items: Filter(dis_trx_details, header of `Gallery8_1.Selected` && category from Dropdown2_1).

## Changes

1. Screen Properties: `Fill: =clrBg`, `LoadingSpinnerColor: =clrAccent`. Screen `Children:` = `conTrxLRoot` only.
2. Shell pattern with prefix TrxL: conTrxLRoot, cmpTrxLSidebar (`activemenu: ="Transaction"`), conTrxLMain,
   cmpTrxLTopBar (`ActiveMenu: ="Transaction"`, `Subtitle: ="Daftar transaksi dan detail item"`), conTrxLBody.
3. Dropdown2 is replaced by the segmented type filter (context var `locTrxType`); list sorted newest first.
4. Keep `inp_search_1`, `Button31`, `Gallery8_1` (Form5.Item on scr_frm_Transaction reads `Gallery8_1.Selected`),
   `Dropdown2_1`, `inp_search_2`, `Gallery8_3`.
5. Delete goes through the confirm strip (cascade on `locSelectedRecord`); `inp_search_2` is wired into Gallery8_3.

## Controls to Add

conTrxLBody children, in order (FillPortions 0, AlignInContainer Stretch):

1. `conTrxLReceipt` - Receipt strip, `Visible: =gblReceipt.Screen = "Transaction"`.
2. `conTrxLConfirm` - Confirm strip, `Visible: =locShowDeleteConfirm`:
   - `txtTrxLConfirmMsg`
     `Text: ="Hapus transaksi " & locSelectedRecord.transaction_number & " beserta semua detailnya? Stok tidak dikembalikan."`
   - `btnTrxLConfirmDel` Destructive "Hapus" W 104, OnSelect (`|-`):
     ```
     =With(
         {
             target: locSelectedRecord,
             lineCount: CountRows(Filter(dis_trx_details, header_id.dis_trx_header = locSelectedRecord.dis_trx_header))
         },
         // 1. Hapus semua baris di tabel detail yang nyambung ke header ini
         RemoveIf(
             dis_trx_details,
             header_id.dis_trx_header = target.dis_trx_header
         );
         // 2. Setelah detail bersih, baru hapus headernya
         Remove(dis_trx_headers, target);
         If(
             IsEmpty(Errors(dis_trx_headers)),
             Set(
                 gblReceipt,
                 {
                     Screen: "Transaction",
                     Action: "Dihapus",
                     Title: target.transaction_number,
                     Detail: "Tipe " & Text(target.type) & " | " & Text(lineCount) & " baris detail ikut dihapus | stok tidak dikembalikan"
                 }
             );
             UpdateContext({locShowDeleteConfirm: false});
             // 3. Munculkan notifikasi
             Notify("Data transaksi beserta seluruh detail item berhasil dihapus.", NotificationType.Success),
             Notify("Gagal menghapus transaksi. " & First(Errors(dis_trx_headers)).Message, NotificationType.Error)
         )
     )
     ```
   - `btnTrxLConfirmCancel` Secondary "Batal" W 96, `OnSelect: =UpdateContext({locShowDeleteConfirm: false})`.
3. `conTrxLListCard` - Card pattern, Height 520, LayoutGap 12:
   - `conTrxLToolbar` (Toolbar pattern):
     - `conTrxLTypeFld` (Segmented type filter pattern, W 360): `txtTrxLTypeLbl` "TIPE" + `conTrxLTypeSeg` with
       `btnTrxLTypeAll` "Semua" W 72, `btnTrxLTypeReceive` "Receive" W 84, `btnTrxLTypeConsume` "Consume" W 92,
       `btnTrxLTypeTransfer` "Transfer" W 88.
       | Button | OnSelect | Active predicate (Appearance / BasePaletteColor / Color via If) |
       | --- | --- | --- |
       | btnTrxLTypeAll | `=UpdateContext({locTrxType: Blank()})` | `IsBlank(locTrxType)` |
       | btnTrxLTypeReceive | `=UpdateContext({locTrxType: 'type (dis_trx_headers)'.Receive})` | `locTrxType = 'type (dis_trx_headers)'.Receive` |
       | btnTrxLTypeConsume | `=UpdateContext({locTrxType: 'type (dis_trx_headers)'.Consume})` | `locTrxType = 'type (dis_trx_headers)'.Consume` |
       | btnTrxLTypeTransfer | `=UpdateContext({locTrxType: 'type (dis_trx_headers)'.Transfer})` | `locTrxType = 'type (dis_trx_headers)'.Transfer` |
       (`Blank()` is allowed here because the same variable is typed by the option-set assignments on this screen.)
     - `conTrxLSearchFld` FillPortions 1, LayoutMinWidth 0: `txtTrxLSearchLbl` "Cari transaksi" + `inp_search_1`
       (TriggerOutput Delayed; `Placeholder: ="Nomor atau catatan"`, `Type: =TextInputType.Search`,
       AccessibleLabel "Cari transaksi"; drop empty `Default: =`).
     - `Button31` (kept) Primary, Icon "Add", Text "Tambah Transaksi", W 176, AlignInContainer End, OnSelect
       unchanged.
   - `conTrxLTable` AutoLayout Vertical, Height 420, LayoutGap 4, transparent:
     - `conTrxLHead`: `txtTrxLHNo` "NOMOR" FP 2, `txtTrxLHDate` "TANGGAL" W 92, `txtTrxLHType` "TIPE" W 92,
       `txtTrxLHArea` "AREA (DARI -> KE)" FP 3, `txtTrxLHNote` "CATATAN" FP 3, `txtTrxLHAct` "AKSI" W 72.
     - `Gallery8_1` (kept) Gallery pattern, Height 380, TemplateSize 52, AccessibleLabel "Daftar transaksi",
       Items (`|-`):
       ```
       =Sort(
           Search(
               Filter(
                   dis_trx_headers,
                   IsBlank(locTrxType) || type = locTrxType
               ),
               inp_search_1.Text,
               transaction_number,
               note
           ),
           'Created On',
           SortOrder.Descending
       )
       ```
       `Visible: =!IsEmpty(<same Items expression>)`. Row `conTrxLRow`:
       - `btnTrxLOpen` ModernButton link cell: `Appearance: =ButtonAppearance.Subtle`, `Color: =clrAccent`,
         `Layout: =ButtonLayout.TextOnly`, `Align: =Align.Left`, FontWeight Semibold, Size 13, Height 28,
         FillPortions 2, LayoutMinWidth 0, LayoutMinHeight 0, AlignInContainer Center,
         `Text: =ThisItem.transaction_number`, Tooltip/AccessibleLabel `="Lihat detail " & ThisItem.transaction_number`,
         `OnSelect: =UpdateContext({locShowDeleteConfirm: false})` (selecting the button selects the row, which
         drives Gallery8_3; it also closes a pending delete strip of another row).
       - `txtTrxLDate` `=Text(ThisItem.'Created On', "dd/mm/yyyy")`, W 92.
       - `bdgTrxLType` Badge W 92, `Content: =Text(ThisItem.type)`,
         `ThemeColor: =Switch(Text(ThisItem.type), "Receive", 'BadgeCanvas.ThemeColor'.Success, "Consume", 'BadgeCanvas.ThemeColor'.Warning, "Transfer", 'BadgeCanvas.ThemeColor'.Brand, 'BadgeCanvas.ThemeColor'.Subtle)`.
       - `txtTrxLArea` `=Coalesce(ThisItem.area_form.Name, "-") & " -> " & Coalesce(ThisItem.area_to.Name, "-")`, FP 3.
       - `txtTrxLNote` `=ThisItem.note`, FP 3.
       - `conTrxLRowActs` (W 72 action group):
         - `icoTrxLEdit` Edit icon, Tooltip/AccessibleLabel `="Edit " & ThisItem.transaction_number`,
           OnSelect = Button15_2 formula verbatim (above).
         - `icoTrxLDelete` Delete icon, Tooltip/AccessibleLabel `="Hapus " & ThisItem.transaction_number`,
           `OnSelect: =UpdateContext({locSelectedRecord: ThisItem, locShowDeleteConfirm: true})`.
     - `txtTrxLEmpty` "Belum ada transaksi yang cocok.", Height 380, `Visible: =IsEmpty(<same Items expression>)`.
4. `conTrxLDetailCard` - Card pattern, Height 376, LayoutGap 12:
   - `txtTrxLDetailTitle` card title,
     `Text: =If(IsBlank(Gallery8_1.Selected), "Detail Item", "Detail Item - " & Gallery8_1.Selected.transaction_number)`.
   - `conTrxLDToolbar` (Toolbar pattern):
     - `conTrxLDCatFld` W 200: `txtTrxLDCatLbl` "Kategori" + `Dropdown2_1` (Items `=dis_category_items`,
       ItemDisplayText `=ThisItem.code` unchanged; AccessibleLabel "Filter kategori detail").
     - `conTrxLDSearchFld` FillPortions 1: `txtTrxLDSearchLbl` "Cari item" + `inp_search_2` (Delayed;
       `Placeholder: ="Nama item atau BPN"`, `Type: =TextInputType.Search`, AccessibleLabel "Cari item detail").
     - `icoTrxLDReset` reset icon, `OnSelect: =Reset(Dropdown2_1); Reset(inp_search_2)`.
   - `conTrxLDTable` AutoLayout Vertical, Height 240, LayoutGap 4, transparent:
     - `conTrxLDHead`: `txtTrxLDHBpn` "BPN" FP 2, `txtTrxLDHName` "NAMA" FP 3, `txtTrxLDHDesc` "DESKRIPSI" FP 3,
       `txtTrxLDHCat` "KATEGORI" FP 2, `txtTrxLDHQty` "QTY" W 64, `txtTrxLDHUom` "UOM" W 56.
     - `Gallery8_3` (kept) Gallery pattern, Height 200, TemplateSize 44, AccessibleLabel "Detail item transaksi",
       Items (`|-`, original two clauses + search clause):
       ```
       =Filter(
           dis_trx_details,
           header_id.dis_trx_header = Gallery8_1.Selected.dis_trx_header
           &&
           (
               IsBlank(Dropdown2_1.Selected) ||
               item.dis_category_item.name = Dropdown2_1.Selected.name
           )
           &&
           (
               IsBlank(inp_search_2.Text) ||
               StartsWith(item.name, inp_search_2.Text) ||
               StartsWith(item.part_number, inp_search_2.Text)
           )
       )
       ```
       `Visible: =!IsEmpty(<same Items expression>)`. Row `conTrxLDRow`: `txtTrxLDBpn` `=ThisItem.item.part_number`
       FP 2; `txtTrxLDName` `=ThisItem.item.name` Semibold FP 3; `txtTrxLDDesc` `=ThisItem.item.description` FP 3;
       `txtTrxLDCat` `=ThisItem.item.dis_category_item.name` FP 2; `txtTrxLDQty` `=Text(ThisItem.qty)` W 64
       Align Right; `txtTrxLDUom` `=Text(ThisItem.item.uom)` W 56.
     - `txtTrxLDEmpty` Height 200,
       `Text: =If(IsBlank(Gallery8_1.Selected), "Pilih nomor transaksi di atas untuk melihat detail.", "Tidak ada item yang cocok.")`,
       `Visible: =IsEmpty(<same Items expression>)`.

## Controls to Remove

con_Main_trans, con_sidebar_trans, com_sidebar_trans, con_content_trans, com_topbar_trans, Container8, Container13,
Container15, Dropdown2, Container16, Container20, Label21, Label21_1..Label21_5, Container21, Container10_1,
Container11_1, Text1_2, Text1_3, Type_1, Type_4, Type_5, Button15_2 (-> icoTrxLEdit), Container12_1, Button15_3
(-> icoTrxLDelete + confirm), Container25, Container13_1, Container15_1, Container16_1, Container20_1,
Label21_6..Label21_10, Label21_12, Container10_2, Container11_2, Text1_4, Text1_5, Type_2, Type_6, Type_7, Type_8,
Container12_2. Keep inp_search_1, Button31, Gallery8_1, Dropdown2_1, inp_search_2, Gallery8_3.

## Properties to Update

- Screen: Fill, LoadingSpinnerColor.
- Kept inputs: Toolbar styling, drop X/Y/Width. Kept galleries: Gallery pattern props, Items as given above.

## Layout and Visual Impact

- List toolbar: 360 + 176 + 2 x 8 = 552 -> search 280. Detail toolbar: 200 + 36 + 2 x 8 = 252 -> search 580.
- List card 16 + 56 + 12 + 420 + 16 = 520 (fills the first viewport); detail card
  16 + 24 + 12 + 56 + 12 + 240 + 16 = 376 below it; body scrolls.
- List row inner 806: fixed 92 + 92 + 72 + 5 x 8 = 296 -> FP 8 -> 63.75 (number 128, area/note 191).
- Detail row: fixed 64 + 56 + 5 x 8 = 160 -> FP 10 -> 64.6.

## Required Record Fields

| Field key | Record surface | Required field | Source field | Bound control | Exact formula | Placement and visibility |
| --- | --- | --- | --- | --- | --- | --- |
| trx/row/number | Gallery8_1 row | Number | transaction_number | btnTrxLOpen | `Text: =ThisItem.transaction_number` | FP 2 link |
| trx/row/date | row | Date | 'Created On' | txtTrxLDate | `=Text(ThisItem.'Created On', "dd/mm/yyyy")` | W 92 |
| trx/row/type | row | Type | type | bdgTrxLType | `Content: =Text(ThisItem.type)` | W 92 badge |
| trx/row/area | row | Area | area_form / area_to | txtTrxLArea | `=Coalesce(ThisItem.area_form.Name, "-") & " -> " & Coalesce(ThisItem.area_to.Name, "-")` | FP 3 |
| trx/row/note | row | Note | note | txtTrxLNote | `=ThisItem.note` | FP 3 |
| trxd/row/* | Gallery8_3 row | BPN, Name, Description, Category, Qty, UoM | item.part_number, item.name, item.description, item.dis_category_item.name, qty, item.uom | txtTrxLDBpn..txtTrxLDUom | see above | 6 cells |

## Required Actions

| Action | Preconditions | Entry point and event | Source and stable ID | Transition and postcondition | Mutation write set | Receipt proof set | Observer and evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ACT-TRX-FILTER | none | btnTrxLType*.OnSelect, inp_search_1 | dis_trx_headers.type | filtered, newest first | N/A | N/A | Gallery8_1; active segment Primary; txtTrxLEmpty |
| ACT-TRX-SELECT | rows | btnTrxLOpen (row selection) | Gallery8_1.Selected.dis_trx_header | detail card shows its lines | N/A | N/A | txtTrxLDetailTitle, Gallery8_3 |
| ACT-TRX-ADD | none | Button31.OnSelect | colTempDetails, Form5 | empty cart, Form5 New | N/A | N/A | scr_frm_Transaction "Transaksi Baru" |
| ACT-TRX-EDIT | row | icoTrxLEdit.OnSelect | ThisItem.dis_trx_header | colTempDetails loaded, Form5 Edit | colTempDetails (staging) | N/A | Gallery7 on form |
| ACT-TRX-DELETE | row | icoTrxLDelete -> btnTrxLConfirmDel | locSelectedRecord.dis_trx_header | header + lines removed; stock not reversed | existence of header + lines | "Dihapus" + number; Detail Tipe, line count | conTrxLReceipt; Gallery8_1 |
| ACT-TRX-SAVE (observer) | saved on scr_frm_Transaction | Form5.OnSuccess -> Back() | LastSubmit.dis_trx_header | list shown | see scr_frm_Transaction | gblReceipt "Transaction" | conTrxLReceipt; Gallery8_1 first row |

## Functional Test Scenarios

| Scenario | Given | When | Then | Evidence surface | Boundary or negative case |
| --- | --- | --- | --- | --- | --- |
| SCN-TRX-FILTER | H1 Receive, H2 Receive, H3 Consume | click Receive | H1, H2 shown; H3 hidden; Receive segment Primary | Gallery8_1 | Semua restores; search "zzz" -> txtTrxLEmpty |
| SCN-TRX-DETAIL | H1 with 2 lines, H2 with 1 | click H1 number | 2 lines of H1 | txtTrxLDetailTitle "Detail Item - H1", Gallery8_3 | category filter hides non-matching line; search by BPN narrows |
| SCN-TRX-ADD | stale cart | Tambah Transaksi | empty cart, Form5 New | scr_frm_Transaction Gallery7 empty | N/A |
| SCN-TRX-EDIT | H1 with 2 lines | Edit icon on H1 | colTempDetails = 2 lines | Gallery7 | N/A |
| SCN-TRX-DELETE | H3 with 1 line | Delete icon -> Hapus | H3 and its line removed | conTrxLReceipt "Dihapus - H3", "1 baris detail" | Batal keeps H3; stock unchanged (preserved) |

## Relevant Data Source Schemas

dis_trx_headers: transaction_number, note, type (option set `'type (dis_trx_headers)'`: Receive, Consume, Transfer),
area_form (-> dis_areas .Name), area_to (-> dis_areas .Name), 'Created On', dis_trx_header (Guid).
dis_trx_details: header_id (-> dis_trx_headers), item (-> dis_item_v2S: part_number, name, description, uom,
dis_category_item.name), qty, PK. Context: locTrxType (option-set value or blank), locSelectedRecord
(dis_trx_headers record), locShowDeleteConfirm. Globals: colTempDetails, gblReceipt. Form5 lives on
scr_frm_Transaction.

## Required Variants

GroupContainer -> AutoLayout. Gallery -> Vertical (unchanged).

## Changed or Added Control Definitions

AutoLayout child extras for all controls below: AlignInContainer (`=AlignInContainer.Stretch` / `.Start` /
`.Center` / `.End`), FillPortions, LayoutMaxHeight, LayoutMaxWidth, LayoutMinHeight, LayoutMinWidth.

- **GroupContainer** - `Control: GroupContainer`, `Variant: AutoLayout`. Inputs: BorderColor, BorderStyle,
  BorderThickness, ContentLanguage, DropShadow, EnableChildFocus, Fill, Height, LayoutAlignItems, LayoutDirection,
  LayoutGap, LayoutJustifyContent, LayoutOverflowX, LayoutOverflowY, LayoutWrap, PaddingBottom, PaddingLeft,
  PaddingRight, PaddingTop, RadiusBottomLeft, RadiusBottomRight, RadiusTopLeft, RadiusTopRight, Visible, Width, X, Y.
  Literals: `=DropShadow.None` / `.Light`; `=BorderStyle.Solid`; `=LayoutDirection.Horizontal` / `.Vertical`;
  `=LayoutAlignItems.Stretch` / `.Center` / `.End`; `=LayoutJustifyContent.Center` / `.End` / `.SpaceBetween`;
  `LayoutOverflowY: =LayoutOverflow.Scroll`.
- **ModernText** - `Control: ModernText`. Inputs: AccessibleLabel, Align, AutoHeight, BorderColor, BorderStyle,
  BorderThickness, Color, ContentLanguage, DisplayMode, Fill, Font, FontWeight, Height, Italic, OnSelect,
  PaddingBottom, PaddingLeft, PaddingRight, PaddingTop, RadiusBottomLeft, RadiusBottomRight, RadiusTopLeft,
  RadiusTopRight, Size, Strikethrough, Text, Underline, VerticalAlign, Visible, Width, Wrap, X, Y. Literals:
  `Font: =Font.'Segoe UI'`; `FontWeight: =FontWeight.Bold` / `.Semibold` / `.Normal`; `Align: =Align.Center` /
  `.Right`; `VerticalAlign: =VerticalAlign.Middle`.
- **ModernButton** - `Control: ModernButton`. Inputs: AccessibleLabel, Align, Appearance, BasePaletteColor,
  BorderColor, BorderStyle, BorderThickness, Color, ContentLanguage, DisplayMode, Font, FontWeight, Height, Icon,
  IconRotation, IconStyle, Italic, Layout, OnSelect, PaddingBottom, PaddingLeft, PaddingRight, PaddingTop,
  RadiusBottomLeft, RadiusBottomRight, RadiusTopLeft, RadiusTopRight, Size, Strikethrough, Text, Tooltip, Underline,
  VerticalAlign, Visible, Width, X, Y. Literals (Enum ButtonAppearance): `=ButtonAppearance.Primary` / `.Secondary` /
  `.Subtle`; `Layout: =ButtonLayout.IconBefore` / `.IconAfter` / `.TextOnly`; `=DisplayMode.Disabled` / `.Edit`.
  AutoLayout defaults 280 x 64: always set Width = LayoutMinWidth and LayoutMinHeight 0.
- **ModernIcon** - `Control: ModernIcon`. Inputs: AccessibleLabel, BasePaletteColor, BorderColor, BorderStyle,
  BorderThickness, ContentLanguage, DisplayMode, Fill, Height, Icon, IconColor, IconStyle, OnSelect, PaddingBottom,
  PaddingLeft, PaddingRight, PaddingTop, RadiusBottomLeft, RadiusBottomRight, RadiusTopLeft, RadiusTopRight,
  Rotation, Tooltip, Visible, Width, X, Y. Icon names are Text (`="Edit"`, `="Delete"`, `="ArrowReset"`,
  `="Warning"`, `="CheckmarkCircle"`, `="Dismiss"`).
- **Badge** - `Control: Badge`. Inputs: AccessibleLabel, Align, Appearance, BasePaletteColor, Content,
  ContentLanguage, DisplayMode, Font, FontColor, FontItalic, FontSize, FontStrikethrough, FontUnderline, FontWeight,
  Height, Shape, ThemeColor, VerticalAlign, Visible, Width, X, Y. Literals: `='BadgeCanvas.Appearance'.Tint`,
  `='BadgeCanvas.Shape'.Rounded`, `='BadgeCanvas.ThemeColor'.Success` / `.Warning` / `.Brand` / `.Danger` /
  `.Informative` / `.Subtle`.
- **Gallery** - `Control: Gallery`, `Variant: Vertical`. Inputs: AccessibleLabel, BorderColor, BorderStyle,
  BorderThickness, ContentLanguage, Default, DelayItemLoading, DisplayMode, Fill, FocusedBorderColor,
  FocusedBorderThickness, Height, Items, LoadingSpinner, LoadingSpinnerColor, NavigationStep, Selectable,
  ShowNavigation, ShowScrollbar, TabIndex, TemplatePadding, TemplateSize, Transition, Visible, Width, WrapCount, X, Y.
  Outputs: AllItems, AllItemsCount, Selected, TemplateHeight, TemplateWidth. No OnSelect / TemplateFill.
- **ModernTextInput** - `Control: ModernTextInput`. Inputs: AccessibleLabel, Align, Appearance, BasePaletteColor,
  BorderColor, BorderStyle, BorderThickness, Color, ContentLanguage, Default, DisplayMode, Fill, Font, FontWeight,
  Height, Italic, MaxLength, OnChange, Padding*, Placeholder, Radius*, Required, Size, Strikethrough, TriggerOutput,
  Type, Underline, ValidationState, Visible, Width, X, Y. Output: Text. Literals: `=Appearance.Outline`,
  `=TriggerOutput.Delayed`, `=TextInputType.Search`. AutoLayout defaults 560 x 64 (override).
- **ModernDropdown** - `Control: ModernDropdown`. Inputs: AccessibleLabel, Appearance, BasePaletteColor, BorderColor,
  BorderStyle, BorderThickness, Color, ContentLanguage, Default, DisplayMode, Fill, Font, FontWeight, Height, Italic,
  ItemDisplayText, Items, OnChange, Padding*, Radius*, Required, Size, Strikethrough, Underline, ValidationState,
  Visible, Width, X, Y. Output: Selected. AutoLayout defaults 560 x 64 (override).
- **Sidebar / TopBar** - `Control: CanvasComponent` + `ComponentName: Sidebar` (inputs activemenu, AlignInContainer,
  Fill, FillPortions, Height, LayoutMaxHeight, LayoutMaxWidth, LayoutMinHeight, LayoutMinWidth, Visible, Width, X, Y)
  / `ComponentName: TopBar` (inputs ActiveMenu, Subtitle + the same generic inputs).
