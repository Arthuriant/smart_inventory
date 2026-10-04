# Discovery Packet (gathered by orchestrator via Canvas Authoring MCP, 2026-10-04)

Session: environment c2194d0b-89b3-ed3b-b65a-1db58a779659, app 87f60c80-e3c1-45bf-ba27-93eb0c079759.
Baseline compile: 5 errors / 2 warnings (listed in canvas-app-requirements.md).

## Data sources (all CdsNative, Writable, Delegatable)
dis_areas, dis_category_items, dis_geounits, dis_histories, dis_item_v2S, dis_items, dis_locations,
dis_move_items, dis_stocks, dis_subbls, dis_trx_details, dis_trx_headers, dis_users, Users.
Note: the app uses dis_item_v2S (not dis_items) everywhere for items.

### dis_users (Power Fx display names in use)
Name (elv_name, String), email (elv_email, String), role (elv_role, OptionSet `dis_role`: user,
administrator, notifier, approval), spv_email (String), dis_user (Guid, elv_dis_userid),
Assigned_area (cr8a3_Assigned_area, DataEntity -> dis_areas; display name "Assigned_area"),
'dis_areas (cr8a3_elv_dis_user_elv_dis_area_elv_dis_area)' (DataEntity, N:N areas),
'Created On'. There is NO column elv_assigned_area (that is the source of the baseline errors).

### dis_stocks
dis_item_v2 (DataEntity -> dis_item_v2S), dis_area (DataEntity -> dis_areas), PK (String),
qty (Number), dis_stock (Guid), 'Created On', 'Modified On'.

### dis_item_v2S
name, part_number (shown as BPN), client_number (shown as SPN), description (String),
dis_category_item (DataEntity -> dis_category_items), min_qty (Number), Image (Record/image),
status (OptionSet `status (dis_item_v2S)`: Active, Non-Active),
uom (OptionSet `uom (dis_item_v2S)`: EA, M, SET, DR, JT, BOX, L, PR, SX, FT, GAL, KG, BBL, MT),
area (DataEntity), dis_item_v2 (Guid), 'Created On'.

### dis_trx_headers
transaction_number (String), note (String), type (OptionSet `type (dis_trx_headers)`: Receive,
Consume, Transfer), area_form (DataEntity -> dis_areas; logical cr8a3_area_from; display name is
literally "area_form"), area_to (DataEntity -> dis_areas), dis_trx_header (Guid), 'Created On'.

### Other bindings used by existing YAML (verified compiling in baseline)
dis_trx_details: header_id (-> dis_trx_headers), item (-> dis_item_v2S), qty, PK.
dis_category_items: name, code, description, dis_category_item (Guid), 'Created On'.
dis_areas: Name, 'elv_location (cr8a3_elv_location)' (-> dis_locations), elv_dis_subblid (-> dis_subbls),
elv_geounit (-> dis_geounits, has elv_name_short), elv_detail, dis_area (Guid).
dis_locations: Name, dis_location (Guid), dis_geounit (-> dis_geounits). dis_geounits: dis_geounit (Guid).

## Existing app-level state (App.pa.yaml)
- App.Formulas: fxMenuItems = Table({TextValue, Icon, NavigateScreen}) with entries Dashboard(Home)->scr_consume,
  Category Item(AppsList)->scr_category, Item(Folder)->scr_item, Area(BuildingRetail)->Area,
  User(Person)->scr_user, Consume(Wrench)->scr_consume, Transaction(Cart)->scr_Transaction,
  Find Item(Search)->scr_find_item, History(History)->scr_History.
- App.OnStart sets imyrole, imyid, imyarea (broken elv_assigned_area), ClearCollect(iroleview, ...N:N areas).
- App.StartScreen: If(IsBlank(LookUp(dis_users, email = User().Email).Name), Register, 'Log In').
- Theme: PowerAppsTheme. Images in app: 'SLB_Logo_2022.svg' (dark logo), 'slb logo white'.
- Global vars used by screens: gblFormMode ("Add"/"Update"), colTempDetails (cart: Urutan, Id, name, description, Qty).

## Components (Components/*.pa.yaml) — owned by orchestrator in this edit
Sidebar: `Control: CanvasComponent` / `ComponentName: Sidebar`; inputs: activemenu (Text, Required),
plus Fill, Height, Width, X, Y, Visible, AlignInContainer, FillPortions, LayoutMinHeight (default 640),
LayoutMinWidth (default 640), LayoutMaxHeight, LayoutMaxWidth. AccessAppScope: true.
TopBar: `Control: CanvasComponent` / `ComponentName: TopBar`; inputs: ActiveMenu (Text, Required), Subtitle (Text, Required;
added by the Before-builders change, confirmed with describe_control after the T1 compile),
same generic inputs as Sidebar.
NOTE: when placed inside an AutoLayout container, set LayoutMinWidth / LayoutMinHeight explicitly
(defaults are 640).

