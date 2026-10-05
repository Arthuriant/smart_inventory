# Screen Plan: Consume

## Assignment

- Action: Modify (rewrite layout; keep YAML key and the functional controls listed below; bug fix)
- Target file: `C:\Project\Powerapps\app\scr_consume.pa.yaml`
- YAML key: scr_consume
- Control name prefix: Cons

Read `C:\Project\Powerapps\app\canvas-app-shared.md` first (Shell, Card, Toolbar, Table, Named State
`colConsumeReceipt`, `locConsHeader`, `locShowConsReceipt`).

## Current State

`con_Main_template_7` shell (Sidebar "Consume", TopBar "Consume") -> `Container8_9` -> `Container13_7`: toolbar
`Container15_7` (dd_Category_1, dd_Geounit_1, dd_Location_1, dd_Area_1, spacer, inp_search_8 - no cascade resets),
Label header `Container20_9` "Item available", ManualLayout `Container10_10` with `Gallery8_11`
(`Variant: BrowseLayout_Vertical_OneTextOneImageVariant_ver5.0`, WrapCount 3 tiles: Image4, Title5_1 stock,
Title5 name, Separator5, Rectangle21, NumberInput1 qty). Screen-level `Button38` "Consume" (absolute) runs the
consume formula.

Preserved logic:
- Dropdown Items / ItemDisplayText: dd_Category_1 (`=dis_category_items`, `=ThisItem.code`), dd_Geounit_1
  (`=dis_geounits`, `=ThisItem.elv_name_long`), dd_Location_1 (Filter dis_locations by dd_Geounit_1), dd_Area_1
  (Filter dis_areas by dd_Location_1), all `ThisItem.Name` for location/area.
- Gallery8_11 Items (3-clause Filter over dis_stocks: category, area, StartsWith name/part_number on inp_search_8).
- Button38: area check, qty check, number generation
  (`First(Sort(dis_trx_headers, 'Created On', SortOrder.Descending)).transaction_number` ->
  `Text(Now(), "dd/mm/yy/") & Text(varNextIndex, "0000")`), header Patch, per-line detail Patch
  (`PK: varTrxNumber & "-" & Text(RandBetween(1000, 9999))`, `item: ItemConsume.dis_item_v2`), stock Patch,
  `Reset(Gallery8_11)`, Notify.

Bugs (approved fixes): header Patch writes only `transaction_number` (missing `type` Consume and `area_form`);
qty greater than stock is not blocked; stock Patch uses the stale gallery value `ItemConsume.qty`.

## Changes

1. Screen Properties: `Fill: =clrBg`, `LoadingSpinnerColor: =clrAccent`. Screen `Children:` = `conConsRoot` only.
2. Shell pattern with prefix Cons: conConsRoot, cmpConsSidebar (`activemenu: ="Consume"`), conConsMain,
   cmpConsTopBar (`ActiveMenu: ="Consume"`, `Subtitle: ="Pakai barang dari stok area"`), conConsBody.
3. Keep dd_Category_1, dd_Geounit_1, dd_Location_1, dd_Area_1, inp_search_8, Gallery8_11 (Items verbatim).
   Gallery8_11 changes to `Variant: Vertical` (table rows instead of tiles; remove WrapCount). NumberInput1 is
   replaced by row control `numConsQty`; Button38 becomes `btnConsSubmit` in the card footer.
4. Cascade resets + DisplayMode gates on the location / area dropdowns (same pattern as Area).
5. Bug-fixed submit: header gets `type` Consume + `area_form`; qty > stock blocked by DisplayMode gate and by a
   handler guard; stock decrease reads a fresh LookUp; per-line receipt in `colConsumeReceipt`.

## Controls to Add

conConsBody children (FillPortions 0, AlignInContainer Stretch):

