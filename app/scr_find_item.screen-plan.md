# Screen Plan: Find Item

## Assignment

- Action: Modify (rewrite layout; keep YAML key and the functional controls listed below)
- Target file: `C:\Project\Powerapps\app\scr_find_item.pa.yaml`
- YAML key: scr_find_item
- Control name prefix: Find

Read `C:\Project\Powerapps\app\canvas-app-shared.md` first (Shell, Card, Toolbar, Table).

## Current State

`con_Main_template_5` shell (Sidebar "Find Item", TopBar "Find Item") -> `Container8_8` -> `Container13_6`:
toolbar `Container15_6` (dd_Category, dd_Geounit, dd_Location, dd_Area, spacer, inp_search_7 - no cascade
resets), Label header `Container20_7`, ManualLayout `Container10_8` with `Gallery8_9` (rows Text1_16 name, Text1_17
part_number, Type_29 client_number, Type_30 category, Type_25 qty, Type_26 uom, Type_27 location - area).

Preserved logic:
- dd_Category (`=dis_category_items`, `=ThisItem.code`), dd_Geounit (`=dis_geounits`, `=ThisItem.elv_name_long`),
  dd_Location (`Filter(dis_locations, dis_geounit.dis_geounit = dd_Geounit.Selected.dis_geounit)`, `=ThisItem.Name`),
  dd_Area (`Filter(dis_areas, 'elv_location (cr8a3_elv_location)'.dis_location = dd_Location.Selected.dis_location)`,
  `=ThisItem.Name`).
- Gallery8_9 Items: `Filter(dis_stocks, <category clause>, <area clause>, <StartsWith name / part_number on inp_search_7>)`
  (same expression as now; the empty lines inside it may be removed, comments kept).

## Changes

1. Screen Properties: `Fill: =clrBg`, `LoadingSpinnerColor: =clrAccent`. Screen `Children:` = `conFindRoot` only.
2. Shell pattern with prefix Find: conFindRoot, cmpFindSidebar (`activemenu: ="Find Item"`), conFindMain,
   cmpFindTopBar (`ActiveMenu: ="Find Item"`, `Subtitle: ="Cari stok item per lokasi"`), conFindBody.
3. Keep dd_Category, dd_Geounit, dd_Location, dd_Area, inp_search_7, Gallery8_9 (Items unchanged; it is the stock
   observer for Consume / Receive).
4. Add cascade resets, DisplayMode gates, reset icon, low-stock badge, empty state.

## Controls to Add

conFindBody child:

1. `conFindCard` - Card pattern, Height 520, LayoutGap 12:
   - `conFindToolbar` (Toolbar pattern):
     - `conFindCatFld` W 140: `txtFindCatLbl` "Kategori" + `dd_Category` (AccessibleLabel "Filter kategori").
     - `conFindGeoFld` W 140: `txtFindGeoLbl` "Geounit" + `dd_Geounit`, `OnChange: =Reset(dd_Location); Reset(dd_Area)`.
     - `conFindLocFld` W 140: `txtFindLocLbl` "Location" + `dd_Location`, `OnChange: =Reset(dd_Area)`,
       `DisplayMode: =If(IsBlank(dd_Geounit.Selected), DisplayMode.Disabled, DisplayMode.Edit)`.
     - `conFindAreaFld` W 140: `txtFindAreaLbl` "Area" + `dd_Area`,
       `DisplayMode: =If(IsBlank(dd_Location.Selected), DisplayMode.Disabled, DisplayMode.Edit)`.
     - `conFindSearchFld` FillPortions 1, LayoutMinWidth 0: `txtFindSearchLbl` "Cari item" + `inp_search_7`
       (Delayed; `Placeholder: ="Nama atau BPN"`, `Type: =TextInputType.Search`, AccessibleLabel "Cari item";
       drop empty `Default: =`).
     - `icoFindReset` reset icon,
       `OnSelect: =Reset(dd_Category); Reset(dd_Geounit); Reset(dd_Location); Reset(dd_Area); Reset(inp_search_7)`.
   - `conFindTable` AutoLayout Vertical, Height 420, LayoutGap 4, transparent:
     - `conFindHead`: `txtFindHName` "NAMA" FP 3, `txtFindHBpn` "BPN" FP 2, `txtFindHSpn` "SPN" FP 2,
       `txtFindHCat` "KATEGORI" FP 2, `txtFindHStock` "STOK" W 80, `txtFindHUom` "UOM" W 56,
       `txtFindHLoc` "LOKASI" FP 3.
     - `Gallery8_9` (kept) Gallery pattern, Height 380, TemplateSize 52, Items unchanged,
       AccessibleLabel "Stok item per lokasi", `Visible: =!IsEmpty(<same Items expression>)`. Row `conFindRow`:
       - `txtFindName` `=ThisItem.dis_item_v2.name`, Semibold, FP 3.
       - `txtFindBpn` `=ThisItem.dis_item_v2.part_number`, FP 2.
       - `txtFindSpn` `=ThisItem.dis_item_v2.client_number`, FP 2.
       - `txtFindCat` `=ThisItem.dis_item_v2.dis_category_item.name`, FP 2.
       - `bdgFindStock` Badge W 80, `Content: =Text(ThisItem.qty)`,
         `ThemeColor: =If(ThisItem.qty < ThisItem.dis_item_v2.min_qty, 'BadgeCanvas.ThemeColor'.Danger, 'BadgeCanvas.ThemeColor'.Success)`,
         AccessibleLabel `="Stok " & Text(ThisItem.qty) & If(ThisItem.qty < ThisItem.dis_item_v2.min_qty, ", di bawah minimum", "")`.
       - `txtFindUom` `=Text(ThisItem.dis_item_v2.uom)`, W 56.
       - `txtFindLoc` `=ThisItem.dis_area.'elv_location (cr8a3_elv_location)'.Name & " - " & ThisItem.dis_area.Name`, FP 3.
     - `txtFindEmpty` "Tidak ada stok yang cocok dengan filter.", Height 380, `Visible: =IsEmpty(<same Items expression>)`.

