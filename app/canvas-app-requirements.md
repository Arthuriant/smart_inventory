# Canvas App Original Request Contract

Contract version: 1
Target device: Fixed desktop

## Original Request

User (Indonesian): "oke, tolong update semua halaman nya menjadi lebih modern dan optimal"
("ok, please update all of its pages to be more modern and optimal")

Approved clarifications (AskUserQuestion answers + approved Canvas Edit Plan):
1. Dashboard: "Buat Dashboard baru" — create a new Dashboard screen with KPI cards (total items,
   items whose stock is below min_qty, transactions today), a recent-transactions list and a
   low-stock list. The Sidebar "Dashboard" menu entry navigates to it, and it becomes the
   destination after Log In.
2. Scope: "Visual + optimasi + bug fix" — modern visuals on every screen, performance
   optimisation, and fixing existing bugs (5 compile errors, Delete acting on the wrong record,
   missing delete confirmations, hard-coded sidebar role). Existing save / stock-update flows
   must be preserved (only presentation changes) except for explicit bug fixes listed below.
3. Device: "Desktop/laptop saja" — fixed desktop layout, sidebar always visible, wide tables.

Approved plan summary:
- Keep SLB navy RGBA(0,18,107,1) as the brand colour; light neutral page background, white
  rounded cards with subtle shadow, consistent type scale, consistent primary / secondary /
  danger buttons, coloured badges for transaction Type and item Status.
- Sidebar + TopBar components restyled; sidebar shows active menu highlight and the real role
  of the signed-in user; widths follow the screen (no hard-coded 975 / App.Width-150).
- List screens (Area, Category, Item, User, Transaction, History, Find Item): toolbar
  (search / filters / Add) over a card table with zebra/hover rows, icon actions, empty state,
  and a confirm dialog for every Delete that deletes the clicked row.
- Form screens (Add_area, scr_frm_category, scr_frm_item, scr_frm_Transaction, User popup):
  form inside a centred card, 2-column grid, Save/Cancel at the bottom; save logic unchanged.
- Log In and Register: modern welcome screens; Log In navigation targets fixed.
- App: one named formula for the current user record replacing the 7 duplicated
  LookUp(dis_users, email = User().Email) calls; keep legacy variables (imyrole, imyid,
  imyarea, iroleview, imyemail) populated for compatibility; fix elv_assigned_area references.

Existing compile errors to fix (baseline compile):
- App.OnStart: 'elv_assigned_area' isn't recognized (real column display name is Assigned_area).
- Log In Button1.OnSelect: 'HomeAdmin' isn't recognized; ButtonUser.OnSelect: 'HomeUser' isn't recognized.
- Register Subtitle2.Text: 'elv_assigned_area' isn't recognized.
- Warnings: scr_user Button30_4 / Button33_3 set locSelectedRecord: Blank() (no type).

Known logic bugs to fix:
- Area: Delete button sets locSelectedRecord: Defaults(Users) and the confirm removes
  Gallery8_12.Selected instead of the clicked row.
- scr_user: Update/Delete set locSelectedRecord: Blank(); delete removes Gallery8_13.Selected.
- scr_category, scr_item: Delete removes immediately without confirmation.
- scr_consume: Consume header Patch writes only transaction_number although the comment says
  "Otomatis tipe Consume" — header must also get type = Consume and area_form = selected area;
  consuming more than the available stock must be blocked.
- Sidebar: fxMenuItems "Dashboard" navigates to scr_consume; profile role text is hard-coded "User".

## Capability Inventory

