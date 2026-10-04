# Screen Plan: User

## Assignment

- Action: Modify (rewrite layout; keep YAML key, Form4 with every data card, Gallery8_13, Button36, Button37)
- Target file: `C:\Project\Powerapps\app\scr_user.pa.yaml`
- YAML key: scr_user
- Control name prefix: UsrL

Read `C:\Project\Powerapps\app\canvas-app-shared.md` first (Shell, Card, Table, Confirm strip, Receipt strip,
Form rules).

## Current State

`con_Main_template_6` shell (ManualLayout sidebar holder, Sidebar "User"; TopBar "User") with `Container7_1` ->
`Container3`: Label header `Container20_11` and ManualLayout `Container10_12` with `Gallery8_13`
(`Items: =dis_users`; rows Text1_23 Name, Text1_24 email, Type_35 role, Type_36 Assigned_area.Name, Type_37 empty,
Button30_4 "Update", spacer, Button33_3 "Delete"). Two screen-level ManualLayout overlays:
`cntDeleteConfirm_1` (Visible `locShowDeleteConfirm_1`, Button34_1 removes `Gallery8_13.Selected`, Button35_1 cancel)
and `form_data` (Visible `locShowUserPopUp`) containing Text5 title, `Form4` (Modern, DataSource `dis_users`,
Item `=Gallery8_13.Selected`, NumberOfColumns 2, Height 330; cards Name_DataCard1 X0 Y0, email_DataCard2 X1 Y0,
role_DataCard1 X0 Y1, Assigned_area_DataCard1 X1 Y1), and `Container45` with Button36 (SubmitForm(Form4)) /
Button37 (ResetForm + hide).

Bugs: Button30_4 / Button33_3 set `locSelectedRecord: Blank()` (untyped warnings); Delete removes
`Gallery8_13.Selected`; Form4 edits the selected row, not necessarily the clicked row; delete notify says "area".

## Changes

1. Screen Properties: `Fill: =clrBg`, `LoadingSpinnerColor: =clrAccent`. Screen `Children:` = `conUsrLRoot` only.
2. Shell pattern with prefix UsrL: conUsrLRoot, cmpUsrLSidebar (`activemenu: ="User"`), conUsrLMain,
   cmpUsrLTopBar (`ActiveMenu: ="User"`, `Subtitle: ="Kelola pengguna dan peran"`), conUsrLBody.
3. The popup overlay becomes an inline editor card at the top of the body; the delete overlay becomes a confirm strip
   above the list card (shared approximation: no screen-level overlays).
4. Bug fixes: row actions store `locSelectedRecord: ThisItem`; `Form4.Item: =locSelectedRecord`; confirm removes
   `locSelectedRecord`.

## Controls to Add

conUsrLBody children, in order (FillPortions 0, AlignInContainer Stretch):

1. `conUsrLReceipt` - Receipt strip, `Visible: =gblReceipt.Screen = "User"` (icoUsrLRcIco, conUsrLRcText,
   txtUsrLRcTitle, txtUsrLRcDetail, icoUsrLRcClose).
2. `conUsrLEditor` - Card pattern, Height 316, LayoutGap 12, `Visible: =locShowUserPopUp`. Children:
   - `txtUsrLEdTitle` card title `Text: ="Edit Pengguna - " & locSelectedRecord.Name`.
   - `Form4` (moved; Height 200; see Properties to Update).
   - `conUsrLEdActions` AutoLayout Horizontal, Height 36, LayoutJustifyContent End, LayoutAlignItems Center,
     LayoutGap 12, transparent, DropShadow None, Radius 0 x4, FillPortions 0, AlignInContainer Stretch:
     - `Button37` (kept name) Secondary, Icon "Dismiss", Text "Batal", W 96,
       OnSelect preserved (`|-`): `=ResetForm(Form4); UpdateContext({locShowUserPopUp: false})`.
     - `Button36` (kept name) Primary, Icon "Save", Text "Simpan", W 120, `OnSelect: =SubmitForm(Form4)`.
3. `conUsrLConfirm` - Confirm strip, `Visible: =locShowDeleteConfirm_1`:
   - `txtUsrLConfirmMsg` `Text: ="Hapus pengguna " & locSelectedRecord.Name & " (" & locSelectedRecord.email & ")?"`.
   - `btnUsrLConfirmDel` (Destructive "Hapus", W 104), OnSelect (`|-`):
     ```
     =With(
         {target: locSelectedRecord},
         Remove(dis_users, target);
         If(
             IsEmpty(Errors(dis_users)),
             Set(
                 gblReceipt,
                 {
                     Screen: "User",
                     Action: "Dihapus",
                     Title: target.Name,
                     Detail: "Email " & target.email & " | Role " & Text(target.role)
                 }
             );
             UpdateContext({locShowDeleteConfirm_1: false});
             Notify("Data user berhasil dihapus!", NotificationType.Success),
             Notify("Gagal menghapus user. " & First(Errors(dis_users)).Message, NotificationType.Error)
         )
     )
     ```
   - `btnUsrLConfirmCancel` (Secondary "Batal", W 96), `OnSelect: =UpdateContext({locShowDeleteConfirm_1: false})`.
