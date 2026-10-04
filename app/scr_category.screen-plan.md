# Screen Plan: Category Item

## Assignment

- Action: Modify (rewrite layout; keep YAML key and the functional controls listed below)
- Target file: `C:\Project\Powerapps\app\scr_category.pa.yaml`
- YAML key: scr_category
- Control name prefix: CatL

Read `C:\Project\Powerapps\app\canvas-app-shared.md` first (Shell, Card, Toolbar, Table, Confirm, Receipt).

## Current State

`con_cat_main` shell (ManualLayout `con_cat_sidebar` with Sidebar "Category Item"; `con_cat_content` with TopBar
"Category") -> `con_cat_body` -> `con_cat_table`: toolbar `con_cat_toolbar` (inp_cat_search, spacer,
btn_cat_add "Add Category"), Label header `con_cat_header`, ManualLayout `con_cat_galleryWrap` with `gal_cat_list`
(Items `=Search(dis_category_items, inp_cat_search.Text, name, code, description)`; rows txt_cat_rowName,
txt_cat_rowDate, txt_cat_rowCode, txt_cat_rowDesc, btn_cat_rowEdit "Update", spacer, btn_cat_rowDelete "Delete").

Bug: btn_cat_rowDelete removes immediately (`Remove(dis_category_items, ThisItem)`) with no confirmation.

## Changes

1. Screen Properties: `Fill: =clrBg`, `LoadingSpinnerColor: =clrAccent`. Screen `Children:` = `conCatLRoot` only.
2. Shell pattern with prefix CatL: conCatLRoot, cmpCatLSidebar (`activemenu: ="Category Item"`), conCatLMain,
   cmpCatLTopBar (`ActiveMenu: ="Category Item"`, `Subtitle: ="Kelola kategori item"`), conCatLBody.
3. Keep `inp_cat_search`, `btn_cat_add` (OnSelect unchanged) and `gal_cat_list` (Items unchanged): other screens
   reference `gal_cat_list` (`frm_catFrm_category.Item`).
4. Delete now goes through the confirm strip and targets the clicked row.

## Controls to Add

conCatLBody children, in order (FillPortions 0, AlignInContainer Stretch):

1. `conCatLReceipt` - Receipt strip, `Visible: =gblReceipt.Screen = "Category"`.
2. `conCatLConfirm` - Confirm strip, `Visible: =locShowDeleteConfirm`:
   - `txtCatLConfirmMsg` `Text: ="Hapus kategori " & locSelectedRecord.name & " (" & locSelectedRecord.code & ")?"`.
   - `btnCatLConfirmDel` Destructive "Hapus" W 104, OnSelect (`|-`):
     ```
     =With(
         {target: locSelectedRecord},
         Remove(dis_category_items, target);
         If(
             IsEmpty(Errors(dis_category_items)),
             Set(
                 gblReceipt,
                 {
                     Screen: "Category",
                     Action: "Dihapus",
                     Title: target.name,
                     Detail: "Kode " & target.code & " | Deskripsi " & Coalesce(target.description, "-")
                 }
             );
             UpdateContext({locShowDeleteConfirm: false});
             Notify("Kategori berhasil dihapus.", NotificationType.Success),
             Notify("Gagal menghapus kategori. " & First(Errors(dis_category_items)).Message, NotificationType.Error)
         )
     )
     ```
   - `btnCatLConfirmCancel` Secondary "Batal" W 96, `OnSelect: =UpdateContext({locShowDeleteConfirm: false})`.
3. `conCatLListCard` - Card pattern, Height 520, LayoutGap 12:
   - `conCatLToolbar` (Toolbar pattern):
     - `conCatLSearchFld` FillPortions 1, LayoutMinWidth 0: `txtCatLSearchLbl` "Cari kategori" + `inp_cat_search`
       (keep TriggerOutput Delayed; `Placeholder: ="Nama, kode, atau deskripsi"`, `Type: =TextInputType.Search`,
       AccessibleLabel "Cari kategori"; drop the empty `Default: =`).
     - `btn_cat_add` (kept) Primary, Icon "Add", Text "Tambah Kategori", W 168, AlignInContainer End,
       OnSelect unchanged (`|-`): `=NewForm(frm_catFrm_category); Navigate(scr_frm_category);`.
   - `conCatLTable` AutoLayout Vertical, Height 420, LayoutGap 4, transparent, DropShadow None, Radius 0 x4:
     - `conCatLHead`: `txtCatLHName` "NAMA" FP 3, `txtCatLHCode` "KODE" W 96, `txtCatLHDate` "DIBUAT" W 96,
       `txtCatLHDesc` "DESKRIPSI" FP 4, `txtCatLHAct` "AKSI" W 72.
     - `gal_cat_list` (kept) Gallery pattern, Height 380, TemplateSize 52, Items unchanged,
       AccessibleLabel "Daftar kategori",
       `Visible: =!IsEmpty(Search(dis_category_items, inp_cat_search.Text, name, code, description))`.
       Row `conCatLRow`:
       - `txtCatLName` `=ThisItem.name`, Semibold, FP 3.
       - `txtCatLCode` `=ThisItem.code`, W 96.
       - `txtCatLDate` `=Text(ThisItem.'Created On', "dd/mm/yyyy")`, W 96.
       - `txtCatLDesc` `=ThisItem.description`, FP 4.
       - `conCatLRowActs` (W 72 action group):
         - `icoCatLEdit` Edit icon, Tooltip/AccessibleLabel `="Edit " & ThisItem.name`,
           OnSelect (`|-`): `=EditForm(frm_catFrm_category); Navigate(scr_frm_category)`.
         - `icoCatLDelete` Delete icon, Tooltip/AccessibleLabel `="Hapus " & ThisItem.name`,
           `OnSelect: =UpdateContext({locSelectedRecord: ThisItem, locShowDeleteConfirm: true})`.
     - `txtCatLEmpty` "Tidak ada kategori yang cocok.", Height 380,
       `Visible: =IsEmpty(Search(dis_category_items, inp_cat_search.Text, name, code, description))`.

