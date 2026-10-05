# Canvas App Acceptance (T7, 2026-10-05)

Runtime evaluation: NOT RUN

Plugin root: C:\Users\Andika Rianto\.claude\plugins\cache\power-platform-skills\canvas-apps\3.0.3
Skill contract version: 3.0.3
Source revision: bb12f75 (W7) + T7 edits (_EditorState local only, this file)

Static conformance of the final YAML against `canvas-app-plan.md`. The plan still uses pre-rename control names
(W4b-W7 renamed every reused control); the column "Final control" gives the name that exists now.
Old -> new: Gallery8_12 -> galAreaL, Form5_1 -> frmAreaF, Gallery8_13 -> galUsrL, Form4 -> frmUsrL,
Button36 -> btnUsrLSave, gal_cat_list -> galCatL, frm_catFrm_category -> frmCatF, btn_cat_add -> btnCatLAdd,
btn_catFrm_submit -> btnCatFSave, Gallery8_6 -> galItmL, Form5_3 -> frmItmF, Button31_2 -> btnItmLAdd,
Button32_6 -> btnItmFSave, Gallery8_1 -> galTrxL, Gallery8_3 -> galTrxLD, Button31 -> btnTrxLAdd,
Form5 -> frmTrxF, Gallery7 -> galTrxFCart, Button15 -> btnTrxFAdd, Button32 -> btnTrxFSave, Gallery8_11 -> galCons,
dd_Area_1 -> ddConsArea, Gallery8_9 -> galFind, Gallery8_7 -> galHist, Gallery8_8 -> galHistD, DatePicker2 -> datHistDate,
ico*Edit/ico*Delete in rows -> btn*Edit/btn*Delete (ModernButton IconOnly, W5c), icoRegMail -> btnRegMail.

## Action Contract Acceptance