1. `conConsReceipt` - AutoLayout Vertical, Height 228, `Visible: =locShowConsReceipt`, Fill clrSuccessTint,
   BorderColor RGBA(180, 222, 196, 1), BorderThickness 1, Radius 10 x4, Padding 12 x4, LayoutGap 8,
   LayoutAlignItems Stretch, DropShadow None. Children:
   - `conConsRcHead` AutoLayout Horizontal, Height 44, LayoutGap 12, LayoutAlignItems Center, transparent:
     - `icoConsRcIco` ModernIcon "CheckmarkCircle" 24 x 24, IconColor clrSuccess.
     - `conConsRcText` AutoLayout Vertical, FP 1, Height 40, LayoutGap 2, LayoutJustifyContent Center:
       `txtConsRcTitle` `Text: ="Consume tersimpan - " & locConsHeader.Number` (13 Bold clrText, Height 20);
       `txtConsRcSub` `Text: ="Tipe " & locConsHeader.Type & " | Area " & locConsHeader.Area & " | " & Text(locConsHeader.Lines) & " item"`
       (12 clrTextMuted, Height 18).
     - `icoConsRcClose` ModernIcon "Dismiss" 32 x 32, IconColor clrTextMuted, Padding 6 x4, Tooltip "Tutup",
       `OnSelect: =UpdateContext({locShowConsReceipt: false}); Clear(colConsumeReceipt)`.
   - `conConsRcTable` AutoLayout Vertical, Height 152, LayoutGap 4, transparent:
     - `conConsRcCols` header (Table header pattern but Height 28): `txtConsRcHItem` "ITEM" FP 3,
       `txtConsRcHOp` "OPERASI" W 88, `txtConsRcHOld` "STOK AWAL" W 88, `txtConsRcHAmt` "JUMLAH" W 80,
       `txtConsRcHExp` "EKSPEKTASI" W 96, `txtConsRcHAct` "AKTUAL" W 80.
     - `galConsReceipt` Gallery Vertical, `Items: =colConsumeReceipt`, Height 120, TemplateSize 32,
       TemplatePadding 1, Fill clrBorder, Selectable false, AccessibleLabel "Hasil consume per item".
       Row `conConsRcRow` (row shell, Fill clrSurface): `txtConsRcItem` `=ThisItem.ItemName` FP 3 Semibold;
       `txtConsRcOp` `=ThisItem.Operation` W 88; `txtConsRcOld` `=Text(ThisItem.OldQty)` W 88;
       `txtConsRcAmt` `=Text(ThisItem.Amount)` W 80; `txtConsRcExp` `=Text(ThisItem.ExpectedQty)` W 96;
       `txtConsRcAct` `=Text(ThisItem.ActualQty)` W 80, Semibold,
       `Color: =If(ThisItem.ActualQty = ThisItem.ExpectedQty, clrSuccess, clrDanger)`.
