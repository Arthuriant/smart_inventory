# Screen Plan: Category Form

## Assignment

- Action: Modify (rewrite layout; keep YAML key, frm_catFrm_category with every card, btn_catFrm_submit,
  btn_catFrm_back)
- Target file: `C:\Project\Powerapps\app\scr_frm_category.pa.yaml`
- YAML key: scr_frm_category
- Control name prefix: CatF

Read `C:\Project\Powerapps\app\canvas-app-shared.md` first (Shell, Card, Form screen pattern).

## Current State

`con_catFrm_main` shell (Sidebar "Category Item", TopBar "Category Item") -> `con_catFrm_body`: ManualLayout
`con_catFrm_formWrap` with `frm_catFrm_category` (Modern, Vertical, DataSource `dis_category_items`,
Item `=gal_cat_list.Selected`, NumberOfColumns 2, Height 308; cards dc_catFrm_name X0 Y0 W449, dc_catFrm_code X1 Y0
W449, dc_catFrm_desc X0 Y1 W898 multiline) and `con_catFrm_actions` (btn_catFrm_submit, btn_catFrm_back).

Preserved logic:
- btn_catFrm_submit `OnSelect: =SubmitForm(frm_catFrm_category)`.
- btn_catFrm_back `OnSelect: =ResetForm(frm_catFrm_category); Back();`.
- frm_catFrm_category `OnSuccess: =Notify("Kategori berhasil disimpan!", NotificationType.Success); Back();`.

## Changes

1. Screen Properties: `Fill: =clrBg`, `LoadingSpinnerColor: =clrAccent`. Screen `Children:` = `conCatFRoot` only.
2. Shell pattern with prefix CatF: conCatFRoot, cmpCatFSidebar (`activemenu: ="Category Item"`), conCatFMain,
   cmpCatFTopBar (`ActiveMenu: =If(frm_catFrm_category.Mode = FormMode.Edit, "Edit Kategori", "Tambah Kategori")`,
   `Subtitle: ="Lengkapi data kategori"`), conCatFBody.
3. Form screen pattern; OnSuccess gains one receipt statement before the preserved statements.

## Controls to Add

conCatFBody children (FillPortions 0, AlignInContainer Stretch):

1. `conCatFFormCard` - Card pattern, Height 328, LayoutGap 12:
   - `txtCatFCardTitle` card title,
     `Text: =If(frm_catFrm_category.Mode = FormMode.Edit, "Edit Kategori - " & gal_cat_list.Selected.name, "Kategori Baru")`.
   - `frm_catFrm_category` (moved), Height 260.
2. `conCatFActions` - actions bar (Height 44, LayoutJustifyContent End, LayoutGap 12):
   - `btn_catFrm_back` (kept) Secondary, Icon "ArrowLeft", Text "Kembali", W 120, OnSelect unchanged.
   - `btn_catFrm_submit` (kept) Primary, `Icon: ="Save"`,
     `Text: =If(frm_catFrm_category.Mode = FormMode.Edit, "Simpan", "Tambah Kategori")`, W 168,
     OnSelect unchanged, AccessibleLabel "Simpan kategori".

## Controls to Remove

con_catFrm_main, con_catFrm_sidebar, com_catFrm_sidebar, con_catFrm_content, com_catFrm_topbar, con_catFrm_body,
con_catFrm_formWrap, con_catFrm_actions. Keep the form, its cards/children and both buttons.

## Properties to Update

- `frm_catFrm_category`: keep Control/Variant/Layout, DataSource, Item, NumberOfColumns 2. Set AlignInContainer
  Stretch, FillPortions 0, `Height: =260`, `Fill: =clrSurface`, `BorderThickness: =0`; delete X, Y, Width.
  OnSuccess (`|-`):
  ```
  =Set(
      gblReceipt,
      {
          Screen: "Category",
          Action: "Disimpan",
          Title: frm_catFrm_category.LastSubmit.name,
          Detail: "Kode " & frm_catFrm_category.LastSubmit.code & " | Deskripsi " & Coalesce(frm_catFrm_category.LastSubmit.description, "-")
      }
  );
  Notify("Kategori berhasil disimpan!", NotificationType.Success);
  Back();
  ```
- Card `Width` only: dc_catFrm_name, dc_catFrm_code `=Parent.Width / 2`; dc_catFrm_desc `=Parent.Width`.
- btn_catFrm_submit / btn_catFrm_back: button styling per shared Actions (Height 36, Size 13, Radius 8 x4,
  LayoutMinWidth = Width, LayoutMinHeight 0, Layout IconBefore); drop X/Y.

## Layout and Visual Impact

- Card 16 + 24 + 12 + 260 + 16 = 328; body 328 + 16 + 44 = 388 <= 532.
- Half cards 416 wide; description spans 832.

## Required Actions

| Action | Preconditions | Entry point and event | Source and stable ID | Transition and postcondition | Mutation write set | Receipt proof set | Observer and evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ACT-CAT-SAVE | name + code filled | btn_catFrm_submit.OnSelect -> OnSuccess | frm_catFrm_category.LastSubmit.dis_category_item | row created/updated; Back() to scr_category | name, code, description | Title name; Detail Kode, Deskripsi | conCatLReceipt; gal_cat_list |
| ACT-CAT-SAVE (cancel) | any | btn_catFrm_back.OnSelect | form | reset + back, nothing written | N/A | N/A | gal_cat_list unchanged |

## Functional Test Scenarios

| Scenario | Given | When | Then | Evidence surface | Boundary or negative case |
| --- | --- | --- | --- | --- | --- |
| SCN-CAT-SAVE | New, name "Hose", code "HS" | Tambah Kategori | row created; back on list | conCatLReceipt "Disimpan - Hose", Detail "Kode HS" | code blank -> card error, no receipt |
| SCN-CAT-EDIT-SAVE | Edit C2, description "Fittings" | Simpan | C2.description updated | conCatLReceipt; txtCatLDesc | N/A |

## Relevant Data Source Schemas

dis_category_items: name (cr8a3_name, required), code (cr8a3_code, required), description (cr8a3_description,
multiline), dis_category_item (Guid). Global gblReceipt.

## Required Variants

GroupContainer -> AutoLayout. Form -> Modern (unchanged). TypedDataCard variants unchanged (ModernTextualEdit,
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
- **Form** (existing, preserved) - `Control: Form`, `Variant: Modern`, `Layout: Vertical`. Inputs: AcceptsFocus,
  BorderColor, BorderStyle, BorderThickness, ContentLanguage, DataSource, DefaultMode, Fill, FocusedBorderColor,
  FocusedBorderThickness, Height, Item, NumberOfColumns, OnFailure, OnReset, OnSuccess, SnapToColumns, Visible,
  Width, X, Y. Outputs: Error, ErrorKind, LastSubmit, Mode, Unsaved, Updates, Valid. TypedDataCards and their
  children (Classic/ComboBox, FluentV8/Label, Label, Image, AddMedia, Modern inputs) are preserved as-is; only
  card `Width` changes. Do not create data cards.
- **Sidebar / TopBar** - `Control: CanvasComponent` + `ComponentName: Sidebar` (inputs activemenu, AlignInContainer,
  Fill, FillPortions, Height, LayoutMaxHeight, LayoutMaxWidth, LayoutMinHeight, LayoutMinWidth, Visible, Width, X, Y)
  / `ComponentName: TopBar` (inputs ActiveMenu, Subtitle + the same generic inputs).
