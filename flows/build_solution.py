"""Builds SmartInventoryFlows_<version>.zip: an unmanaged Dataverse solution with two cloud flows.

Flow "Smart Inventory - Bulk Import Read Excel" (Power Apps V2 trigger):
  1. receives the uploaded .xlsx from the app as a data URI text (input "fileContent"; the app builds it with
     JSON(<attachment>, JSONFormat.IncludeBinaryData), because a standalone attachments control has no Blob type),
  2. saves it in the flow owner's OneDrive under /Apps/SmartInventory/BulkImport,
  3. reads the Excel table "tblImport" (sheet Import of the template),
  4. turns the rows into tab-separated text, the same format as a paste from Excel,
  5. deletes the temporary file and returns the text to the app ("rows").
The app puts that text into inpBlkPaste and runs the existing Check, so all rules stay in the app.

Flow "Smart Inventory - Bulk Import Template" (Power Apps V2 trigger):
  1. receives the current lists of the user's business line as JSON text (input "listsJson":
     {areas:[{a}], cats:[{c,n}], racks:[{r,a}]}); the racks sent by the app are ignored since v1.2.0.0,
  2. reads the active racks from Dataverse (dis_racks) and keeps those whose area is in the app's area list,
  3. copies the master template /Apps/SmartInventory/Bulk_Import_Template_Master.xlsx (see build_template.py),
  4. fills its tables tblArea, tblCategory and tblRack (sheet Lists) one row at a time; racks are written
     area by area, because the Rack dropdown in Excel takes one block per area,
  5. creates an organization view link and returns it to the app ("url"), which downloads it,
  6. deletes the copy after 15 minutes.

Usage: python build_solution.py <output folder>
"""
import json
import os
import sys
import zipfile

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
VERSION = "1.2.0.0"
SOLUTION = "SmartInventoryFlows"
FLOW_NAME = "Smart Inventory - Bulk Import Read Excel"
# fixed ids so a rebuilt zip updates the same flow on re-import
FLOW_ID = "6b1d2f3a-4c5e-4f60-9a71-8b2c3d4e5f60"
CR_ONEDRIVE = "cr8a3_sharedonedriveforbusiness_sinv"
CR_EXCEL = "cr8a3_sharedexcelonlinebusiness_sinv"
CR_DATAVERSE = "cr8a3_sharedcommondataserviceforapps_sinv"
# OneDrive (flow owner ARianto2) drive id for the Excel actions; Create file does not return it.
# Another owner: pick Location/Document Library once in each Excel action (README) or change this value.
DRIVE_ID = "b!Pu5E4zGfBEG3nzDH_B0Xe6FOFTIKA_RFl_1YdZpKsqbratFKyU_NSI1tsjkc69Jm"
FLOW2_NAME = "Smart Inventory - Bulk Import Template"
FLOW2_ID = "7c2e3f4b-5d6f-4071-8b82-9c3d4e5f6071"
MASTER = "/Apps/SmartInventory/Bulk_Import_Template_Master.xlsx"
FOLDER = "/Apps/SmartInventory/BulkImport"
TABLE = "tblImport"
COLUMNS = ["Area", "Item name", "BPN", "SPN", "Category", "UOM", "Qty", "Min in area", "Rack"]

TAB = "decodeUriComponent('%09')"
NL = "decodeUriComponent('%0A')"
line_expr = "concat(" + f", {TAB}, ".join(f"coalesce(string(item()?['{c}']), '')" for c in COLUMNS) + ")"

# file content from the app: data URI or plain base64
FILE_BODY = ("@if(startsWith(triggerBody()?['text'], 'data:'), dataUriToBinary(triggerBody()?['text']), "
             "base64ToBinary(triggerBody()?['text']))")
RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "rows": {"title": "rows", "x-ms-dynamically-added": True, "type": "string"},
        "error": {"title": "error", "x-ms-dynamically-added": True, "type": "string"},
    },
}
# the real reason (OneDrive or Excel) is passed to the app
ERROR_TEXT = ("@{concat('The file could not be read (', coalesce(outputs('List_rows_present_in_a_table')?['body']?['error']?['message'], "
              "outputs('Create_file')?['body']?['message'], outputs('Create_file')?['body']?['error']?['message'], 'see the flow run'), "
              "'). Use the Bulk Import template and keep the table tblImport on the Import sheet.')}")