2. `conConsCard` - Card pattern, Height 508, LayoutGap 12:
   - `conConsToolbar` (Toolbar pattern):
     - `conConsCatFld` W 140: `txtConsCatLbl` "Kategori" + `dd_Category_1` (AccessibleLabel "Filter kategori").
     - `conConsGeoFld` W 140: `txtConsGeoLbl` "Geounit" + `dd_Geounit_1`,
       `OnChange: =Reset(dd_Location_1); Reset(dd_Area_1)`.
     - `conConsLocFld` W 140: `txtConsLocLbl` "Location" + `dd_Location_1`, `OnChange: =Reset(dd_Area_1)`,
       `DisplayMode: =If(IsBlank(dd_Geounit_1.Selected), DisplayMode.Disabled, DisplayMode.Edit)`.
     - `conConsAreaFld` W 140: `txtConsAreaLbl` "Area (From)" + `dd_Area_1`,
       `DisplayMode: =If(IsBlank(dd_Location_1.Selected), DisplayMode.Disabled, DisplayMode.Edit)`.
     - `conConsSearchFld` FillPortions 1, LayoutMinWidth 0: `txtConsSearchLbl` "Cari item" + `inp_search_8`
       (Delayed; `Placeholder: ="Nama atau BPN"`, `Type: =TextInputType.Search`; drop empty `Default: =`).
     - `icoConsReset` reset icon,
       `OnSelect: =Reset(dd_Category_1); Reset(dd_Geounit_1); Reset(dd_Location_1); Reset(dd_Area_1); Reset(inp_search_8)`.
   - `conConsTable` AutoLayout Vertical, Height 352, LayoutGap 4, transparent:
     - `conConsHead`: `txtConsHItem` "ITEM" FP 3, `txtConsHArea` "AREA" FP 2, `txtConsHStock` "STOK" W 88,
       `txtConsHWarn` "" W 120, `txtConsHQty` "QTY PAKAI" W 120.
     - `Gallery8_11` (kept, `Variant: Vertical`) Gallery pattern, Height 312, TemplateSize 68, Items verbatim,
       AccessibleLabel "Stok yang bisa dipakai", `Visible: =!IsEmpty(<same Items expression>)`.
       Row `conConsRow`:
       - `conConsRowName` AutoLayout Vertical, FP 3, Height 40, LayoutGap 2, AlignInContainer Center:
         `txtConsName` `=ThisItem.dis_item_v2.name` (13 Semibold, H 20); `txtConsBpn`
         `="BPN " & Coalesce(ThisItem.dis_item_v2.part_number, "-")` (12 clrTextMuted, H 18).
       - `txtConsArea` `=ThisItem.dis_area.Name`, FP 2.
       - `bdgConsStock` Badge W 88, `Content: =Text(ThisItem.qty) & " " & Text(ThisItem.dis_item_v2.uom)`,
         `ThemeColor: =If(ThisItem.qty <= 0, 'BadgeCanvas.ThemeColor'.Danger, 'BadgeCanvas.ThemeColor'.Informative)`.
       - `txtConsWarn` W 120, Size 12 Semibold, `Color: =clrDanger`, `Text: ="Qty melebihi stok"`,
         `Visible: =numConsQty.Value > ThisItem.qty`.
       - `conConsQtyFld` AutoLayout Vertical, W 120, Height 56, LayoutGap 4, AlignInContainer Center:
         `txtConsQtyLbl` "Qty pakai" (field label style) + `numConsQty` ModernNumberInput (Height 36, LayoutMin* 0,
         FillPortions 0, AlignInContainer Stretch, Appearance Outline, Size 13, Radius 8 x4, `Default: =0`,
         `Min: =0`, `Step: =1`, AccessibleLabel `="Qty pakai " & ThisItem.dis_item_v2.name`,
         `ValidationState: =If(Self.Value > ThisItem.qty || Self.Value < 0, ValidationState.Error, ValidationState.None)`).
     - `txtConsEmpty` "Tidak ada stok yang cocok dengan filter.", Height 312, `Visible: =IsEmpty(<same Items expression>)`.
   - `conConsFooter` AutoLayout Horizontal, Height 44, LayoutGap 12, LayoutAlignItems Center, transparent:
     - `txtConsSummary` FP 1, Size 13 clrTextMuted,
       `Text: =Text(CountRows(Filter(Gallery8_11.AllItems, numConsQty.Value > 0))) & " item dipilih" & If(IsBlank(dd_Area_1.Selected), " - pilih Area (From) dulu", "")`.
     - `btnConsSubmit` Primary, Icon "Cart", Text "Consume", W 140,
       `DisplayMode` (`|-`):
       ```
       =If(
           IsBlank(dd_Area_1.Selected) ||
           CountRows(Filter(Gallery8_11.AllItems, numConsQty.Value > 0)) = 0 ||
           CountRows(Filter(Gallery8_11.AllItems, numConsQty.Value > qty || numConsQty.Value < 0)) > 0,
           DisplayMode.Disabled,
           DisplayMode.Edit
       )
       ```
       OnSelect (`|-`; original structure with the bug fixes marked FIX):
       ```
       =// 1. Validasi: Area dipilih, ada qty, dan tidak ada qty > stok
       If(
           IsBlank(dd_Area_1.Selected),
           Notify("Silakan pilih Area (From) terlebih dahulu!", NotificationType.Error),

           CountRows(Filter(Gallery8_11.AllItems, numConsQty.Value > 0)) = 0,
           Notify("Masukkan jumlah (Qty) pada minimal 1 barang yang ingin digunakan!", NotificationType.Error),

           // FIX: qty melebihi stok diblokir
           CountRows(Filter(Gallery8_11.AllItems, numConsQty.Value > qty || numConsQty.Value < 0)) > 0,
           Notify("Qty melebihi stok yang tersedia!", NotificationType.Error),

           // 2. Generate Nomor Transaksi (Autogenerate)
           With(
               {
                   varLastTrx: First(Sort(dis_trx_headers, 'Created On', SortOrder.Descending)).transaction_number
               },
               With(
                   {
                       varNextIndex: If(IsBlank(varLastTrx), 1, Value(Right(varLastTrx, 4)) + 1)
                   },
                   With(
                       {
                           varTrxNumber: Text(Now(), "dd/mm/yy/") & Text(varNextIndex, "0000")
                       },
                       // 3. Simpan Header Transaksi (FIX: tipe Consume + area asal)
                       With(
                           {
                               newHeader: Patch(
                                   dis_trx_headers,
                                   Defaults(dis_trx_headers),
                                   {
                                       transaction_number: varTrxNumber,
                                       type: 'type (dis_trx_headers)'.Consume,
                                       area_form: dd_Area_1.Selected
                                   }
                               )
                           },
                           Clear(colConsumeReceipt);
                           // 4. Looping untuk setiap barang di galeri yang Qty-nya diisi
                           ForAll(
                               Filter(Gallery8_11.AllItems, numConsQty.Value > 0) As ItemConsume,
                               With(
                                   {
                                       // FIX: baca stok terbaru, bukan snapshot galeri
                                       oldQty: LookUp(dis_stocks, dis_stock = ItemConsume.dis_stock).qty,
                                       amt: ItemConsume.numConsQty.Value
                                   },
                                   // A. Simpan ke Detail Transaksi
                                   Patch(
                                       dis_trx_details,
                                       Defaults(dis_trx_details),
                                       {
                                           header_id: newHeader,
                                           PK: varTrxNumber & "-" & Text(RandBetween(1000, 9999)),
                                           item: ItemConsume.dis_item_v2,
                                           qty: amt
                                       }
                                   );
                                   // B. Kurangi stok + catat bukti
                                   With(
                                       {
                                           updated: Patch(
                                               dis_stocks,
                                               LookUp(dis_stocks, dis_stock = ItemConsume.dis_stock),
                                               {qty: oldQty - amt}
                                           )
                                       },
                                       Collect(
                                           colConsumeReceipt,
                                           {
                                               StockId: ItemConsume.dis_stock,
                                               ItemName: ItemConsume.dis_item_v2.name,
                                               Operation: "Consume",
                                               OldQty: oldQty,
                                               Amount: amt,
                                               ExpectedQty: oldQty - amt,
                                               ActualQty: updated.qty
                                           }
                                       )
                                   )
                               )
                           );
                           // 5. Bukti, bersihkan input, notifikasi
                           UpdateContext(
                               {
                                   locConsHeader: {
                                       Number: newHeader.transaction_number,
                                       Type: Text(newHeader.type),
                                       Area: dd_Area_1.Selected.Name,
                                       Lines: CountRows(colConsumeReceipt)
                                   },
                                   locShowConsReceipt: true
                               }
                           );
                           Reset(Gallery8_11);
                           Notify("Transaksi Consume berhasil dan stok telah dikurangi!", NotificationType.Success)
                       )
                   )
               )
           )
       )
       ```

