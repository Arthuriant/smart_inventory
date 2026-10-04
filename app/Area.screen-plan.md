# Screen Plan: Area

## Assignment

- Action: Modify (rewrite layout; keep YAML key and the functional controls listed below)
- Target file: `C:\Project\Powerapps\app\Area.pa.yaml`
- YAML key: Area
- Control name prefix: AreaL

Read `C:\Project\Powerapps\app\canvas-app-shared.md` first (Shell, Card, Toolbar, Table, Confirm strip, Receipt strip).

## Current State

`con_Main_template_1` (AutoLayout) with ManualLayout `con_sidebar_template_1` (Sidebar, activemenu "Area", Width 180)
and `con_content_template_1` (hard-coded width) holding TopBar "Area" and `Container7` -> `Container1`:
toolbar `Container15_8` (Button2 "Area" add, dd_Geounit_2, dd_Location_2, dd_Area_2, spacer, inp_search_9), classic
Label header `Container20_10`, ManualLayout `Container10_11` with `Gallery8_12` (rows Text1_21, Text1_22, Type_33,
Type_34, Button30_1 "Update", spacer, Button33_2 "Delete"). Screen-level ManualLayout overlay `cntDeleteConfirm`
(Visible `locShowDeleteConfirm`) with Button34 / Button35.

Bug: Button33_2 sets `locSelectedRecord: Defaults(Users)` and Button34 removes `Gallery8_12.Selected`, so Delete
targets the selected row (often the first row), not the clicked row.

## Changes

1. Delete every existing child except the functional controls kept below; the screen `Children:` contains only
   `conAreaLRoot`.
2. Screen Properties: `Fill: =clrBg`, `LoadingSpinnerColor: =clrAccent`. No OnVisible.
3. Shell pattern with prefix AreaL: conAreaLRoot, cmpAreaLSidebar (`activemenu: ="Area"`), conAreaLMain,
   cmpAreaLTopBar (`ActiveMenu: ="Area"`, `Subtitle: ="Kelola area penyimpanan"`), conAreaLBody.
4. Keep (same name, same logic, restyled per Toolbar pattern): `dd_Geounit_2`, `dd_Location_2`, `dd_Area_2`,
   `inp_search_9`, `Gallery8_12` (Items verbatim). Button2 becomes `btnAreaLAdd` (same OnSelect).
5. Bug fix: row Delete stores the clicked row (`ThisItem`); confirm removes `locSelectedRecord`.

## Controls to Add

conAreaLBody children, in order (all FillPortions 0, AlignInContainer Stretch):

1. `conAreaLReceipt` - Receipt strip pattern, `Visible: =gblReceipt.Screen = "Area"`. Children icoAreaLRcIco,
   conAreaLRcText (txtAreaLRcTitle, txtAreaLRcDetail), icoAreaLRcClose.
2. `conAreaLConfirm` - Confirm strip pattern, `Visible: =locShowDeleteConfirm`. Children:
   - `icoAreaLConfirmIco`.
   - `txtAreaLConfirmMsg` `Text: ="Hapus area " & locSelectedRecord.Name & "? Data yang dihapus tidak dapat dikembalikan."`
   - `btnAreaLConfirmDel` (Destructive "Hapus", W 104). OnSelect (write as `|-`):
     ```
     =With(
         {target: locSelectedRecord},
         Remove(dis_areas, target);
         If(
             IsEmpty(Errors(dis_areas)),
             Set(
                 gblReceipt,
                 {
                     Screen: "Area",
                     Action: "Dihapus",
                     Title: target.Name,
                     Detail: "Lokasi " & Coalesce(target.'elv_location (cr8a3_elv_location)'.Name, "-") & " | Geounit " & Coalesce(target.elv_geounit.elv_name_short, "-")
                 }
             );
             UpdateContext({locShowDeleteConfirm: false});
             Notify("Data area berhasil dihapus!", NotificationType.Success),
             Notify("Gagal menghapus area. " & First(Errors(dis_areas)).Message, NotificationType.Error)
         )
     )
     ```
   - `btnAreaLConfirmCancel` (Secondary "Batal", W 96), `OnSelect: =UpdateContext({locShowDeleteConfirm: false})`.
