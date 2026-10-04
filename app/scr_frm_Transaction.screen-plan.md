# Screen Plan: Transaction Form

## Assignment

- Action: Modify (rewrite layout; keep YAML key, Form5 with every card, Combobox1_1, TextInput12_1, Button15,
  Gallery7, Button32, Button32_1)
- Target file: `C:\Project\Powerapps\app\scr_frm_Transaction.pa.yaml`
- YAML key: scr_frm_Transaction
- Control name prefix: TrxF

Read `C:\Project\Powerapps\app\canvas-app-shared.md` first (Shell, Card, Toolbar, Table, Form screen pattern).

## Current State

`con_Main_trans_1` shell (Sidebar "Transaction", TopBar "Add Transaction") -> `Container8_1`:
- Button bar `Container12` at the TOP: Button32 (`SubmitForm(Form5)`, Text Update/Confirm), Button32_1
  (`ResetForm(Form5); Clear(colTempDetails); Back();`).
- ManualLayout `Container26` with `Form5` (Modern, Vertical, DataSource `dis_trx_headers`,
  Item `=Gallery8_1.Selected`, NumberOfColumns 2, Height 380). Cards (X, Y, Width): transaction_number_DataCard1
  (0,0,443; DataCardValue4 auto-number Default, DisplayMode View), type_DataCard1 (1,0,443; DataCardValue7
  ModernCombobox), area_form_DataCard1 (0,1,443; DataCardValue9 Classic/ComboBox visible for Transfer/Consume),
  area_to_DataCard1 (1,1,443; DataCardValue33 ModernCombobox visible for Transfer/Receive), note_DataCard1
  (0,2,898 multiline).
- Cart `Container27`: picker `Container28` (Label37 "Item" + Combobox1_1 `Items: =dis_item_v2S`; Label37_1
  "Quantity" + TextInput12_1; spacer; Button15 "Add Item") and list `Container32` (Text4* header, ManualLayout
  `Container34` with `Gallery7` `Items: =colTempDetails`, TemplateSize 30, rows Text4_7 name, Text4_8 Qty, Text4_9
  description, spacer, Button30_2 "Delete" `Remove(colTempDetails, ThisItem)`).

Form5.OnSuccess (approved constraint: logic must stay IDENTICAL): (1) RemoveIf old details of
`Form5.LastSubmit`; (2) ForAll colTempDetails Patch new dis_trx_details (header_id, PK number/Urutan, item, qty);
(3) `With({varTrxType, recAreaFrom, recAreaTo, idAreaFrom, idAreaTo}, ForAll(colTempDetails As TempRecord, ...))`
Receive/Transfer adds to (or creates) the `idAreaTo` stock row, Consume/Transfer subtracts from the `idAreaFrom`
stock row; (4) `Clear(colTempDetails); Notify("Transaksi berhasil disimpan & Stok terupdate!", ...); Back();`.

Button15.OnSelect (preserved verbatim):
```
=Collect(
    colTempDetails, 
    {
        // Generate nomor urut otomatis (1, 2, 3, dst.)
        Urutan: CountRows(colTempDetails) + 1,
        
        Id: Combobox1_1.Selected.dis_item_v2, 
        name: Combobox1_1.Selected.name, 
        description :  Combobox1_1.Selected.description,
        Qty: Value(TextInput12_1.Text)
    }
);
Reset(Combobox1_1);
Reset(TextInput12_1);
```

## Changes

1. Screen Properties: `Fill: =clrBg`, `LoadingSpinnerColor: =clrAccent`. Screen `Children:` = `conTrxFRoot` only.
2. Shell pattern with prefix TrxF: conTrxFRoot, cmpTrxFSidebar (`activemenu: ="Transaction"`), conTrxFMain,
   cmpTrxFTopBar (`ActiveMenu: =If(Form5.Mode = FormMode.Edit, "Edit Transaksi", "Transaksi Baru")`,
   `Subtitle: ="Header transaksi dan keranjang item"`), conTrxFBody.
