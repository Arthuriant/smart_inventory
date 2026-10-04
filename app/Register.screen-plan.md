# Screen Plan: Register

## Assignment

- Action: Modify (rewrite all children; keep YAML key)
- Target file: `C:\Project\Powerapps\app\Register.pa.yaml`
- YAML key: Register
- Control name prefix: Reg

Read `C:\Project\Powerapps\app\canvas-app-shared.md` first.

## Current State

ManualLayout navy screen: Label13, Label15, Label16, Image3_1 and Gallery5
(`BrowseLayout_Vertical_TwoTextOneImageVariant_ver5.0`, absolute rows) listing
`Filter(dis_users, role = dis_role.administrator)`. Subtitle2 uses `ThisItem.elv_assigned_area.Name` (compile error);
NextArrow1 launches "outlook.com" instead of mailing the admin.

## Changes

1. Delete every existing child (none referenced elsewhere).
2. Screen Properties: `Fill: =clrBg`, `LoadingSpinnerColor: =clrAccent`.
3. Build the split layout below; the screen `Children:` contains only `conRegRoot`.

## Controls to Add

- `conRegRoot` - AutoLayout Horizontal, `Width: =Parent.Width`, `Height: =Parent.Height`, LayoutMinWidth 0,
  LayoutMinHeight 0, Fill clrBg, LayoutAlignItems Stretch, LayoutGap 0, DropShadow None, Radius 0 x4.
  - `conRegBrand` - identical values to the Log In brand panel: AutoLayout Vertical, FillPortions 1, Fill clrNavy,
    Padding 48 x4, LayoutGap 16, LayoutJustifyContent Center, LayoutAlignItems Stretch. Children:
    `imgRegLogo` (Image `='slb logo white'` 140 x 56, Fit, AlignInContainer Start), `txtRegTitle`
    ("DIGITAL INVENTORY SYSTEM", white, Size 30 Bold, Height 92, Wrap true), `txtRegTag`
    ("Well Construction Equipment & Fluid - ING - TLM", RGBA(255, 255, 255, 0.8), Size 14, Height 42, Wrap true).
  - `conRegRight` - AutoLayout Vertical, FillPortions 1, Fill clrBg, Padding 48 x4, LayoutJustifyContent Center,
    LayoutAlignItems Center, LayoutOverflowY Scroll.
    - `conRegCard` - Card (Radius 16), Width 472, Height 466, AlignInContainer Center, FillPortions 0, Padding 28 x4,
      LayoutGap 12, LayoutAlignItems Stretch.
      - `txtRegHello` "Halo, pengguna baru", Size 24 Bold clrText, Height 32, Wrap false.
      - `txtRegIntro` "Untuk menggunakan Digital Inventory App, silakan hubungi salah satu Administrator berikut
        untuk pendaftaran akun:", Size 13 clrTextMuted, Height 54, Wrap true (3 lines x 18).
      - `galRegAdmins` Gallery Vertical, Height 300, TemplateSize 72, TemplatePadding 1, Fill clrBorder,
        `Items: =Filter(dis_users, role = dis_role.administrator)`, Selectable false, TabIndex 0,
        AccessibleLabel "Daftar administrator",
        `Visible: =!IsEmpty(Filter(dis_users, role = dis_role.administrator))`.
        - `conRegRow` shell (pattern), PaddingLeft 12, PaddingRight 8, LayoutGap 12, LayoutAlignItems Center:
          - `icoRegAvatar` ModernIcon "Person", 40 x 40, Padding 9 x4, Radius 20 x4, Fill clrRowSelected,
            IconColor clrNavy, FillPortions 0, AlignInContainer Center, AccessibleLabel "Administrator".
          - `conRegRowTxt` AutoLayout Vertical, FillPortions 1, Height 60, LayoutGap 2, LayoutJustifyContent Center,
            LayoutAlignItems Stretch, AlignInContainer Center:
            - `txtRegName` `=ThisItem.Name`, Size 14 Semibold clrText, Height 20.
            - `txtRegEmail` `=ThisItem.email`, Size 12 clrTextMuted, Height 18.
            - `txtRegArea` `Text: '="Area: " & Coalesce(ThisItem.Assigned_area.Name, "-")'`, Size 12 clrTextMuted,
              Height 18.
          - `icoRegMail` ModernIcon "Mail", 36 x 36, Padding 7 x4, Radius 8 x4, IconColor clrAccent,
            FillPortions 0, AlignInContainer Center, Tooltip `="Kirim email ke " & ThisItem.Name`,
            AccessibleLabel same, `OnSelect: =Launch("mailto:" & ThisItem.email)`.
      - `txtRegEmpty` "Belum ada administrator terdaftar.", Height 300, Align Center, clrTextMuted,
        `Visible: =IsEmpty(Filter(dis_users, role = dis_role.administrator))`.
      Vertical: 28 + 32 + 12 + 54 + 12 + 300 + 28 = 466. Right half 640 - 96 = 544 >= 466.
      Row: 20 + 2 + 18 + 2 + 18 = 60 <= 72 template. Row width 472 - 56 - 2 - 20 = 394: 40 + 36 + 2 x 12 = 100 ->
      text 294 (emails ~ 230px at 12px fit).