3. `conAreaLListCard` - Card pattern, Height 520, LayoutGap 12. Children:
   - `conAreaLToolbar` (Toolbar pattern, Height 56):
     - `conAreaLGeoFld` W 150: `txtAreaLGeoLbl` "Geounit" + `dd_Geounit_2` (keep Items `=dis_geounits`,
       ItemDisplayText `=ThisItem.elv_name_long`, OnChange `=Reset(dd_Location_2); Reset(dd_Area_2)`;
       AccessibleLabel "Filter geounit").
     - `conAreaLLocFld` W 150: `txtAreaLLocLbl` "Location" + `dd_Location_2` (keep Items, ItemDisplayText,
       OnChange `=Reset(dd_Area_2)`, DisplayMode gate; AccessibleLabel "Filter lokasi").
     - `conAreaLAreaFld` W 150: `txtAreaLAreaLbl` "Area" + `dd_Area_2` (keep Items, ItemDisplayText, DisplayMode
       gate; AccessibleLabel "Filter area").
     - `conAreaLSearchFld` FillPortions 1, LayoutMinWidth 0: `txtAreaLSearchLbl` "Cari" + `inp_search_9` (keep
       TriggerOutput Delayed; `Placeholder: ="Cari nama area"`, `Type: =TextInputType.Search`, AccessibleLabel
       "Cari area"; remove the empty `Default: =`).
     - `icoAreaLReset` (Toolbar reset icon) `OnSelect: =Reset(dd_Geounit_2); Reset(dd_Location_2); Reset(dd_Area_2); Reset(inp_search_9)`.
     - `btnAreaLAdd` Primary, Icon "Add", Text "Tambah Area", W 140, AlignInContainer End,
       OnSelect (preserved from Button2, `|-`): `=Set(gblFormMode, "Add"); NewForm(Form5_1); Navigate(Add_area, ScreenTransition.None)`.
   - `conAreaLTable` - AutoLayout Vertical, Height 420, LayoutGap 4, transparent, DropShadow None, Radius 0 x4,
     LayoutAlignItems Stretch. Children:
     - `conAreaLHead` (Table header pattern): `txtAreaLHName` "NAMA" FP 2, `txtAreaLHLoc` "LOKASI" FP 2,
       `txtAreaLHBl` "BUSINESS LINE" FP 2, `txtAreaLHGeo` "GEOUNIT" W 96, `txtAreaLHAct` "AKSI" W 72.
     - `Gallery8_12` - Gallery pattern, Height 380, TemplateSize 52, AccessibleLabel "Daftar area",
       Items verbatim (the 4-clause Filter over dis_areas), `Visible: =!IsEmpty(<same Items expression>)`.
       Row `conAreaLRow` (row shell). Cells:
       - `txtAreaLName` `=ThisItem.Name`, Semibold, FP 2.
       - `txtAreaLLoc` `=ThisItem.'elv_location (cr8a3_elv_location)'.Name`, FP 2.
       - `txtAreaLBl` `=ThisItem.elv_dis_subblid.Name`, FP 2.
       - `txtAreaLGeo` `=ThisItem.elv_geounit.elv_name_short`, W 96.
       - `conAreaLRowActs` AutoLayout Horizontal, W 72, Height 32, LayoutGap 8, FillPortions 0, transparent,
         DropShadow None, Radius 0 x4, AlignInContainer Center:
         - `icoAreaLEdit` (row Edit icon), Tooltip / AccessibleLabel `="Edit " & ThisItem.Name`,
           OnSelect (`|-`): `=Set(gblFormMode, "Update"); EditForm(Form5_1); Navigate(Add_area, ScreenTransition.None)`
           (selecting the icon selects the row, so `Form5_1.Item = Gallery8_12.Selected` is the clicked row).
         - `icoAreaLDelete` (row Delete icon), Tooltip / AccessibleLabel `="Hapus " & ThisItem.Name`,
           `OnSelect: =UpdateContext({locSelectedRecord: ThisItem, locShowDeleteConfirm: true})`.
     - `txtAreaLEmpty` (Empty state pattern) "Tidak ada area yang cocok dengan filter.", Height 380,
       `Visible: =IsEmpty(<same Items expression>)`.

## Controls to Remove

con_Main_template_1, con_sidebar_template_1, com_sidebar_template_1, con_content_template_1, com_topbar_template_1,
Container7, Container1, Container15_8, Button2 (replaced by btnAreaLAdd), Container16_8, Container20_10,
Label21_53..Label21_56, Container21_5, Label21_58, Container10_11, Container11_10, Text1_21, Text1_22, Type_33,
Type_34, Button30_1, Container2, Button33_2, cntDeleteConfirm, Container36, Container37, Text1, Container35, Button34,
Container38, Button35.

## Properties to Update

- Screen: Fill, LoadingSpinnerColor.
- dd_Geounit_2 / dd_Location_2 / dd_Area_2 / inp_search_9: drop X/Y/Width; Toolbar input styling (Height 36,
  FillPortions 0, AlignInContainer Stretch, LayoutMinWidth 0, LayoutMinHeight 0, `Appearance: =Appearance.Outline`,
  Size 13, Radius 8 x4, Font Segoe UI). Logic properties unchanged.
- Gallery8_12: Gallery pattern props; Items unchanged; TemplateSize 52; no OnSelect.

## Layout and Visual Impact