| Action | Final control | Event formula (final YAML) | Source / stable ID | Observer | Result |
| --- | --- | --- | --- | --- | --- |
| ACT-NAV-MENU | Sidebar icoSbItem/txtSbItem | `OnSelect: =Navigate(ThisItem.NavigateScreen, ScreenTransition.None)`; fxMenuItems Dashboard -> scr_dashboard (W7) | fxMenuItems.TextValue | `conSbItem.Fill: =If(ThisItem.TextValue = Sidebar.activemenu, ...)`; every screen's activemenu equals its menu TextValue | PASS |
| ACT-APP-START | App | `StartScreen: =If(IsBlank(nfMe.Name), Register, 'Log In')` | nfMe | txtLoginName / galRegAdmins | PASS |
| ACT-LOGIN-ENTER | btnLoginEnter | `OnSelect: =Navigate(scr_dashboard, ScreenTransition.Fade)`; DisplayMode disabled when IsBlank(nfMe.Name) | nfMe | scr_dashboard TopBar "Dashboard" | PASS |
| ACT-REG-CONTACT | btnRegMail | `OnSelect: =Launch("mailto:" & ThisItem.email)` | galRegAdmins row (`role = dis_role.administrator`) | txtRegInfo | PASS |
| ACT-DASH-VIEW | KPI texts, galDashRecent, galDashLow | `galDashRecent.Items: =FirstN(Sort(dis_trx_headers, 'Created On', SortOrder.Descending), 10)`; `galDashLow.Items: =FirstN(Sort(nfLowStock, qty, ...), 10)` | dis_item_v2S, dis_stocks, dis_trx_headers | KPI values; empty texts `IsEmpty(...)` | PASS |
| ACT-DASH-OPEN-TRX | btnDashNewTrx, btnDashSeeAll, btnDashConsume, btnDashFind | `=Clear(colTempDetails); NewForm(frmTrxF); Navigate(scr_frm_Transaction)`; `Navigate(scr_Transaction)` etc. | colTempDetails, frmTrxF | txtTrxFCartEmpty visible | PASS |
| ACT-AREA-FILTER | ddAreaLGeo/Loc/Area, inpAreaLSearch, icoAreaLReset | cascade `Reset` OnChange; reset icon resets 4 inputs; galAreaL.Items preserved filter | dis_areas | galAreaL / txtAreaLEmpty | PASS |
| ACT-AREA-ADD | btnAreaLAdd | `=Set(gblFormMode, "Add"); NewForm(frmAreaF); Navigate(Add_area, ...)` | frmAreaF | TopBar "Tambah Area" | PASS |
| ACT-AREA-EDIT | btnAreaLEdit | `=Set(gblFormMode, "Update"); EditForm(frmAreaF); Navigate(Add_area, ...)`; click selects row, `frmAreaF.Item: =galAreaL.Selected` | dis_areas.dis_area | Add_area cards | PASS |
| ACT-AREA-DELETE | btnAreaLDelete -> btnAreaLConfirmDel | `UpdateContext({locSelectedRecord: ThisItem, ...})`; `With({target: locSelectedRecord}, Remove(dis_areas, target); If(IsEmpty(Errors(dis_areas)), Set(gblReceipt, {Screen: "Area", Action: "Dihapus", Title: target.Name, ...})...))` | locSelectedRecord.dis_area | conAreaLReceipt (`gblReceipt.Screen = "Area"`); galAreaL | PASS |
| ACT-AREA-SAVE | btnAreaFSave | `=SubmitForm(frmAreaF)`; OnSuccess receipt from `frmAreaF.LastSubmit` (Name, Geounit, Lokasi, Business Line, Detail) + preserved statements | LastSubmit.dis_area | conAreaLReceipt; galAreaL | PASS |
| ACT-USER-EDIT | btnUsrLEdit | `=UpdateContext({locSelectedRecord: ThisItem, locShowUserPopUp: true, locShowDeleteConfirm_1: false}); Set(gblFormMode, "Update"); EditForm(frmUsrL)` | `frmUsrL.Item: =locSelectedRecord` | conUsrLEditor (`Visible: =locShowUserPopUp`) | PASS |
| ACT-USER-SAVE | btnUsrLSave | `=SubmitForm(frmUsrL)`; OnSuccess receipt Name/Email/Role/Area from LastSubmit, closes editor | LastSubmit.dis_user | conUsrLReceipt; galUsrL | PASS |
| ACT-USER-DELETE | btnUsrLDelete -> btnUsrLConfirmDel | `Remove(dis_users, target)` inside `With({target: locSelectedRecord}, ...)` + receipt on no error | locSelectedRecord.dis_user | conUsrLReceipt; galUsrL | PASS |
| ACT-CAT-SEARCH | inpCatLSearch | `galCatL.Items: =Search(dis_category_items, inpCatLSearch.Text, name, code, description)` | dis_category_items | galCatL / txtCatLEmpty | PASS |
| ACT-CAT-ADD | btnCatLAdd | `=NewForm(frmCatF); Navigate(scr_frm_category)` | frmCatF | TopBar "Tambah Kategori" | PASS |
| ACT-CAT-EDIT | btnCatLEdit | `=EditForm(frmCatF); Navigate(scr_frm_category)`; `frmCatF.Item: =galCatL.Selected` | dis_category_item | form cards | PASS |
| ACT-CAT-DELETE | btnCatLDelete -> btnCatLConfirmDel | `Remove(dis_category_items, target)` + receipt name/code | locSelectedRecord.dis_category_item | conCatLReceipt; galCatL | PASS |
| ACT-CAT-SAVE | btnCatFSave | `=SubmitForm(frmCatF)`; OnSuccess receipt name/Kode/Deskripsi | LastSubmit.dis_category_item | conCatLReceipt | PASS |
| ACT-ITEM-FILTER | ddItmLCat, inpItmLSearch, icoItmLReset | galItmL.Items Search(Filter(dis_item_v2S, category), name, description); reset both | dis_item_v2S | galItmL / txtItmLEmpty | PASS |
| ACT-ITEM-ADD | btnItmLAdd | `=NewForm(frmItmF); Navigate(scr_frm_item)` | frmItmF | TopBar "Tambah Item" | PASS |
| ACT-ITEM-EDIT | btnItmLEdit | `=EditForm(frmItmF); Navigate(scr_frm_item)`; `frmItmF.Item: =galItmL.Selected` | dis_item_v2 | form cards | PASS |
| ACT-ITEM-DELETE | btnItmLDelete -> btnItmLConfirmDel | `Remove(dis_item_v2S, target)` + receipt name/BPN/SPN/Kategori | locSelectedRecord.dis_item_v2 | conItmLReceipt; galItmL | PASS |
| ACT-ITEM-SAVE | btnItmFSave | `=SubmitForm(frmItmF)`; OnSuccess receipt with all 9 fields (Image as ada/tidak ada) | LastSubmit.dis_item_v2 | conItmLReceipt | PASS |
| ACT-TRX-FILTER | btnTrxLType*, inpTrxLSearch | `UpdateContext({locTrxType: ...})`; galTrxL.Items `Sort(Search(Filter(dis_trx_headers, IsBlank(locTrxType) \|\| type = locTrxType), ...), 'Created On', Descending)` | dis_trx_headers.type | galTrxL; segment Appearance Primary; txtTrxLEmpty | PASS |
| ACT-TRX-SELECT | btnTrxLOpen | click selects row (`OnSelect` closes confirm strip) | galTrxL.Selected.dis_trx_header | galTrxLD filter `header_id.dis_trx_header = galTrxL.Selected.dis_trx_header` | PASS |
| ACT-TRX-ADD | btnTrxLAdd | `=Clear(colTempDetails); NewForm(frmTrxF); Navigate(scr_frm_Transaction)` | colTempDetails | txtTrxFCartEmpty | PASS |
| ACT-TRX-EDIT | btnTrxLEdit | original Button15_2 formula (Clear + ForAll Collect from dis_trx_details of ThisItem; EditForm(frmTrxF); Navigate) | dis_trx_header | galTrxFCart | PASS |
| ACT-TRX-DELETE | btnTrxLDelete -> btnTrxLConfirmDel | `RemoveIf(dis_trx_details, header_id.dis_trx_header = target.dis_trx_header); Remove(dis_trx_headers, target)` + receipt number/type/line count | locSelectedRecord.dis_trx_header | conTrxLReceipt; galTrxL | PASS |
| ACT-TRX-CART-ADD | btnTrxFAdd | original Collect (Urutan, Id, name, description, Qty); DisplayMode disabled when no item or qty <= 0 | colTempDetails.Urutan | galTrxFCart, txtTrxFCartCount | PASS |
| ACT-TRX-CART-REMOVE | btnTrxFCartDel | `=Remove(colTempDetails, ThisItem)` | colTempDetails row | galTrxFCart, count | PASS |
| ACT-TRX-SAVE | btnTrxFSave | `=SubmitForm(frmTrxF)`; OnSuccess identical to original except Form5 -> frmTrxF and one gblReceipt statement (verified in T6) | LastSubmit.dis_trx_header | conTrxLReceipt; galFind stock | PASS |
| ACT-CONSUME-FILTER | ddConsCat/Geo/Loc/Area, inpConsSearch, icoConsReset | cascade Reset; galCons.Items Filter(dis_stocks, category, area, search) | dis_stocks | galCons / txtConsEmpty | PASS |
| ACT-CONSUME-SUBMIT | btnConsSubmit | guards (area, any qty > 0, no qty > stock or < 0) in DisplayMode and OnSelect; header Patch `{transaction_number, type: 'type (dis_trx_headers)'.Consume, area_form: ddConsArea.Selected}`; per line detail Patch + `Patch(dis_stocks, LookUp(dis_stocks, dis_stock = ItemConsume.dis_stock), {qty: oldQty - amt})` with oldQty from fresh LookUp | ItemConsume.dis_stock; newHeader | conConsReceipt + galConsReceipt (Operation/OldQty/Amount/ExpectedQty/ActualQty = updated.qty) | PASS |
| ACT-FIND-FILTER | ddFindCat/Geo/Loc/Area, inpFindSearch, icoFindReset | same pattern as Consume | dis_stocks | galFind / txtFindEmpty | PASS |
| ACT-HIST-FILTER | btnHistType*, datHistDate, icoHistDateClear, inpHistSearch | `UpdateContext({locHistType: ...})`; `icoHistDateClear.OnSelect: =Reset(datHistDate)`; galHist.Items Sort(Search(Filter(dis_trx_headers, type, 'Created On' within selected day), number, note), 'Created On', Descending) | dis_trx_headers | galHist / txtHistEmpty | PASS |
| ACT-HIST-SELECT | btnHistOpen | click selects row (`OnSelect: =false`) | galHist.Selected.dis_trx_header | txtHistDetailTitle `"Detail Item - " & galHist.Selected.transaction_number`; galHistD | PASS |