definition = {
    "$schema": "https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#",
    "contentVersion": "1.0.0.0",
    "parameters": {
        "$connections": {"defaultValue": {}, "type": "Object"},
        "$authentication": {"defaultValue": {}, "type": "SecureObject"},
    },
    "triggers": {
        "manual": {
            "type": "Request",
            "kind": "PowerAppV2",
            "inputs": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "text": {
                            "title": "fileContent",
                            "type": "string",
                            "x-ms-dynamically-added": True,
                            "description": "The filled-in Bulk Import template (.xlsx) as a data URI",
                            "x-ms-content-hint": "TEXT",
                        }
                    },
                    "required": ["text"],
                }
            },
        }
    },
    "actions": {
        # what the app sent; a data URI ("data:...;base64,...") or plain base64 is accepted
        "Check_file_content": {
            "runAfter": {},
            "type": "If",
            "expression": {"greater": ["@length(coalesce(triggerBody()?['text'], ''))", 100]},
            "actions": {
                "Create_file": {
                    "runAfter": {},
                    "type": "OpenApiConnection",
                    "inputs": {
                        "host": {
                            "connectionName": "shared_onedriveforbusiness",
                            "operationId": "CreateFile",
                            "apiId": "/providers/Microsoft.PowerApps/apis/shared_onedriveforbusiness",
                        },
                        "parameters": {
                            "folderPath": FOLDER,
                            "name": "@{guid()}.xlsx",
                            "body": FILE_BODY,
                        },
                        "authentication": "@parameters('$authentication')",
                    },
                    "runtimeConfiguration": {"contentTransfer": {"transferMode": "Chunked"}},
                },
                "List_rows_present_in_a_table": {
                    "runAfter": {"Create_file": ["Succeeded"]},
                    "type": "OpenApiConnection",
                    "inputs": {
                        "host": {
                            "connectionName": "shared_excelonlinebusiness",
                            "operationId": "GetItems",
                            "apiId": "/providers/Microsoft.PowerApps/apis/shared_excelonlinebusiness",
                        },
                        "parameters": {
                            "source": "me",
                            "drive": DRIVE_ID,
                            "file": "@outputs('Create_file')?['body/Id']",
                            "table": TABLE,
                        },
                        "authentication": "@parameters('$authentication')",
                    },
                    "runtimeConfiguration": {"paginationPolicy": {"minimumItemCount": 5000}},
                    "retryPolicy": {"type": "fixed", "count": 4, "interval": "PT5S"},
                },
                "Select_lines": {
                    "runAfter": {"List_rows_present_in_a_table": ["Succeeded"]},
                    "type": "Select",
                    "inputs": {
                        "from": "@outputs('List_rows_present_in_a_table')?['body/value']",
                        "select": "@" + line_expr,
                    },
                },
                "Respond_to_app_rows": {
                    "runAfter": {"Select_lines": ["Succeeded"]},
                    "type": "Response",
                    "kind": "PowerApp",
                    "inputs": {
                        "statusCode": 200,
                        "body": {"rows": f"@{{join(body('Select_lines'), {NL})}}", "error": ""},
                        "schema": RESPONSE_SCHEMA,
                    },
                },
                "Respond_to_app_error": {
                    # Create file failed (List rows skipped) or the table could not be read
                    "runAfter": {"List_rows_present_in_a_table": ["Failed", "TimedOut", "Skipped"]},
                    "type": "Response",
                    "kind": "PowerApp",
                    "inputs": {
                        "statusCode": 200,
                        "body": {"rows": "", "error": ERROR_TEXT},
                        "schema": RESPONSE_SCHEMA,
                    },
                },
                "Delete_temp_file": {
                    # after the app got its answer (exactly one of the two responses runs, the other is skipped)
                    "runAfter": {
                        "Respond_to_app_rows": ["Succeeded", "Failed", "Skipped"],
                        "Respond_to_app_error": ["Succeeded", "Failed", "Skipped"],
                    },
                    "type": "OpenApiConnection",
                    "inputs": {
                        "host": {
                            "connectionName": "shared_onedriveforbusiness",
                            "operationId": "DeleteFile",
                            "apiId": "/providers/Microsoft.PowerApps/apis/shared_onedriveforbusiness",
                        },
                        "parameters": {"id": "@outputs('Create_file')?['body/Id']"},
                        "authentication": "@parameters('$authentication')",
                    },
                },
            },
            "else": {
                "actions": {
                    "Respond_to_app_no_file": {
                        "runAfter": {},
                        "type": "Response",
                        "kind": "PowerApp",
                        "inputs": {
                            "statusCode": 200,
                            "body": {
                                "rows": "",
                                "error": "@{concat('The app sent no file content. Received: ''', take(coalesce(triggerBody()?['text'], '(nothing)'), 80), '''')}",
                            },
                            "schema": RESPONSE_SCHEMA,
                        },
                    }
                }
            },
        },
    },
    "outputs": {},
}