## Controls to Remove

Label13, Label15, Label16, Image3_1, Gallery5 and its children (Title2, Subtitle2, NextArrow1, Separator3,
Rectangle13, Label40, Rectangle8_2).

## Required Record Fields

| Field key | Record surface | Required field | Source field | Bound control | Exact formula | Placement and visibility |
| --- | --- | --- | --- | --- | --- | --- |
| reg/row/name | galRegAdmins row | Name | Name | txtRegName | `=ThisItem.Name` | line 1, Semibold |
| reg/row/email | row | Email | email | txtRegEmail | `=ThisItem.email` | line 2 |
| reg/row/area | row | Assigned area | Assigned_area.Name | txtRegArea | `="Area: " & Coalesce(ThisItem.Assigned_area.Name, "-")` | line 3 (fixes elv_assigned_area error) |

## Required Actions

| Action | Preconditions | Entry point and event | Source and stable ID | Transition and postcondition | Mutation write set | Receipt proof set | Observer and evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ACT-REG-CONTACT | admin rows | icoRegMail.OnSelect | dis_users admin email | mail client opens addressed to that admin | N/A | N/A | row text identifies admin |

## Functional Test Scenarios

| Scenario | Given | When | Then | Evidence surface | Boundary or negative case |
| --- | --- | --- | --- | --- | --- |
| SCN-START-UNREGISTERED | no dis_users row for User().Email | launch | Register shown | conRegCard | N/A |
| SCN-REG-LIST | 2 admins + 1 user | open | 2 rows with name, email, area | galRegAdmins | mail icon -> mailto:<admin email>; zero admins -> txtRegEmpty |

## Relevant Data Source Schemas

dis_users: Name, email, role (option set `dis_role`: user, administrator, notifier, approval), Assigned_area
(lookup -> dis_areas, `.Name`). There is NO `elv_assigned_area` column.

## Required Variants

GroupContainer -> AutoLayout. Gallery -> Vertical (replaces the BrowseLayout variant; new control name).

## Changed or Added Control Definitions

AutoLayout child extras: AlignInContainer (`=AlignInContainer.Stretch` / `.Start` / `.Center`), FillPortions,
LayoutMaxHeight, LayoutMaxWidth, LayoutMinHeight, LayoutMinWidth.

- **GroupContainer** - `Control: GroupContainer`, `Variant: AutoLayout`. Inputs: BorderColor, BorderStyle,
  BorderThickness, ContentLanguage, DropShadow, EnableChildFocus, Fill, Height, LayoutAlignItems, LayoutDirection,
  LayoutGap, LayoutJustifyContent, LayoutOverflowX, LayoutOverflowY, LayoutWrap, Padding*, Radius*, Visible, Width,
  X, Y. Literals: `=DropShadow.None` / `.Light`; `=BorderStyle.Solid`; `=LayoutDirection.*`; `=LayoutAlignItems.*`;
  `=LayoutJustifyContent.Center`; `=LayoutOverflow.Scroll`.
- **ModernText** - `Control: ModernText`. Inputs: AccessibleLabel, Align, AutoHeight, BorderColor, BorderStyle,
  BorderThickness, Color, ContentLanguage, DisplayMode, Fill, Font, FontWeight, Height, Italic, OnSelect, Padding*,
  Radius*, Size, Strikethrough, Text, Underline, VerticalAlign, Visible, Width, Wrap, X, Y.
  Literals: `=Font.'Segoe UI'`, `=FontWeight.Bold` / `.Semibold`, `=Align.Center`.
- **ModernIcon** - `Control: ModernIcon`. Inputs: AccessibleLabel, BasePaletteColor, BorderColor, BorderStyle,
  BorderThickness, ContentLanguage, DisplayMode, Fill, Height, Icon, IconColor, IconStyle, OnSelect, Padding*,
  Radius*, Rotation, Tooltip, Visible, Width, X, Y.
- **Gallery** - `Control: Gallery`, `Variant: Vertical`. Inputs: AccessibleLabel, BorderColor, BorderStyle,
  BorderThickness, ContentLanguage, Default, DelayItemLoading, DisplayMode, Fill, FocusedBorderColor,
  FocusedBorderThickness, Height, Items, LoadingSpinner, LoadingSpinnerColor, NavigationStep, Selectable,
  ShowNavigation, ShowScrollbar, TabIndex, TemplatePadding, TemplateSize, Transition, Visible, Width, WrapCount, X, Y.
- **Image** - `Control: Image`. Inputs as in shared list: AccessibleLabel, BorderColor, BorderStyle, BorderThickness,
  DisplayMode, Fill, Height, Image, ImagePosition (`=ImagePosition.Fit`), Radius*, Tooltip, Visible, Width, X, Y
  (plus ApplyEXIFOrientation, AutoDisableOnSelect, CalculateOriginalDimensions, ContentLanguage, Disabled*, Flip*,
  Focused*, Hover*, ImageRotation, OnSelect, Padding*, Pressed*, TabIndex, Transparency).