4. `conUsrLListCard` - Card pattern, Height 488, LayoutGap 12. Children:
   - `txtUsrLCardTitle` card title "Daftar Pengguna".
   - `conUsrLTable` AutoLayout Vertical, Height 420, LayoutGap 4, transparent, DropShadow None, Radius 0 x4,
     LayoutAlignItems Stretch:
     - `conUsrLHead` header cells: `txtUsrLHName` "NAMA" FP 3, `txtUsrLHEmail` "EMAIL" FP 3, `txtUsrLHRole` "ROLE"
       W 112, `txtUsrLHArea` "AREA" FP 2, `txtUsrLHAct` "AKSI" W 72.
     - `Gallery8_13` (kept) Gallery pattern, Height 380, TemplateSize 52, `Items: =dis_users` (unchanged),
       AccessibleLabel "Daftar pengguna", `Visible: =!IsEmpty(dis_users)`. Row `conUsrLRow`:
       - `txtUsrLName` `=ThisItem.Name`, Semibold, FP 3.
       - `txtUsrLEmail` `=ThisItem.email`, FP 3.
       - `bdgUsrLRole` Badge W 112, `Content: =Proper(Text(ThisItem.role))`,
         `ThemeColor: =Switch(Text(ThisItem.role), "administrator", 'BadgeCanvas.ThemeColor'.Brand, "approval", 'BadgeCanvas.ThemeColor'.Success, "notifier", 'BadgeCanvas.ThemeColor'.Warning, 'BadgeCanvas.ThemeColor'.Subtle)`,
         AlignInContainer Center, AccessibleLabel `="Role " & Text(ThisItem.role)`.
       - `txtUsrLArea` `=Coalesce(ThisItem.Assigned_area.Name, "-")`, FP 2.
       - `conUsrLRowActs` (W 72 action group, as in the Area brief):
         - `icoUsrLEdit` Edit icon, Tooltip/AccessibleLabel `="Edit " & ThisItem.Name`, OnSelect (`|-`):
           `=UpdateContext({locSelectedRecord: ThisItem, locShowUserPopUp: true, locShowDeleteConfirm_1: false}); Set(gblFormMode, "Update"); EditForm(Form4)`.
         - `icoUsrLDelete` Delete icon, Tooltip/AccessibleLabel `="Hapus " & ThisItem.Name`,
           `OnSelect: =UpdateContext({locSelectedRecord: ThisItem, locShowDeleteConfirm_1: true, locShowUserPopUp: false})`.
     - `txtUsrLEmpty` "Belum ada pengguna.", Height 380, `Visible: =IsEmpty(dis_users)`.

## Controls to Remove

con_Main_template_6, con_sidebar_template_6, com_sidebar_template_6, con_content_template_6, com_topbar_template_6,
Container7_1, Container3, Container20_11, Label21_59..Label21_63, Container21_6, Container10_12, Container11_11,
Text1_23, Text1_24, Type_35, Type_36, Type_37, Button30_4, Container24_2, Button33_3, cntDeleteConfirm_1,
Container36_1, Container37_1, Text1_20, Container35_1, Button34_1, Container38_1, Button35_1, form_data, Container43,
Container44, Text5, Container45, Container46_1, Container46, Container46_2.
Keep Form4 (+ all cards and card children), Gallery8_13, Button36, Button37.

## Properties to Update

- `Form4`: keep Control/Variant/Layout, DataSource `=dis_users`, NumberOfColumns 2, all cards. Change
  `Item: =locSelectedRecord`. Set AlignInContainer Stretch, FillPortions 0, `Height: =200`, `Fill: =clrSurface`,
  `BorderThickness: =0`; delete X, Y, Width. OnSuccess (`|-`):
  ```
  =Set(
      gblReceipt,
      {
          Screen: "User",
          Action: "Disimpan",
          Title: Form4.LastSubmit.Name,
          Detail: "Email " & Form4.LastSubmit.email & " | Role " & Text(Form4.LastSubmit.role) & " | Area " & Coalesce(Form4.LastSubmit.Assigned_area.Name, "-")
      }
  );
  Notify("Data user berhasil disimpan!", NotificationType.Success);
  ResetForm(Self);
  UpdateContext({locShowUserPopUp: false})
  ```
- Data cards `Width` only: Name_DataCard1, email_DataCard2, role_DataCard1, Assigned_area_DataCard1 all
  `=Parent.Width / 2`. Everything else on cards unchanged.