# ---------- flow 2: Bulk Import Template ----------
def excel_add(table, item):
    return {
        "type": "OpenApiConnection",
        "inputs": {
            "host": {
                "connectionName": "shared_excelonlinebusiness",
                "operationId": "AddRowV2",
                "apiId": "/providers/Microsoft.PowerApps/apis/shared_excelonlinebusiness",
            },
            "parameters": {
                "source": "me",
                "drive": DRIVE_ID,
                "file": "@outputs('Create_copy')?['body/Id']",
                "table": table,
                "item": item,
            },
            "authentication": "@parameters('$authentication')",
        },
        "retryPolicy": {"type": "fixed", "count": 4, "interval": "PT5S"},
    }


def loop(after, items_expr, inner_name, inner):
    # one row at a time, in the order the app sent
    return {
        "runAfter": after,
        "type": "Foreach",
        "foreach": items_expr,
        "actions": {inner_name: inner},
        "runtimeConfiguration": {"concurrency": {"repetitions": 1}},
    }


ITEM_SCHEMA = lambda props: {"type": "array", "items": {"type": "object", "properties": {p: {"type": "string"} for p in props}}}
URL_SCHEMA = {
    "type": "object",
    "properties": {
        "url": {"title": "url", "x-ms-dynamically-added": True, "type": "string"},
        "error": {"title": "error", "x-ms-dynamically-added": True, "type": "string"},
    },
}

definition2 = {
    "$schema": definition["$schema"],
    "contentVersion": "1.0.0.0",
    "parameters": definition["parameters"],
    "triggers": {
        "manual": {
            "type": "Request",
            "kind": "PowerAppV2",
            "inputs": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "text": {
                            "title": "listsJson",
                            "type": "string",
                            "x-ms-dynamically-added": True,
                            "description": "Current areas, categories and racks of the user's business line (JSON)",
                            "x-ms-content-hint": "TEXT",
                        }
                    },
                    "required": ["text"],
                }
            },
        }
    },
    "actions": {
        "Parse_lists": {
            "runAfter": {},
            "type": "ParseJson",
            "inputs": {
                "content": "@triggerBody()?['text']",
                "schema": {
                    "type": "object",
                    "properties": {
                        "areas": ITEM_SCHEMA(["a"]),
                        "cats": ITEM_SCHEMA(["c", "n"]),
                        "racks": ITEM_SCHEMA(["r", "a"]),
                    },
                },
            },
        },
        "Get_master": {
            "runAfter": {"Parse_lists": ["Succeeded"]},
            "type": "OpenApiConnection",
            "inputs": {
                "host": {
                    "connectionName": "shared_onedriveforbusiness",
                    "operationId": "GetFileContentByPath",
                    "apiId": "/providers/Microsoft.PowerApps/apis/shared_onedriveforbusiness",
                },
                "parameters": {"path": MASTER, "inferContentType": False},
                "authentication": "@parameters('$authentication')",
            },
        },
        "Create_copy": {
            "runAfter": {"Get_master": ["Succeeded"]},
            "type": "OpenApiConnection",
            "inputs": {
                "host": {
                    "connectionName": "shared_onedriveforbusiness",
                    "operationId": "CreateFile",
                    "apiId": "/providers/Microsoft.PowerApps/apis/shared_onedriveforbusiness",
                },
                "parameters": {
                    "folderPath": FOLDER,
                    "name": "@{concat('Bulk_Import_Template_', formatDateTime(utcNow(), 'yyyyMMdd_HHmmss'), '_', take(guid(), 4), '.xlsx')}",
                    "body": "@body('Get_master')",
                },
                "authentication": "@parameters('$authentication')",
            },
            "runtimeConfiguration": {"contentTransfer": {"transferMode": "Chunked"}},
        },
    },
    "outputs": {},
}
acts = definition2["actions"]
acts["Add_areas"] = loop({"Create_copy": ["Succeeded"]}, "@body('Parse_lists')?['areas']",
                         "Add_area_row", excel_add("tblArea", {"Area": "@items('Add_areas')?['a']"}))
