# Screen Plan: History

## Assignment

- Action: Modify (rewrite layout; keep YAML key and the functional controls listed below)
- Target file: `C:\Project\Powerapps\app\scr_History.pa.yaml`
- YAML key: scr_History
- Control name prefix: Hist

Read `C:\Project\Powerapps\app\canvas-app-shared.md` first (Shell, Card, Toolbar, Table, Segmented type filter).

## Current State

`con_Main_trans_4` shell (Sidebar "History", TopBar "History") -> `Container8_7`:
- Header list `Container13_4`: toolbar `Container15_4` (Dropdown2_3 type `Choices(dis_trx_headers.type)`,
  inp_search_5, spacer, DatePicker2, Icon2 "Dismiss" `Reset(DatePicker2)`), Label header `Container20_5`,
  ManualLayout `Container10_6` with `Gallery8_7` (rows Text1_12 number, Text1_13 date, Type_18 type, Type_19
  area_to.Name, Type_20 note).
- Spacer `Container25_1`.
- Detail `Container13_5`: toolbar `Container15_5` (Dropdown2_4 category, inp_search_6 never wired), Label header
  `Container20_6`, ManualLayout `Container10_7` with `Gallery8_8` (rows Text1_14..Type_24).

Preserved logic:
- Gallery8_7 Items: `Search(Filter(dis_trx_headers, <type clause>, (IsBlank(DatePicker2.SelectedDate) Or ('Created On' >= DatePicker2.SelectedDate And 'Created On' < DateAdd(DatePicker2.SelectedDate, 1, TimeUnit.Days)))), inp_search_5.Text, transaction_number, note)`.
- Gallery8_8 Items: Filter(dis_trx_details, header of `Gallery8_7.Selected` && category from Dropdown2_4).
- Read-only screen: no mutations.

## Changes

1. Screen Properties: `Fill: =clrBg`, `LoadingSpinnerColor: =clrAccent`. Screen `Children:` = `conHistRoot` only.
2. Shell pattern with prefix Hist: conHistRoot, cmpHistSidebar (`activemenu: ="History"`), conHistMain,
   cmpHistTopBar (`ActiveMenu: ="History"`, `Subtitle: ="Riwayat transaksi"`), conHistBody.
3. Dropdown2_3 is replaced by the segmented type filter (context var `locHistType`); list sorted newest first.
4. Keep inp_search_5, DatePicker2, Gallery8_7, Dropdown2_4, inp_search_6, Gallery8_8. Icon2 becomes
   `icoHistDateClear` (same OnSelect). `inp_search_6` is wired into Gallery8_8.

## Controls to Add

conHistBody children (FillPortions 0, AlignInContainer Stretch):