## Controls to Remove

con_Main_template_7, con_sidebar_template_7, com_sidebar_template_7, con_content_template_7, com_topbar_template_7,
Container8_9, Container13_7, Container15_7, Container16_7, Container20_9, Label21_57, Container10_10, Image4,
Title5_1, Title5, Separator5, Rectangle21, NumberInput1 (-> numConsQty), Button38 (-> btnConsSubmit).
Keep dd_Category_1, dd_Geounit_1, dd_Location_1, dd_Area_1, inp_search_8, Gallery8_11.

## Properties to Update

- Screen: Fill, LoadingSpinnerColor.
- Dropdowns / inp_search_8: Toolbar styling; drop X/Y/Width; Items / ItemDisplayText unchanged; OnChange /
  DisplayMode as listed.
- Gallery8_11: `Variant: Vertical`; remove WrapCount, X, Y, Width; Gallery pattern props; Items unchanged.

## Layout and Visual Impact

- Toolbar: 4 x 140 + 36 + 5 x 8 = 636 -> search 196 (plan budget used 32 for the icon; 36 per shared pattern still
  fits 832).
- Card: 16 + 56 + 12 + 352 + 12 + 44 + 16 = 508 <= 532. Table 36 + 4 + 312 (4.5 rows of 68).
- Row inner 806: fixed 88 + 120 + 120 + 4 x 8 = 360 -> FP 5 -> 89 (item 267, area 178).
- Receipt 12 + 44 + 8 + 152 + 12 = 228, shown above the card after a successful Consume (body scrolls).