3. Form screen pattern extended with a cart card between the form card and the actions bar.
4. Form5.OnSuccess: copy the CURRENT formula character-for-character, then insert exactly ONE statement (the
   receipt below) on its own line(s) immediately before the line `// 4. Bersihkan Keranjang & Notifikasi`.
   Nothing else in OnSuccess changes (no reformatting, no renamed variables). The W6 session first copies the
   original formula into "Catatan tambahan" of LANJUTAN-MODERNISASI.md and diffs after editing.
5. Cart add button gains a DisplayMode gate; cart remove becomes an icon.

## Controls to Add

conTrxFBody children (FillPortions 0, AlignInContainer Stretch):

1. `conTrxFFormCard` - Card pattern, Height 368, LayoutGap 12:
   - `txtTrxFCardTitle` card title "Header Transaksi".
   - `Form5` (moved), Height 300.
2. `conTrxFCartCard` - Card pattern, Height 396, LayoutGap 12:
   - `conTrxFCartHead` AutoLayout Horizontal, Height 24, LayoutAlignItems Center, transparent, DropShadow None,
     Radius 0 x4: `txtTrxFCartTitle` card title "Keranjang Item" FP 1; `txtTrxFCartCount` W 120, Size 13 Semibold
     clrTextMuted, Align Right, `Text: =Text(CountRows(colTempDetails)) & " item"`.
   - `conTrxFPicker` (Toolbar pattern, Height 56):
     - `conTrxFItemFld` FillPortions 1, LayoutMinWidth 0: `txtTrxFItemLbl` "Item" + `Combobox1_1` (kept;
       Items `=dis_item_v2S`, ItemDisplayText `=ThisItem.name` unchanged; `InputTextPlaceholder: ="Pilih item"`,
       `IsSearchable: =true`, `SelectMultiple: =false`, AccessibleLabel "Pilih item"; Height 36, LayoutMin* 0,
       Appearance Outline, Size 13, Radius 8 x4).
     - `conTrxFQtyFld` W 120: `txtTrxFQtyLbl` "Qty" + `TextInput12_1` (kept ModernTextInput; `Placeholder: ="0"`,
       `Align: =Align.Right`, AccessibleLabel "Jumlah item"; toolbar input styling).
     - `Button15` (kept) Primary, Icon "Add", Text "Tambah ke Keranjang", W 196, AlignInContainer End,
       OnSelect verbatim (above),
       `DisplayMode: =If(IsBlank(Combobox1_1.Selected) || Coalesce(Value(TextInput12_1.Text), 0) <= 0, DisplayMode.Disabled, DisplayMode.Edit)`.
   - `conTrxFCartTable` AutoLayout Vertical, Height 260, LayoutGap 4, transparent:
     - `conTrxFCartCols` header: `txtTrxFHName` "ITEM" FP 3, `txtTrxFHQty` "QTY" W 64, `txtTrxFHDesc`
       "DESKRIPSI" FP 4, `txtTrxFHAct` "" W 32.
     - `Gallery7` (kept) Gallery pattern, `Items: =colTempDetails`, Height 220, TemplateSize 44,
       AccessibleLabel "Keranjang item", `Visible: =!IsEmpty(colTempDetails)`. Row `conTrxFCartRow`:
       - `txtTrxFCartName` `=ThisItem.name`, Semibold, FP 3.
       - `txtTrxFCartQty` `=Text(ThisItem.Qty)`, W 64, Align Right.
       - `txtTrxFCartDesc` `=ThisItem.description`, FP 4.
       - `icoTrxFCartDel` ModernIcon "Delete" 32 x 32, IconColor clrDanger, Padding 6 x4, Radius 6 x4,
         Tooltip/AccessibleLabel `="Hapus " & ThisItem.name & " dari keranjang"`,
         `OnSelect: =Remove(colTempDetails, ThisItem)`.
     - `txtTrxFCartEmpty` "Keranjang masih kosong. Pilih item dan qty, lalu klik Tambah ke Keranjang.",
       Height 220, `Visible: =IsEmpty(colTempDetails)`.