acts["Add_categories"] = loop({"Add_areas": ["Succeeded"]}, "@body('Parse_lists')?['cats']",
                              "Add_category_row", excel_add("tblCategory",
                                                            {"Category code": "@items('Add_categories')?['c']",
                                                             "Category name": "@items('Add_categories')?['n']"}))
# racks come from Dataverse, not from the app (the app's list arrived empty); the formatted value of the
# area lookup is the area name, the same text the app sends in "areas"
AREA_NAME = "_cr8a3_area_value@OData.Community.Display.V1.FormattedValue"
acts["List_racks"] = {
    "runAfter": {"Parse_lists": ["Succeeded"]},
    "type": "OpenApiConnection",
    "inputs": {
        "host": {
            "connectionName": "shared_commondataserviceforapps",
            "operationId": "ListRecords",
            "apiId": "/providers/Microsoft.PowerApps/apis/shared_commondataserviceforapps",
        },
        "parameters": {
            "entityName": "cr8a3_dis_racks",
            "$select": "cr8a3_name,_cr8a3_area_value",
            "$filter": "statecode eq 0",
            "$orderby": "cr8a3_name asc",
        },
        "authentication": "@parameters('$authentication')",
    },
}
acts["Add_racks"] = {
    # one block per area, in the order of the app's area list
    "runAfter": {"Add_categories": ["Succeeded"], "List_racks": ["Succeeded"]},
    "type": "Foreach",
    "foreach": "@body('Parse_lists')?['areas']",
    "actions": {
        "Racks_in_area": {
            "runAfter": {},
            "type": "Query",
            "inputs": {
                "from": "@coalesce(outputs('List_racks')?['body/value'], json('[]'))",
                "where": f"@equals(item()?['{AREA_NAME}'], items('Add_racks')?['a'])",
            },
        },
        "Add_area_racks": {
            "runAfter": {"Racks_in_area": ["Succeeded"]},
            "type": "Foreach",
            "foreach": "@body('Racks_in_area')",
            "actions": {
                "Add_rack_row": excel_add("tblRack", {"Rack": "@items('Add_area_racks')?['cr8a3_name']",
                                                      "Rack is in area": "@items('Add_racks')?['a']"}),
            },
            "runtimeConfiguration": {"concurrency": {"repetitions": 1}},
        },
    },
    "runtimeConfiguration": {"concurrency": {"repetitions": 1}},
}
acts["Create_link"] = {
    "runAfter": {"Add_racks": ["Succeeded"]},
    "type": "OpenApiConnection",
    "inputs": {
        "host": {
            "connectionName": "shared_onedriveforbusiness",
            "operationId": "CreateShareLinkV2",
            "apiId": "/providers/Microsoft.PowerApps/apis/shared_onedriveforbusiness",
        },
        "parameters": {"id": "@outputs('Create_copy')?['body/Id']", "type": "View", "scope": "Organization"},
        "authentication": "@parameters('$authentication')",
    },
}
acts["Respond_to_app_url"] = {
    "runAfter": {"Create_link": ["Succeeded"]},
    "type": "Response",
    "kind": "PowerApp",
    "inputs": {"statusCode": 200, "body": {"url": "@{outputs('Create_link')?['body/WebUrl']}", "error": ""},
               "schema": URL_SCHEMA},
}
acts["Respond_to_app_error"] = {
    # any earlier step failed (the later ones are skipped)
    "runAfter": {"Create_link": ["Failed", "Skipped", "TimedOut"]},
    "type": "Response",
    "kind": "PowerApp",
    "inputs": {
        "statusCode": 200,
        "body": {
            "url": "",
            "error": ("@{concat('The template could not be created (', coalesce(outputs('Get_master')?['body']?['message'], "
                      "outputs('Create_copy')?['body']?['message'], outputs('List_racks')?['body']?['error']?['message'], "
                      "outputs('Create_link')?['body']?['message'], 'see the flow run'), "
                      "'). Check that ', '" + MASTER + "', ' exists in the OneDrive of the flow owner.')}"),
        },
        "schema": URL_SCHEMA,
    },
}
acts["Wait_15_minutes"] = {
    "runAfter": {"Respond_to_app_url": ["Succeeded", "Failed", "Skipped"],
                 "Respond_to_app_error": ["Succeeded", "Failed", "Skipped"]},
    "type": "Wait",
    "inputs": {"interval": {"count": 15, "unit": "Minute"}},
}
acts["Delete_copy"] = {
    "runAfter": {"Wait_15_minutes": ["Succeeded"]},
    "type": "OpenApiConnection",
    "inputs": {
        "host": {
            "connectionName": "shared_onedriveforbusiness",
            "operationId": "DeleteFile",
            "apiId": "/providers/Microsoft.PowerApps/apis/shared_onedriveforbusiness",
        },
        "parameters": {"id": "@outputs('Create_copy')?['body/Id']"},
        "authentication": "@parameters('$authentication')",
    },
}