## Layout and Visual Impact

- Editor: 16 + 24 + 12 + 200 + 12 + 36 + 16 = 316. List card: 16 + 24 + 12 + 420 + 16 = 488 <= 532.
- Row inner 806: fixed 112 + 72 + 4 x 8 = 216 -> FP 8 -> 73.75 per portion (name/email 221, area 147).
- When editor / confirm / receipt are visible the body scrolls; the editor is the first child, so it appears in the
  initial viewport.

## Required Record Fields

| Field key | Record surface | Required field | Source field | Bound control | Exact formula | Placement and visibility |
| --- | --- | --- | --- | --- | --- | --- |
| user/row/name | Gallery8_13 row | Name | Name | txtUsrLName | `=ThisItem.Name` | FP 3 Semibold |
| user/row/email | row | Email | email | txtUsrLEmail | `=ThisItem.email` | FP 3 |
| user/row/role | row | Role | role | bdgUsrLRole | `Content: =Proper(Text(ThisItem.role))` | W 112 badge |
| user/row/area | row | Assigned area | Assigned_area.Name | txtUsrLArea | `=Coalesce(ThisItem.Assigned_area.Name, "-")` | FP 2 |

## Required Actions

| Action | Preconditions | Entry point and event | Source and stable ID | Transition and postcondition | Mutation write set | Receipt proof set | Observer and evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ACT-USER-EDIT | row exists | icoUsrLEdit.OnSelect | ThisItem.dis_user -> locSelectedRecord | editor visible; Form4 Edit with clicked row | N/A | N/A | txtUsrLEdTitle "Edit Pengguna - <Name>", prefilled cards |
| ACT-USER-SAVE | editor open, form valid | Button36.OnSelect -> Form4.OnSuccess | Form4.LastSubmit.dis_user | row updated; editor hidden | Name, email, role, Assigned_area | Title Name; Detail Email, Role, Area | conUsrLReceipt; Gallery8_13 row |
| ACT-USER-DELETE | row exists | icoUsrLDelete -> btnUsrLConfirmDel | locSelectedRecord.dis_user | clicked row removed | existence | "Dihapus" + Name; Detail Email, Role | conUsrLReceipt; Gallery8_13 |

## Functional Test Scenarios

| Scenario | Given | When | Then | Evidence surface | Boundary or negative case |
| --- | --- | --- | --- | --- | --- |
| SCN-USER-EDIT | U1, U2 | Edit icon on U2 | editor visible, U2 values | txtUsrLEdTitle "Edit Pengguna - U2"; Form4 cards | Batal hides editor, nothing saved |
| SCN-USER-SAVE | editor U2, role -> approval | Simpan | U2.role = approval; editor hidden | conUsrLReceipt "Role approval"; bdgUsrLRole "Approval" | Name blank -> card error, editor stays |
| SCN-USER-DELETE | U1 selected, Delete on U2 | Hapus | only U2 removed | conUsrLReceipt "Dihapus - U2" | Batal keeps U2 |

## Relevant Data Source Schemas

dis_users: Name (required), email, role (option set `dis_role`: user, administrator, notifier, approval),
Assigned_area (-> dis_areas .Name), dis_user (Guid). Context vars: locSelectedRecord (dis_users record, always
ThisItem), locShowUserPopUp, locShowDeleteConfirm_1 (Boolean). Global gblFormMode, gblReceipt.

## Required Variants

GroupContainer -> AutoLayout. Gallery -> Vertical (unchanged). Form -> Modern (unchanged). TypedDataCard variants
unchanged (ModernTextualEdit, ModernComboBoxOptionSetSingleEdit, PcfCoreComboBoxEditCard).

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
- **Form** (existing, preserved) - `Control: Form`, `Variant: Modern`, `Layout: Vertical`. Inputs: AcceptsFocus,
  BorderColor, BorderStyle, BorderThickness, ContentLanguage, DataSource, DefaultMode, Fill, FocusedBorderColor,
  FocusedBorderThickness, Height, Item, NumberOfColumns, OnFailure, OnReset, OnSuccess, SnapToColumns, Visible,
  Width, X, Y. Outputs: Error, ErrorKind, LastSubmit, Mode, Unsaved, Updates, Valid. TypedDataCards and their
  children (Classic/ComboBox, FluentV8/Label, Label, Image, AddMedia, Modern inputs) are preserved as-is; only
  card `Width` changes. Do not create data cards.
- **Sidebar / TopBar** - `Control: CanvasComponent` + `ComponentName: Sidebar` (inputs activemenu, AlignInContainer,
  Fill, FillPortions, Height, LayoutMaxHeight, LayoutMaxWidth, LayoutMinHeight, LayoutMinWidth, Visible, Width, X, Y)
  / `ComponentName: TopBar` (inputs ActiveMenu, Subtitle + the same generic inputs).
