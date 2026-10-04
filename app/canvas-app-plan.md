# Canvas App Plan

## Mode

EDIT

## Requirements

User (Indonesian): "oke, tolong update semua halaman nya menjadi lebih modern dan optimal" (modernize ALL pages + optimize).
Approved clarifications: (1) new Dashboard screen (KPI total items, low-stock count, transactions today, recent
transactions, low-stock list, quick actions; Sidebar "Dashboard" and Log In land on it); (2) scope = visual +
optimisation + bug fixes, save / stock-update flows preserved except listed bug fixes; (3) target = fixed desktop
(sidebar always visible, wide tables). Full contract: `C:\Project\Powerapps\app\canvas-app-requirements.md` (immutable).

Bug fixes in scope: App.OnStart / Register `elv_assigned_area` -> `Assigned_area`; Log In `HomeAdmin`/`HomeUser`
removed; scr_user `locSelectedRecord: Blank()` warnings; Area Delete removed `Gallery8_12.Selected` instead of the
clicked row; scr_user Edit/Delete used Blank()/`Gallery8_13.Selected`; scr_category / scr_item Delete had no
confirmation; scr_consume header lacked `type = Consume` + `area_form`, and qty > stock was not blocked; Sidebar
"Dashboard" pointed at scr_consume and role text was hard-coded "User". Optimisation: one named formula `nfMe`
replaces 7 duplicated `LookUp(dis_users, email = User().Email)` calls; palette named formulas; no hard-coded
975 / App.Width-150 widths; detail search inputs (`inp_search_2`, `inp_search_6`) that were never wired are wired.

## Original Request Capability Inventory

| Requirement key | Original request clause | Capability family | Required outcome / scope | Required action(s) | Observer(s) | Scenario(s) |
| --- | --- | --- | --- | --- | --- | --- |
| REQ-VISUAL | "update semua halaman nya menjadi lebih modern" | App shell and navigation | All 16 screens use the shared visual contract (navy brand, `clrBg` page, white 12px-radius cards, Segoe UI scale, consistent buttons); layout fills the screen (no 975 / App.Width-150) | ACT-NAV-MENU | `con<P>Root.Width: =Parent.Width` on every screen; `cmp<P>Sidebar`, `cmp<P>TopBar` | SCN-NAV-MENU |
| REQ-SHELL | Sidebar/TopBar modern + correct | App shell and navigation | Sidebar lists fxMenuItems, active pill for `activemenu`, navigates; profile shows `nfMe.Name` + real role; TopBar shows title + subtitle | ACT-NAV-MENU | `Sidebar.conSbItem.Fill`, `Sidebar.txtSbUserRole.Text`, `TopBar.txtTbTitle.Text` | SCN-NAV-MENU, SCN-NAV-ROLE |
| REQ-PERF-USER | "optimal" - single current-user lookup | Security, persistence, resilience | `App.Formulas nfMe`; OnStart / StartScreen / Log In / Sidebar read it; legacy vars imyrole, imyid, imyarea, iroleview, imyemail still set; Assigned_area replaces elv_assigned_area | ACT-APP-START | `App.StartScreen`, `txtLoginName.Text: =nfMe.Name` | SCN-START-REGISTERED, SCN-START-UNREGISTERED |
| REQ-DASH | Dashboard baru | Analytics and visualization | scr_dashboard: KPI total items (`dis_item_v2S`), KPI low stock (`dis_stocks` qty < item min_qty), KPI transactions today (`dis_trx_headers` 'Created On' today), recent transactions list (number/date/type/area), low-stock list (item, area, qty, min); quick links to Transaction / Find Item | ACT-DASH-VIEW, ACT-DASH-OPEN-TRX | `txtDashKpiItemsVal`, `txtDashKpiLowVal`, `txtDashKpiTodayVal`, `galDashRecent`, `galDashLow` | SCN-DASH-KPI, SCN-DASH-EMPTY, SCN-DASH-OPEN-TRX |
| REQ-LOGIN | Log In navigation fixed | App shell and navigation | Welcome card with name + role badge; single "Masuk ke Dashboard" button -> scr_dashboard for any registered role | ACT-LOGIN-ENTER | `btnLoginEnter.OnSelect`, `bdgLoginRole.Content` | SCN-LOGIN-ENTER |
| REQ-REGISTER | Register fixed | App shell and navigation | Admin list (Name, email, Assigned_area.Name) with per-row mail action `Launch("mailto:" & email)` | ACT-REG-CONTACT | `galRegAdmins` rows | SCN-REG-LIST |
| REQ-AREA | Area list modern + delete bug fix | Data lifecycle; Data exploration | Geounit -> Location -> Area cascade + search + reset; Add -> Add_area new; row Edit -> Add_area edit prefilled; row Delete -> confirm strip -> removes clicked row | ACT-AREA-FILTER, ACT-AREA-ADD, ACT-AREA-EDIT, ACT-AREA-DELETE | `Gallery8_12.Items`, `conAreaLConfirm`, `conAreaLReceipt` | SCN-AREA-FILTER, SCN-AREA-ADD, SCN-AREA-EDIT, SCN-AREA-DELETE, SCN-AREA-DELETE-CANCEL |
| REQ-AREA-FORM | Add_area form modern, logic preserved | Data lifecycle | Form5_1 (dis_areas) Name, Geounit, Location, Business Line, Detail; Save submits; Back resets + returns | ACT-AREA-SAVE | `conAreaLReceipt` (gblReceipt.Screen="Area"), `Gallery8_12` | SCN-AREA-SAVE |
| REQ-USER | User list modern + bug fix | Data lifecycle; Role-scoped | List (Name, email, role badge, assigned area); row Edit opens inline editor prefilled with that row; Save submits Form4; row Delete -> confirm -> removes clicked row | ACT-USER-EDIT, ACT-USER-SAVE, ACT-USER-DELETE | `Form4.Item: =locSelectedRecord`, `conUsrLReceipt`, `Gallery8_13` | SCN-USER-EDIT, SCN-USER-SAVE, SCN-USER-DELETE |
| REQ-CAT | Category list modern + confirm delete | Data lifecycle; Data exploration | Search name/code/description; Add / Edit -> scr_frm_category; Delete -> confirm -> removes clicked row | ACT-CAT-SEARCH, ACT-CAT-ADD, ACT-CAT-EDIT, ACT-CAT-DELETE | `gal_cat_list`, `conCatLConfirm`, `conCatLReceipt` | SCN-CAT-SEARCH, SCN-CAT-ADD, SCN-CAT-EDIT, SCN-CAT-DELETE |
| REQ-CAT-FORM | scr_frm_category modern, logic preserved | Data lifecycle | frm_catFrm_category name, code, description; Submit; Back | ACT-CAT-SAVE | `conCatLReceipt` | SCN-CAT-SAVE |
| REQ-ITEM | Item list modern + confirm delete | Data lifecycle; Data exploration | Category filter + search; Name, BPN, SPN, Category, Min Qty, UoM, Status badge; Add / Edit / Delete-with-confirm | ACT-ITEM-FILTER, ACT-ITEM-ADD, ACT-ITEM-EDIT, ACT-ITEM-DELETE | `Gallery8_6`, `conItmLConfirm`, `conItmLReceipt` | SCN-ITEM-FILTER, SCN-ITEM-ADD, SCN-ITEM-EDIT, SCN-ITEM-DELETE |
| REQ-ITEM-FORM | scr_frm_item modern, logic preserved | Data lifecycle; Files and media | Form5_3 name, min_qty, BPN, SPN, uom, status, category, description, image; Submit; Back | ACT-ITEM-SAVE | `conItmLReceipt` | SCN-ITEM-SAVE |
| REQ-TRX | Transaction list modern + confirm delete | Data lifecycle; Exploration; Relationships | Type filter + search; header list; selected header shows detail lines (category filter + search); Add -> new form empty cart; Edit -> loads lines into colTempDetails; Delete -> confirm -> RemoveIf details + Remove header | ACT-TRX-FILTER, ACT-TRX-SELECT, ACT-TRX-ADD, ACT-TRX-EDIT, ACT-TRX-DELETE | `Gallery8_1`, `Gallery8_3`, `conTrxLConfirm`, `conTrxLReceipt` | SCN-TRX-FILTER, SCN-TRX-DETAIL, SCN-TRX-ADD, SCN-TRX-EDIT, SCN-TRX-DELETE |
| REQ-TRX-FORM | scr_frm_Transaction modern, logic preserved | Data lifecycle; Workflow | Header (auto number, type, From/To visibility by type, note); cart add/remove; Submit runs existing OnSuccess (detail rewrite + Receive/Consume/Transfer stock update) unchanged | ACT-TRX-CART-ADD, ACT-TRX-CART-REMOVE, ACT-TRX-SAVE | `Gallery7`, `txtTrxFCartCount`, `conTrxLReceipt`, `Gallery8_9` stock | SCN-TRX-CART, SCN-TRX-CART-REMOVE, SCN-TRX-SAVE-RECEIVE |
| REQ-CONSUME | scr_consume modern + bug fix | Workflow; Exploration | Category/Geounit/Location/Area filters + search over dis_stocks; per-row qty; Consume creates header (number, type Consume, area_form) + details and decreases stock; blocked when no area, no qty, qty > stock | ACT-CONSUME-FILTER, ACT-CONSUME-SUBMIT | `Gallery8_11`, `conConsReceipt`, `galConsReceipt`, `btnConsSubmit.DisplayMode` | SCN-CONSUME-FILTER, SCN-CONSUME-OK, SCN-CONSUME-BLOCKED, SCN-CONSUME-COMPOUND |
| REQ-FIND | scr_find_item modern | Data exploration | Category/Geounit/Location/Area filters + search over dis_stocks; Name, BPN, SPN, Category, Stock (low-stock highlight), UoM, Location | ACT-FIND-FILTER | `Gallery8_9`, `bdgFindStock.ThemeColor` | SCN-FIND-FILTER |
| REQ-HISTORY | scr_History modern | Data exploration; Time | Type filter, date filter + clear, search; header list; detail lines of selected header with category filter | ACT-HIST-FILTER, ACT-HIST-SELECT | `Gallery8_7`, `Gallery8_8` | SCN-HIST-DATE, SCN-HIST-DETAIL |
| REQ-TEMPLATE | Template updated to new shell | App shell and navigation | Template shows sidebar + topbar + empty body card | ACT-NAV-MENU | `conTplRoot` | SCN-NAV-MENU |

