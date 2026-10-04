# Screen Plan: Template

## Assignment

- Action: Modify (rewrite children; keep YAML key)
- Target file: `C:\Project\Powerapps\app\Template.pa.yaml`
- YAML key: Template
- Control name prefix: Tpl

Read `C:\Project\Powerapps\app\canvas-app-shared.md` first (Shell + Card patterns).

## Current State

`con_Main_template` (AutoLayout) with ManualLayout `con_sidebar_template` holding `com_sidebar_template`
(activemenu "Transaction") and `con_content_template` (Width 975) holding `com_topbar_template`
(Width App.Width - 150). Nothing else; no references from other screens.

## Changes

1. Remove all existing children.
2. Screen Properties: `Fill: =clrBg`, `LoadingSpinnerColor: =clrAccent`.
3. Instantiate the Shell pattern with prefix Tpl: conTplRoot, cmpTplSidebar (`activemenu: =""`), conTplMain,
   cmpTplTopBar (`ActiveMenu: ="Template"`, `Subtitle: ="Kerangka halaman baru"`), conTplBody.
4. Add one body card `conTplCard` (Card pattern, Height 200, FillPortions 0, LayoutGap 8) with:
   - `txtTplCardTitle` "Area konten" (card title, Size 16 Semibold, Height 24).
   - `txtTplCardBody` "Salin layar ini untuk membuat halaman baru: sidebar, top bar dan body yang dapat di-scroll
     sudah tersedia. Tambahkan kartu konten di dalam body." Size 13 clrTextMuted, Height 60, Wrap true.
     Use a `|-` block or single quotes because the text contains `: `.
   Card budget: 16 + 24 + 8 + 60 + 16 = 124 <= 200 (remaining space intentional placeholder area).

## Controls to Remove

con_Main_template, con_sidebar_template, com_sidebar_template, con_content_template, com_topbar_template.

## Layout and Visual Impact

Fixed desktop: Sidebar 224 + main 912; body inner 864 x 532; card 864 x 200.

## Required Actions

| Action | Preconditions | Entry point and event | Source and stable ID | Transition and postcondition | Mutation write set | Receipt proof set | Observer and evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ACT-NAV-MENU | screen open | Sidebar rows | fxMenuItems | navigates | N/A | N/A | no active pill (activemenu "") |

## Functional Test Scenarios

| Scenario | Given | When | Then | Evidence surface | Boundary or negative case |
| --- | --- | --- | --- | --- | --- |
| SCN-NAV-MENU | on Template | click "Item" | scr_item shown | scr_item TopBar | N/A |

## Required Variants

GroupContainer -> AutoLayout.

## Changed or Added Control Definitions

AutoLayout child extras: AlignInContainer (`=AlignInContainer.Stretch` / `.Start`), FillPortions, LayoutMaxHeight,
LayoutMaxWidth, LayoutMinHeight, LayoutMinWidth.

- **GroupContainer** - `Control: GroupContainer`, `Variant: AutoLayout`. Inputs: BorderColor, BorderStyle,
  BorderThickness, ContentLanguage, DropShadow, EnableChildFocus, Fill, Height, LayoutAlignItems, LayoutDirection,
  LayoutGap, LayoutJustifyContent, LayoutOverflowX, LayoutOverflowY, LayoutWrap, PaddingBottom, PaddingLeft,
  PaddingRight, PaddingTop, RadiusBottomLeft, RadiusBottomRight, RadiusTopLeft, RadiusTopRight, Visible, Width, X, Y.
  Literals: `=DropShadow.None` / `.Light`, `=BorderStyle.Solid`, `=LayoutDirection.Horizontal` / `.Vertical`,
  `=LayoutAlignItems.Stretch`, `=LayoutOverflow.Scroll`.
- **ModernText** - `Control: ModernText`. Inputs: AccessibleLabel, Align, AutoHeight, BorderColor, BorderStyle,
  BorderThickness, Color, ContentLanguage, DisplayMode, Fill, Font, FontWeight, Height, Italic, OnSelect,
  PaddingBottom, PaddingLeft, PaddingRight, PaddingTop, Radius*, Size, Strikethrough, Text, Underline, VerticalAlign,
  Visible, Width, Wrap, X, Y. Literals: `=Font.'Segoe UI'`, `=FontWeight.Semibold`.
- **Sidebar / TopBar** - `Control: CanvasComponent` + `ComponentName: Sidebar` (inputs activemenu, AlignInContainer,
  Fill, FillPortions, Height, LayoutMaxHeight, LayoutMaxWidth, LayoutMinHeight, LayoutMinWidth, Visible, Width, X, Y)
  / `ComponentName: TopBar` (ActiveMenu, Subtitle + same generic inputs).