def wrap(defn):
    return {
    "properties": {
        "connectionReferences": {
            "shared_onedriveforbusiness": {
                "runtimeSource": "embedded",
                "connection": {"connectionReferenceLogicalName": CR_ONEDRIVE},
                "api": {"name": "shared_onedriveforbusiness"},
            },
            "shared_excelonlinebusiness": {
                "runtimeSource": "embedded",
                "connection": {"connectionReferenceLogicalName": CR_EXCEL},
                "api": {"name": "shared_excelonlinebusiness"},
            },
            "shared_commondataserviceforapps": {
                "runtimeSource": "embedded",
                "connection": {"connectionReferenceLogicalName": CR_DATAVERSE},
                "api": {"name": "shared_commondataserviceforapps"},
            },
        },
        "definition": defn,
        "templateName": "",
    },
    "schemaVersion": "1.0.0.0",
    }


FLOWS = [
    (FLOW_ID, FLOW_NAME, f"Workflows/SmartInventory-BulkImportReadExcel-{FLOW_ID.upper()}.json", definition),
    (FLOW2_ID, FLOW2_NAME, f"Workflows/SmartInventory-BulkImportTemplate-{FLOW2_ID.upper()}.json", definition2),
]


solution_xml = f"""<?xml version="1.0" encoding="utf-8"?>
<ImportExportXml version="9.2.26094.160" SolutionPackageVersion="9.2" languagecode="1033" generatedBy="CrmLive" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" OrganizationVersion="9.2.26094.160" OrganizationSchemaType="Standard">
  <SolutionManifest>
    <UniqueName>{SOLUTION}</UniqueName>
    <LocalizedNames>
      <LocalizedName description="Smart Inventory Flows" languagecode="1033" />
    </LocalizedNames>
    <Descriptions>
      <Description description="Cloud flows used by the Smart Inventory canvas app (Bulk Import: read an uploaded Excel template)." languagecode="1033" />
    </Descriptions>
    <Version>{VERSION}</Version>
    <Managed>0</Managed>
    <Publisher>
      <UniqueName>Cra708b</UniqueName>
      <LocalizedNames>
        <LocalizedName description="CDS Default Publisher" languagecode="1033" />
      </LocalizedNames>
      <Descriptions />
      <EMailAddress xsi:nil="true"></EMailAddress>
      <SupportingWebsiteUrl xsi:nil="true"></SupportingWebsiteUrl>
      <CustomizationPrefix>cr8a3</CustomizationPrefix>
      <CustomizationOptionValuePrefix>54206</CustomizationOptionValuePrefix>
      <Addresses>
        <Address>
          <AddressNumber>1</AddressNumber>
          <AddressTypeCode>1</AddressTypeCode>
          <City xsi:nil="true"></City>
          <County xsi:nil="true"></County>
          <Country xsi:nil="true"></Country>
          <Fax xsi:nil="true"></Fax>
          <FreightTermsCode xsi:nil="true"></FreightTermsCode>
          <ImportSequenceNumber xsi:nil="true"></ImportSequenceNumber>
          <Latitude xsi:nil="true"></Latitude>
          <Line1 xsi:nil="true"></Line1>
          <Line2 xsi:nil="true"></Line2>
          <Line3 xsi:nil="true"></Line3>
          <Longitude xsi:nil="true"></Longitude>
          <Name xsi:nil="true"></Name>
          <PostalCode xsi:nil="true"></PostalCode>
          <PostOfficeBox xsi:nil="true"></PostOfficeBox>
          <PrimaryContactName xsi:nil="true"></PrimaryContactName>
          <ShippingMethodCode>1</ShippingMethodCode>
          <StateOrProvince xsi:nil="true"></StateOrProvince>
          <Telephone1 xsi:nil="true"></Telephone1>
          <Telephone2 xsi:nil="true"></Telephone2>
          <Telephone3 xsi:nil="true"></Telephone3>
          <TimeZoneRuleVersionNumber xsi:nil="true"></TimeZoneRuleVersionNumber>
          <UPSZone xsi:nil="true"></UPSZone>
          <UTCOffset xsi:nil="true"></UTCOffset>
          <UTCConversionTimeZoneCode xsi:nil="true"></UTCConversionTimeZoneCode>
        </Address>
        <Address>
          <AddressNumber>2</AddressNumber>
          <AddressTypeCode>1</AddressTypeCode>
          <City xsi:nil="true"></City>
          <County xsi:nil="true"></County>
          <Country xsi:nil="true"></Country>
          <Fax xsi:nil="true"></Fax>
          <FreightTermsCode xsi:nil="true"></FreightTermsCode>
          <ImportSequenceNumber xsi:nil="true"></ImportSequenceNumber>
          <Latitude xsi:nil="true"></Latitude>
          <Line1 xsi:nil="true"></Line1>
          <Line2 xsi:nil="true"></Line2>
          <Line3 xsi:nil="true"></Line3>
          <Longitude xsi:nil="true"></Longitude>
          <Name xsi:nil="true"></Name>
          <PostalCode xsi:nil="true"></PostalCode>
          <PostOfficeBox xsi:nil="true"></PostOfficeBox>
          <PrimaryContactName xsi:nil="true"></PrimaryContactName>
          <ShippingMethodCode>1</ShippingMethodCode>
          <StateOrProvince xsi:nil="true"></StateOrProvince>
          <Telephone1 xsi:nil="true"></Telephone1>
          <Telephone2 xsi:nil="true"></Telephone2>
          <Telephone3 xsi:nil="true"></Telephone3>
          <TimeZoneRuleVersionNumber xsi:nil="true"></TimeZoneRuleVersionNumber>
          <UPSZone xsi:nil="true"></UPSZone>
          <UTCOffset xsi:nil="true"></UTCOffset>
          <UTCConversionTimeZoneCode xsi:nil="true"></UTCConversionTimeZoneCode>
        </Address>
      </Addresses>
    </Publisher>
    <RootComponents>
      <RootComponent type="29" id="{{{FLOW_ID}}}" behavior="0" />
      <RootComponent type="29" id="{{{FLOW2_ID}}}" behavior="0" />
    </RootComponents>
    <MissingDependencies />
  </SolutionManifest>
</ImportExportXml>
"""