3. `conTrxFActions` - actions bar (Height 44, LayoutJustifyContent End, LayoutGap 12):
   - `Button32_1` (kept) Secondary, Icon "ArrowLeft", Text "Kembali", W 120, OnSelect unchanged
     (`ResetForm(Form5); Clear(colTempDetails); Back();`).
   - `Button32` (kept) Primary, `Icon: ="Save"`, Text "Simpan Transaksi", W 184, `OnSelect: =SubmitForm(Form5)`,
     AccessibleLabel "Simpan transaksi".

## Controls to Remove

con_Main_trans_1, con_sidebar_trans_1, com_sidebar_trans_1, con_content_trans_1, com_topbar_trans_1, Container8_1,
Container12, Container26, Container27, Container28, Container31, Label37, Container31_1, Label37_1, Container30,
Container32, Container33, Text4, Text4_1, Text4_3, Text4_4, Container34, Container4, Text4_7, Text4_8, Text4_9,
Container10, Button30_2 (-> icoTrxFCartDel). Keep Form5 (all cards + children), Combobox1_1, TextInput12_1,
Button15, Gallery7, Button32, Button32_1.

## Properties to Update

- `Form5`: keep Control/Variant/Layout, DataSource, `Item: =Gallery8_1.Selected`, NumberOfColumns 2. Set
  AlignInContainer Stretch, FillPortions 0, `Height: =300`, `Fill: =clrSurface`, `BorderThickness: =0`;
  delete X, Y, Width. OnSuccess = original + this statement inserted before `// 4. Bersihkan Keranjang & Notifikasi`:
  ```
  // Bukti simpan untuk strip receipt di scr_Transaction
  Set(
      gblReceipt,
      {
          Screen: "Transaction",
          Action: "Disimpan",
          Title: Form5.LastSubmit.transaction_number,
          Detail: "Tipe " & Text(Form5.LastSubmit.type) & " | Dari " & Coalesce(Form5.LastSubmit.area_form.Name, "-") & " | Ke " & Coalesce(Form5.LastSubmit.area_to.Name, "-") & " | Catatan " & Coalesce(Form5.LastSubmit.note, "-") & " | " & Text(CountRows(colTempDetails)) & " item"
      }
  );
  ```
  (It must come before step 4 because step 4 clears `colTempDetails`.)
- Card `Width` only: transaction_number_DataCard1, type_DataCard1, area_form_DataCard1, area_to_DataCard1
  `=Parent.Width / 2`; note_DataCard1 `=Parent.Width`. Keep DataCardValue4 auto-number Default, both area
  `Visible` formulas, WidthFit, X/Y and all children unchanged.

## Layout and Visual Impact

- Form card 16 + 24 + 12 + 300 + 16 = 368. Cart card 16 + 24 + 12 + 56 + 12 + 260 + 16 = 396.
  Body 368 + 16 + 396 + 16 + 44 = 840 > 532 -> body scrolls; actions bar is the last child.
- Picker: 120 + 196 + 2 x 8 = 332 -> item combobox 500.
- Cart row inner 806: fixed 64 + 32 + 3 x 8 = 120 -> FP 7 -> 98 (name 294, description 392).

## Required Record Fields

| Field key | Record surface | Required field | Source field | Bound control | Exact formula | Placement and visibility |
| --- | --- | --- | --- | --- | --- | --- |
| cart/row/name | Gallery7 row | Item name | colTempDetails.name | txtTrxFCartName | `=ThisItem.name` | FP 3 Semibold |
| cart/row/qty | row | Qty | Qty | txtTrxFCartQty | `=Text(ThisItem.Qty)` | W 64 |
| cart/row/desc | row | Description | description | txtTrxFCartDesc | `=ThisItem.description` | FP 4 |

## Required Actions

