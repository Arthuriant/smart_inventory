# Screen Plan: Dashboard

## Assignment

- Action: Create
- Target file: `C:\Project\Powerapps\app\scr_dashboard.pa.yaml`
- YAML key: scr_dashboard
- Control name prefix: Dash

Read `C:\Project\Powerapps\app\canvas-app-shared.md` first (palette names, Shell / Card / Table patterns, YAML rules).

## Specification

- Purpose: landing page after Log In - live KPIs, recent transactions, low-stock items, quick actions.
- Screen Properties: `Fill: =clrBg`, `LoadingSpinnerColor: =clrAccent`. No OnVisible.
- Shell: Shell pattern with `activemenu: ="Dashboard"`, TopBar `ActiveMenu: ="Dashboard"`,
  `Subtitle: ="Ringkasan stok dan transaksi hari ini"`. Names: conDashRoot, cmpDashSidebar, conDashMain,
  cmpDashTopBar, conDashBody.
- conDashBody children (in order, all FillPortions 0, AlignInContainer Stretch):

1. `conDashKpis` - AutoLayout Horizontal, Height 104, LayoutGap 16, LayoutAlignItems Stretch, transparent, DropShadow
   None, Radius 0. Three KPI cards, each Card pattern but **Horizontal**, FillPortions 1 (LayoutMinWidth 0),
   AlignInContainer Stretch, Padding 16, LayoutGap 14, LayoutAlignItems Center:
   - `ico<Dash>Kpi<X>Ico` ModernIcon 44 x 44, Padding 10 x4, Radius 10 x4, FillPortions 0, AlignInContainer Center.
   - `conDashKpi<X>Txt` AutoLayout Vertical, FillPortions 1, Height 72, LayoutGap 2, LayoutJustifyContent Center,
     LayoutAlignItems Stretch, AlignInContainer Center, containing label (Size 12 clrTextMuted Height 18) and value
     (Size 28 Bold clrText Height 36) and caption (Size 11 clrTextMuted Height 14). 18 + 2 + 36 + 2 + 14 = 72.

   | X | Icon / Fill / IconColor | Label | Value `Text` | Caption |
   | --- | --- | --- | --- | --- |
   | Items (`conDashKpiItemsCard`, `icoDashKpiItemsIco`, `txtDashKpiItemsLbl`, `txtDashKpiItemsVal`, `txtDashKpiItemsCap`) | `="Box"`, Fill clrRowSelected, IconColor clrNavy | "Total Item" | `=Text(CountRows(dis_item_v2S))` | "Item terdaftar" |
   | Low (`...KpiLow...`) | `="Warning"`, Fill clrWarningTint, IconColor clrWarning | "Stok di bawah minimum" | `=Text(CountRows(Filter(dis_stocks, qty < dis_item_v2.min_qty)))` | "Baris stok perlu diisi ulang" |
   | Today (`...KpiToday...`) | `="ArrowSwap"`, Fill clrSuccessTint, IconColor clrSuccess | "Transaksi hari ini" | `=Text(CountRows(Filter(dis_trx_headers, 'Created On' >= Today(), 'Created On' < DateAdd(Today(), 1, TimeUnit.Days))))` | `=Text(Today(), "dd mmm yyyy", "id-ID")` |

2. `conDashQuick` - AutoLayout Horizontal, Height 40, LayoutGap 12, LayoutAlignItems Center, transparent. Buttons
   (Height 36, FillPortions 0, Width = LayoutMinWidth):
   - `btnDashNewTrx` Primary, Icon "Add", Text "Transaksi Baru", W 168,
     `OnSelect: =Clear(colTempDetails); NewForm(Form5); Navigate(scr_frm_Transaction)` (use `|-`).
   - `btnDashConsume` Secondary, Icon "Cart", Text "Consume Barang", W 172, `OnSelect: =Navigate(scr_consume)`.
   - `btnDashFind` Secondary, Icon "Search", Text "Cari Item", W 136, `OnSelect: =Navigate(scr_find_item)`.
   - `btnDashHistory` Secondary, Icon "History", Text "Riwayat", W 120, `OnSelect: =Navigate(scr_History)`.
   Width: 168 + 172 + 136 + 120 + 3 x 12 = 632 <= 864.