WORKFLOWS_XML = "".join(
    f"""    <Workflow WorkflowId="{{{fid}}}" Name="{fname}">
      <JsonFileName>/{ffile}</JsonFileName>
      <Type>1</Type>
      <Subprocess>0</Subprocess>
      <Category>5</Category>
      <Mode>0</Mode>
      <Scope>4</Scope>
      <OnDemand>0</OnDemand>
      <TriggerOnCreate>0</TriggerOnCreate>
      <TriggerOnDelete>0</TriggerOnDelete>
      <AsyncAutodelete>0</AsyncAutodelete>
      <SyncWorkflowLogOnFailure>0</SyncWorkflowLogOnFailure>
      <StateCode>0</StateCode>
      <StatusCode>1</StatusCode>
      <RunAs>1</RunAs>
      <IsTransacted>1</IsTransacted>
      <IntroducedVersion>1.0.0.0</IntroducedVersion>
      <IsCustomizable>1</IsCustomizable>
      <BusinessProcessType>0</BusinessProcessType>
      <IsCustomProcessingStepAllowedForOtherPublishers>1</IsCustomProcessingStepAllowedForOtherPublishers>
      <PrimaryEntity>none</PrimaryEntity>
      <LocalizedNames>
        <LocalizedName languagecode="1033" description="{fname}" />
      </LocalizedNames>
    </Workflow>
"""
    for fid, fname, ffile, _ in FLOWS
)