| Requirement key | Original request clause | Capability family | Required outcome / scope | Required action(s) | Scenario(s) | Specialized contract mappings |
| --------------- | ----------------------- | ----------------- | ------------------------ | ------------------ | ----------- | ----------------------------- |
| REQ-VISUAL | "update semua halaman nya menjadi lebih modern" | App shell and navigation | Every screen (Log In, Register, Template, Area, Add_area, scr_user, scr_Transaction, scr_frm_Transaction, scr_category, scr_frm_category, scr_item, scr_frm_item, scr_find_item, scr_History, scr_consume, new Dashboard) uses the shared modern visual contract: brand navy, neutral background, white rounded cards, consistent type scale and buttons; layout fills the screen with no hard-coded content width | ACT-NAV-MENU | SCN-NAV-MENU | Viewport containment for every screen (Fixed desktop) |
| REQ-SHELL | Sidebar/TopBar modern + correct (approved plan) | App shell and navigation | Sidebar lists fxMenuItems, highlights the active entry, navigates on click, shows signed-in user's name and real role; TopBar shows page title | ACT-NAV-MENU | SCN-NAV-MENU, SCN-NAV-ROLE | N/A |
| REQ-PERF-USER | "optimal" — single current-user lookup | Security, persistence, and resilience | App.Formulas defines one named formula for the current dis_users record; OnStart / StartScreen / Log In read it instead of repeating LookUp; legacy variables imyrole, imyid, imyarea, iroleview, imyemail still populated; elv_assigned_area replaced with Assigned_area | ACT-APP-START | SCN-START-REGISTERED, SCN-START-UNREGISTERED | N/A |
| REQ-DASH | Dashboard baru (clarification 1) | Analytics and visualization | New Dashboard screen: KPI total items (dis_item_v2S), KPI low-stock count (dis_stocks rows whose qty < their item's min_qty), KPI transactions created today (dis_trx_headers), recent transactions list (latest headers, number/date/type/area), low-stock list (item name, area, qty, min qty); quick links to Transaction and Find Item | ACT-DASH-VIEW, ACT-DASH-OPEN-TRX | SCN-DASH-KPI, SCN-DASH-EMPTY | N/A |
| REQ-LOGIN | Log In navigation fixed (approved plan) | App shell and navigation | Log In shows welcome + role; the single "Masuk"/HOME action navigates to the Dashboard for any registered role (no HomeAdmin/HomeUser) | ACT-LOGIN-ENTER | SCN-LOGIN-ENTER | N/A |
| REQ-REGISTER | Register fixed (approved plan) | App shell and navigation | Register lists administrators (name, email, assigned area via Assigned_area) and each row offers a mail action (Launch "mailto:" & email) | ACT-REG-CONTACT | SCN-REG-LIST | N/A |
| REQ-AREA | Area list modern + delete bug fix | Data lifecycle; Data exploration | Area list with Geounit→Location→Area cascading filters and search; Add → Add_area (new); row Edit → Add_area (edit) prefilled; row Delete → confirm dialog → removes the clicked dis_areas row | ACT-AREA-FILTER, ACT-AREA-ADD, ACT-AREA-EDIT, ACT-AREA-DELETE | SCN-AREA-FILTER, SCN-AREA-DELETE, SCN-AREA-DELETE-CANCEL | N/A |
| REQ-AREA-FORM | Add_area form modern, logic preserved | Data lifecycle | Form5_1 (dis_areas) fields Name, Geounit, Location, Business Line, Detail; Save submits; Back resets and returns | ACT-AREA-SAVE | SCN-AREA-SAVE | N/A |
| REQ-USER | User list modern + bug fix | Data lifecycle; Role-scoped | User list (name, email, role badge, assigned area); row Edit opens the popup form prefilled with that row; Save submits Form4; row Delete → confirm → removes the clicked dis_users row | ACT-USER-EDIT, ACT-USER-SAVE, ACT-USER-DELETE | SCN-USER-EDIT, SCN-USER-DELETE | N/A |
| REQ-CAT | Category list modern + confirm delete | Data lifecycle; Data exploration | Search over name/code/description; Add → form new; row Edit → form edit; row Delete → confirm → removes clicked row | ACT-CAT-SEARCH, ACT-CAT-ADD, ACT-CAT-EDIT, ACT-CAT-DELETE | SCN-CAT-SEARCH, SCN-CAT-DELETE | N/A |
| REQ-CAT-FORM | scr_frm_category modern, logic preserved | Data lifecycle | frm_catFrm_category fields name, code, description; Submit; Back | ACT-CAT-SAVE | SCN-CAT-SAVE | N/A |
| REQ-ITEM | Item list modern + confirm delete | Data lifecycle; Data exploration | Category filter + search; columns Name, BPN, SPN, Category, Min Qty, UoM, Status badge; Add / Edit / Delete-with-confirm | ACT-ITEM-FILTER, ACT-ITEM-ADD, ACT-ITEM-EDIT, ACT-ITEM-DELETE | SCN-ITEM-FILTER, SCN-ITEM-DELETE | N/A |
| REQ-ITEM-FORM | scr_frm_item modern, logic preserved | Data lifecycle; Files and media | Form5_3 fields name, min_qty, part_number (BPN), client_number (SPN), uom, status, category, description, image upload; Submit; Back | ACT-ITEM-SAVE | SCN-ITEM-SAVE | N/A |
| REQ-TRX | Transaction list modern + confirm delete | Data lifecycle; Data exploration; Relationships | Type filter + search; header list; selecting a header shows its detail lines (category filter); Add → new form with empty cart; Edit → loads detail lines into colTempDetails then edit form; Delete → confirm → RemoveIf details then Remove header (existing cascade) | ACT-TRX-FILTER, ACT-TRX-SELECT, ACT-TRX-ADD, ACT-TRX-EDIT, ACT-TRX-DELETE | SCN-TRX-FILTER, SCN-TRX-DETAIL, SCN-TRX-DELETE | N/A |
| REQ-TRX-FORM | scr_frm_Transaction modern, logic preserved | Data lifecycle; Workflow | Header fields (auto number, type, area from/to visibility by type, note); cart: pick item + qty → Add Item to colTempDetails, remove line; Submit runs the existing OnSuccess (detail rewrite + stock Receive/Consume/Transfer update) unchanged | ACT-TRX-CART-ADD, ACT-TRX-CART-REMOVE, ACT-TRX-SAVE | SCN-TRX-CART, SCN-TRX-SAVE-RECEIVE | N/A |
| REQ-CONSUME | scr_consume modern + bug fix | Workflow; Data exploration | Category/Geounit/Location/Area filters + search over dis_stocks; per-row qty input; Consume button creates header (number, type Consume, area_form) + details and decreases stock; blocked when no area, no qty, or qty > stock | ACT-CONSUME-FILTER, ACT-CONSUME-SUBMIT | SCN-CONSUME-OK, SCN-CONSUME-BLOCKED | N/A |
| REQ-FIND | scr_find_item modern | Data exploration | Category/Geounit/Location/Area filters + search over dis_stocks; columns Name, BPN, SPN, Category, Stock (low-stock highlight), UoM, Location | ACT-FIND-FILTER | SCN-FIND-FILTER | N/A |
| REQ-HISTORY | scr_History modern | Data exploration; Time | Type filter, date filter (with clear), search; header list; detail lines of selected header with category filter | ACT-HIST-FILTER, ACT-HIST-SELECT | SCN-HIST-DATE, SCN-HIST-DETAIL | N/A |
| REQ-TEMPLATE | Template screen updated to new shell | App shell and navigation | Template shows the new shell (sidebar + topbar + empty body card) for future screens | ACT-NAV-MENU | SCN-NAV-MENU | N/A |