## Controls (describe_control results; input-property names + exact enum names)
Every control below also supports, when child of a Vertical/Horizontal AutoLayout GroupContainer:
AlignInContainer (Enum name: AlignInContainer — Center, End, SetByContainer, Start, Stretch),
FillPortions, LayoutMaxHeight, LayoutMaxWidth, LayoutMinHeight, LayoutMinWidth.

### GroupContainer — `Control: GroupContainer` + required `Variant: AutoLayout | GridLayout | ManualLayout`
Inputs: BorderColor, BorderStyle (Enum name BorderStyle: Dashed, Dotted, None, Solid), BorderThickness,
ContentLanguage, DropShadow (Enum name DropShadow: Bold, ExtraBold, Light, None, Regular, Semibold, Semilight),
EnableChildFocus, Fill, Height, RadiusBottomLeft, RadiusBottomRight, RadiusTopLeft, RadiusTopRight, Visible, Width, X, Y.
AutoLayout adds: LayoutAlignItems (Enum LayoutAlignItems: Center, End, Start, Stretch),
LayoutDirection (Enum LayoutDirection: Horizontal, Vertical; required), LayoutGap,
LayoutJustifyContent (Enum LayoutJustifyContent: Center, End, SpaceBetween, Start),
LayoutOverflowX / LayoutOverflowY (Enum name LayoutOverflow: Hide, Scroll), LayoutWrap,
PaddingBottom, PaddingLeft, PaddingRight, PaddingTop.
GridLayout adds: ChildTabPriority, LayoutGap, LayoutGridColumnMinWidth, LayoutGridColumns, LayoutGridRowMinHeight,
LayoutGridRows, LayoutOverflowX/Y, Padding*. Children of Grid: LayoutGridColumnStart/End, LayoutGridRowStart/End.
ManualLayout adds: ChildTabPriority, Padding*.
Defaults to override: DropShadow default Light; Radius default 4; child-of-autolayout LayoutMinHeight 112, LayoutMinWidth 250, FillPortions 1.

### ModernText — `Control: ModernText`
Inputs: AccessibleLabel, Align (Enum Align: Center, Justify, Left, Right), AutoHeight, BorderColor,
BorderStyle (BorderStyle), BorderThickness, Color, ContentLanguage, DisplayMode (Enum DisplayMode: Disabled, Edit, View),
Fill, Font (Enum Font: Arial, Courier New, Dancing Script, Georgia, Great Vibes, Lato, Lato Black, Lato Hairline,
Lato Light, Open Sans, Open Sans Condensed, Patrick Hand, Segoe UI, Verdana — literal e.g. Font.'Segoe UI'),
FontWeight (Enum FontWeight: Bold, Lighter, Normal, Semibold), Height, Italic, OnSelect, PaddingBottom/Left/Right/Top
(default 5), Radius*, Size (default 26), Strikethrough, Text, Underline, VerticalAlign (Enum VerticalAlign: Bottom,
Middle, Top), Visible, Width, Wrap, X, Y. Child-of-autolayout defaults LayoutMinHeight 50, LayoutMinWidth 200.

### ModernButton — `Control: ModernButton`
Inputs: AccessibleLabel, Align (Align), Appearance (Enum ButtonAppearance: Outline, Primary, Secondary, Subtle, Transparent),
BasePaletteColor, BorderColor, BorderStyle, BorderThickness, Color, ContentLanguage, DisplayMode, Font (Font),
FontWeight, Height (default 64), Icon (Text, Fluent icon name e.g. "Add"), IconRotation,
IconStyle (Enum IconStyle: Filled, Outline), Italic, Layout (Enum ButtonLayout: IconAfter, IconBefore, IconOnly, TextOnly),
OnSelect, Padding*, Radius*, Size (default 24), Strikethrough, Text, Tooltip, Underline, VerticalAlign, Visible, Width (default 280), X, Y.
Child-of-autolayout defaults LayoutMinHeight 64, LayoutMinWidth 280 (override!).

### ModernIcon — `Control: ModernIcon`
Inputs: AccessibleLabel, BasePaletteColor, BorderColor, BorderStyle, BorderThickness, ContentLanguage, DisplayMode,
Fill, Height, Icon (Text), IconColor, IconStyle (IconStyle), OnSelect, Padding*, Radius*, Rotation, Tooltip, Visible, Width, X, Y.
Child-of-autolayout defaults LayoutMinHeight 42, LayoutMinWidth 42.

