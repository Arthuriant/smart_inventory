// Office Script "SmartInventoryFillLists", run by the flow "Smart Inventory - Bulk Import Template".
// Fills the list tables on the Lists sheet of the template copy in one go (the flow used to add one row
// per call, which took minutes). Paste this whole file into Excel Online > Automate > New Script.
// listsJson: {"areas":[{"a":""}], "cats":[{"c":"","n":""}], "racks":[{"r":"","a":""}], "catalog":[{"k":""}]}

interface Area { a: string; }
interface Cat { c: string; n: string; }
interface Rack { r: string; a: string; }
interface Chunk { k: string; }
interface Lists { areas?: Area[]; cats?: Cat[]; racks?: Rack[]; catalog?: Chunk[]; }

function main(workbook: ExcelScript.Workbook, listsJson: string): string {
  const d: Lists = JSON.parse(listsJson) as Lists;
  const areas: string[] = (d.areas || []).map((x) => String(x.a || "")).filter((a) => a !== "");
  const cats: string[][] = (d.cats || []).map((x) => [String(x.c || ""), String(x.n || "")]);
  // the Rack dropdown needs the racks of one area in one block, in the order of the area list
  const racks: string[][] = [];
  areas.forEach((a) => {
    (d.racks || []).forEach((r) => {
      if (r.a === a && r.r) racks.push([String(r.r), a]);
    });
  });
  const catalog: string[][] = (d.catalog || []).map((x) => [String(x.k || "")]);

  add(workbook, "tblArea", areas.map((a) => [a]));
  add(workbook, "tblCategory", cats);
  add(workbook, "tblRack", racks);
  add(workbook, "tblCatalog", catalog);
  return `areas ${areas.length}, categories ${cats.length}, racks ${racks.length}, catalog rows ${catalog.length}`;
}

// appends the rows below the table's hidden empty first row (one call per table)
function add(workbook: ExcelScript.Workbook, name: string, rows: string[][]) {
  if (rows.length === 0) return;
  const t = workbook.getTable(name);
  if (!t) throw new Error(`Table ${name} not found in the template`);
  t.addRows(-1, rows);
}
