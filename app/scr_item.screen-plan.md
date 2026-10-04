# Screen Plan: Item

## Assignment

- Action: Modify (rewrite layout; keep YAML key and the functional controls listed below)
- Target file: `C:\Project\Powerapps\app\scr_item.pa.yaml`
- YAML key: scr_item
- Control name prefix: ItmL

Read `C:\Project\Powerapps\app\canvas-app-shared.md` first (Shell, Card, Toolbar, Table, Confirm, Receipt).

## Current State

`con_Main_template_4` shell (Sidebar "Item", TopBar "Item") -> `Container8_5` -> `Container13_3`: toolbar
`Container15_3` (Dropdown2_2 category, inp_search_4, spacer, Button31_2 "Add Item"), Label header `Container20_4`,
ManualLayout `Container10_5` with `Gallery8_6` (rows Text1_10 name, Text1_11 part_number, Type_13 client_number,
Type_14 category name, Type_15 min_qty, Type_16 uom, Type_17 status, Button15_8 "Update", spacer, Button15_9
"Delete").

Preserved logic:
- Dropdown2_2 `Items: =Choices(dis_item_v2S.dis_category_item)`, `ItemDisplayText: =ThisItem.code`.
- Gallery8_6 Items:
  `=Search(Filter(dis_item_v2S, IsBlank(Dropdown2_2.Selected) Or dis_category_item.dis_category_item = Dropdown2_2.Selected.dis_category_item), inp_search_4.Text, name, description)`.
- Button31_2 `OnSelect: =NewForm(Form5_3); Navigate(scr_frm_item);`.
- Button15_8 `OnSelect: =EditForm(Form5_3); Navigate(scr_frm_item);`.

Bug: Button15_9 removes immediately (`Remove(dis_item_v2S, ThisItem)`) with no confirmation.

## Changes

1. Screen Properties: `Fill: =clrBg`, `LoadingSpinnerColor: =clrAccent`. Screen `Children:` = `conItmLRoot` only.
2. Shell pattern with prefix ItmL: conItmLRoot, cmpItmLSidebar (`activemenu: ="Item"`), conItmLMain, cmpItmLTopBar
   (`ActiveMenu: ="Item"`, `Subtitle: ="Master data item"`), conItmLBody.
3. Keep `Dropdown2_2`, `inp_search_4`, `Button31_2`, `Gallery8_6` (Items verbatim) - `Form5_3.Item` on scr_frm_item
   reads `Gallery8_6.Selected`.
4. Delete goes through the confirm strip; Status shown as a badge.

## Controls to Add

conItmLBody children, in order (FillPortions 0, AlignInContainer Stretch):

1. `conItmLReceipt` - Receipt strip, `Visible: =gblReceipt.Screen = "Item"`.
2. `conItmLConfirm` - Confirm strip, `Visible: =locShowDeleteConfirm`:
   - `txtItmLConfirmMsg` `Text: ="Hapus item " & locSelectedRecord.name & " (BPN " & Coalesce(locSelectedRecord.part_number, "-") & ")?"`.
   - `btnItmLConfirmDel` Destructive "Hapus" W 104, OnSelect (`|-`):
     ```
     =With(
         {target: locSelectedRecord},
         Remove(dis_item_v2S, target);
         If(
             IsEmpty(Errors(dis_item_v2S)),
             Set(
                 gblReceipt,
                 {
                     Screen: "Item",
                     Action: "Dihapus",
                     Title: target.name,
                     Detail: "BPN " & Coalesce(target.part_number, "-") & " | SPN " & Coalesce(target.client_number, "-") & " | Kategori " & Coalesce(target.dis_category_item.name, "-")
                 }
             );
             UpdateContext({locShowDeleteConfirm: false});
             Notify("Item berhasil dihapus.", NotificationType.Success),
             Notify("Gagal menghapus item. " & First(Errors(dis_item_v2S)).Message, NotificationType.Error)
         )
     )
     ```
   - `btnItmLConfirmCancel` Secondary "Batal" W 96, `OnSelect: =UpdateContext({locShowDeleteConfirm: false})`.