customizations_xml = f"""<?xml version="1.0" encoding="utf-8"?>
<ImportExportXml xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" OrganizationVersion="9.2.26094.160" OrganizationSchemaType="Standard">
  <Entities />
  <Roles />
  <Workflows>
{WORKFLOWS_XML}  </Workflows>
  <FieldSecurityProfiles />
  <Templates />
  <EntityMaps />
  <EntityRelationships />
  <OrganizationSettings />
  <optionsets />
  <CustomControls />
  <EntityDataProviders />
  <connectionreferences>
    <connectionreference connectionreferencelogicalname="{CR_ONEDRIVE}">
      <connectionreferencedisplayname>Smart Inventory - OneDrive for Business</connectionreferencedisplayname>
      <connectorid>/providers/Microsoft.PowerApps/apis/shared_onedriveforbusiness</connectorid>
      <iscustomizable>1</iscustomizable>
      <statecode>0</statecode>
      <statuscode>1</statuscode>
    </connectionreference>
    <connectionreference connectionreferencelogicalname="{CR_EXCEL}">
      <connectionreferencedisplayname>Smart Inventory - Excel Online (Business)</connectionreferencedisplayname>
      <connectorid>/providers/Microsoft.PowerApps/apis/shared_excelonlinebusiness</connectorid>
      <iscustomizable>1</iscustomizable>
      <statecode>0</statecode>
      <statuscode>1</statuscode>
    </connectionreference>
    <connectionreference connectionreferencelogicalname="{CR_DATAVERSE}">
      <connectionreferencedisplayname>Smart Inventory - Microsoft Dataverse</connectionreferencedisplayname>
      <connectorid>/providers/Microsoft.PowerApps/apis/shared_commondataserviceforapps</connectorid>
      <iscustomizable>1</iscustomizable>
      <statecode>0</statecode>
      <statuscode>1</statuscode>
    </connectionreference>
  </connectionreferences>
  <Languages>
    <Language>1033</Language>
  </Languages>
</ImportExportXml>
"""

content_types = """<?xml version="1.0" encoding="utf-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="xml" ContentType="application/octet-stream" /><Default Extension="json" ContentType="application/octet-stream" /></Types>"""

zip_path = os.path.join(OUT, f"{SOLUTION}_{VERSION.replace('.', '_')}.zip")
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("[Content_Types].xml", content_types)
    z.writestr("solution.xml", solution_xml)
    z.writestr("customizations.xml", customizations_xml)
    for _, _, ffile, defn in FLOWS:
        z.writestr(ffile, json.dumps(wrap(defn), indent=2))
print(zip_path)
