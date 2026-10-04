# Screen Plan: Add_area

## Assignment

- Action: Modify (rewrite layout; keep YAML key, Form5_1 and every data card)
- Target file: `C:\Project\Powerapps\app\Add_area.pa.yaml`
- YAML key: Add_area
- Control name prefix: AreaF

Read `C:\Project\Powerapps\app\canvas-app-shared.md` first (Shell, Card, Form screen pattern, Receipt keys).

## Current State

`con_Main_template_2` with ManualLayout sidebar holder (Sidebar activemenu "Area") and content column holding TopBar
"Add Area" and `Container8_2`: button bar `Container12_4` at the TOP (Button32_2 submit, Button32_3 Back) and
ManualLayout `Container26_1` holding `Container22` (empty) and `Form5_1` (Modern, Vertical, DataSource `dis_areas`,
Item `=Gallery8_12.Selected`, NumberOfColumns 2, Height 308). Cards: Name_DataCard9 (X0 Y0), elv_geounit_DataCard1
(X1 Y0), elv_location_DataCard1 (X0 Y1), elv_dis_subblid_DataCard1 (X1 Y1), elv_detail_DataCard2 (X0 Y2,
multiline), all `Width: =467`.

Preserved logic:
- Button32_2 `OnSelect: =SubmitForm(Form5_1)`, Text `=If(gblFormMode = "Add", "+ Add Area", "Save")`.
- Button32_3 `OnSelect: =ResetForm(Form5_1); Clear(colTempDetails); Back();`.
- Form5_1 `OnSuccess: =Notify("Data area berhasil ditambahkan!", NotificationType.Success); ResetForm(Self); Back()`.

## Changes

1. Screen Properties: `Fill: =clrBg`, `LoadingSpinnerColor: =clrAccent`. The screen `Children:` contains only
   `conAreaFRoot`.
2. Shell pattern with prefix AreaF: conAreaFRoot, cmpAreaFSidebar (`activemenu: ="Area"`), conAreaFMain,
   cmpAreaFTopBar (`ActiveMenu: =If(gblFormMode = "Add", "Tambah Area", "Edit Area")`,
   `Subtitle: ="Lengkapi data area"`), conAreaFBody.
3. Form screen pattern: move `Form5_1` (same name, DataSource, Item, NumberOfColumns 2, all cards and card children)
   into `conAreaFFormCard`; actions bar at the bottom.
4. Form5_1 OnSuccess: add one receipt statement first, keep the rest (see below).

## Controls to Add

conAreaFBody children (FillPortions 0, AlignInContainer Stretch):

1. `conAreaFFormCard` - Card pattern, Height 408, LayoutGap 12. Children:
   - `txtAreaFCardTitle` card title, `Text: =If(gblFormMode = "Add", "Data Area Baru", "Edit Area - " & Gallery8_12.Selected.Name)`.
   - `Form5_1` (moved, see Properties to Update), Height 340.
2. `conAreaFActions` - Form screen actions bar (Height 44, LayoutJustifyContent End, LayoutGap 12). Children:
   - `btnAreaFBack` Secondary, Icon "ArrowLeft", Text "Kembali", W 120,
     OnSelect (preserved from Button32_3, `|-`): `=ResetForm(Form5_1); Clear(colTempDetails); Back()`.
   - `btnAreaFSave` Primary, Icon "Save", Text `=If(gblFormMode = "Add", "Tambah Area", "Simpan")`, W 160,
     `OnSelect: =SubmitForm(Form5_1)`, AccessibleLabel "Simpan area".

## Controls to Remove

con_Main_template_2, con_sidebar_template_2, com_sidebar_template_2, con_content_template_2, com_topbar_template_2,
Container8_2, Container12_4, Button32_2 (-> btnAreaFSave), Button32_3 (-> btnAreaFBack), Container26_1, Container22.
Do NOT remove Form5_1 or any data card / card child.

## Properties to Update

- `Form5_1`: keep `Control: Form`, `Variant: Modern`, `Layout: Vertical`, DataSource `=dis_areas`,
  Item `=Gallery8_12.Selected`, NumberOfColumns 2. Set `AlignInContainer: =AlignInContainer.Stretch`,
  `FillPortions: =0`, `Height: =340`, `Fill: =clrSurface`, `BorderThickness: =0`; delete X, Y, Width.
  OnSuccess (`|-`):
  ```
  =Set(
      gblReceipt,
      {
          Screen: "Area",
          Action: "Disimpan",
          Title: Form5_1.LastSubmit.Name,
          Detail: "Geounit " & Coalesce(Form5_1.LastSubmit.elv_geounit.elv_name_short, "-") & " | Lokasi " & Coalesce(Form5_1.LastSubmit.'elv_location (cr8a3_elv_location)'.Name, "-") & " | Business Line " & Coalesce(Form5_1.LastSubmit.elv_dis_subblid.Name, "-") & " | Detail " & Coalesce(Form5_1.LastSubmit.elv_detail, "-")
      }
  );
  Notify("Data area berhasil ditambahkan!", NotificationType.Success);
  ResetForm(Self);
  Back()
  ```