- Fixed desktop 1136 x 640: body inner 864 x 532; card inner 832.
- Toolbar: 3 x 150 + 36 + 140 + 5 x 8 = 666 -> search field 166 (placeholder "Cari nama area" ~ 100px at 13px).
- Card vertical: 16 + 56 + 12 + 420 + 16 = 520 <= 532. Table: 36 + 4 + 380 = 420 (7 rows of 52 visible).
- Row inner 806: fixed 96 + 72 + 4 x 8 = 200 -> FP 6 -> 101 per portion (name / location / BL 202 each).
- Receipt (80) and confirm (56) appear above the card only when active; the body then scrolls.

## Required Record Fields

| Field key | Record surface | Required field | Source field | Bound control | Exact formula | Placement and visibility |
| --- | --- | --- | --- | --- | --- | --- |
| area/row/name | Gallery8_12 row | Area name | Name | txtAreaLName | `=ThisItem.Name` | FP 2, Semibold |
| area/row/location | row | Location | 'elv_location (cr8a3_elv_location)'.Name | txtAreaLLoc | `=ThisItem.'elv_location (cr8a3_elv_location)'.Name` | FP 2 |
| area/row/bl | row | Business line | elv_dis_subblid.Name | txtAreaLBl | `=ThisItem.elv_dis_subblid.Name` | FP 2 |
| area/row/geounit | row | Geounit | elv_geounit.elv_name_short | txtAreaLGeo | `=ThisItem.elv_geounit.elv_name_short` | W 96 |

## Required Actions

| Action | Preconditions | Entry point and event | Source and stable ID | Transition and postcondition | Mutation write set | Receipt proof set | Observer and evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ACT-AREA-FILTER | none | dd_Geounit_2 / dd_Location_2 OnChange, inp_search_9, icoAreaLReset.OnSelect | dis_areas | Gallery8_12 filtered (Items preserved) | N/A | N/A | Gallery8_12, txtAreaLEmpty |
| ACT-AREA-ADD | none | btnAreaLAdd.OnSelect | Form5_1 | gblFormMode "Add", Form5_1 New, Add_area shown | N/A | N/A | Add_area TopBar "Tambah Area" |
| ACT-AREA-EDIT | row exists | icoAreaLEdit.OnSelect | Gallery8_12.Selected.dis_area (clicked row) | gblFormMode "Update", Form5_1 Edit | N/A | N/A | Add_area cards prefilled |
| ACT-AREA-DELETE | row exists | icoAreaLDelete.OnSelect -> btnAreaLConfirmDel.OnSelect | locSelectedRecord.dis_area | clicked row removed; strip hidden | existence | Action "Dihapus", Title Name, Detail Lokasi + Geounit | conAreaLReceipt; Gallery8_12 no longer lists it |
| ACT-AREA-SAVE (observer) | Form5_1 submitted on Add_area | Form5_1.OnSuccess -> Back() | LastSubmit.dis_area | Area visible again | see Add_area | gblReceipt Screen "Area" | conAreaLReceipt, Gallery8_12 row |

## Functional Test Scenarios

| Scenario | Given | When | Then | Evidence surface | Boundary or negative case |
| --- | --- | --- | --- | --- | --- |
| SCN-AREA-FILTER | A1, A2 in Geounit G1; A3 in G2 | pick G1 | A1, A2 shown; A3 hidden; Location enabled | Gallery8_12 | reset icon restores all 3; no match -> txtAreaLEmpty |
| SCN-AREA-ADD | none | Tambah Area | Add_area New, empty fields | Add_area TopBar "Tambah Area" | N/A |
| SCN-AREA-EDIT | A1, A2 | Edit icon on A2 | Add_area shows A2 values | Form5_1 cards | N/A |
| SCN-AREA-DELETE | A1 selected (first row) | Delete icon on A3 -> Hapus | A3 removed, A1 untouched | conAreaLReceipt "Dihapus - A3"; Gallery8_12 | bug-fix proof: target is the clicked row |
| SCN-AREA-DELETE-CANCEL | confirm open for A3 | Batal | A3 still listed; strip hidden | Gallery8_12, conAreaLConfirm | N/A |

## Relevant Data Source Schemas

dis_areas: Name, 'elv_location (cr8a3_elv_location)' (-> dis_locations: Name, dis_location, dis_geounit),
elv_dis_subblid (-> dis_subbls: Name), elv_geounit (-> dis_geounits: elv_name_short, elv_name_long, dis_geounit),
elv_detail, dis_area (Guid). Form5_1 lives on Add_area (DataSource dis_areas, Item `Gallery8_12.Selected`).
Global `gblFormMode` ("Add"/"Update"), `gblReceipt` (shared Named State). Context: `locSelectedRecord`
(dis_areas record), `locShowDeleteConfirm` (Boolean).

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