## State-Driven Surface Visibility Evidence

| Key | Final binding | Result |
| --- | --- | --- |
| area-confirm | `conAreaLConfirm.Visible: =locShowDeleteConfirm` | PASS |
| area-receipt | `conAreaLReceipt.Visible: =gblReceipt.Screen = "Area"` | PASS |
| user-confirm | `conUsrLConfirm.Visible: =locShowDeleteConfirm_1` | PASS |
| user-editor | `conUsrLEditor.Visible: =locShowUserPopUp` | PASS |
| user-receipt | `conUsrLReceipt.Visible: =gblReceipt.Screen = "User"` | PASS |
| cat-confirm / cat-receipt | `conCatLConfirm.Visible: =locShowDeleteConfirm`; `conCatLReceipt.Visible: =gblReceipt.Screen = "Category"` | PASS |
| item-confirm / item-receipt | `conItmLConfirm.Visible: =locShowDeleteConfirm`; `conItmLReceipt.Visible: =gblReceipt.Screen = "Item"` | PASS |
| trx-confirm / trx-receipt | `conTrxLConfirm.Visible: =locShowDeleteConfirm`; `conTrxLReceipt.Visible: =gblReceipt.Screen = "Transaction"` | PASS |
| cons-receipt | `conConsReceipt.Visible: =locShowConsReceipt` | PASS |

