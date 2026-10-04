# Screen Plan: Log In

## Assignment

- Action: Modify (rewrite all children; keep YAML key)
- Target file: `C:\Project\Powerapps\app\Log In.pa.yaml`
- YAML key: Log In  (write it as `Log In:` under `Screens:`)
- Control name prefix: Login

Read `C:\Project\Powerapps\app\canvas-app-shared.md` first.

## Current State

ManualLayout welcome screen: Rectangle1, Label1_2, Label3_1, Button1 (`Navigate(HomeAdmin)` - compile error),
Label3, Image3, LabelLogInforUser, Label3_2, ButtonUser (`Navigate(HomeUser)` - compile error). `OnVisible` repeats
`LookUp(dis_users, email = User().Email)` twice to set imyrole / imyemail.

## Changes

1. Delete every existing child control (all are absolute-positioned; none is referenced elsewhere).
2. Delete the screen `OnVisible` property entirely (App.OnStart sets imyrole / imyemail from `nfMe`).
3. Screen Properties: `Fill: =clrBg`, `LoadingSpinnerColor: =clrAccent`.
4. Build the split welcome layout below (no Sidebar/TopBar). The screen `Children:` contains only `conLoginRoot`.

## Controls to Add

- `conLoginRoot` - AutoLayout Horizontal, `Width: =Parent.Width`, `Height: =Parent.Height`, LayoutMinWidth 0,
  LayoutMinHeight 0, Fill clrBg, LayoutGap 0, LayoutAlignItems Stretch, DropShadow None, Radius 0 x4.
  - `conLoginBrand` - AutoLayout Vertical, FillPortions 1, LayoutMinWidth 0, AlignInContainer Stretch, Fill clrNavy,
    Padding 48 x4, LayoutGap 16, LayoutJustifyContent Center, LayoutAlignItems Stretch, DropShadow None, Radius 0.
    - `imgLoginLogo` Image `='slb logo white'`, Width 140, Height 56, ImagePosition Fit, AlignInContainer Start,
      FillPortions 0, AccessibleLabel "SLB logo".
    - `txtLoginTitle` ModernText "DIGITAL INVENTORY SYSTEM", Color RGBA(255, 255, 255, 1), Size 30, Bold,
      Height 92, Wrap true (2 lines x 45 + 2), FillPortions 0, AlignInContainer Stretch.
    - `txtLoginTag` ModernText "Well Construction Equipment & Fluid - ING - TLM", Color RGBA(255, 255, 255, 0.8),
      Size 14, Height 42, Wrap true, FillPortions 0.
    Budget: 568 wide - 96 padding = 472 text width; title 30px Bold ~ 470px for "DIGITAL INVENTORY SYSTEM" -> may wrap,
    hence 2-line height. Vertical: 56 + 16 + 92 + 16 + 42 = 222 <= 640 - 96.
  - `conLoginRight` - AutoLayout Vertical, FillPortions 1, LayoutMinWidth 0, AlignInContainer Stretch, Fill clrBg,
    Padding 48 x4, LayoutJustifyContent Center, LayoutAlignItems Center, LayoutOverflowY Scroll, DropShadow None.
    - `conLoginCard` - Card pattern (Vertical, Fill clrSurface, border, DropShadow Light, Radius 16 x4), Width 420,
      Height 290, FillPortions 0, AlignInContainer Center, Padding 32 x4, LayoutGap 12, LayoutAlignItems Stretch.
      - `txtLoginHello` "Selamat datang," Size 14, clrTextMuted, Height 20.
      - `txtLoginName` `Text: =Coalesce(nfMe.Name, User().FullName)`, Size 24, Bold, clrText, Height 32, Wrap false.
      - `bdgLoginRole` Badge, `Content: =If(IsBlank(nfMe.role), "Belum terdaftar", Proper(Text(nfMe.role)))`,
        ThemeColor Brand, Appearance Tint, Shape Rounded, FontSize 12, Semibold, Width 160, Height 28,
        AlignInContainer Start, FillPortions 0, AccessibleLabel "Peran pengguna".
      - `txtLoginDesc` "Kelola stok, transaksi, dan pemakaian peralatan dalam satu aplikasi.", Size 13,
        clrTextMuted, Height 40, Wrap true.
      - `btnLoginEnter` ModernButton Primary (BasePaletteColor clrNavy), Text "Masuk ke Dashboard", Icon "ArrowRight",
        `Layout: =ButtonLayout.IconAfter`, Height 44, AlignInContainer Stretch, FillPortions 0, LayoutMinWidth 0,
        LayoutMinHeight 0, Size 14, Radius 8 x4,
        `DisplayMode: =If(IsBlank(nfMe.Name), DisplayMode.Disabled, DisplayMode.Edit)`,
        `OnSelect: =Navigate(scr_dashboard, ScreenTransition.Fade)`, AccessibleLabel "Masuk ke Dashboard".
      Vertical budget: 32 + 20 + 12 + 32 + 12 + 28 + 12 + 40 + 12 + 44 + 32 = 276 <= 290.
      Horizontal: card inner 420 - 64 = 356; button label at 14px ~ 150px fits.

## Controls to Remove

Rectangle1, Label1_2, Label3_1, Button1, Label3, Image3, LabelLogInforUser, Label3_2, ButtonUser; screen OnVisible.