| Action | Preconditions | Entry point and event | Source and stable ID | Transition and postcondition | Mutation write set | Receipt proof set | Observer and evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ACT-TRX-CART-ADD | item selected, qty > 0 | Button15.OnSelect (gated) | colTempDetails.Urutan | line appended; picker reset | Urutan, Id, name, description, Qty | Gallery7 row | Gallery7, txtTrxFCartCount |
| ACT-TRX-CART-REMOVE | line exists | icoTrxFCartDel.OnSelect | colTempDetails row | line removed | existence | count | txtTrxFCartCount |
| ACT-TRX-SAVE | Form5 valid (number, type required) | Button32.OnSelect -> Form5.OnSuccess | Form5.LastSubmit.dis_trx_header | header saved, details rewritten, stock +/- by type, cart cleared, Back() | header fields, dis_trx_details, dis_stocks.qty | Title number; Detail Tipe, Dari, Ke, Catatan, N item | conTrxLReceipt; Gallery8_1; Gallery8_9 stock on scr_find_item |

## Functional Test Scenarios

| Scenario | Given | When | Then | Evidence surface | Boundary or negative case |
| --- | --- | --- | --- | --- | --- |
| SCN-TRX-CART | item Bentonite, qty 3 | Tambah ke Keranjang | colTempDetails +1 (Qty 3) | Gallery7 row, "1 item" | button disabled with no item, blank qty or qty 0 |
| SCN-TRX-CART-REMOVE | 2 lines | delete icon on line 1 | 1 line left | Gallery7, "1 item" | N/A |
| SCN-TRX-SAVE-RECEIVE | S1 (Bentonite @ Yard A) qty 10 | New Receive to Yard A, Bentonite 3, Simpan Transaksi | header + 1 line; S1.qty = 13 | conTrxLReceipt "Tipe Receive, Ke Yard A, 1 item"; scr_find_item S1 = 13 | Receive to an area without stock row creates a new row |

## Relevant Data Source Schemas

dis_trx_headers: transaction_number (required), type (option set, required), area_form (logical cr8a3_area_from),
area_to, note, dis_trx_header. dis_trx_details: header_id, item, qty, PK. dis_stocks: dis_item_v2, dis_area, qty, PK.
dis_item_v2S: name, description, dis_item_v2. Globals: colTempDetails `{Urutan, Id, name, description, Qty}`,
gblReceipt.

## Required Variants

GroupContainer -> AutoLayout. Gallery -> Vertical (unchanged). Form -> Modern (unchanged). TypedDataCard variants
unchanged (ModernTextualEdit, ModernComboBoxOptionSetSingleEdit, PcfCoreComboBoxEditCard,
ModernTextualMultilineEdit).

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
- **ModernCombobox** - `Control: ModernCombobox`. Inputs: AccessibleLabel, AllowExternalSelectedItems, Appearance,
  BasePaletteColor, BorderColor, BorderStyle, BorderThickness, Color, ContentLanguage, DefaultSelectedItems,
  DelayOutput, DisplayMode, Fill, Font, FontWeight, Height, InputTextPlaceholder, IsSearchable, Italic,
  ItemDisplayText, Items, MultiValueDelimiter, OnChange, Padding*, Radius*, Required, SelectMultiple, Size,
  Strikethrough, Underline, ValidationState, Visible, Width, X, Y. Outputs: SearchText, Selected, SelectedItems.
- **Form** (existing, preserved) - `Control: Form`, `Variant: Modern`, `Layout: Vertical`. Inputs: AcceptsFocus,
  BorderColor, BorderStyle, BorderThickness, ContentLanguage, DataSource, DefaultMode, Fill, FocusedBorderColor,
  FocusedBorderThickness, Height, Item, NumberOfColumns, OnFailure, OnReset, OnSuccess, SnapToColumns, Visible,
  Width, X, Y. Outputs: Error, ErrorKind, LastSubmit, Mode, Unsaved, Updates, Valid. TypedDataCards and their
  children (Classic/ComboBox, FluentV8/Label, Label, Image, AddMedia, Modern inputs) are preserved as-is; only
  card `Width` changes. Do not create data cards.
- **Sidebar / TopBar** - `Control: CanvasComponent` + `ComponentName: Sidebar` (inputs activemenu, AlignInContainer,
  Fill, FillPortions, Height, LayoutMaxHeight, LayoutMaxWidth, LayoutMinHeight, LayoutMinWidth, Visible, Width, X, Y)
  / `ComponentName: TopBar` (inputs ActiveMenu, Subtitle + the same generic inputs).