1. `conHistListCard` - Card pattern, Height 520, LayoutGap 12:
   - `conHistToolbar` (Toolbar pattern):
     - `conHistTypeFld` (Segmented type filter, W 360): `txtHistTypeLbl` "TIPE" + `conHistTypeSeg` with
       `btnHistTypeAll` "Semua" W 72, `btnHistTypeReceive` "Receive" W 84, `btnHistTypeConsume` "Consume" W 92,
       `btnHistTypeTransfer` "Transfer" W 88.
       | Button | OnSelect | Active predicate |
       | --- | --- | --- |
       | btnHistTypeAll | `=UpdateContext({locHistType: Blank()})` | `IsBlank(locHistType)` |
       | btnHistTypeReceive | `=UpdateContext({locHistType: 'type (dis_trx_headers)'.Receive})` | `locHistType = 'type (dis_trx_headers)'.Receive` |
       | btnHistTypeConsume | `=UpdateContext({locHistType: 'type (dis_trx_headers)'.Consume})` | `locHistType = 'type (dis_trx_headers)'.Consume` |
       | btnHistTypeTransfer | `=UpdateContext({locHistType: 'type (dis_trx_headers)'.Transfer})` | `locHistType = 'type (dis_trx_headers)'.Transfer` |
     - `conHistDateFld` W 168: `txtHistDateLbl` "Tanggal" + `DatePicker2` (kept; Height 36, LayoutMin* 0,
       Appearance Outline, Size 13, Radius 8 x4, `Format: =DatePickerFormat.Short`, `Placeholder: ="Semua tanggal"`,
       AccessibleLabel "Filter tanggal").
     - `icoHistDateClear` ModernIcon "Dismiss" 36 x 36, IconColor clrTextMuted, Padding 8 x4, Radius 8 x4,
       AlignInContainer End, Tooltip/AccessibleLabel "Hapus filter tanggal", `OnSelect: =Reset(DatePicker2)`.
     - `conHistSearchFld` FillPortions 1, LayoutMinWidth 0: `txtHistSearchLbl` "Cari transaksi" + `inp_search_5`
       (Delayed; `Placeholder: ="Nomor atau catatan"`, `Type: =TextInputType.Search`; drop empty `Default: =`).
   - `conHistTable` AutoLayout Vertical, Height 420, LayoutGap 4, transparent:
     - `conHistHead`: `txtHistHNo` "NOMOR" FP 2, `txtHistHDate` "TANGGAL" W 92, `txtHistHType` "TIPE" W 92,
       `txtHistHArea` "AREA (DARI -> KE)" FP 3, `txtHistHNote` "CATATAN" FP 3.
     - `Gallery8_7` (kept) Gallery pattern, Height 380, TemplateSize 52, AccessibleLabel "Riwayat transaksi",
       Items (`|-`):
       ```
       =Sort(
           Search(
               Filter(
                   dis_trx_headers,
                   IsBlank(locHistType) || type = locHistType,
                   (IsBlank(DatePicker2.SelectedDate) Or
                       ('Created On' >= DatePicker2.SelectedDate And 'Created On' < DateAdd(DatePicker2.SelectedDate, 1, TimeUnit.Days))
                   )
               ),
               inp_search_5.Text,
               transaction_number,
               note
           ),
           'Created On',
           SortOrder.Descending
       )
       ```
       `Visible: =!IsEmpty(<same Items expression>)`. Row `conHistRow`:
       - `btnHistOpen` ModernButton link cell (same styling as `btnTrxLOpen` in the scr_Transaction brief:
         Subtle, Color clrAccent, TextOnly, Align Left, Semibold 13, Height 28, FP 2, LayoutMin* 0),
         `Text: =ThisItem.transaction_number`, Tooltip/AccessibleLabel `="Lihat detail " & ThisItem.transaction_number`,
         `OnSelect: =false` (selecting the button selects the row; Gallery8_8 follows `Gallery8_7.Selected`).
       - `txtHistDate` `=Text(ThisItem.'Created On', "dd/mm/yyyy")`, W 92.
       - `bdgHistType` Badge W 92, `Content: =Text(ThisItem.type)`,
         `ThemeColor: =Switch(Text(ThisItem.type), "Receive", 'BadgeCanvas.ThemeColor'.Success, "Consume", 'BadgeCanvas.ThemeColor'.Warning, "Transfer", 'BadgeCanvas.ThemeColor'.Brand, 'BadgeCanvas.ThemeColor'.Subtle)`.
       - `txtHistArea` `=Coalesce(ThisItem.area_form.Name, "-") & " -> " & Coalesce(ThisItem.area_to.Name, "-")`, FP 3.
       - `txtHistNote` `=ThisItem.note`, FP 3.
     - `txtHistEmpty` "Tidak ada transaksi pada filter ini.", Height 380, `Visible: =IsEmpty(<same Items expression>)`.