## Functional Test Matrix Results

| Scenario | Result | Note |
| --- | --- | --- |
| SCN-NAV-MENU, SCN-NAV-ROLE | PASS | Template activemenu "" -> no pill; role text `If(IsBlank(imyrole), "Belum terdaftar", Proper(Text(imyrole)))` |
| SCN-START-REGISTERED, SCN-START-UNREGISTERED, SCN-LOGIN-ENTER, SCN-REG-LIST | PASS | |
| SCN-DASH-KPI, SCN-DASH-EMPTY, SCN-DASH-OPEN-TRX | PASS | nfLowStock evaluated locally (delegation limit accepted in brief) |
| SCN-AREA-FILTER, -ADD, -EDIT, -SAVE, -DELETE, -DELETE-CANCEL | PASS | delete targets clicked row via locSelectedRecord |
| SCN-USER-EDIT, -SAVE, -DELETE | PASS | |
| SCN-CAT-SEARCH, -ADD, -EDIT, -SAVE, -DELETE | PASS | |
| SCN-ITEM-FILTER, -ADD, -EDIT, -SAVE, -DELETE | PASS | |
| SCN-TRX-FILTER, -DETAIL, -ADD, -EDIT, -DELETE, -CART, -CART-REMOVE | PASS | |
| SCN-TRX-SAVE-RECEIVE | PASS | Receive path of OnSuccess unchanged; stock observed on galFind |
| SCN-CONSUME-FILTER, -OK, -BLOCKED, -COMPOUND | PASS | oldQty from fresh LookUp, so compound old = 13 |
| SCN-FIND-FILTER | PASS | |
| SCN-HIST-DATE, SCN-HIST-DETAIL | PASS | new in W7 |

## Viewport Containment Evidence

Every screen in the Dispatch table has one top-level `con<P>Root` GroupContainer AutoLayout with
`Width: =Parent.Width` / `Height: =Parent.Height` (checked in W2-W7 self-QA; compile accepts all 16 screens).

## Known open items (not static defects)

- Studio binding symptom (T5c): Fill of gallery rows and "Depends on" of form dropdowns may need a manual re-type
  in Studio after compile. New in T7: conHistRow, conHistDRow.
- Runtime tests (Receive 3 / Consume 2 / qty > stock) and File > Save are user steps.