3. `conItmLListCard` - Card pattern, Height 520, LayoutGap 12:
   - `conItmLToolbar` (Toolbar pattern):
     - `conItmLCatFld` W 200: `txtItmLCatLbl` "Kategori" + `Dropdown2_2` (Items / ItemDisplayText unchanged;
       AccessibleLabel "Filter kategori").
     - `conItmLSearchFld` FillPortions 1, LayoutMinWidth 0: `txtItmLSearchLbl` "Cari item" + `inp_search_4`
       (TriggerOutput Delayed; `Placeholder: ="Nama atau deskripsi"`, `Type: =TextInputType.Search`,
       AccessibleLabel "Cari item"; drop empty `Default: =`).
     - `icoItmLReset` reset icon, `OnSelect: =Reset(Dropdown2_2); Reset(inp_search_4)`.
     - `Button31_2` (kept) Primary, Icon "Add", Text "Tambah Item", W 140, AlignInContainer End, OnSelect unchanged.
   - `conItmLTable` AutoLayout Vertical, Height 420, LayoutGap 4, transparent:
     - `conItmLHead`: `txtItmLHName` "NAMA" FP 3, `txtItmLHBpn` "BPN" FP 2, `txtItmLHSpn` "SPN" FP 2,
       `txtItmLHCat` "KATEGORI" FP 2, `txtItmLHMin` "MIN" W 64, `txtItmLHUom` "UOM" W 56,
       `txtItmLHStatus` "STATUS" W 96, `txtItmLHAct` "AKSI" W 72.
     - `Gallery8_6` (kept) Gallery pattern, Height 380, TemplateSize 52, Items unchanged,
       AccessibleLabel "Daftar item", `Visible: =!IsEmpty(<same Items expression>)`. Row `conItmLRow`:
       - `txtItmLName` `=ThisItem.name`, Semibold, FP 3.
       - `txtItmLBpn` `=ThisItem.part_number`, FP 2.
       - `txtItmLSpn` `=ThisItem.client_number`, FP 2.
       - `txtItmLCat` `=ThisItem.dis_category_item.name`, FP 2.
       - `txtItmLMin` `=Text(ThisItem.min_qty)`, W 64, `Align: =Align.Right`.
       - `txtItmLUom` `=Text(ThisItem.uom)`, W 56.
       - `bdgItmLStatus` Badge W 96, `Content: =Text(ThisItem.status)`,
         `ThemeColor: =If(Text(ThisItem.status) = "Active", 'BadgeCanvas.ThemeColor'.Success, 'BadgeCanvas.ThemeColor'.Subtle)`,
         AccessibleLabel `="Status " & Text(ThisItem.status)`.
       - `conItmLRowActs` (W 72 action group):
         - `icoItmLEdit` Edit icon, Tooltip/AccessibleLabel `="Edit " & ThisItem.name`,
           OnSelect (`|-`): `=EditForm(Form5_3); Navigate(scr_frm_item)`.
         - `icoItmLDelete` Delete icon, Tooltip/AccessibleLabel `="Hapus " & ThisItem.name`,
           `OnSelect: =UpdateContext({locSelectedRecord: ThisItem, locShowDeleteConfirm: true})`.
     - `txtItmLEmpty` "Tidak ada item yang cocok dengan filter.", Height 380,
       `Visible: =IsEmpty(<same Items expression>)`.

## Controls to Remove

con_Main_template_4, con_sidebar_template_4, com_sidebar_template_4, con_content_template_4, com_topbar_template_4,
Container8_5, Container13_3, Container15_3, Container16_3, Container20_4, Label21_21, Label21_27, Label21_28,
Label21_29, Label21_23, Label21_24, Label21_25, Label21_26, Container10_5, Container11_5, Text1_10, Text1_11,
Type_13, Type_14, Type_15, Type_16, Type_17, Button15_8 (-> icoItmLEdit), Container12_7, Button15_9
(-> icoItmLDelete). Keep Dropdown2_2, inp_search_4, Button31_2, Gallery8_6.

## Properties to Update

- Screen: Fill, LoadingSpinnerColor.
- Dropdown2_2 / inp_search_4: Toolbar input styling; drop X/Y/Width. Logic unchanged.
- Button31_2: Primary styling; drop X/Y.
- Gallery8_6: Gallery pattern props; Items unchanged.