### Badge — `Control: Badge`
Inputs: AccessibleLabel, Align (Align), Appearance (Enum name BadgeCanvas.Appearance: Filled, Ghost, Outline, Tint),
BasePaletteColor, Content (Text), ContentLanguage, DisplayMode, Font (Font), FontColor, FontItalic, FontSize,
FontStrikethrough, FontUnderline, FontWeight (FontWeight), Height (32), Shape (Enum BadgeCanvas.Shape: Circular, Rounded, Square),
ThemeColor (Enum BadgeCanvas.ThemeColor: Brand, Danger, Important, Informative, Severe, Subtle, Success, Warning),
VerticalAlign, Visible, Width (32), X, Y. Child-of-autolayout defaults LayoutMinHeight 32, LayoutMinWidth 32.

### Gallery — `Control: Gallery` + required `Variant: Horizontal | VariableHeight | Vertical`
Common inputs: BorderStyle, ContentLanguage, Default, DisplayMode, Fill, FocusedBorderColor, FocusedBorderThickness,
LoadingSpinnerColor, NavigationStep, Selectable, ShowNavigation, TabIndex, Transition (Enum Transition: None, Pop, Push), Visible.
Vertical adds: AccessibleLabel, BorderColor, BorderThickness, DelayItemLoading, Height, Items,
LoadingSpinner (Enum LoadingSpinner: Controls, Data, None), ShowScrollbar, TemplatePadding, TemplateSize, Width, WrapCount, X, Y.
VariableHeight adds the same minus WrapCount plus MaxTemplateSize.
NOTE: TemplateFill is NOT in the input list — zebra/hover rows must be drawn with a row GroupContainer Fill
(e.g. Fill: =If(Mod(...),...) using a row index is unavailable; use ThisItem.IsSelected for selected-row fill).
Outputs: AllItems, AllItemsCount, Selected, TemplateHeight, TemplateWidth, VisibleIndex.
Child-of-autolayout defaults LayoutMinHeight 287, LayoutMinWidth 320, FillPortions 1.

### ModernTextInput — `Control: ModernTextInput`
Inputs: AccessibleLabel, Align, Appearance (Enum name Appearance: FilledDarker, FilledLighter, Outline), BasePaletteColor,
BorderColor, BorderStyle, BorderThickness, Color, ContentLanguage, Default, DisplayMode, Fill, Font, FontWeight, Height (64),
Italic, MaxLength, OnChange, Padding*, Placeholder, Radius*, Required, Size (24), Strikethrough,
TriggerOutput (Enum TriggerOutput: Delayed, FocusOut, Keypress), Type (Enum TextInputType: Multiline, Password, Search, SingleLine),
Underline, ValidationState (Enum ValidationState: Error, None), Visible, Width (560), X, Y. Output: Text.
Child-of-autolayout defaults LayoutMinHeight 64, LayoutMinWidth 560 (override!).

### ModernDropdown — `Control: ModernDropdown`
Inputs: AccessibleLabel, Appearance (Appearance), BasePaletteColor, BorderColor, BorderStyle, BorderThickness, Color,
ContentLanguage, Default (Record), DisplayMode, Fill, Font, FontWeight, Height (64), Italic, ItemDisplayText, Items, OnChange,
Padding*, Radius*, Required, Size (24), Strikethrough, Underline, ValidationState, Visible, Width (560), X, Y. Output: Selected.
Child-of-autolayout defaults LayoutMinHeight 64, LayoutMinWidth 560 (override!).

### ModernCombobox — `Control: ModernCombobox`
Inputs: AccessibleLabel, AllowExternalSelectedItems, Appearance (Appearance), BasePaletteColor, BorderColor, BorderStyle,
BorderThickness, Color, ContentLanguage, DefaultSelectedItems, DelayOutput, DisplayMode, Fill, Font, FontWeight, Height (64),
InputTextPlaceholder, IsSearchable, Italic, ItemDisplayText, Items, MultiValueDelimiter, OnChange, Padding*, Radius*, Required,
SelectMultiple, Size (24), Strikethrough, Underline, ValidationState, Visible, Width (560), X, Y.
Outputs: SearchText, Selected, SelectedItems. Child-of-autolayout defaults 64 / 560.

### ModernNumberInput — `Control: ModernNumberInput`
Inputs: AccessibleLabel, Align, Appearance (Appearance), BasePaletteColor, BorderColor, BorderStyle, BorderThickness, Color,
ContentLanguage, Default (Number), DisplayMode, Fill, Font, FontWeight, Height (64), HintText, Italic, Max, Min, OnChange,
Padding*, Precision (Enum DecimalPrecision: '0','1','2','3','4','5', Auto — digits must be quoted, e.g. DecimalPrecision.'0'),
Radius*, Size (24), Step, Strikethrough, Underline, ValidationState, Visible, Width (560), X, Y. Output: Value.