## Properties to Update

Screen: Fill, LoadingSpinnerColor (above); remove OnVisible.

## Layout and Visual Impact

- Fixed desktop 1136 x 640: two halves of 568; card centred in the right half (568 - 96 = 472 >= 420).
- Visual: brand navy panel with white type (Color set explicitly on every text inside it), white card on clrBg.

## Required Actions

| Action | Preconditions | Entry point and event | Source and stable ID | Transition and postcondition | Mutation write set | Receipt proof set | Observer and evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ACT-LOGIN-ENTER | `!IsBlank(nfMe.Name)` | btnLoginEnter.OnSelect | nfMe | navigates to scr_dashboard for every registered role (no HomeAdmin/HomeUser) | N/A | N/A | Dashboard TopBar "Dashboard" |
| ACT-APP-START (observer) | registered user | App.StartScreen | nfMe | Log In shown | N/A | N/A | txtLoginName shows nfMe.Name, bdgLoginRole real role |

## Functional Test Scenarios

| Scenario | Given | When | Then | Evidence surface | Boundary or negative case |
| --- | --- | --- | --- | --- | --- |
| SCN-START-REGISTERED | dis_users row for User().Email (role administrator) | launch | Log In shows name + "Administrator" | txtLoginName, bdgLoginRole | N/A |
| SCN-LOGIN-ENTER | registered user | click Masuk ke Dashboard | scr_dashboard | Dashboard | disabled if nfMe blank |

## Relevant Data Source Schemas

App named formula `nfMe` = dis_users row: Name (Text), role (option set `dis_role`), email.

## Changed or Added Control Definitions

AutoLayout child extras for all: AlignInContainer (`=AlignInContainer.Stretch` / `.Start` / `.Center`), FillPortions,
LayoutMaxHeight, LayoutMaxWidth, LayoutMinHeight, LayoutMinWidth.

- **GroupContainer** - `Control: GroupContainer`, `Variant: AutoLayout`. Inputs: BorderColor, BorderStyle,
  BorderThickness, ContentLanguage, DropShadow, EnableChildFocus, Fill, Height, LayoutAlignItems, LayoutDirection,
  LayoutGap, LayoutJustifyContent, LayoutOverflowX, LayoutOverflowY, LayoutWrap, PaddingBottom, PaddingLeft,
  PaddingRight, PaddingTop, RadiusBottomLeft, RadiusBottomRight, RadiusTopLeft, RadiusTopRight, Visible, Width, X, Y.
  Literals: `=DropShadow.None` / `.Light`; `=BorderStyle.Solid`; `=LayoutDirection.Horizontal` / `.Vertical`;
  `=LayoutAlignItems.Stretch` / `.Center`; `=LayoutJustifyContent.Center`; `=LayoutOverflow.Scroll`.
- **ModernText** - `Control: ModernText`. Inputs: AccessibleLabel, Align, AutoHeight, BorderColor, BorderStyle,
  BorderThickness, Color, ContentLanguage, DisplayMode, Fill, Font, FontWeight, Height, Italic, OnSelect,
  PaddingBottom, PaddingLeft, PaddingRight, PaddingTop, Radius*, Size, Strikethrough, Text, Underline, VerticalAlign,
  Visible, Width, Wrap, X, Y. Literals: `=Font.'Segoe UI'`, `=FontWeight.Bold` / `.Normal`.
- **ModernButton** - `Control: ModernButton`. Inputs: AccessibleLabel, Align, Appearance, BasePaletteColor,
  BorderColor, BorderStyle, BorderThickness, Color, ContentLanguage, DisplayMode, Font, FontWeight, Height, Icon,
  IconRotation, IconStyle, Italic, Layout, OnSelect, Padding*, Radius*, Size, Strikethrough, Text, Tooltip,
  Underline, VerticalAlign, Visible, Width, X, Y. Literals: `=ButtonAppearance.Primary`, `=ButtonLayout.IconAfter`,
  `=DisplayMode.Disabled` / `.Edit`.
- **Badge** - `Control: Badge`. Inputs: AccessibleLabel, Align, Appearance, BasePaletteColor, Content,
  ContentLanguage, DisplayMode, Font, FontColor, FontItalic, FontSize, FontStrikethrough, FontUnderline, FontWeight,
  Height, Shape, ThemeColor, VerticalAlign, Visible, Width, X, Y. Literals: `='BadgeCanvas.Appearance'.Tint`,
  `='BadgeCanvas.Shape'.Rounded`, `='BadgeCanvas.ThemeColor'.Brand`, `=FontWeight.Semibold`.
- **Image** - `Control: Image`. Inputs: AccessibleLabel, ApplyEXIFOrientation, AutoDisableOnSelect, BorderColor,
  BorderStyle, BorderThickness, CalculateOriginalDimensions, ContentLanguage, DisabledBorderColor, DisabledFill,
  DisplayMode, Fill, FlipHorizontal, FlipVertical, FocusedBorderColor, FocusedBorderThickness, Height,
  HoverBorderColor, HoverFill, Image, ImagePosition, ImageRotation, OnSelect, Padding*, PressedBorderColor,
  PressedFill, Radius*, TabIndex, Tooltip, Transparency, Visible, Width, X, Y. Literal: `=ImagePosition.Fit`.