## Required Record Fields

| Field key | Record surface | Required field | Source field | Bound control | Exact formula | Placement and visibility |
| --- | --- | --- | --- | --- | --- | --- |
| cons/row/name | Gallery8_11 row | Item name | dis_item_v2.name | txtConsName | `=ThisItem.dis_item_v2.name` | FP 3 line 1 |
| cons/row/bpn | row | BPN | dis_item_v2.part_number | txtConsBpn | `="BPN " & Coalesce(ThisItem.dis_item_v2.part_number, "-")` | line 2 |
| cons/row/area | row | Area | dis_area.Name | txtConsArea | `=ThisItem.dis_area.Name` | FP 2 |
| cons/row/stock | row | Stock | qty | bdgConsStock | `Content: =Text(ThisItem.qty) & " " & Text(ThisItem.dis_item_v2.uom)` | W 88 |
| cons/row/qty | row | Qty input | input | numConsQty | `Default: =0` | W 120 with label |
| cons/rc/* | galConsReceipt row | Item, Operation, Old, Amount, Expected, Actual | colConsumeReceipt | txtConsRc* | see above | 6 columns |

## Required Actions

| Action | Preconditions | Entry point and event | Source and stable ID | Transition and postcondition | Mutation write set | Receipt proof set | Observer and evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ACT-CONSUME-FILTER | none | 4 dropdowns (cascade OnChange), inp_search_8, icoConsReset | dis_stocks | Gallery8_11 filtered | N/A | N/A | Gallery8_11, txtConsEmpty |
| ACT-CONSUME-SUBMIT | area selected, >= 1 qty > 0, no qty > stock | btnConsSubmit (gated) | ItemConsume.dis_stock per line; newHeader.dis_trx_header | header {number, type Consume, area_form}; details; stock = fresh old - amount; inputs reset | header 3 fields, detail rows, dis_stocks.qty | number, type, area, line count; per line operation / old / amount / expected / actual | conConsReceipt + galConsReceipt; Gallery8_9 on scr_find_item |

## Functional Test Scenarios

| Scenario | Given | When | Then | Evidence surface | Boundary or negative case |
| --- | --- | --- | --- | --- | --- |
| SCN-CONSUME-FILTER | S1, S2 in Yard A; S3 in Yard B | choose Area Yard A | S1, S2 shown, S3 hidden | Gallery8_11 | reset restores all |
| SCN-CONSUME-OK | S1 qty 13, Area Yard A | qty 2 on S1, Consume | header type Consume, area_form Yard A; detail qty 2; S1.qty = 11 | conConsReceipt "Tipe Consume, Area Yard A, 1 item"; row Consume / 13 / 2 / 11 / 11 | N/A |
| SCN-CONSUME-BLOCKED | Area blank, OR all qty 0, OR S1 qty 13 with input 20 | look at Consume | btnConsSubmit Disabled; "Qty melebihi stok" visible for 20; nothing written | btnConsSubmit.DisplayMode, txtConsWarn, numConsQty ValidationState | handler guard repeats all three checks |
| SCN-CONSUME-COMPOUND | S1 qty 10 | Receive 3 via Form5 (-> 13), then Consume 2 here | S1.qty = 11; receipt old = 13 (fresh LookUp) | galConsReceipt OldQty 13, ActualQty 11 | N/A |

## Relevant Data Source Schemas

dis_stocks: dis_item_v2 (-> dis_item_v2S: name, part_number, uom, dis_category_item), dis_area (-> dis_areas .Name,
.dis_area), qty, dis_stock (Guid), PK. dis_trx_headers: transaction_number, type (`'type (dis_trx_headers)'.Consume`),
area_form (-> dis_areas), 'Created On'. dis_trx_details: header_id, item, qty, PK. Filters: dis_category_items,
dis_geounits, dis_locations, dis_areas. State: colConsumeReceipt `{StockId, ItemName, Operation, OldQty, Amount,
ExpectedQty, ActualQty}`, locConsHeader `{Number, Type, Area, Lines}`, locShowConsReceipt (Boolean).

## Required Variants

GroupContainer -> AutoLayout. Gallery -> Vertical (Gallery8_11 changes from BrowseLayout_Vertical_OneTextOneImage
to Vertical; galConsReceipt new Vertical).

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
- **ModernNumberInput** - `Control: ModernNumberInput`. Inputs: AccessibleLabel, Align, Appearance, BasePaletteColor,
  BorderColor, BorderStyle, BorderThickness, Color, ContentLanguage, Default, DisplayMode, Fill, Font, FontWeight,
  Height, HintText, Italic, Max, Min, OnChange, Padding*, Precision, Radius*, Size, Step, Strikethrough, Underline,
  ValidationState, Visible, Width, X, Y. Output: Value. Literals: `=ValidationState.Error` / `.None`.
- **Sidebar / TopBar** - `Control: CanvasComponent` + `ComponentName: Sidebar` (inputs activemenu, AlignInContainer,
  Fill, FillPortions, Height, LayoutMaxHeight, LayoutMaxWidth, LayoutMinHeight, LayoutMinWidth, Visible, Width, X, Y)
  / `ComponentName: TopBar` (inputs ActiveMenu, Subtitle + the same generic inputs).

## Revisi 2026-10-05 (WEB): foto item + alur cepat teknisi

Logika Patch btnConsSubmit (header, detail, stok, receipt) TIDAK diubah. Perubahan hanya tampilan dan default filter:

- Baris galCons: `imgConsItem` (Image klasik, bukan ModernIcon; KOREKSI #7 aman) 56 x 56 di kolom pertama,
  `Image: =ThisItem.dis_item_v2.Image`, Fit, Fill abu muda sebagai placeholder kalau item tanpa foto,
  `OnSelect: =Select(Parent)`. Header tambah `txtConsHImg` "FOTO" W 56. `TemplateSize` 60 -> 72 (4,3 baris terlihat).
  Budget baris 806: tetap 56 + 88 + 120 + 120 + 5 x 8 = 424 -> FP 5 = 382 (item 229, area 153).
- Default filter dari area user (`nfMe.Assigned_area`): ddConsGeo = geounit lokasi area user, ddConsLoc = lokasi
  area user (hanya kalau geounit cocok), ddConsArea = area user (hanya kalau lokasi cocok). User tanpa Assigned_area
  -> kosong seperti sebelumnya. Reset filter kembali ke area user.
- `numConsQty.DisplayMode` Disabled kalau stok <= 0 (tidak bisa salah isi barang habis).
- Footer: `btnConsClear` Secondary "Kosongkan" (ArrowReset, W 132), `OnSelect: =Reset(galCons)`, Disabled kalau
  belum ada qty.

## Revisi 2026-10-05 (TERMINAL): grid kartu ala online shop

- galCons jadi grid: `WrapCount: =4`, `TemplateSize: =346`, `TemplatePadding: =8`, Fill RGBA(244, 246, 250, 1),
  Height 720 (2 baris kartu terlihat, sisanya scroll). conConsTable 720, conConsCard 508 -> 876 (body scroll).
- Header kolom `conConsHead` + `txtConsH*` dihapus (tidak cocok untuk grid).
- Kartu `conConsRow` (AutoLayout vertikal, Stretch, pad 8, gap 6, radius 12, Fill putih, border biru 2 kalau
  numConsQty > 0): imgConsItem 176 (Stretch, Fit), txtConsName 36 (nama, wrap 2 baris), bdgConsStock 24
  ("Stok n uom", Start, W 120), txtConsArea 16 ("BPN x · area", abu 11), numConsQty 32, txtConsWarn 16.
  Budget: 16 + 176 + 36 + 24 + 16 + 32 + 16 + 5 x 6 = 346. Tanpa container bersarang (KOREKSI #7).
- ModernText tidak punya Tooltip (compile menolak); jangan ditambahkan.