3. `conDashPanels` - AutoLayout Horizontal, Height 356, LayoutGap 16, LayoutAlignItems Stretch, transparent.
   - `conDashRecentCard` (Card, FillPortions 3, LayoutMinWidth 0, LayoutGap 8). Children:
     - `conDashRecentHead` Horizontal Height 28, LayoutAlignItems Center, LayoutJustifyContent SpaceBetween:
       `txtDashRecentTitle` "Transaksi Terbaru" (card title, FillPortions 1) and `btnDashSeeAll`
       (`Appearance: =ButtonAppearance.Subtle`, `Color: =clrAccent`, Text "Lihat semua", Icon "ArrowRight",
       `Layout: =ButtonLayout.IconAfter`, W 132, Height 28, `OnSelect: =Navigate(scr_Transaction)`).
     - `conDashRecentCols` table header (pattern), cells: "NOMOR" FP 2, "TANGGAL" W 88, "TIPE" W 88, "AREA" FP 2.
     - `galDashRecent` Gallery Vertical, Height 248, TemplateSize 48, TemplatePadding 1, Fill clrBorder,
       `Items: =FirstN(Sort(dis_trx_headers, 'Created On', SortOrder.Descending), 10)`,
       `Visible: =!IsEmpty(dis_trx_headers)`, `Selectable: =false`. Row `conDashRecentRow` cells:
       `txtDashRecentNo` (`=ThisItem.transaction_number`, Semibold, FP 2), `txtDashRecentDate`
       (`=Text(ThisItem.'Created On', "dd/mm/yyyy")`, W 88), `bdgDashRecentType` (Badge W 88,
       `Content: =Text(ThisItem.type)`, ThemeColor Switch below), `txtDashRecentArea`
       (`=Coalesce(ThisItem.area_to.Name, ThisItem.area_form.Name, "-")`, FP 2).
       Type ThemeColor: `=Switch(Text(ThisItem.type), "Receive", 'BadgeCanvas.ThemeColor'.Success, "Consume", 'BadgeCanvas.ThemeColor'.Warning, "Transfer", 'BadgeCanvas.ThemeColor'.Brand, 'BadgeCanvas.ThemeColor'.Subtle)`.
     - `txtDashRecentEmpty` "Belum ada transaksi." Height 248, `Visible: =IsEmpty(dis_trx_headers)`.
     Height: 16 + 28 + 8 + 36 + 8 + 248 + 16 = 360 -> card uses parent stretch (356 parent; set gallery 244 so
     16 + 28 + 8 + 36 + 8 + 244 + 16 = 356). Use gallery Height 244 and empty Height 244.
   - `conDashLowCard` (Card, FillPortions 2, LayoutMinWidth 0, LayoutGap 8). Children:
     - `txtDashLowTitle` "Stok Menipis" (card title Height 28).
     - `galDashLow` Gallery Vertical, Height 288, TemplateSize 56, TemplatePadding 1, Fill clrBorder,
       `Selectable: =false`,
       `Items: =FirstN(Sort(Filter(dis_stocks, qty < dis_item_v2.min_qty), qty, SortOrder.Ascending), 10)`,
       `Visible: =!IsEmpty(Filter(dis_stocks, qty < dis_item_v2.min_qty))`.
       Row `conDashLowRow`: `conDashLowTxt` Vertical FP 1 Height 40 gap 2 (Stretch) holding `txtDashLowName`
       (`=ThisItem.dis_item_v2.name`, 13 Semibold H 20) and `txtDashLowArea` (`=ThisItem.dis_area.Name`, 12 muted
       H 18); `bdgDashLowQty` Badge W 84 ThemeColor Danger,
       `Content: =Text(ThisItem.qty) & " / " & Text(ThisItem.dis_item_v2.min_qty)`.
     - `txtDashLowEmpty` "Semua stok di atas minimum." Height 288, `Visible: =IsEmpty(Filter(dis_stocks, qty < dis_item_v2.min_qty))`.
     Height: 16 + 28 + 8 + 288 + 16 = 356.

- Vertical budget: 104 + 16 + 40 + 16 + 356 = 532 = body inner height (no scroll at 1136 x 640).
- Horizontal budget: KPI cards (864 - 32) / 3 = 277 each; text column 277 - 32 - 44 - 14 = 187 ("Stok di bawah minimum"
  at 12px ~ 140px fits). Panels: recent (864 - 16) x 3/5 = 509 -> row inner 509 - 32 - 2 - 24 = 451; fixed
  88 + 88 + 3 x 8 = 200; FP 4 -> 251 / 4 = 63 per portion (number ~126 px fits "04/10/26/0012" at 13px).
  Low card 339 -> row inner 281; badge 84 + gap 8 -> text 189.