## Controls to Remove

con_Main_template_5, con_sidebar_template_5, com_sidebar_template_5, con_content_template_5, com_topbar_template_5,
Container8_8, Container13_6, Container15_6, Container16_6, Container20_7, Label21_35, Label21_42, Label21_43,
Label21_47, Label21_44, Label21_45, Label21_46, Container10_8, Container11_8, Text1_16, Text1_17, Type_29, Type_30,
Type_25, Type_26, Type_27. Keep the four dropdowns, inp_search_7, Gallery8_9.

## Properties to Update

- Screen: Fill, LoadingSpinnerColor.
- Dropdowns / inp_search_7: Toolbar styling; drop X/Y/Width; logic unchanged except the added OnChange / DisplayMode.
- Gallery8_9: Gallery pattern props; Items unchanged.

## Layout and Visual Impact

- Toolbar: 4 x 140 + 36 + 5 x 8 = 636 -> search 196.
- Card 16 + 56 + 12 + 420 + 16 = 520 <= 532.
- Row inner 806: fixed 80 + 56 + 6 x 8 = 184 -> FP 12 -> 51.8 (name / location 155, BPN / SPN / cat 104).

## Required Record Fields

| Field key | Record surface | Required field | Source field | Bound control | Exact formula | Placement and visibility |
| --- | --- | --- | --- | --- | --- | --- |
| find/row/name | Gallery8_9 row | Name | dis_item_v2.name | txtFindName | `=ThisItem.dis_item_v2.name` | FP 3 Semibold |
| find/row/bpn | row | BPN | dis_item_v2.part_number | txtFindBpn | `=ThisItem.dis_item_v2.part_number` | FP 2 |
| find/row/spn | row | SPN | dis_item_v2.client_number | txtFindSpn | `=ThisItem.dis_item_v2.client_number` | FP 2 |
| find/row/cat | row | Category | dis_item_v2.dis_category_item.name | txtFindCat | `=ThisItem.dis_item_v2.dis_category_item.name` | FP 2 |
| find/row/stock | row | Stock (low highlight) | qty vs dis_item_v2.min_qty | bdgFindStock | `Content: =Text(ThisItem.qty)` | W 80; Danger when qty < min_qty |
| find/row/uom | row | UoM | dis_item_v2.uom | txtFindUom | `=Text(ThisItem.dis_item_v2.uom)` | W 56 |
| find/row/loc | row | Location | dis_area location + name | txtFindLoc | see above | FP 3 |

## Required Actions

| Action | Preconditions | Entry point and event | Source and stable ID | Transition and postcondition | Mutation write set | Receipt proof set | Observer and evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ACT-FIND-FILTER | none | 4 dropdowns (cascade OnChange), inp_search_7, icoFindReset | dis_stocks | Gallery8_9 filtered | N/A | N/A | Gallery8_9, txtFindEmpty |
| ACT-TRX-SAVE / ACT-CONSUME-SUBMIT (observer) | stock changed elsewhere | screen visible | dis_stocks.dis_stock | live qty | N/A | N/A | bdgFindStock |

## Functional Test Scenarios

| Scenario | Given | When | Then | Evidence surface | Boundary or negative case |
| --- | --- | --- | --- | --- | --- |
| SCN-FIND-FILTER | S1 Bentonite qty 2 min 5, S2 qty 10 min 5 (same category), S3 other category | pick that category | S1, S2 shown; S1 badge Danger, S2 Success | Gallery8_9 | reset restores; no match -> txtFindEmpty |
| SCN-TRX-SAVE-RECEIVE (observer) | S1 qty 10 | Receive 3 saved | S1 shows 13 | bdgFindStock | N/A |

## Relevant Data Source Schemas

dis_stocks: dis_item_v2 (-> dis_item_v2S: name, part_number, client_number, uom, min_qty, dis_category_item .name /
.dis_category_item), dis_area (-> dis_areas: Name, dis_area, 'elv_location (cr8a3_elv_location)'.Name), qty,
dis_stock. Filters: dis_category_items, dis_geounits, dis_locations, dis_areas.

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