### ModernDatePicker — `Control: ModernDatePicker`
Inputs: AccessibleLabel, Appearance (Appearance), BasePaletteColor, BorderColor, BorderStyle, BorderThickness, Color,
ContentLanguage, DateTimeZone (Enum DateTimeZone: Local, UTC), DefaultDate, DisplayMode, EndDate, Fill, Font, FontWeight,
Format (Enum DatePickerFormat: LongAbbreviated, Short, YearMonth), Height (64), IsEditable, Italic, OnChange, Padding*,
Placeholder, Radius*, Size (24), StartDate, StartOfWeek (Enum StartOfWeek: Friday, Monday, MondayZero, Saturday, Sunday,
Thursday, Tuesday, Wednesday), Strikethrough, Underline, ValidationState, Visible, Width (560), X, Y. Output: SelectedDate.

### Rectangle — `Control: Rectangle`
Inputs: AccessibleLabel, BorderColor, BorderStyle, BorderThickness, ContentLanguage, DisabledFill, DisplayMode, Fill,
FocusedBorderColor, FocusedBorderThickness, Height, HoverFill, OnSelect, PressedFill, TabIndex, Tooltip, Visible, Width, X, Y.

### Image — `Control: Image`
Inputs: AccessibleLabel, ApplyEXIFOrientation, AutoDisableOnSelect, BorderColor, BorderStyle, BorderThickness,
CalculateOriginalDimensions, ContentLanguage, DisabledBorderColor, DisabledFill, DisplayMode, Fill, FlipHorizontal,
FlipVertical, FocusedBorderColor, FocusedBorderThickness, Height, HoverBorderColor, HoverFill, Image,
ImagePosition (Enum ImagePosition: Center, Fill, Fit, Stretch, Tile), ImageRotation (Enum ImageRotation: None, Rotate180,
Rotate270, Rotate90), OnSelect, Padding*, PressedBorderColor, PressedFill, Radius* (default 0), TabIndex, Tooltip,
Transparency, Visible, Width, X, Y.

### Form — `Control: Form` + optional `Variant: Classic | Modern` + required `Layout: Vertical | Horizontal`
Inputs: AcceptsFocus, BorderColor, BorderStyle, BorderThickness, ContentLanguage, DataSource,
DefaultMode (Enum FormMode: Edit, New, View), Fill, FocusedBorderColor, FocusedBorderThickness, Height, Item,
NumberOfColumns, OnFailure, OnReset, OnSuccess, SnapToColumns, Visible, Width, X, Y.
Outputs: Error, ErrorKind, LastSubmit, Mode, Unsaved, Updates, Valid.
Existing forms in the app (Form5_1, Form4, frm_catFrm_category, Form5_3, Form5) use `Variant: Modern` — preserve
their existing creation keywords and DataCard children; restyle via Form props (NumberOfColumns: =2, Fill, Width) and
card props already present.

### TypedDataCard — `Control: TypedDataCard` + required Variant
Full describe output (60 KB) saved at:
C:\Users\Andika Rianto\.claude\projects\C--Project-Powerapps\9457fedf-24ea-43c5-823b-32c62447ce3d\tool-results\toolu_01XQprfD9tqBeAtWj42gUSby.json
Existing cards use variants ModernTextualEdit, ModernTextualMultilineEdit, ModernNumberEdit,
ModernComboBoxOptionSetSingleEdit, PcfCoreComboBoxEditCard, ClassicLargePicture — preserve variants and children.
Do NOT create new data cards in this edit.

### Controls already present in YAML and preserved as-is (not re-described)
Label (classic), FluentV8/Label, Classic/ComboBox, Classic/Button, Classic/Icon, AddMedia. Builders may restyle only
properties already present on them, or replace Label/Classic/Button/Classic/Icon with the Modern controls above.

## Available control list (list_controls)
ModernAvatar, ModernButton, ModernCard, ModernCheckbox, ModernCombobox, ModernDataGrid, ModernDatePicker, ModernDropdown,
ModernIcon, ModernInformationButton, ModernLink, ModernNumberInput, ModernProgressBar, ModernRadio, ModernSpinner,
ModernTabList, ModernText, ModernTextInput, ModernToggle, Badge, GroupContainer, Gallery, Form, TypedDataCard, Image,
Rectangle, Label, AddMedia, Classic/* … (only the ones described above may be used).