- Delegation note (accepted): `qty < dis_item_v2.min_qty` compares a related column and is evaluated over the first
  2000 rows; acceptable for this inventory size.

## Required Record Fields

| Field key | Record surface | Required field | Source field | Bound control | Exact formula | Placement and visibility |
| --- | --- | --- | --- | --- | --- | --- |
| dash/recent/number | galDashRecent row | Number | transaction_number | txtDashRecentNo | `=ThisItem.transaction_number` | FP 2, Semibold |
| dash/recent/date | row | Date | 'Created On' | txtDashRecentDate | `=Text(ThisItem.'Created On', "dd/mm/yyyy")` | W 88 |
| dash/recent/type | row | Type | type | bdgDashRecentType | `Content: =Text(ThisItem.type)` | W 88 badge |
| dash/recent/area | row | Area | area_to / area_form | txtDashRecentArea | `=Coalesce(ThisItem.area_to.Name, ThisItem.area_form.Name, "-")` | FP 2 |
| dash/low/name | galDashLow row | Item | dis_item_v2.name | txtDashLowName | `=ThisItem.dis_item_v2.name` | line 1 |
| dash/low/area | row | Area | dis_area.Name | txtDashLowArea | `=ThisItem.dis_area.Name` | line 2 |
| dash/low/qty | row | qty / min | qty, min_qty | bdgDashLowQty | see above | W 84 |

## Required Actions

| Action | Preconditions | Entry point and event | Source and stable ID | Transition and postcondition | Mutation write set | Receipt proof set | Observer and evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ACT-DASH-VIEW | screen visible | KPI / gallery formulas | dis_item_v2S, dis_stocks, dis_trx_headers | live values | N/A | N/A | KPI value texts, galleries, empty texts |
| ACT-DASH-OPEN-TRX | none | btnDashNewTrx / btnDashSeeAll / btnDashConsume / btnDashFind / btnDashHistory OnSelect | colTempDetails, Form5 (cross-screen) | cart cleared + Form5 New, or navigation | N/A | N/A | target screen TopBar |

## Functional Test Scenarios

| Scenario | Given | When | Then | Evidence surface | Boundary or negative case |
| --- | --- | --- | --- | --- | --- |
| SCN-DASH-KPI | 12 items; S1 qty 2 / min 5; S2 qty 10 / min 5; 3 headers today | open | 12 / 1 / 3; low list S1 only; recent newest first | KPI values, galleries | S2 excluded |
| SCN-DASH-EMPTY | no headers, no low stock | open | values "0"; both empty texts visible | txtDashRecentEmpty, txtDashLowEmpty | N/A |
| SCN-DASH-OPEN-TRX | colTempDetails has stale lines | Transaksi Baru | cart empty, Form5 New | scr_frm_Transaction Gallery7 | Lihat semua -> scr_Transaction |

## Relevant Data Source Schemas

dis_item_v2S (name, min_qty). dis_stocks (qty, dis_item_v2 -> dis_item_v2S, dis_area -> dis_areas.Name).
dis_trx_headers (transaction_number, type option set `'type (dis_trx_headers)'`, area_form, area_to -> dis_areas,
'Created On'). Form5 lives on scr_frm_Transaction; colTempDetails is the shared cart collection.

## Required Variants

GroupContainer -> AutoLayout. Gallery -> Vertical.

## Control Definitions

All controls below, as children of an AutoLayout GroupContainer, also accept AlignInContainer
(`=AlignInContainer.Stretch` / `.Start` / `.Center` / `.End`), FillPortions, LayoutMaxHeight, LayoutMaxWidth,
LayoutMinHeight, LayoutMinWidth.

- **GroupContainer** - `Control: GroupContainer`, `Variant: AutoLayout`. Inputs: BorderColor, BorderStyle,
  BorderThickness, ContentLanguage, DropShadow, EnableChildFocus, Fill, Height, LayoutAlignItems, LayoutDirection,
  LayoutGap, LayoutJustifyContent, LayoutOverflowX, LayoutOverflowY, LayoutWrap, PaddingBottom, PaddingLeft,
  PaddingRight, PaddingTop, RadiusBottomLeft, RadiusBottomRight, RadiusTopLeft, RadiusTopRight, Visible, Width, X, Y.
  Literals: `=DropShadow.None` / `=DropShadow.Light`; `=BorderStyle.Solid`; `=LayoutDirection.Vertical` /
  `.Horizontal`; `=LayoutAlignItems.Stretch` / `.Center` / `.End`; `=LayoutJustifyContent.Center` / `.End` /
  `.SpaceBetween` / `.Start`; `LayoutOverflowY: =LayoutOverflow.Scroll`.