2. `conHistDetailCard` - Card pattern, Height 376, LayoutGap 12:
   - `txtHistDetailTitle` card title,
     `Text: =If(IsBlank(Gallery8_7.Selected), "Detail Item", "Detail Item - " & Gallery8_7.Selected.transaction_number)`.
   - `conHistDToolbar` (Toolbar pattern):
     - `conHistDCatFld` W 200: `txtHistDCatLbl` "Kategori" + `Dropdown2_4` (Items `=dis_category_items`,
       ItemDisplayText `=ThisItem.code` unchanged; AccessibleLabel "Filter kategori detail").
     - `conHistDSearchFld` FillPortions 1: `txtHistDSearchLbl` "Cari item" + `inp_search_6` (Delayed;
       `Placeholder: ="Nama item atau BPN"`, `Type: =TextInputType.Search`).
     - `icoHistDReset` reset icon, `OnSelect: =Reset(Dropdown2_4); Reset(inp_search_6)`.
   - `conHistDTable` AutoLayout Vertical, Height 240, LayoutGap 4, transparent:
     - `conHistDHead`: "BPN" FP 2, "NAMA" FP 3, "DESKRIPSI" FP 3, "KATEGORI" FP 2, "QTY" W 64, "UOM" W 56
       (`txtHistDHBpn`, `txtHistDHName`, `txtHistDHDesc`, `txtHistDHCat`, `txtHistDHQty`, `txtHistDHUom`).
     - `Gallery8_8` (kept) Gallery pattern, Height 200, TemplateSize 44, AccessibleLabel "Detail item riwayat",
       Items (`|-`):
       ```
       =Filter(
           dis_trx_details,
           header_id.dis_trx_header = Gallery8_7.Selected.dis_trx_header
           &&
           (
               IsBlank(Dropdown2_4.Selected) ||
               item.dis_category_item.name = Dropdown2_4.Selected.name
           )
           &&
           (
               IsBlank(inp_search_6.Text) ||
               StartsWith(item.name, inp_search_6.Text) ||
               StartsWith(item.part_number, inp_search_6.Text)
           )
       )
       ```
       `Visible: =!IsEmpty(<same Items expression>)`. Row `conHistDRow`: `txtHistDBpn` `=ThisItem.item.part_number`
       FP 2; `txtHistDName` `=ThisItem.item.name` Semibold FP 3; `txtHistDDesc` `=ThisItem.item.description` FP 3;
       `txtHistDCat` `=ThisItem.item.dis_category_item.name` FP 2; `txtHistDQty` `=Text(ThisItem.qty)` W 64 Align
       Right; `txtHistDUom` `=Text(ThisItem.item.uom)` W 56.
     - `txtHistDEmpty` Height 200,
       `Text: =If(IsBlank(Gallery8_7.Selected), "Pilih nomor transaksi di atas untuk melihat detail.", "Tidak ada item yang cocok.")`,
       `Visible: =IsEmpty(<same Items expression>)`.

## Controls to Remove

con_Main_trans_4, con_sidebar_trans_4, com_sidebar_trans_4, con_content_trans_4, com_topbar_trans_4, Container8_7,
Container13_4, Container15_4, Dropdown2_3, Container16_4, Icon2 (-> icoHistDateClear), Container20_5,
Label21_30..Label21_34, Container21_3, Container10_6, Container11_6, Text1_12, Text1_13, Type_18, Type_19, Type_20,
Container12_9, Container25_1, Container13_5, Container15_5, Container16_5, Container20_6, Label21_36..Label21_41,
Container10_7, Container11_7, Text1_14, Text1_15, Type_21, Type_22, Type_23, Type_24, Container12_10.
Keep inp_search_5, DatePicker2, Gallery8_7, Dropdown2_4, inp_search_6, Gallery8_8.

## Properties to Update

- Screen: Fill, LoadingSpinnerColor.
- Kept inputs: Toolbar styling, drop X/Y/Width. Kept galleries: Gallery pattern props, Items as given above.

## Layout and Visual Impact

- List toolbar: 360 + 168 + 36 + 3 x 8 = 588 -> search 244.
- List card 520 (first viewport); detail card 16 + 24 + 12 + 56 + 12 + 240 + 16 = 376 below; body scrolls.
- List row inner 806: fixed 92 + 92 + 4 x 8 = 216 -> FP 8 -> 73.75 (number 148, area / note 221).