- Data card `Width` only: Name_DataCard9, elv_geounit_DataCard1, elv_location_DataCard1, elv_dis_subblid_DataCard1
  `=Parent.Width / 2`; elv_detail_DataCard2 `=Parent.Width` (full row). Keep X/Y grid, DataField, Default, Update,
  Required, variants and every child exactly as they are (including the "Bussines Line" label text and
  `elv_location_DataCard1.Default: =ThisItem.location`).

## Layout and Visual Impact

- Card: 16 + 24 + 12 + 340 + 16 = 408; body: 408 + 16 + 44 = 468 <= 532 (no scroll at 1136 x 640).
- Card inner 832 -> half cards 416 each; Detail card spans 832 (multiline).
- Buttons moved from top to bottom-right; title shows which record is edited.

## Required Actions

| Action | Preconditions | Entry point and event | Source and stable ID | Transition and postcondition | Mutation write set | Receipt proof set | Observer and evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ACT-AREA-SAVE | Form5_1 valid (Name required) | btnAreaFSave.OnSelect -> Form5_1.OnSuccess | Form5_1.LastSubmit.dis_area | row created / updated; ResetForm; Back() to Area | Name, elv_geounit, location, elv_dis_subblid, elv_detail | Title Name; Detail Geounit, Lokasi, Business Line, Detail | conAreaLReceipt on Area; Gallery8_12 row |
| ACT-AREA-SAVE (cancel) | any | btnAreaFBack.OnSelect | Form5_1 | form reset, back to Area, nothing written | N/A | N/A | Gallery8_12 unchanged |

## Functional Test Scenarios

| Scenario | Given | When | Then | Evidence surface | Boundary or negative case |
| --- | --- | --- | --- | --- | --- |
| SCN-AREA-SAVE | Edit A2, Detail "Rack 4" | Simpan | A2.elv_detail = "Rack 4"; back on Area | conAreaLReceipt "Disimpan - A2", Detail contains "Rack 4"; Gallery8_12 | Name blank -> card error (Parent.Error), no receipt, stays on Add_area |
| SCN-AREA-ADD | Tambah Area | fill Name "Yard-9", Simpan | new row Yard-9 | conAreaLReceipt "Disimpan - Yard-9" | Kembali -> no row created |

## Relevant Data Source Schemas

dis_areas: Name (elv_name, required), elv_geounit (-> dis_geounits .elv_name_short), 'elv_location
(cr8a3_elv_location)' (-> dis_locations .Name), elv_dis_subblid (-> dis_subbls .Name), elv_detail (multiline),
dis_area (Guid). Globals: gblFormMode, gblReceipt, colTempDetails (preserved Clear on Back).

## Required Variants

GroupContainer -> AutoLayout. Form -> Modern (unchanged). TypedDataCard variants unchanged
(ModernTextualEdit, PcfCoreComboBoxEditCard, ModernTextualMultilineEdit).

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
- **Form** (existing, preserved) - `Control: Form`, `Variant: Modern`, `Layout: Vertical`. Inputs: AcceptsFocus,
  BorderColor, BorderStyle, BorderThickness, ContentLanguage, DataSource, DefaultMode, Fill, FocusedBorderColor,
  FocusedBorderThickness, Height, Item, NumberOfColumns, OnFailure, OnReset, OnSuccess, SnapToColumns, Visible,
  Width, X, Y. Outputs: Error, ErrorKind, LastSubmit, Mode, Unsaved, Updates, Valid. TypedDataCards and their
  children (Classic/ComboBox, FluentV8/Label, Label, Image, AddMedia, Modern inputs) are preserved as-is; only
  card `Width` changes. Do not create data cards.
- **Sidebar / TopBar** - `Control: CanvasComponent` + `ComponentName: Sidebar` (inputs activemenu, AlignInContainer,
  Fill, FillPortions, Height, LayoutMaxHeight, LayoutMaxWidth, LayoutMinHeight, LayoutMinWidth, Visible, Width, X, Y)
  / `ComponentName: TopBar` (inputs ActiveMenu, Subtitle + the same generic inputs).