## Controls to Remove

con_cat_main, con_cat_sidebar, com_cat_sidebar, con_cat_content, com_cat_topbar, con_cat_body, con_cat_table,
con_cat_toolbar, con_cat_toolbarSpacer, con_cat_header, lbl_cat_hdrName, lbl_cat_hdrDate, lbl_cat_hdrCode,
lbl_cat_hdrDesc, con_cat_hdrSpacer, lbl_cat_hdrAction, con_cat_galleryWrap, con_cat_row, txt_cat_rowName,
txt_cat_rowDate, txt_cat_rowCode, txt_cat_rowDesc, btn_cat_rowEdit, con_cat_rowSpacer, btn_cat_rowDelete.
Keep inp_cat_search, btn_cat_add, gal_cat_list.

## Properties to Update

- Screen: Fill, LoadingSpinnerColor.
- inp_cat_search: Toolbar input styling (Height 36, FillPortions 0, AlignInContainer Stretch, LayoutMin* 0,
  Appearance Outline, Size 13, Radius 8 x4); drop X/Y/Width.
- btn_cat_add: Primary styling; drop X/Y.
- gal_cat_list: Gallery pattern props; Items unchanged; drop X/Y/Width.

## Layout and Visual Impact

- Toolbar: 832 - 168 - 8 = 656 for the search field.
- Card: 16 + 56 + 12 + 420 + 16 = 520 <= 532. Table 36 + 4 + 380.
- Row inner 806: fixed 96 + 96 + 72 + 4 x 8 = 296 -> FP 7 -> 72.9 per portion (name 219, description 291).

## Required Record Fields

| Field key | Record surface | Required field | Source field | Bound control | Exact formula | Placement and visibility |
| --- | --- | --- | --- | --- | --- | --- |
| cat/row/name | gal_cat_list row | Name | name | txtCatLName | `=ThisItem.name` | FP 3 Semibold |
| cat/row/code | row | Code | code | txtCatLCode | `=ThisItem.code` | W 96 |
| cat/row/date | row | Created date | 'Created On' | txtCatLDate | `=Text(ThisItem.'Created On', "dd/mm/yyyy")` | W 96 |
| cat/row/desc | row | Description | description | txtCatLDesc | `=ThisItem.description` | FP 4 |

## Required Actions

| Action | Preconditions | Entry point and event | Source and stable ID | Transition and postcondition | Mutation write set | Receipt proof set | Observer and evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ACT-CAT-SEARCH | none | inp_cat_search | dis_category_items | gal_cat_list filtered (Items preserved) | N/A | N/A | gal_cat_list, txtCatLEmpty |
| ACT-CAT-ADD | none | btn_cat_add.OnSelect | frm_catFrm_category | form New, scr_frm_category shown | N/A | N/A | TopBar "Tambah Kategori" |
| ACT-CAT-EDIT | row | icoCatLEdit.OnSelect | gal_cat_list.Selected.dis_category_item (clicked row) | form Edit prefilled | N/A | N/A | form cards |
| ACT-CAT-DELETE | row | icoCatLDelete -> btnCatLConfirmDel | locSelectedRecord.dis_category_item | clicked row removed | existence | "Dihapus" + name; Detail Kode, Deskripsi | conCatLReceipt; gal_cat_list |
| ACT-CAT-SAVE (observer) | saved on scr_frm_category | frm_catFrm_category.OnSuccess -> Back() | LastSubmit | back on list | see scr_frm_category | gblReceipt "Category" | conCatLReceipt |

## Functional Test Scenarios

| Scenario | Given | When | Then | Evidence surface | Boundary or negative case |
| --- | --- | --- | --- | --- | --- |
| SCN-CAT-SEARCH | C1 "Pipe", C2 "Pipe Fitting", C3 "Valve" | type "Pipe" | C1, C2 shown, C3 hidden | gal_cat_list | clear text restores 3; "zzz" -> txtCatLEmpty |
| SCN-CAT-ADD | none | Tambah Kategori | form New | scr_frm_category TopBar | N/A |
| SCN-CAT-EDIT | C2 | Edit icon on C2 | form shows C2 | form cards | N/A |
| SCN-CAT-DELETE | C3 | Delete icon -> Hapus | C3 removed | conCatLReceipt "Dihapus - Valve" | Batal keeps C3; category used by items -> error notify, no receipt |

## Relevant Data Source Schemas

dis_category_items: name, code, description, 'Created On', dis_category_item (Guid). Form frm_catFrm_category lives
on scr_frm_category (Item `=gal_cat_list.Selected`). Context: locSelectedRecord (dis_category_items record),
locShowDeleteConfirm (Boolean). Global gblReceipt.

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
- **Sidebar / TopBar** - `Control: CanvasComponent` + `ComponentName: Sidebar` (inputs activemenu, AlignInContainer,
  Fill, FillPortions, Height, LayoutMaxHeight, LayoutMaxWidth, LayoutMinHeight, LayoutMinWidth, Visible, Width, X, Y)
  / `ComponentName: TopBar` (inputs ActiveMenu, Subtitle + the same generic inputs).