- **ModernText** - `Control: ModernText`. Inputs: AccessibleLabel, Align, AutoHeight, BorderColor, BorderStyle,
  BorderThickness, Color, ContentLanguage, DisplayMode, Fill, Font, FontWeight, Height, Italic, OnSelect,
  PaddingBottom, PaddingLeft, PaddingRight, PaddingTop, RadiusBottomLeft, RadiusBottomRight, RadiusTopLeft,
  RadiusTopRight, Size, Strikethrough, Text, Underline, VerticalAlign, Visible, Width, Wrap, X, Y. Literals:
  `Font: =Font.'Segoe UI'`; `FontWeight: =FontWeight.Bold` / `.Semibold` / `.Normal`; `Align: =Align.Center`;
  `VerticalAlign: =VerticalAlign.Middle`.
- **ModernButton** - `Control: ModernButton`. Inputs: AccessibleLabel, Align, Appearance, BasePaletteColor,
  BorderColor, BorderStyle, BorderThickness, Color, ContentLanguage, DisplayMode, Font, FontWeight, Height, Icon,
  IconRotation, IconStyle, Italic, Layout, OnSelect, PaddingBottom, PaddingLeft, PaddingRight, PaddingTop,
  RadiusBottomLeft, RadiusBottomRight, RadiusTopLeft, RadiusTopRight, Size, Strikethrough, Text, Tooltip, Underline,
  VerticalAlign, Visible, Width, X, Y. Literals (Enum name ButtonAppearance): `=ButtonAppearance.Primary` /
  `.Secondary` / `.Subtle`; `Layout: =ButtonLayout.IconBefore` / `.IconAfter`.
- **ModernIcon** - `Control: ModernIcon`. Inputs: AccessibleLabel, BasePaletteColor, BorderColor, BorderStyle,
  BorderThickness, ContentLanguage, DisplayMode, Fill, Height, Icon, IconColor, IconStyle, OnSelect, PaddingBottom,
  PaddingLeft, PaddingRight, PaddingTop, RadiusBottomLeft, RadiusBottomRight, RadiusTopLeft, RadiusTopRight,
  Rotation, Tooltip, Visible, Width, X, Y.
- **Badge** - `Control: Badge`. Inputs: AccessibleLabel, Align, Appearance, BasePaletteColor, Content,
  ContentLanguage, DisplayMode, Font, FontColor, FontItalic, FontSize, FontStrikethrough, FontUnderline, FontWeight,
  Height, Shape, ThemeColor, VerticalAlign, Visible, Width, X, Y. Literals: `='BadgeCanvas.Appearance'.Tint`,
  `='BadgeCanvas.Shape'.Rounded`, `='BadgeCanvas.ThemeColor'.Success` / `.Warning` / `.Brand` / `.Danger` / `.Subtle`.
- **Gallery** - `Control: Gallery`, `Variant: Vertical`. Inputs: AccessibleLabel, BorderColor, BorderStyle,
  BorderThickness, ContentLanguage, Default, DelayItemLoading, DisplayMode, Fill, FocusedBorderColor,
  FocusedBorderThickness, Height, Items, LoadingSpinner, LoadingSpinnerColor, NavigationStep, Selectable,
  ShowNavigation, ShowScrollbar, TabIndex, TemplatePadding, TemplateSize, Transition, Visible, Width, WrapCount, X, Y.
  Outputs: Selected, TemplateHeight, TemplateWidth. No OnSelect / TemplateFill.
- **Sidebar / TopBar** - `Control: CanvasComponent` + `ComponentName: Sidebar` (inputs activemenu, AlignInContainer,
  Fill, FillPortions, Height, LayoutMaxHeight, LayoutMaxWidth, LayoutMinHeight, LayoutMinWidth, Visible, Width, X, Y)
  / `ComponentName: TopBar` (inputs ActiveMenu, Subtitle + the same generic inputs).