## Requirement Coverage

| Requirement | Planned affordance | Fidelity |
| --- | --- | --- |
| Modern look on every page | Shared shell (Sidebar 224 + TopBar 64 + scrolling body), white cards, Badge for Type/Status/Role, ModernIcon row actions, Segoe UI type scale | Exact |
| Sidebar active highlight + real role | `conSbItem.Fill` pill when `ThisItem.TextValue = Sidebar.activemenu`; `txtSbUserRole` = `Proper(Text(imyrole))` | Exact |
| Dashboard KPI cards / recent list / low-stock list / quick links | scr_dashboard KPI row (3 cards), `galDashRecent`, `galDashLow`, buttons Transaksi Baru / Consume / Cari Item / Lihat semua | Exact |
| Log In single action to Dashboard | `btnLoginEnter` -> `Navigate(scr_dashboard, ScreenTransition.Fade)` | Exact |
| Register admin list + mail | `galRegAdmins` + `icoRegMail` -> `Launch("mailto:" & ThisItem.email)` | Exact |
| "confirm dialog for every Delete" | State-driven inline confirmation strip `con<P>Confirm` nested in the screen root directly above the list card (red tint, record name, Hapus / Batal) | Approximation: AutoLayout cannot overlap siblings and viewport containment forbids screen-level overlays, so the dialog is an inline strip in the initial viewport rather than a floating modal |
| User "edit popup" | Inline editor card `conUsrLEditor` (Visible `locShowUserPopUp`) at the top of the body, Form4 2 columns, Save / Batal | Approximation: same containment reason as above; card appears in the initial viewport above the list |
| Zebra / hover rows | Row dividers via `Gallery.Fill = clrBorder` + `TemplatePadding 1`; selected-row tint `clrRowSelected` | Approximation: Gallery has no TemplateFill / row index in this control version (discovery packet) |
| Type filter (3 option values) | Segmented ModernButtons Semua / Receive / Consume / Transfer with active Primary state (Trx list, History) | Exact (short-choice rule) |
| Save/Cancel at bottom of forms | `con<P>Actions` bar as last body child on each form screen | Exact |
| Mutation evidence after save/delete | Shared receipt strip `con<P>Receipt` bound to `gblReceipt` (set in form OnSuccess / delete handler); Consume uses `conConsReceipt` with per-line old/amount/expected/actual | Exact |
| Fixed desktop | Minimum supported canvas 1136 x 640 (current app size); all budgets computed at that size; wider canvases stretch | Exact |

## Required Record Fields