## Required Record Fields

| Field key | Record surface | Required field | Source field | Bound control | Exact formula | Placement and visibility |
| --- | --- | --- | --- | --- | --- | --- |
| hist/row/number | Gallery8_7 row | Number | transaction_number | btnHistOpen | `Text: =ThisItem.transaction_number` | FP 2 link |
| hist/row/date | row | Date | 'Created On' | txtHistDate | `=Text(ThisItem.'Created On', "dd/mm/yyyy")` | W 92 |
| hist/row/type | row | Type | type | bdgHistType | `Content: =Text(ThisItem.type)` | W 92 |
| hist/row/area | row | Area | area_form / area_to | txtHistArea | `=Coalesce(ThisItem.area_form.Name, "-") & " -> " & Coalesce(ThisItem.area_to.Name, "-")` | FP 3 |
| hist/row/note | row | Note | note | txtHistNote | `=ThisItem.note` | FP 3 |
| histd/row/* | Gallery8_8 row | BPN, Name, Description, Category, Qty, UoM | item.*, qty | txtHistDBpn..txtHistDUom | see above | 6 cells |

## Required Actions

| Action | Preconditions | Entry point and event | Source and stable ID | Transition and postcondition | Mutation write set | Receipt proof set | Observer and evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ACT-HIST-FILTER | none | btnHistType*, DatePicker2, icoHistDateClear, inp_search_5 | dis_trx_headers | filtered, newest first | N/A | N/A | Gallery8_7, txtHistEmpty |
| ACT-HIST-SELECT | rows | btnHistOpen (row selection) | Gallery8_7.Selected.dis_trx_header | detail lines shown | N/A | N/A | txtHistDetailTitle, Gallery8_8 |

## Functional Test Scenarios

| Scenario | Given | When | Then | Evidence surface | Boundary or negative case |
| --- | --- | --- | --- | --- | --- |
| SCN-HIST-DATE | H1 created 2026-10-01, H2 2026-10-03 | pick 2026-10-03 | H2 only | Gallery8_7 | clear icon restores both |
| SCN-HIST-TYPE | H1 Receive, H2 Consume | click Consume | H2 only; Consume segment Primary | Gallery8_7 | Semua restores |
| SCN-HIST-DETAIL | H2 with 2 lines | click H2 number | 2 lines | txtHistDetailTitle "Detail Item - H2", Gallery8_8 | detail search by item name / BPN narrows; nothing selected -> txtHistDEmpty hint |

## Relevant Data Source Schemas

dis_trx_headers: transaction_number, note, type (`'type (dis_trx_headers)'`), area_form, area_to (-> dis_areas
.Name), 'Created On', dis_trx_header. dis_trx_details: header_id, item (-> dis_item_v2S: part_number, name,
description, uom, dis_category_item.name), qty. Context: locHistType (option-set value or blank).

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
- **ModernDatePicker** - `Control: ModernDatePicker`. Inputs: AccessibleLabel, Appearance, BasePaletteColor,
  BorderColor, BorderStyle, BorderThickness, Color, ContentLanguage, DateTimeZone, DefaultDate, DisplayMode, EndDate,
  Fill, Font, FontWeight, Format, Height, IsEditable, Italic, OnChange, Padding*, Placeholder, Radius*, Size,
  StartDate, StartOfWeek, Strikethrough, Underline, ValidationState, Visible, Width, X, Y. Output: SelectedDate.
  Literal: `Format: =DatePickerFormat.Short`.
- **Sidebar / TopBar** - `Control: CanvasComponent` + `ComponentName: Sidebar` (inputs activemenu, AlignInContainer,
  Fill, FillPortions, Height, LayoutMaxHeight, LayoutMaxWidth, LayoutMinHeight, LayoutMinWidth, Visible, Width, X, Y)
  / `ComponentName: TopBar` (inputs ActiveMenu, Subtitle + the same generic inputs).
