# Screen Plan: Item Form

## Assignment

- Action: Modify (rewrite layout; keep YAML key, Form5_3 with every card, Button32_6, Button32_7)
- Target file: `C:\Project\Powerapps\app\scr_frm_item.pa.yaml`
- YAML key: scr_frm_item
- Control name prefix: ItmF

Read `C:\Project\Powerapps\app\canvas-app-shared.md` first (Shell, Card, Form screen pattern).

## Current State

`con_Main_trans_3` shell (Sidebar "Item", TopBar "Item") -> `Container8_6`: ManualLayout `Container26_3` with
`Form5_3` (Modern, Vertical, DataSource `dis_item_v2S`, Item `=Gallery8_6.Selected`, NumberOfColumns 2,
`Height: =Parent.Height`) and button bar `Container12_8` (Button32_6 submit, Button32_7 Back). Cards (X, Y):
name_DataCard2 (0,0), min_qty_DataCard3 (1,0), part_number_DataCard3 (0,1), client_number_DataCard1 (1,1),
uom_DataCard3 (0,2), status_DataCard1 (1,2), dis_category_item_DataCard1 (0,3), description_DataCard4 (0,4,
Height 143, multiline), Image_DataCard1 (1,4, Height 100, ClassicLargePicture with Image6 + AddPicture1).

Preserved logic:
- Button32_6 `OnSelect: =SubmitForm(Form5_3)`.
- Button32_7 `OnSelect: =ResetForm(Form5_3); Back();`.
- Form5_3 `OnSuccess: =Notify("Item berhasil disimpan!", NotificationType.Success); Back();`.

## Changes

1. Screen Properties: `Fill: =clrBg`, `LoadingSpinnerColor: =clrAccent`. Screen `Children:` = `conItmFRoot` only.
2. Shell pattern with prefix ItmF: conItmFRoot, cmpItmFSidebar (`activemenu: ="Item"`), conItmFMain, cmpItmFTopBar
   (`ActiveMenu: =If(Form5_3.Mode = FormMode.Edit, "Edit Item", "Tambah Item")`,
   `Subtitle: ="Lengkapi data item"`), conItmFBody.
3. Form screen pattern; OnSuccess gains one receipt statement.

## Controls to Add

conItmFBody children (FillPortions 0, AlignInContainer Stretch):

1. `conItmFFormCard` - Card pattern, Height 588, LayoutGap 12:
   - `txtItmFCardTitle` card title,
     `Text: =If(Form5_3.Mode = FormMode.Edit, "Edit Item - " & Gallery8_6.Selected.name, "Item Baru")`.
   - `Form5_3` (moved), Height 520.
2. `conItmFActions` - actions bar (Height 44, LayoutJustifyContent End, LayoutGap 12):
   - `Button32_7` (kept) Secondary, Icon "ArrowLeft", Text "Kembali", W 120, OnSelect unchanged.
   - `Button32_6` (kept) Primary, `Icon: ="Save"`, `Text: =If(Form5_3.Mode = FormMode.Edit, "Simpan", "Tambah Item")`,
     W 160, OnSelect unchanged, AccessibleLabel "Simpan item".

## Controls to Remove

con_Main_trans_3, con_sidebar_trans_3, com_sidebar_trans_3, con_content_trans_3, com_topbar_trans_3, Container8_6,
Container26_3, Container12_8. Keep Form5_3 (all cards, all card children incl. Image6 / AddPicture1 / classic
Labels), Button32_6, Button32_7.

## Properties to Update

- `Form5_3`: keep Control/Variant/Layout, DataSource, Item `=Gallery8_6.Selected`, NumberOfColumns 2. Set
  AlignInContainer Stretch, FillPortions 0, `Height: =520` (replaces `=Parent.Height`), `Fill: =clrSurface`,
  `BorderThickness: =0`; delete X, Y, Width. OnSuccess (`|-`):
  ```
  =Set(
      gblReceipt,
      {
          Screen: "Item",
          Action: "Disimpan",
          Title: Form5_3.LastSubmit.name,
          Detail: "BPN " & Coalesce(Form5_3.LastSubmit.part_number, "-") & " | SPN " & Coalesce(Form5_3.LastSubmit.client_number, "-") & " | Min " & Text(Form5_3.LastSubmit.min_qty) & " | UoM " & Text(Form5_3.LastSubmit.uom) & " | Status " & Text(Form5_3.LastSubmit.status) & " | Kategori " & Coalesce(Form5_3.LastSubmit.dis_category_item.name, "-") & " | Deskripsi " & Coalesce(Form5_3.LastSubmit.description, "-") & " | Gambar " & If(IsBlank(Form5_3.LastSubmit.Image), "tidak ada", "ada")
      }
  );
  Notify("Item berhasil disimpan!", NotificationType.Success);
  Back();
  ```
- Card `Width` only, all nine cards `=Parent.Width / 2` (grid unchanged: category alone on row 3, description +
  image on row 4). Keep card Heights (description 143, image 100), X/Y, DataField, Default, Update, Required,
  variants, children.
- Button32_6 / Button32_7: shared button styling; drop X/Y.

## Layout and Visual Impact

- Card 16 + 24 + 12 + 520 + 16 = 588; body 588 + 16 + 44 = 648 > 532 -> body scrolls (Kembali / Simpan stay
  reachable at the bottom; the form card itself never scrolls).
- Half cards 416 wide.

## Required Actions

| Action | Preconditions | Entry point and event | Source and stable ID | Transition and postcondition | Mutation write set | Receipt proof set | Observer and evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ACT-ITEM-SAVE | required name, min_qty, uom, status, category | Button32_6.OnSelect -> Form5_3.OnSuccess | Form5_3.LastSubmit.dis_item_v2 | row created/updated; Back() to scr_item | name, min_qty, part_number, client_number, uom, status, dis_category_item, description, Image | Title name; Detail BPN, SPN, Min, UoM, Status, Kategori, Deskripsi, Gambar ada/tidak ada | conItmLReceipt; Gallery8_6 row |
| ACT-ITEM-SAVE (cancel) | any | Button32_7.OnSelect | form | reset + back | N/A | N/A | Gallery8_6 unchanged |

## Functional Test Scenarios

| Scenario | Given | When | Then | Evidence surface | Boundary or negative case |
| --- | --- | --- | --- | --- | --- |
| SCN-ITEM-SAVE | Edit I2, min_qty 5 -> 8 | Simpan | I2.min_qty = 8; back on list | conItmLReceipt "Min 8"; txtItmLMin "8" | status blank -> card error, no receipt |
| SCN-ITEM-ADD-IMAGE | New item with picture | Tambah Item | row created with Image | receipt "Gambar ada" | no picture -> "Gambar tidak ada" |

## Relevant Data Source Schemas

dis_item_v2S: name (required), min_qty (Number, required), part_number, client_number, uom (option set, required),
status (option set, required), dis_category_item (-> dis_category_items .name, required), description, Image,
dis_item_v2 (Guid). Global gblReceipt.

## Required Variants

GroupContainer -> AutoLayout. Form -> Modern (unchanged). TypedDataCard variants unchanged (ModernTextualEdit,
ModernNumberEdit, ModernComboBoxOptionSetSingleEdit, PcfCoreComboBoxEditCard, ModernTextualMultilineEdit,
ClassicLargePicture).

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