| Field key | Screen | Record surface | Required field | Source field | Presentation requirement |
| --- | --- | --- | --- | --- | --- |
| area/row/name | Area | Gallery8_12 row | Area name (identity) | dis_areas.Name | Full text, Semibold, FP 2 |
| area/row/location | Area | Gallery8_12 row | Location | 'elv_location (cr8a3_elv_location)'.Name | FP 2 |
| area/row/bl | Area | Gallery8_12 row | Business line | elv_dis_subblid.Name | FP 2 |
| area/row/geounit | Area | Gallery8_12 row | Geounit | elv_geounit.elv_name_short | W 96 |
| user/row/name | scr_user | Gallery8_13 row | Name (identity) | dis_users.Name | Semibold FP 3 |
| user/row/email | scr_user | Gallery8_13 row | Email | email | FP 3 |
| user/row/role | scr_user | Gallery8_13 row | Role | role | Badge Content `Proper(Text(ThisItem.role))`, W 112 |
| user/row/area | scr_user | Gallery8_13 row | Assigned area | Assigned_area.Name | FP 2 |
| cat/row/name | scr_category | gal_cat_list row | Name (identity) | name | Semibold FP 3 |
| cat/row/code | scr_category | gal_cat_list row | Code | code | W 96 |
| cat/row/date | scr_category | gal_cat_list row | Created date | 'Created On' | `Text(..., "dd/mm/yyyy")` W 96 |
| cat/row/desc | scr_category | gal_cat_list row | Description | description | FP 4 |
| item/row/name | scr_item | Gallery8_6 row | Name (identity) | name | Semibold FP 3 |
| item/row/bpn | scr_item | Gallery8_6 row | BPN | part_number | FP 2 |
| item/row/spn | scr_item | Gallery8_6 row | SPN | client_number | FP 2 |
| item/row/cat | scr_item | Gallery8_6 row | Category | dis_category_item.name | FP 2 |
| item/row/min | scr_item | Gallery8_6 row | Min qty | min_qty | W 64 |
| item/row/uom | scr_item | Gallery8_6 row | UoM | uom | W 56 |
| item/row/status | scr_item | Gallery8_6 row | Status | status | Badge W 96 |
| trx/row/number | scr_Transaction | Gallery8_1 row | Number (identity) | transaction_number | ModernButton link, FP 2 |
| trx/row/date | scr_Transaction | Gallery8_1 row | Date | 'Created On' | W 92 |
| trx/row/type | scr_Transaction | Gallery8_1 row | Type | type | Badge W 92 |
| trx/row/area | scr_Transaction | Gallery8_1 row | Area | area_form / area_to | `Coalesce(area_form.Name, "-") & " -> " & Coalesce(area_to.Name, "-")`, FP 3 |
| trx/row/note | scr_Transaction | Gallery8_1 row | Note | note | FP 3 |
| trxd/row/* | scr_Transaction | Gallery8_3 row | BPN, Name (identity), Description, Category, Qty, UoM | item.part_number, item.name, item.description, item.dis_category_item.name, qty, item.uom | 6 cells |
| hist/row/* | scr_History | Gallery8_7 row | Number (identity), Date, Type badge, Area, Note | same as trx/row | same widths as Trx minus actions |
| histd/row/* | scr_History | Gallery8_8 row | BPN, Name, Description, Category, Qty, UoM | same as trxd | 6 cells |
| find/row/* | scr_find_item | Gallery8_9 row | Name (identity), BPN, SPN, Category, Stock (low highlight), UoM, Location | dis_item_v2.name, .part_number, .client_number, .dis_category_item.name, qty, dis_item_v2.uom, dis_area location + name | Stock Badge Danger when qty < min_qty |
| cons/row/* | scr_consume | Gallery8_11 row | Item name (identity) + BPN, Area, Stock, Qty input | dis_item_v2.name/part_number, dis_area.Name, qty | name Semibold, stock Badge |
| dash/recent/* | scr_dashboard | galDashRecent row | Number (identity), Date, Type, Area | transaction_number, 'Created On', type, area_to/area_form | 4 cells |
| dash/low/* | scr_dashboard | galDashLow row | Item name (identity), Area, qty / min | dis_item_v2.name, dis_area.Name, qty, dis_item_v2.min_qty | Badge `qty / min` |
| reg/row/* | Register | galRegAdmins row | Name (identity), email, assigned area | Name, email, Assigned_area.Name | 3 stacked lines |
| cart/row/* | scr_frm_Transaction | Gallery7 row | Item name (identity), Qty, Description | colTempDetails.name, Qty, description | 3 cells + remove icon |

## State-Driven Surface Visibility

| Surface key | Owner screen | Surface control | State predicate | Visible and hidden states |
| --- | --- | --- | --- | --- |
| area-confirm | Area | conAreaLConfirm | `=locShowDeleteConfirm` | Visible after row Delete; hidden after Hapus success / Batal |
| area-receipt | Area | conAreaLReceipt | `=gblReceipt.Screen = "Area"` | Visible after Area save/delete; hidden after dismiss or another screen's receipt |
| user-confirm | scr_user | conUsrLConfirm | `=locShowDeleteConfirm_1` | Visible after row Delete; hidden after Hapus / Batal |
| user-editor | scr_user | conUsrLEditor | `=locShowUserPopUp` | Visible after row Edit; hidden after save success / Batal / Delete click |
| user-receipt | scr_user | conUsrLReceipt | `=gblReceipt.Screen = "User"` | after save/delete |
| cat-confirm | scr_category | conCatLConfirm | `=locShowDeleteConfirm` | after row Delete |
| cat-receipt | scr_category | conCatLReceipt | `=gblReceipt.Screen = "Category"` | after save/delete |
| item-confirm | scr_item | conItmLConfirm | `=locShowDeleteConfirm` | after row Delete |
| item-receipt | scr_item | conItmLReceipt | `=gblReceipt.Screen = "Item"` | after save/delete |
| trx-confirm | scr_Transaction | conTrxLConfirm | `=locShowDeleteConfirm` | after row Delete |
| trx-receipt | scr_Transaction | conTrxLReceipt | `=gblReceipt.Screen = "Transaction"` | after save/delete |
| cons-receipt | scr_consume | conConsReceipt | `=locShowConsReceipt` | after successful Consume; hidden on close |

## Action Contracts

| Requested action | Preconditions | Entry point | Owner screen | Control and event | Source and stable ID | Transition and postcondition | Mutation write set | Receipt proof set | Observer and evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ACT-NAV-MENU | Any shell screen | Sidebar row | All shell screens (component) | `Sidebar.icoSbItem.OnSelect` / `Sidebar.txtSbItem.OnSelect: =Navigate(ThisItem.NavigateScreen, ScreenTransition.None)` | fxMenuItems.TextValue | Target screen shown; its `activemenu` equals the clicked TextValue | N/A | N/A | Active pill `conSbItem.Fill` on target screen; TopBar title |
| ACT-APP-START | App launch | n/a | App | `App.StartScreen`, `App.OnStart` | nfMe (dis_users by User().Email) | Registered -> 'Log In'; unregistered -> Register; legacy vars set | N/A (app vars only) | N/A | `txtLoginName.Text: =nfMe.Name`; Register visible |
| ACT-LOGIN-ENTER | `!IsBlank(nfMe.Name)` | "Masuk ke Dashboard" | Log In | `btnLoginEnter.OnSelect: =Navigate(scr_dashboard, ScreenTransition.Fade)`; DisplayMode Disabled when IsBlank(nfMe.Name) | nfMe | Dashboard shown | N/A | N/A | scr_dashboard TopBar "Dashboard" |
| ACT-REG-CONTACT | Admin rows exist | Mail icon per row | Register | `icoRegMail.OnSelect: =Launch("mailto:" & ThisItem.email)` | dis_users admin row email | Mail client opens to that admin | N/A | N/A | Row shows Name/email/area |
| ACT-DASH-VIEW | Screen visible | Dashboard | scr_dashboard | KPI Text formulas, gallery Items | dis_item_v2S, dis_stocks, dis_trx_headers | Live aggregates | N/A | N/A | `txtDashKpiItemsVal`, `txtDashKpiLowVal`, `txtDashKpiTodayVal`, galleries / empty texts |
| ACT-DASH-OPEN-TRX | none | "Transaksi Baru", "Lihat semua", "Consume Barang", "Cari Item" | scr_dashboard | `btnDashNewTrx.OnSelect: =Clear(colTempDetails); NewForm(Form5); Navigate(scr_frm_Transaction)`; `btnDashSeeAll.OnSelect: =Navigate(scr_Transaction)`; `btnDashConsume -> scr_consume`; `btnDashFind -> scr_find_item` | colTempDetails, Form5 | Form5 New mode, empty cart | N/A | N/A | scr_frm_Transaction title + empty `Gallery7` |
| ACT-AREA-FILTER | none | Geounit/Location/Area dropdowns, search, reset icon | Area | `dd_Geounit_2.OnChange: =Reset(dd_Location_2); Reset(dd_Area_2)`; `dd_Location_2.OnChange: =Reset(dd_Area_2)`; `icoAreaLReset.OnSelect: =Reset(dd_Geounit_2); Reset(dd_Location_2); Reset(dd_Area_2); Reset(inp_search_9)` | dis_areas | `Gallery8_12.Items` existing filter (preserved) | N/A | N/A | Gallery8_12 rows; `txtAreaLEmpty` when zero |
| ACT-AREA-ADD | none | "Tambah Area" | Area | `btnAreaLAdd.OnSelect: =Set(gblFormMode, "Add"); NewForm(Form5_1); Navigate(Add_area, ScreenTransition.None)` (preserved) | Form5_1 | Form New | N/A | N/A | Add_area title "Tambah Area" |
| ACT-AREA-EDIT | Row exists | Edit icon per row | Area | `icoAreaLEdit.OnSelect: =Set(gblFormMode, "Update"); EditForm(Form5_1); Navigate(Add_area, ScreenTransition.None)` (click selects row -> Form5_1.Item = Gallery8_12.Selected) | dis_areas.dis_area of clicked row | Form Edit prefilled | N/A | N/A | Add_area fields show row values |
| ACT-AREA-DELETE | Row exists | Delete icon -> Hapus | Area | `icoAreaLDelete.OnSelect: =UpdateContext({locSelectedRecord: ThisItem, locShowDeleteConfirm: true})`; `btnAreaLConfirmDel.OnSelect` (see brief) | dis_areas, `locSelectedRecord.dis_area` | `Remove(dis_areas, locSelectedRecord)`; row absent | existence | Name + "Dihapus" | `conAreaLReceipt` (gblReceipt Area); Gallery8_12 no longer lists it |
| ACT-AREA-SAVE | Form valid | "Simpan" (Add_area) | Add_area | `btnAreaFSave.OnSelect: =SubmitForm(Form5_1)`; `Form5_1.OnSuccess` (preserved + receipt line) | dis_areas, `Form5_1.LastSubmit.dis_area` | Row created/updated | Name, elv_geounit, location, elv_dis_subblid, elv_detail | Name, Geounit, Location, Business Line, Detail | `conAreaLReceipt` on Area after Back(); Gallery8_12 |
| ACT-USER-EDIT | Row exists | Edit icon per row | scr_user | `icoUsrLEdit.OnSelect: =UpdateContext({locSelectedRecord: ThisItem, locShowUserPopUp: true, locShowDeleteConfirm_1: false}); Set(gblFormMode, "Update"); EditForm(Form4)` | dis_users.dis_user | Editor visible, Form4.Item = locSelectedRecord | N/A | N/A | `conUsrLEditor` title "Edit Pengguna - " & locSelectedRecord.Name; prefilled cards |
| ACT-USER-SAVE | Editor open | "Simpan" | scr_user | `Button36.OnSelect: =SubmitForm(Form4)`; `Form4.OnSuccess` (preserved + receipt) | dis_users, `Form4.LastSubmit.dis_user` | Row updated; editor closes | Name, email, role, Assigned_area | Name, email, role, assigned area | `conUsrLReceipt`; Gallery8_13 row |
| ACT-USER-DELETE | Row exists | Delete icon -> Hapus | scr_user | `icoUsrLDelete.OnSelect: =UpdateContext({locSelectedRecord: ThisItem, locShowDeleteConfirm_1: true, locShowUserPopUp: false})`; `btnUsrLConfirmDel.OnSelect` | dis_users, `locSelectedRecord.dis_user` | `Remove(dis_users, locSelectedRecord)` | existence | Name + email + "Dihapus" | `conUsrLReceipt`; Gallery8_13 |
| ACT-CAT-SEARCH | none | search input | scr_category | `gal_cat_list.Items` Search(name, code, description) preserved | dis_category_items | filtered rows | N/A | N/A | gal_cat_list; `txtCatLEmpty` |
| ACT-CAT-ADD | none | "Tambah Kategori" | scr_category | `btn_cat_add.OnSelect: =NewForm(frm_catFrm_category); Navigate(scr_frm_category)` (preserved) | form | New | N/A | N/A | scr_frm_category card title |
| ACT-CAT-EDIT | row | Edit icon | scr_category | `icoCatLEdit.OnSelect: =EditForm(frm_catFrm_category); Navigate(scr_frm_category)` | dis_category_item | Edit prefilled from gal_cat_list.Selected | N/A | N/A | form fields |
| ACT-CAT-DELETE | row | Delete icon -> Hapus | scr_category | `icoCatLDelete` + `btnCatLConfirmDel` | dis_category_items, locSelectedRecord.dis_category_item | Remove | existence | name + code + "Dihapus" | `conCatLReceipt`; gal_cat_list |
| ACT-CAT-SAVE | valid | "Simpan" | scr_frm_category | `btn_catFrm_submit.OnSelect: =SubmitForm(frm_catFrm_category)`; OnSuccess (+receipt) | LastSubmit.dis_category_item | create/update | name, code, description | name, code, description | `conCatLReceipt` |
| ACT-ITEM-FILTER | none | category dropdown + search + reset | scr_item | `Gallery8_6.Items` preserved; `icoItmLReset.OnSelect: =Reset(Dropdown2_2); Reset(inp_search_4)` | dis_item_v2S | filtered | N/A | N/A | Gallery8_6; `txtItmLEmpty` |
| ACT-ITEM-ADD | none | "Tambah Item" | scr_item | `Button31_2.OnSelect: =NewForm(Form5_3); Navigate(scr_frm_item)` | form | New | N/A | N/A | form title |
| ACT-ITEM-EDIT | row | Edit icon | scr_item | `icoItmLEdit.OnSelect: =EditForm(Form5_3); Navigate(scr_frm_item)` | dis_item_v2 | Edit prefilled | N/A | N/A | form fields |
| ACT-ITEM-DELETE | row | Delete icon -> Hapus | scr_item | `icoItmLDelete` + `btnItmLConfirmDel` | dis_item_v2S, locSelectedRecord.dis_item_v2 | Remove | existence | name + BPN + "Dihapus" | `conItmLReceipt`; Gallery8_6 |
| ACT-ITEM-SAVE | valid | "Simpan" | scr_frm_item | `Button32_6.OnSelect: =SubmitForm(Form5_3)`; OnSuccess (+receipt) | LastSubmit.dis_item_v2 | create/update | name, min_qty, part_number, client_number, uom, status, dis_category_item, description, Image | all 9 (Image as "ada/tidak ada") | `conItmLReceipt`; Gallery8_6 |
| ACT-TRX-FILTER | none | Type segment, search | scr_Transaction | `btnTrxLType*.OnSelect: =UpdateContext({locTrxType: ...})`; `Gallery8_1.Items` (see brief) | dis_trx_headers.type | filtered, newest first | N/A | N/A | Gallery8_1; active segment Primary; `txtTrxLEmpty` |
| ACT-TRX-SELECT | rows | click row number link | scr_Transaction | `btnTrxLOpen.OnSelect` (gallery selection) | dis_trx_header | Gallery8_1.Selected | N/A | N/A | `txtTrxLDetailTitle` + Gallery8_3 lines |
| ACT-TRX-ADD | none | "Tambah Transaksi" | scr_Transaction | `Button31.OnSelect: =Clear(colTempDetails); NewForm(Form5); Navigate(scr_frm_Transaction)` (preserved) | colTempDetails | empty cart, New | N/A | N/A | scr_frm_Transaction |
| ACT-TRX-EDIT | row | Edit icon | scr_Transaction | `icoTrxLEdit.OnSelect` = existing Button15_2 formula verbatim | dis_trx_header | cart loaded, Edit | colTempDetails (staging) | N/A | Gallery7 lines on form |
| ACT-TRX-DELETE | row | Delete icon -> Hapus | scr_Transaction | `icoTrxLDelete` + `btnTrxLConfirmDel` (existing cascade on locSelectedRecord) | dis_trx_headers + dis_trx_details by dis_trx_header | header + lines removed (stock NOT reversed - preserved behaviour) | existence of header + lines | number + type + "Dihapus" | `conTrxLReceipt`; Gallery8_1 |
| ACT-TRX-CART-ADD | item selected, qty > 0 | "Tambah ke Keranjang" | scr_frm_Transaction | `Button15.OnSelect` (preserved verbatim); DisplayMode gate | colTempDetails.Urutan | line appended | Urutan, Id, name, description, Qty | name, Qty, description in Gallery7 row | Gallery7 + `txtTrxFCartCount` |
| ACT-TRX-CART-REMOVE | line exists | Delete icon in cart row | scr_frm_Transaction | `icoTrxFCartDel.OnSelect: =Remove(colTempDetails, ThisItem)` | colTempDetails row | line removed | existence | count | `txtTrxFCartCount` |
| ACT-TRX-SAVE | Form valid | "Simpan Transaksi" | scr_frm_Transaction | `Button32.OnSelect: =SubmitForm(Form5)`; `Form5.OnSuccess` verbatim + 1 receipt statement | dis_trx_headers + dis_trx_details + dis_stocks | header saved, lines rewritten, stock +/- by type (Receive increase) | transaction_number, type, area_form, area_to, note, details, stock qty | number, type, from, to, note, line count | `conTrxLReceipt`; Gallery8_9 (Find) stock |
| ACT-CONSUME-FILTER | none | 4 dropdowns + search + reset | scr_consume | `Gallery8_11.Items` preserved; cascade OnChange; `icoConsReset` | dis_stocks | filtered | N/A | N/A | Gallery8_11; `txtConsEmpty` |
| ACT-CONSUME-SUBMIT | area selected, >=1 qty>0, no qty>stock | "Consume" | scr_consume | `btnConsSubmit.OnSelect` (bug-fixed, see brief); DisplayMode gate | dis_stocks.dis_stock per line; new dis_trx_header | header {number, type Consume, area_form}; details; stock = old - amount | header 3 fields, detail rows, stock qty | number, type, area, per line operation/old/amount/expected/actual | `conConsReceipt` + `galConsReceipt`; Gallery8_9 stock |
| ACT-FIND-FILTER | none | 4 dropdowns + search + reset | scr_find_item | `Gallery8_9.Items` preserved; cascade OnChange; `icoFindReset` | dis_stocks | filtered | N/A | N/A | Gallery8_9; `txtFindEmpty` |
| ACT-HIST-FILTER | none | Type segment, DatePicker2 + clear, search | scr_History | `btnHistType*`, `icoHistDateClear.OnSelect: =Reset(DatePicker2)`, `Gallery8_7.Items` | dis_trx_headers | filtered | N/A | N/A | Gallery8_7; `txtHistEmpty` |
| ACT-HIST-SELECT | rows | number link | scr_History | `btnHistOpen` (gallery selection) | dis_trx_header | Gallery8_7.Selected | N/A | N/A | `txtHistDetailTitle`, Gallery8_8 |

## Mutation Lifecycle Evidence

| Action | Receipt binding | Canonical source and observer | Requested destination and observer | Stable ID continuity | Synchronization when sources differ | Destination focus |
| --- | --- | --- | --- | --- | --- | --- |
| ACT-AREA-SAVE | `Form5_1.OnSuccess` sets `gblReceipt` from `Form5_1.LastSubmit`; `conAreaLReceipt` | dis_areas; `Gallery8_12.Items` | Area list Gallery8_12 | LastSubmit.dis_area | N/A - same live source | N/A (receipt names record) |
| ACT-AREA-DELETE | snapshot `With({target: locSelectedRecord}, ...)` -> gblReceipt | dis_areas; Gallery8_12 | Gallery8_12 | locSelectedRecord.dis_area | N/A | N/A |
| ACT-USER-SAVE | `Form4.OnSuccess` -> gblReceipt from `Form4.LastSubmit` | dis_users; Gallery8_13 | Gallery8_13 (same screen) | LastSubmit.dis_user | N/A | N/A |
| ACT-USER-DELETE | snapshot target -> gblReceipt | dis_users; Gallery8_13 | Gallery8_13 | locSelectedRecord.dis_user | N/A | N/A |
| ACT-CAT-SAVE | `frm_catFrm_category.OnSuccess` -> gblReceipt | dis_category_items; gal_cat_list | gal_cat_list | LastSubmit.dis_category_item | N/A | N/A |
| ACT-CAT-DELETE | snapshot -> gblReceipt | dis_category_items | gal_cat_list | locSelectedRecord.dis_category_item | N/A | N/A |
| ACT-ITEM-SAVE | `Form5_3.OnSuccess` -> gblReceipt | dis_item_v2S | Gallery8_6 | LastSubmit.dis_item_v2 | N/A | N/A |
| ACT-ITEM-DELETE | snapshot -> gblReceipt | dis_item_v2S | Gallery8_6 | locSelectedRecord.dis_item_v2 | N/A | N/A |
| ACT-TRX-SAVE | inserted `Set(gblReceipt, ...)` in Form5.OnSuccess before step 4 | dis_trx_headers / dis_trx_details / dis_stocks | Gallery8_1 (scr_Transaction), Gallery8_9 stock | LastSubmit.dis_trx_header | N/A - Dataverse live | N/A |
| ACT-TRX-DELETE | snapshot -> gblReceipt | dis_trx_headers + details | Gallery8_1 | locSelectedRecord.dis_trx_header | N/A | N/A |
| ACT-TRX-CART-ADD / REMOVE | Gallery7 row itself + `txtTrxFCartCount` (staging collection) | colTempDetails | Gallery7 | Urutan | N/A | N/A |
| ACT-CONSUME-SUBMIT | `colConsumeReceipt` rows + `locConsHeader` (Patch result) | dis_stocks (per dis_stock), dis_trx_headers | `galConsReceipt` + Gallery8_9 on scr_find_item | ItemConsume.dis_stock; newHeader.dis_trx_header | N/A | N/A |

## Mutation Field Ledger

| Action | Field | Classification | Canonical pre-state or input | Write or preservation mechanism | Receipt/proof binding | Post-state observer |
| --- | --- | --- | --- | --- | --- | --- |
| ACT-AREA-SAVE | Name / elv_geounit / location / elv_dis_subblid / elv_detail | Changed | Form5_1 card values (preserved Update formulas) | SubmitForm(Form5_1) | `gblReceipt.Title` = LastSubmit.Name; `gblReceipt.Detail` lists Geounit, Lokasi, Business Line, Detail | Gallery8_12 row cells |
| ACT-USER-SAVE | Name / email / role / Assigned_area | Changed | Form4 card values | SubmitForm(Form4) | Title = LastSubmit.Name; Detail = Email, Role, Area | Gallery8_13 row |
| ACT-CAT-SAVE | name / code / description | Changed | card inputs | SubmitForm | Title name; Detail Kode, Deskripsi | gal_cat_list |
| ACT-ITEM-SAVE | name, min_qty, part_number, client_number, uom, status, dis_category_item, description, Image | Changed | card inputs | SubmitForm(Form5_3) | Title name; Detail BPN, SPN, Min, UoM, Status, Kategori, Deskripsi, Gambar | Gallery8_6 row |
| ACT-TRX-SAVE | header fields + detail rows + dis_stocks.qty | Changed | Form5 cards + colTempDetails | existing OnSuccess verbatim | Title number; Detail Tipe, Dari, Ke, Catatan, N item | Gallery8_1; Gallery8_9 |
| ACT-CONSUME-SUBMIT | dis_trx_headers.transaction_number / type / area_form | Changed | generated number; `'type (dis_trx_headers)'.Consume`; `dd_Area_1.Selected` | Patch Defaults | `txtConsRcTitle`, `txtConsRcSub` | Gallery8_1 / Gallery8_7 |
| ACT-CONSUME-SUBMIT | dis_stocks.qty | Changed | `LookUp(dis_stocks, dis_stock = ItemConsume.dis_stock).qty` - `numConsQty.Value` | Patch by dis_stock | galConsReceipt Old/Amount/Expected/Actual | Gallery8_9 Stock badge |
| ACT-CONSUME-SUBMIT | dis_stocks.dis_item_v2 / dis_area | Preserved | canonical row | omitted from partial Patch | N/A | Gallery8_9 row |
| ACT-*-DELETE | record existence | Changed | locSelectedRecord | Remove(source, locSelectedRecord) | gblReceipt Action "Dihapus" + Title | gallery absence |

## Functional Test Matrix

| Scenario | Given | When | Then | Evidence surface | Boundary or negative case |
| --- | --- | --- | --- | --- | --- |
| SCN-NAV-MENU | On scr_item | Click "Area" in sidebar | Area screen shown | Area TopBar "Area"; sidebar pill on "Area" | Template has no active pill (activemenu "") |
| SCN-NAV-ROLE | Signed-in user role administrator | Open any shell screen | Sidebar shows "Administrator" | `txtSbUserRole.Text` | Unregistered -> "Belum terdaftar" |
| SCN-START-REGISTERED | dis_users row with email = User().Email | Launch app | 'Log In' start screen; imyrole/imyid/imyarea/imyemail set | `txtLoginName` shows nfMe.Name | N/A |
| SCN-START-UNREGISTERED | No matching dis_users row | Launch | Register start screen | `galRegAdmins` | N/A |
| SCN-LOGIN-ENTER | Registered user on Log In | Click "Masuk ke Dashboard" | scr_dashboard shown | Dashboard TopBar | Button disabled when nfMe blank |
| SCN-REG-LIST | 2 admins (A: Area Yard-1), 1 user | Open Register | 2 rows with Name, email, area; user absent | galRegAdmins | Mail icon -> mailto:A email |
| SCN-DASH-KPI | 12 items; stock rows S1 qty 2 / min 5, S2 qty 10 / min 5; 3 headers created today | Open Dashboard | KPIs 12 / 1 / 3; low list shows S1 only; recent list newest first | KPI texts, galDashLow, galDashRecent | S2 excluded (qty >= min) |
| SCN-DASH-EMPTY | No headers, no low stock | Open Dashboard | KPI "0"; `txtDashRecentEmpty` + `txtDashLowEmpty` visible | empty texts | N/A |
| SCN-DASH-OPEN-TRX | cart has stale lines | Click "Transaksi Baru" | colTempDetails empty, Form5 New | scr_frm_Transaction Gallery7 empty | "Lihat semua" -> scr_Transaction |
| SCN-AREA-FILTER | Areas A1, A2 in Geounit G1, A3 in G2 | Pick G1 | A1, A2 shown; A3 hidden; Location enabled | Gallery8_12 | Reset icon restores all 3 |
| SCN-AREA-ADD | none | Click "Tambah Area" | Add_area in New mode, empty fields | Add_area header "Tambah Area" | N/A |
| SCN-AREA-EDIT | Rows A1, A2 | Click Edit on A2 | Add_area shows A2 values | Form5_1 cards | N/A |
| SCN-AREA-SAVE | Edit A2, Detail "Rack 4" | Simpan | dis_areas A2.elv_detail = "Rack 4"; back on Area | conAreaLReceipt "Disimpan - A2" detail lists Rack 4; Gallery8_12 | Required Name blank -> Parent.Error shown, no receipt |
| SCN-AREA-DELETE | A1 selected (first row), click Delete on A3 | Hapus | A3 removed, A1 untouched | conAreaLReceipt "Dihapus - A3"; Gallery8_12 | Bug-fix proof: target is clicked row |
| SCN-AREA-DELETE-CANCEL | Confirm open for A3 | Batal | A3 still present; strip hidden | Gallery8_12 | N/A |
| SCN-USER-EDIT | Users U1, U2 | Edit on U2 | Editor visible with U2 values | conUsrLEditor title "Edit Pengguna - U2" | N/A |
| SCN-USER-SAVE | Editor U2, role -> approval | Simpan | U2.role = approval; editor closed | conUsrLReceipt Role approval; Gallery8_13 badge | N/A |
| SCN-USER-DELETE | U1 selected, Delete on U2 | Hapus | U2 removed only | conUsrLReceipt "Dihapus - U2" | Batal leaves U2 |
| SCN-CAT-SEARCH | C1 "Pipe", C2 "Pipe Fitting", C3 "Valve" | type "Pipe" | C1, C2 shown, C3 hidden | gal_cat_list | clear text restores 3 |
| SCN-CAT-ADD | none | Tambah Kategori | form New | scr_frm_category title | N/A |
| SCN-CAT-EDIT | C2 | Edit on C2 | form shows C2 | form cards | N/A |
| SCN-CAT-SAVE | New category "Hose", code "HS" | Simpan | row created | conCatLReceipt Title Hose, Detail code HS | required blank -> error |
| SCN-CAT-DELETE | C3 | Delete -> Hapus | C3 removed | conCatLReceipt | Batal keeps C3 |
| SCN-ITEM-FILTER | I1, I2 in cat PIPE, I3 in VALVE | pick PIPE | I1, I2 only | Gallery8_6 | reset restores |
| SCN-ITEM-ADD | none | Tambah Item | New | form | N/A |
| SCN-ITEM-EDIT | I2 | Edit | prefilled | form | N/A |
| SCN-ITEM-SAVE | Edit I2 min_qty 5 -> 8 | Simpan | I2.min_qty = 8 | conItmLReceipt Min 8; Gallery8_6 | N/A |
| SCN-ITEM-DELETE | I3 | Delete -> Hapus | I3 removed | conItmLReceipt | Batal keeps I3 |
| SCN-TRX-FILTER | H1 Receive, H2 Receive, H3 Consume | click "Receive" | H1, H2 shown; H3 hidden; Receive segment Primary | Gallery8_1 | "Semua" restores |
| SCN-TRX-DETAIL | H1 with 2 lines, H2 with 1 | click H1 number | detail shows 2 lines of H1 | txtTrxLDetailTitle, Gallery8_3 | category filter hides non-matching line |
| SCN-TRX-ADD | none | Tambah Transaksi | empty cart, New | scr_frm_Transaction | N/A |
| SCN-TRX-EDIT | H1 with 2 lines | Edit on H1 | colTempDetails has 2 lines | Gallery7 | N/A |
| SCN-TRX-DELETE | H3 with 1 line | Delete -> Hapus | H3 and its line removed | conTrxLReceipt; Gallery8_1 | stock not reversed (preserved) |
| SCN-TRX-CART | Item "Bentonite", qty 3 | Tambah ke Keranjang | colTempDetails +1 (Qty 3) | Gallery7 row, txtTrxFCartCount "1 item" | button disabled when qty blank/0 or no item |
| SCN-TRX-CART-REMOVE | 2 lines | delete icon line 1 | 1 line | Gallery7, count | N/A |
| SCN-TRX-SAVE-RECEIVE | Stock S1 (Bentonite @ Yard A) qty 10 | New Receive to Yard A, Bentonite 3, Simpan | header + 1 line; S1.qty = 13 | conTrxLReceipt (Tipe Receive, Ke Yard A, 1 item); Find Gallery8_9 S1 = 13 | Receive to area without stock row creates new row |
| SCN-CONSUME-FILTER | S1 Yard A, S2 Yard A, S3 Yard B | choose Area Yard A | S1, S2 shown; S3 hidden | Gallery8_11 | reset restores |
| SCN-CONSUME-OK | S1 qty 13, Area Yard A | qty 2 on S1, Consume | header type Consume, area_form Yard A; detail qty 2; S1.qty = 11 | conConsReceipt: Consume / old 13 / amount 2 / expected 11 / actual 11 | N/A |
| SCN-CONSUME-BLOCKED | Area blank OR all qty 0 OR S1 qty 13 with input 20 | look at Consume | btnConsSubmit Disabled; txtConsWarn "Qty melebihi stok" for 20; source unchanged | btnConsSubmit.DisplayMode, numConsQty ValidationState | handler guard repeats checks |
| SCN-CONSUME-COMPOUND | S1 qty 10 | Receive 3 via Form5 (-> 13), then Consume 2 on scr_consume | S1.qty = 11; consume receipt old = 13 (fresh LookUp) | galConsReceipt OldQty 13, ActualQty 11 | N/A |
| SCN-FIND-FILTER | S1 Bentonite qty 2 min 5, S2 qty 10 min 5, S3 in other category | pick category | S1, S2 shown; S1 stock badge Danger, S2 Success | Gallery8_9 | reset restores |
| SCN-HIST-DATE | H1 created 2026-10-01, H2 2026-10-03 | pick 2026-10-03 | H2 only | Gallery8_7 | clear icon restores both |
| SCN-HIST-DETAIL | H2 with 2 lines | click H2 number | 2 lines | txtHistDetailTitle, Gallery8_8 | detail search filters by item name/BPN |

## Directional Mutation Evidence

| Pair | Selected-record expression | Operation-state reset binding | Invalid-submit gate | Receive/increase mutation | Issue/decrease mutation | Canonical-source observer | Receipt bindings |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Receive/Consume (dis_stocks.qty) | Direct row actions, no shared selection: Consume uses each gallery line's `ItemConsume.dis_stock`; Receive uses `LookUp(dis_stocks, dis_item_v2.dis_item_v2 = TempRecord.Id And dis_area.dis_area = idAreaTo)` | N/A - independent direct actions (Consume button identity commits direction; Receive direction from Form5 `type`); amounts reset by `Reset(Gallery8_11)` after success (`numConsQty.Default: =0`) | `btnConsSubmit.DisplayMode: =If(IsBlank(dd_Area_1.Selected) \|\| CountRows(Filter(Gallery8_11.AllItems, numConsQty.Value > 0)) = 0 \|\| CountRows(Filter(Gallery8_11.AllItems, numConsQty.Value > qty \|\| numConsQty.Value < 0)) > 0, DisplayMode.Disabled, DisplayMode.Edit)` | `Form5.OnSuccess` (preserved): `If(varTrxType = "Receive" Or varTrxType = "Transfer", ... Patch(dis_stocks, varStockTo, {qty: varStockTo.qty + TempRecord.Qty}))` | `btnConsSubmit.OnSelect`: `With({oldQty: LookUp(dis_stocks, dis_stock = ItemConsume.dis_stock).qty, amt: ItemConsume.numConsQty.Value}, ... Patch(dis_stocks, LookUp(dis_stocks, dis_stock = ItemConsume.dis_stock), {qty: oldQty - amt}) ...)` | `Gallery8_9` (scr_find_item) `bdgFindStock.Content: =Text(ThisItem.qty)` | operation=txtConsRcOp.Text: =ThisItem.Operation<br>old=txtConsRcOld.Text: =Text(ThisItem.OldQty)<br>amount=txtConsRcAmt.Text: =Text(ThisItem.Amount)<br>expected=txtConsRcExp.Text: =Text(ThisItem.ExpectedQty)<br>actual=txtConsRcAct.Text: =Text(ThisItem.ActualQty) |

Receive receipt approximation: Form5.OnSuccess must stay verbatim (approved constraint), so the Receive direction proves
header, type, destination and line count in `conTrxLReceipt`; its stock post-state is observed on scr_find_item
(Gallery8_9) rather than an old/expected/actual receipt.

## Compound Sequence Evidence

| Pair | Same-record ID expression | Sequence (start -> op1 amount -> mid -> op2 amount -> end) | Second-op old-value binding (reads mutated canonical source) |
| --- | --- | --- | --- |
| Receive/Consume | `ItemConsume.dis_stock` (= S1 dis_stock) | `Qty 10 -> Receive 3 -> 13 -> Consume 2 -> 11` | `btnConsSubmit.OnSelect: =... With({oldQty: LookUp(dis_stocks, dis_stock = ItemConsume.dis_stock).qty, ...}, ... {qty: oldQty - amt} ...)` (replaces the stale `ItemConsume.qty` gallery snapshot) |

## Data Entry Label Contracts

| Required input | Persistent visible label | Shared field region |
| --- | --- | --- |
| dd_Geounit_2 / dd_Location_2 / dd_Area_2 / inp_search_9 | txtAreaLGeoLbl "Geounit" / txtAreaLLocLbl "Location" / txtAreaLAreaLbl "Area" / txtAreaLSearchLbl "Cari" | conAreaLGeoFld / conAreaLLocFld / conAreaLAreaFld / conAreaLSearchFld |
| inp_cat_search | txtCatLSearchLbl "Cari kategori" | conCatLSearchFld |
| Dropdown2_2 / inp_search_4 | txtItmLCatLbl "Kategori" / txtItmLSearchLbl "Cari item" | conItmLCatFld / conItmLSearchFld |
| inp_search_1 / Dropdown2_1 / inp_search_2 | txtTrxLSearchLbl / txtTrxLDCatLbl / txtTrxLDSearchLbl | conTrxLSearchFld / conTrxLDCatFld / conTrxLDSearchFld |
| Combobox1_1 / TextInput12_1 | txtTrxFItemLbl "Item" / txtTrxFQtyLbl "Qty" | conTrxFItemFld / conTrxFQtyFld |
| dd_Category_1 / dd_Geounit_1 / dd_Location_1 / dd_Area_1 / inp_search_8 | txtConsCatLbl / txtConsGeoLbl / txtConsLocLbl / txtConsAreaLbl "Area (From)" / txtConsSearchLbl | conConsCatFld / conConsGeoFld / conConsLocFld / conConsAreaFld / conConsSearchFld |
| numConsQty (row) | txtConsQtyLbl "Qty pakai" | conConsQtyFld (inside row) |
| dd_Category / dd_Geounit / dd_Location / dd_Area / inp_search_7 | txtFind*Lbl | conFind*Fld |
| DatePicker2 / inp_search_5 / Dropdown2_4 / inp_search_6 | txtHistDateLbl / txtHistSearchLbl / txtHistDCatLbl / txtHistDSearchLbl | conHistDateFld / conHistSearchFld / conHistDCatFld / conHistDSearchFld |
| Form data-card inputs (Form5_1, Form4, frm_catFrm_category, Form5_3, Form5) | existing `MetadataKey: FieldName` card label | each TypedDataCard |

## Layout Budget Contracts

| Screen / container | Branch / screen-width source | Horizontal total-width arithmetic | Vertical height arithmetic | Protected controls |
| --- | --- | --- | --- | --- |
| All shell screens / con<P>Root | Fixed desktop, minimum canvas 1136 x 640 (single branch) | 1136 = Sidebar 224 + Main 912; Body inner = 912 - 24 - 24 = 864 | Main 640 = TopBar 64 + Body 576; Body inner = 576 - 20 - 24 = 532 (scrolls beyond) | Sidebar menu, TopBar title |
| List card (Area/Cat/Item/User/Find) | same | card inner 864 - 32 = 832; row inner 832 - 2 (padding) - 24 = 806 | 16 + 56 + 12 + 36 + 4 + gallery 380 + 16 = 520 <= 532 | Add button, row Edit/Delete icons |
| Toolbars | same | per brief, each <= 832 | 56 | Add / reset |
| Confirm strip | same | 864 - 28 - 24 - 104 - 96 - 36 = 576 message | 56 | Hapus, Batal |
| Receipt strip | same | 864 - 28 - 24 - 32 - 24 = 756 text | 10 + 58 + 10 = 78 -> Height 80 | Title + Detail |
| Dashboard | same | KPI card (864 - 32)/3 = 277 | 104 + 16 + 40 + 16 + 356 = 532 | KPI values, quick actions |
| Consume card | same | toolbar 4x140 + 140 + 32 + 5x8 = 772 <= 832 | 16 + 56 + 12 + 36 + 4 + 312 + 12 + 44 + 16 = 508 | Consume button, qty inputs |
| Consume receipt | same | 6 columns in 832 | 12 + 44 + 8 + 28 + 4 + 120 + 12 = 228 | op/old/amount/expected/actual |

## Viewport Containment Contracts

| Screen | Root control | Layout variant | Width binding | Height binding | Overflow policy |
| --- | --- | --- | --- | --- | --- |
| scr_dashboard | conDashRoot | AutoLayout | `conDashRoot.Width: =Parent.Width` | `conDashRoot.Height: =Parent.Height` | conDashBody vertical scroll |
| Log In | conLoginRoot | AutoLayout | `conLoginRoot.Width: =Parent.Width` | `conLoginRoot.Height: =Parent.Height` | conLoginRight vertical scroll (content 290 <= 544) |
| Register | conRegRoot | AutoLayout | `conRegRoot.Width: =Parent.Width` | `conRegRoot.Height: =Parent.Height` | conRegRight vertical scroll |
| Template | conTplRoot | AutoLayout | `=Parent.Width` | `=Parent.Height` | conTplBody scroll |
| Area | conAreaLRoot | AutoLayout | `=Parent.Width` | `=Parent.Height` | conAreaLBody scroll |
| Add_area | conAreaFRoot | AutoLayout | `=Parent.Width` | `=Parent.Height` | conAreaFBody scroll |
| scr_user | conUsrLRoot | AutoLayout | `=Parent.Width` | `=Parent.Height` | conUsrLBody scroll |
| scr_category | conCatLRoot | AutoLayout | `=Parent.Width` | `=Parent.Height` | conCatLBody scroll |
| scr_frm_category | conCatFRoot | AutoLayout | `=Parent.Width` | `=Parent.Height` | conCatFBody scroll |
| scr_item | conItmLRoot | AutoLayout | `=Parent.Width` | `=Parent.Height` | conItmLBody scroll |
| scr_frm_item | conItmFRoot | AutoLayout | `=Parent.Width` | `=Parent.Height` | conItmFBody scroll |
| scr_Transaction | conTrxLRoot | AutoLayout | `=Parent.Width` | `=Parent.Height` | conTrxLBody scroll |
| scr_frm_Transaction | conTrxFRoot | AutoLayout | `=Parent.Width` | `=Parent.Height` | conTrxFBody scroll |
| scr_consume | conConsRoot | AutoLayout | `=Parent.Width` | `=Parent.Height` | conConsBody scroll |
| scr_find_item | conFindRoot | AutoLayout | `=Parent.Width` | `=Parent.Height` | conFindBody scroll |
| scr_History | conHistRoot | AutoLayout | `=Parent.Width` | `=Parent.Height` | conHistBody scroll |

## Temporal Ordering Contracts

| Ordering key | Source | Sort field | Storage semantics | Input validation / normalization | Canonical sort binding | Accepted formats | Invalid / blank behavior |
| --- | --- | --- | --- | --- | --- | --- | --- |
| trx-created | dis_trx_headers | 'Created On' | Typed DateTime (system) | N/A (system-set) | `Sort(..., 'Created On', SortOrder.Descending)` in galDashRecent, Gallery8_1, Gallery8_7 | N/A | N/A |

## Working Directory

C:\Project\Powerapps\app

## Discovery Summary

- Existing screens: Register, Log In, Template, Area, Add_area, scr_user, scr_Transaction, scr_frm_Transaction,
  scr_category, scr_frm_category, scr_item, scr_frm_item, scr_find_item, scr_History, scr_consume (+ new scr_dashboard)
- Components: Sidebar (activemenu), TopBar (ActiveMenu; Subtitle added in this edit) - `Control: CanvasComponent`
- Layout: mixed today (AutoLayout shells with ManualLayout spacers + absolute overlays); target = pure AutoLayout
- Controls used: GroupContainer (AutoLayout), ModernText, ModernButton, ModernIcon, Badge, Gallery (Vertical),
  ModernTextInput, ModernDropdown, ModernNumberInput, ModernDatePicker, ModernCombobox (existing), Image, Form (existing
  Modern/Vertical), TypedDataCard + Classic/ComboBox / FluentV8/Label / AddMedia (existing, preserved)
- Data sources: dis_users, dis_areas, dis_geounits, dis_locations, dis_category_items, dis_item_v2S, dis_stocks,
  dis_trx_headers, dis_trx_details (all Dataverse)
- Connectors: none

## Dispatch

Wave note: scr_dashboard must be written (and present for compile) before or together with Log In, because
`btnLoginEnter` navigates to it. Keep row 1 in wave 1.

| Action | Screen | Target File | YAML Key | Name Prefix | Screen Brief |
| --- | --- | --- | --- | --- | --- |
| Create | Dashboard | `C:\Project\Powerapps\app\scr_dashboard.pa.yaml` | scr_dashboard | Dash | `C:\Project\Powerapps\app\scr_dashboard.screen-plan.md` |
| Modify | Log In | `C:\Project\Powerapps\app\Log In.pa.yaml` | Log In | Login | `C:\Project\Powerapps\app\Log In.screen-plan.md` |
| Modify | Register | `C:\Project\Powerapps\app\Register.pa.yaml` | Register | Reg | `C:\Project\Powerapps\app\Register.screen-plan.md` |
| Modify | Template | `C:\Project\Powerapps\app\Template.pa.yaml` | Template | Tpl | `C:\Project\Powerapps\app\Template.screen-plan.md` |
| Modify | Area | `C:\Project\Powerapps\app\Area.pa.yaml` | Area | AreaL | `C:\Project\Powerapps\app\Area.screen-plan.md` |
| Modify | Add_area | `C:\Project\Powerapps\app\Add_area.pa.yaml` | Add_area | AreaF | `C:\Project\Powerapps\app\Add_area.screen-plan.md` |
| Modify | scr_user | `C:\Project\Powerapps\app\scr_user.pa.yaml` | scr_user | UsrL | `C:\Project\Powerapps\app\scr_user.screen-plan.md` |
| Modify | scr_category | `C:\Project\Powerapps\app\scr_category.pa.yaml` | scr_category | CatL | `C:\Project\Powerapps\app\scr_category.screen-plan.md` |
| Modify | scr_frm_category | `C:\Project\Powerapps\app\scr_frm_category.pa.yaml` | scr_frm_category | CatF | `C:\Project\Powerapps\app\scr_frm_category.screen-plan.md` |
| Modify | scr_item | `C:\Project\Powerapps\app\scr_item.pa.yaml` | scr_item | ItmL | `C:\Project\Powerapps\app\scr_item.screen-plan.md` |
| Modify | scr_frm_item | `C:\Project\Powerapps\app\scr_frm_item.pa.yaml` | scr_frm_item | ItmF | `C:\Project\Powerapps\app\scr_frm_item.screen-plan.md` |
| Modify | scr_Transaction | `C:\Project\Powerapps\app\scr_Transaction.pa.yaml` | scr_Transaction | TrxL | `C:\Project\Powerapps\app\scr_Transaction.screen-plan.md` |
| Modify | scr_frm_Transaction | `C:\Project\Powerapps\app\scr_frm_Transaction.pa.yaml` | scr_frm_Transaction | TrxF | `C:\Project\Powerapps\app\scr_frm_Transaction.screen-plan.md` |
| Modify | scr_consume | `C:\Project\Powerapps\app\scr_consume.pa.yaml` | scr_consume | Cons | `C:\Project\Powerapps\app\scr_consume.screen-plan.md` |
| Modify | scr_find_item | `C:\Project\Powerapps\app\scr_find_item.pa.yaml` | scr_find_item | Find | `C:\Project\Powerapps\app\scr_find_item.screen-plan.md` |
| Modify | scr_History | `C:\Project\Powerapps\app\scr_History.pa.yaml` | scr_History | Hist | `C:\Project\Powerapps\app\scr_History.screen-plan.md` |

## App Changes

### Before builders

Apply all three files verbatim, compile, then re-run `describe_control` for `Sidebar` and `TopBar` (TopBar gains the
`Subtitle` input). Every screen brief already lists `Subtitle` and requires instances to set both TopBar inputs.
The Dashboard menu entry intentionally keeps `scr_consume` until scr_dashboard exists (see After builders).

`C:\Project\Powerapps\app\App.pa.yaml` (complete file):

```yaml
App:
  Properties:
    BackEnabled: =false
    Formulas: |-
      =nfMe = LookUp(dis_users, email = User().Email);
      clrNavy = RGBA(0, 18, 107, 1);
      clrAccent = RGBA(56, 96, 178, 1);
      clrBg = RGBA(244, 246, 250, 1);
      clrSurface = RGBA(255, 255, 255, 1);
      clrBorder = RGBA(226, 230, 239, 1);
      clrHeaderBg = RGBA(241, 244, 250, 1);
      clrRowSelected = RGBA(232, 238, 252, 1);
      clrText = RGBA(31, 41, 55, 1);
      clrTextMuted = RGBA(100, 112, 130, 1);
      clrDanger = RGBA(196, 43, 28, 1);
      clrDangerTint = RGBA(253, 237, 236, 1);
      clrSuccess = RGBA(16, 124, 65, 1);
      clrSuccessTint = RGBA(232, 246, 238, 1);
      clrWarning = RGBA(188, 118, 0, 1);
      clrWarningTint = RGBA(255, 246, 225, 1);
      fxMenuItems = Table(
          {
              TextValue: "Dashboard",
              Icon: "Home",
              NavigateScreen: scr_consume
          },
          {
              TextValue: "Category Item",
              Icon: "AppsList",
              NavigateScreen: scr_category
          },
          {
              TextValue: "Item",
              Icon: "Folder",
              NavigateScreen: scr_item
          },
          {
              TextValue: "Area",
              Icon: "BuildingRetail",
              NavigateScreen: Area
          },
          {
              TextValue: "User",
              Icon: "Person",
              NavigateScreen: scr_user
          },
          {
              TextValue: "Consume",
              Icon: "Wrench",
              NavigateScreen: scr_consume
          },
          {
              TextValue: "Transaction",
              Icon: "Cart",
              NavigateScreen: scr_Transaction
          },
          {
              TextValue: "Find Item",
              Icon: "Search",
              NavigateScreen: scr_find_item
          },
          {
              TextValue: "History",
              Icon: "History",
              NavigateScreen: scr_History
          }
      );
    OnStart: |-
      =Set(imyrole, nfMe.role);
      Set(imyid, nfMe.dis_user);
      Set(imyarea, nfMe.Assigned_area);
      Set(imyemail, nfMe.email);
      ClearCollect(
          iroleview,
          nfMe.'dis_areas (cr8a3_elv_dis_user_elv_dis_area_elv_dis_area)'
      );
      Set(gblReceipt, {Screen: "", Action: "", Title: "", Detail: ""})
    StartScreen: =If(IsBlank(nfMe.Name), Register, 'Log In')
    Theme: =PowerAppsTheme
```

`C:\Project\Powerapps\app\Components\Sidebar.pa.yaml` (complete file):

```yaml
ComponentDefinitions:
  Sidebar:
    DefinitionType: CanvasComponent
    AccessAppScope: true
    CustomProperties:
      activemenu:
        PropertyKind: Input
        DisplayName: activemenu
        Description: TextValue of the active fxMenuItems entry
        DataType: Text
        Default: =""
    Properties:
      Height: =640
      Width: =224
    Children:
      - conSbRoot:
          Control: GroupContainer
          Variant: AutoLayout
          Properties:
            DropShadow: =DropShadow.None
            Fill: =clrNavy
            Height: =Sidebar.Height
            LayoutAlignItems: =LayoutAlignItems.Stretch
            LayoutDirection: =LayoutDirection.Vertical
            LayoutGap: =8
            LayoutMinHeight: =0
            LayoutMinWidth: =0
            PaddingBottom: =16
            PaddingLeft: =12
            PaddingRight: =12
            PaddingTop: =20
            RadiusBottomLeft: =0
            RadiusBottomRight: =0
            RadiusTopLeft: =0
            RadiusTopRight: =0
            Width: =Sidebar.Width
            X: =0
            Y: =0
          Children:
            - conSbBrand:
                Control: GroupContainer
                Variant: AutoLayout
                Properties:
                  AlignInContainer: =AlignInContainer.Stretch
                  DropShadow: =DropShadow.None
                  FillPortions: =0
                  Height: =48
                  LayoutAlignItems: =LayoutAlignItems.Center
                  LayoutDirection: =LayoutDirection.Horizontal
                  LayoutGap: =10
                  LayoutMinHeight: =0
                  LayoutMinWidth: =0
                  PaddingLeft: =4
                  RadiusBottomLeft: =0
                  RadiusBottomRight: =0
                  RadiusTopLeft: =0
                  RadiusTopRight: =0
                Children:
                  - imgSbLogo:
                      Control: Image
                      Properties:
                        AccessibleLabel: ="SLB logo"
                        AlignInContainer: =AlignInContainer.Center
                        FillPortions: =0
                        Height: =32
                        Image: ='slb logo white'
                        ImagePosition: =ImagePosition.Fit
                        LayoutMinHeight: =0
                        LayoutMinWidth: =0
                        Width: =64
                  - txtSbBrand:
                      Control: ModernText
                      Properties:
                        AccessibleLabel: ="Digital Inventory"
                        AlignInContainer: =AlignInContainer.Center
                        Color: =RGBA(255, 255, 255, 1)
                        FillPortions: =1
                        Font: =Font.'Segoe UI'
                        FontWeight: =FontWeight.Bold
                        Height: =40
                        LayoutMinHeight: =0
                        LayoutMinWidth: =0
                        PaddingBottom: =0
                        PaddingLeft: =0
                        PaddingRight: =0
                        PaddingTop: =0
                        Size: =13
                        Text: ="Digital Inventory"
                        VerticalAlign: =VerticalAlign.Middle
                        Wrap: =true
            - txtSbSection:
                Control: ModernText
                Properties:
                  AccessibleLabel: ="Menu"
                  AlignInContainer: =AlignInContainer.Stretch
                  Color: =RGBA(255, 255, 255, 0.55)
                  FillPortions: =0
                  Font: =Font.'Segoe UI'
                  FontWeight: =FontWeight.Semibold
                  Height: =24
                  LayoutMinHeight: =0
                  LayoutMinWidth: =0
                  PaddingBottom: =0
                  PaddingLeft: =8
                  PaddingRight: =0
                  PaddingTop: =0
                  Size: =11
                  Text: ="MENU"
                  VerticalAlign: =VerticalAlign.Bottom
                  Wrap: =false
            - galSbMenu:
                Control: Gallery
                Variant: Vertical
                Properties:
                  AccessibleLabel: ="Menu navigasi"
                  AlignInContainer: =AlignInContainer.Stretch
                  BorderThickness: =0
                  Fill: =RGBA(0, 0, 0, 0)
                  FillPortions: =1
                  Items: =fxMenuItems
                  LayoutMinHeight: =0
                  LayoutMinWidth: =0
                  ShowScrollbar: =false
                  TabIndex: =0
                  TemplatePadding: =2
                  TemplateSize: =40
                Children:
                  - conSbItem:
                      Control: GroupContainer
                      Variant: AutoLayout
                      Properties:
                        DropShadow: =DropShadow.None
                        Fill: =If(ThisItem.TextValue = Sidebar.activemenu, RGBA(255, 255, 255, 0.16), RGBA(0, 0, 0, 0))
                        Height: =Parent.TemplateHeight
                        LayoutAlignItems: =LayoutAlignItems.Center
                        LayoutDirection: =LayoutDirection.Horizontal
                        LayoutGap: =12
                        LayoutMinHeight: =0
                        LayoutMinWidth: =0
                        PaddingLeft: =12
                        PaddingRight: =8
                        RadiusBottomLeft: =8
                        RadiusBottomRight: =8
                        RadiusTopLeft: =8
                        RadiusTopRight: =8
                        Width: =Parent.TemplateWidth
                      Children:
                        - icoSbItem:
                            Control: ModernIcon
                            Properties:
                              AccessibleLabel: =ThisItem.TextValue
                              AlignInContainer: =AlignInContainer.Center
                              FillPortions: =0
                              Height: =20
                              Icon: =ThisItem.Icon
                              IconColor: =If(ThisItem.TextValue = Sidebar.activemenu, RGBA(255, 255, 255, 1), RGBA(255, 255, 255, 0.72))
                              LayoutMinHeight: =0
                              LayoutMinWidth: =0
                              OnSelect: =Navigate(ThisItem.NavigateScreen, ScreenTransition.None)
                              Width: =20
                        - txtSbItem:
                            Control: ModernText
                            Properties:
                              AccessibleLabel: ="Buka " & ThisItem.TextValue
                              AlignInContainer: =AlignInContainer.Stretch
                              Color: =If(ThisItem.TextValue = Sidebar.activemenu, RGBA(255, 255, 255, 1), RGBA(255, 255, 255, 0.72))
                              FillPortions: =1
                              Font: =Font.'Segoe UI'
                              FontWeight: =If(ThisItem.TextValue = Sidebar.activemenu, FontWeight.Semibold, FontWeight.Normal)
                              LayoutMinHeight: =0
                              LayoutMinWidth: =0
                              OnSelect: =Navigate(ThisItem.NavigateScreen, ScreenTransition.None)
                              PaddingBottom: =0
                              PaddingLeft: =0
                              PaddingRight: =0
                              PaddingTop: =0
                              Size: =14
                              Text: =ThisItem.TextValue
                              VerticalAlign: =VerticalAlign.Middle
                              Wrap: =false
            - conSbProfile:
                Control: GroupContainer
                Variant: AutoLayout
                Properties:
                  AlignInContainer: =AlignInContainer.Stretch
                  DropShadow: =DropShadow.None
                  Fill: =RGBA(255, 255, 255, 0.08)
                  FillPortions: =0
                  Height: =64
                  LayoutAlignItems: =LayoutAlignItems.Center
                  LayoutDirection: =LayoutDirection.Horizontal
                  LayoutGap: =10
                  LayoutMinHeight: =0
                  LayoutMinWidth: =0
                  PaddingLeft: =10
                  PaddingRight: =10
                  RadiusBottomLeft: =10
                  RadiusBottomRight: =10
                  RadiusTopLeft: =10
                  RadiusTopRight: =10
                Children:
                  - imgSbAvatar:
                      Control: Image
                      Properties:
                        AccessibleLabel: ="Foto profil"
                        AlignInContainer: =AlignInContainer.Center
                        FillPortions: =0
                        Height: =36
                        Image: =User().Image
                        ImagePosition: =ImagePosition.Fill
                        LayoutMinHeight: =0
                        LayoutMinWidth: =0
                        RadiusBottomLeft: =18
                        RadiusBottomRight: =18
                        RadiusTopLeft: =18
                        RadiusTopRight: =18
                        Width: =36
                  - conSbProfileText:
                      Control: GroupContainer
                      Variant: AutoLayout
                      Properties:
                        AlignInContainer: =AlignInContainer.Center
                        DropShadow: =DropShadow.None
                        FillPortions: =1
                        Height: =40
                        LayoutAlignItems: =LayoutAlignItems.Stretch
                        LayoutDirection: =LayoutDirection.Vertical
                        LayoutGap: =2
                        LayoutJustifyContent: =LayoutJustifyContent.Center
                        LayoutMinHeight: =0
                        LayoutMinWidth: =0
                        RadiusBottomLeft: =0
                        RadiusBottomRight: =0
                        RadiusTopLeft: =0
                        RadiusTopRight: =0
                      Children:
                        - txtSbUserName:
                            Control: ModernText
                            Properties:
                              AccessibleLabel: ="Pengguna " & Coalesce(nfMe.Name, User().FullName)
                              AlignInContainer: =AlignInContainer.Stretch
                              Color: =RGBA(255, 255, 255, 1)
                              FillPortions: =0
                              Font: =Font.'Segoe UI'
                              FontWeight: =FontWeight.Semibold
                              Height: =20
                              LayoutMinHeight: =0
                              LayoutMinWidth: =0
                              PaddingBottom: =0
                              PaddingLeft: =0
                              PaddingRight: =0
                              PaddingTop: =0
                              Size: =13
                              Text: =Coalesce(nfMe.Name, User().FullName)
                              Wrap: =false
                        - txtSbUserRole:
                            Control: ModernText
                            Properties:
                              AccessibleLabel: ="Peran " & If(IsBlank(imyrole), "Belum terdaftar", Proper(Text(imyrole)))
                              AlignInContainer: =AlignInContainer.Stretch
                              Color: =RGBA(255, 255, 255, 0.72)
                              FillPortions: =0
                              Font: =Font.'Segoe UI'
                              Height: =18
                              LayoutMinHeight: =0
                              LayoutMinWidth: =0
                              PaddingBottom: =0
                              PaddingLeft: =0
                              PaddingRight: =0
                              PaddingTop: =0
                              Size: =11
                              Text: =If(IsBlank(imyrole), "Belum terdaftar", Proper(Text(imyrole)))
                              Wrap: =false
```

`C:\Project\Powerapps\app\Components\TopBar.pa.yaml` (complete file):

```yaml
ComponentDefinitions:
  TopBar:
    DefinitionType: CanvasComponent
    AccessAppScope: true
    CustomProperties:
      ActiveMenu:
        PropertyKind: Input
        DisplayName: ActiveMenu
        Description: Page title
        DataType: Text
        Default: =""
      Subtitle:
        PropertyKind: Input
        DisplayName: Subtitle
        Description: Optional page subtitle
        DataType: Text
        Default: =""
    Properties:
      Height: =64
      Width: =912
    Children:
      - conTbRoot:
          Control: GroupContainer
          Variant: AutoLayout
          Properties:
            DropShadow: =DropShadow.None
            Fill: =clrSurface
            Height: =TopBar.Height
            LayoutAlignItems: =LayoutAlignItems.Center
            LayoutDirection: =LayoutDirection.Horizontal
            LayoutGap: =16
            LayoutMinHeight: =0
            LayoutMinWidth: =0
            PaddingBottom: =8
            PaddingLeft: =24
            PaddingRight: =24
            PaddingTop: =8
            RadiusBottomLeft: =0
            RadiusBottomRight: =0
            RadiusTopLeft: =0
            RadiusTopRight: =0
            Width: =TopBar.Width
            X: =0
            Y: =0
          Children:
            - conTbTitles:
                Control: GroupContainer
                Variant: AutoLayout
                Properties:
                  AlignInContainer: =AlignInContainer.Center
                  DropShadow: =DropShadow.None
                  FillPortions: =1
                  Height: =46
                  LayoutAlignItems: =LayoutAlignItems.Stretch
                  LayoutDirection: =LayoutDirection.Vertical
                  LayoutGap: =0
                  LayoutJustifyContent: =LayoutJustifyContent.Center
                  LayoutMinHeight: =0
                  LayoutMinWidth: =0
                  RadiusBottomLeft: =0
                  RadiusBottomRight: =0
                  RadiusTopLeft: =0
                  RadiusTopRight: =0
                Children:
                  - txtTbTitle:
                      Control: ModernText
                      Properties:
                        AccessibleLabel: =TopBar.ActiveMenu
                        AlignInContainer: =AlignInContainer.Stretch
                        Color: =clrText
                        FillPortions: =0
                        Font: =Font.'Segoe UI'
                        FontWeight: =FontWeight.Bold
                        Height: =27
                        LayoutMinHeight: =0
                        LayoutMinWidth: =0
                        PaddingBottom: =0
                        PaddingLeft: =0
                        PaddingRight: =0
                        PaddingTop: =0
                        Size: =18
                        Text: =TopBar.ActiveMenu
                        Wrap: =false
                  - txtTbSubtitle:
                      Control: ModernText
                      Properties:
                        AccessibleLabel: =TopBar.Subtitle
                        AlignInContainer: =AlignInContainer.Stretch
                        Color: =clrTextMuted
                        FillPortions: =0
                        Font: =Font.'Segoe UI'
                        Height: =18
                        LayoutMinHeight: =0
                        LayoutMinWidth: =0
                        PaddingBottom: =0
                        PaddingLeft: =0
                        PaddingRight: =0
                        PaddingTop: =0
                        Size: =12
                        Text: =TopBar.Subtitle
                        Visible: =!IsBlank(TopBar.Subtitle)
                        Wrap: =false
            - txtTbDate:
                Control: ModernText
                Properties:
                  AccessibleLabel: ="Tanggal hari ini"
                  Align: =Align.Right
                  AlignInContainer: =AlignInContainer.Center
                  Color: =clrTextMuted
                  FillPortions: =0
                  Font: =Font.'Segoe UI'
                  Height: =20
                  LayoutMinHeight: =0
                  LayoutMinWidth: =0
                  PaddingBottom: =0
                  PaddingLeft: =0
                  PaddingRight: =0
                  PaddingTop: =0
                  Size: =12
                  Text: =Text(Today(), "dddd, dd mmmm yyyy", "id-ID")
                  Width: =240
                  Wrap: =false
```

### After builders

Once `scr_dashboard.pa.yaml` exists and compiles, change exactly one line in `App.pa.yaml` - the Dashboard entry of
`fxMenuItems`:

```yaml
          {
              TextValue: "Dashboard",
              Icon: "Home",
              NavigateScreen: scr_dashboard
          },
```

(`NavigateScreen: scr_consume` -> `NavigateScreen: scr_dashboard` in the first record only; the "Consume" entry keeps
scr_consume.) StartScreen stays `If(IsBlank(nfMe.Name), Register, 'Log In')`.

## Editor State Changes

ScreensOrder:

- Register
- Log In
- scr_dashboard
- Template
- Area
- Add_area
- scr_user
- scr_Transaction
- scr_frm_Transaction
- scr_category
- scr_frm_category
- scr_item
- scr_frm_item
- scr_find_item
- scr_History
- scr_consume

ComponentDefinitionsOrder:

- Sidebar
- TopBar