## Layout and Visual Impact

- Toolbar: 200 + 36 + 140 + 3 x 8 = 400 -> search 432.
- Card 16 + 56 + 12 + 420 + 16 = 520 <= 532.
- Row inner 806: fixed 64 + 56 + 96 + 72 + 7 x 8 = 344 -> FP 9 -> 51.3 per portion (name 154, BPN/SPN/cat 103).

## Required Record Fields

| Field key | Record surface | Required field | Source field | Bound control | Exact formula | Placement and visibility |
| --- | --- | --- | --- | --- | --- | --- |
| item/row/name | Gallery8_6 row | Name | name | txtItmLName | `=ThisItem.name` | FP 3 Semibold |
| item/row/bpn | row | BPN | part_number | txtItmLBpn | `=ThisItem.part_number` | FP 2 |
| item/row/spn | row | SPN | client_number | txtItmLSpn | `=ThisItem.client_number` | FP 2 |
| item/row/cat | row | Category | dis_category_item.name | txtItmLCat | `=ThisItem.dis_category_item.name` | FP 2 |
| item/row/min | row | Min qty | min_qty | txtItmLMin | `=Text(ThisItem.min_qty)` | W 64 |
| item/row/uom | row | UoM | uom | txtItmLUom | `=Text(ThisItem.uom)` | W 56 |
| item/row/status | row | Status | status | bdgItmLStatus | `Content: =Text(ThisItem.status)` | W 96 badge |

## Required Actions

| Action | Preconditions | Entry point and event | Source and stable ID | Transition and postcondition | Mutation write set | Receipt proof set | Observer and evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ACT-ITEM-FILTER | none | Dropdown2_2, inp_search_4, icoItmLReset | dis_item_v2S | Gallery8_6 filtered (Items preserved) | N/A | N/A | Gallery8_6, txtItmLEmpty |
| ACT-ITEM-ADD | none | Button31_2.OnSelect | Form5_3 | New; scr_frm_item | N/A | N/A | TopBar "Tambah Item" |
| ACT-ITEM-EDIT | row | icoItmLEdit.OnSelect | Gallery8_6.Selected.dis_item_v2 (clicked row) | Edit prefilled | N/A | N/A | form cards |
| ACT-ITEM-DELETE | row | icoItmLDelete -> btnItmLConfirmDel | locSelectedRecord.dis_item_v2 | clicked row removed | existence | "Dihapus" + name; Detail BPN, SPN, Kategori | conItmLReceipt; Gallery8_6 |
| ACT-ITEM-SAVE (observer) | saved on scr_frm_item | Form5_3.OnSuccess -> Back() | LastSubmit | list shown | see scr_frm_item | gblReceipt "Item" | conItmLReceipt; Gallery8_6 row |

## Functional Test Scenarios

| Scenario | Given | When | Then | Evidence surface | Boundary or negative case |
| --- | --- | --- | --- | --- | --- |
| SCN-ITEM-FILTER | I1, I2 in PIPE, I3 in VALVE | pick PIPE | I1, I2 only | Gallery8_6 | reset icon restores all; no match -> txtItmLEmpty |
| SCN-ITEM-ADD | none | Tambah Item | Form5_3 New | scr_frm_item | N/A |
| SCN-ITEM-EDIT | I2 | Edit icon | prefilled with I2 | Form5_3 cards | N/A |
| SCN-ITEM-DELETE | I3 | Delete icon -> Hapus | I3 removed | conItmLReceipt "Dihapus - I3" | Batal keeps I3; item referenced by stock -> error notify |

## Relevant Data Source Schemas

dis_item_v2S: name, part_number (BPN), client_number (SPN), description, dis_category_item (-> dis_category_items
.name/.code/.dis_category_item), min_qty (Number), uom (option set), status (option set `status (dis_item_v2S)`:
Active, Non-Active), Image, dis_item_v2 (Guid). Context: locSelectedRecord (dis_item_v2S record),
locShowDeleteConfirm. Global gblReceipt.

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
