"""Builds SmartInventoryFlows_1_0_0_0.zip: an unmanaged Dataverse solution with one cloud flow.

Flow "Smart Inventory - Bulk Import Read Excel" (Power Apps V2 trigger):
  1. receives the uploaded .xlsx from the app (file input "File"),
  2. saves it in the flow owner's OneDrive under /Apps/SmartInventory/BulkImport,
  3. reads the Excel table "tblImport" (sheet Import of the template),
  4. turns the rows into tab-separated text, the same format as a paste from Excel,
  5. deletes the temporary file and returns the text to the app ("rows").
The app puts that text into inpBlkPaste and runs the existing Check, so all rules stay in the app.

Usage: python build_solution.py <output folder>
"""
import json
import os
import sys
import zipfile

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
VERSION = "1.0.0.0"
SOLUTION = "SmartInventoryFlows"
FLOW_NAME = "Smart Inventory - Bulk Import Read Excel"
# fixed ids so a rebuilt zip updates the same flow on re-import
FLOW_ID = "6b1d2f3a-4c5e-4f60-9a71-8b2c3d4e5f60"
CR_ONEDRIVE = "cr8a3_sharedonedriveforbusiness_sinv"
CR_EXCEL = "cr8a3_sharedexcelonlinebusiness_sinv"
FOLDER = "/Apps/SmartInventory/BulkImport"
TABLE = "tblImport"
COLUMNS = ["Area", "Item name", "BPN", "SPN", "Category", "UOM", "Qty", "Min in area", "Rack"]

TAB = "decodeUriComponent('%09')"
NL = "decodeUriComponent('%0A')"
line_expr = "concat(" + f", {TAB}, ".join(f"coalesce(string(item()?['{c}']), '')" for c in COLUMNS) + ")"

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
                        "file": {
                            "title": "File",
                            "type": "object",
                            "x-ms-dynamically-added": True,
                            "description": "The filled-in Bulk Import template (.xlsx)",
                            "x-ms-content-hint": "FILE",
                            "properties": {
                                "name": {"type": "string"},
                                "contentBytes": {"type": "string", "format": "byte"},
                            },
                        }
                    },
                    "required": ["file"],
                }
            },
        }
    },
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
                    "body": "@base64ToBinary(triggerBody()?['file']?['contentBytes'])",
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
                    # OneDrive's Create file returns no DriveId and the drive id differs per account:
                    # after import, pick Location/Document Library in the designer (README, step 2b)
                    "drive": "@outputs('Create_file')?['body/DriveId']",
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
        "Respond_to_app_rows": {
            "runAfter": {"Select_lines": ["Succeeded"]},
            "type": "Response",
            "kind": "PowerApp",
            "inputs": {
                "statusCode": 200,
                "body": {
                    "rows": f"@{{join(body('Select_lines'), {NL})}}",
                    "error": "",
                },
                "schema": {
                    "type": "object",
                    "properties": {
                        "rows": {"title": "rows", "x-ms-dynamically-added": True, "type": "string"},
                        "error": {"title": "error", "x-ms-dynamically-added": True, "type": "string"},
                    },
                },
            },
        },
        "Respond_to_app_error": {
            # Skipped = the upload to OneDrive already failed
            "runAfter": {"List_rows_present_in_a_table": ["Failed", "TimedOut", "Skipped"]},
            "type": "Response",
            "kind": "PowerApp",
            "inputs": {
                "statusCode": 200,
                "body": {
                    "rows": "",
                    "error": "The file could not be read. Use the Bulk Import template and keep the table 'tblImport' on the Import sheet.",
                },
                "schema": {
                    "type": "object",
                    "properties": {
                        "rows": {"title": "rows", "x-ms-dynamically-added": True, "type": "string"},
                        "error": {"title": "error", "x-ms-dynamically-added": True, "type": "string"},
                    },
                },
            },
        },
    },
    "outputs": {},
}

flow_json = {
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
        },
        "definition": definition,
        "templateName": "",
    },
    "schemaVersion": "1.0.0.0",
}

flow_file = f"Workflows/SmartInventory-BulkImportReadExcel-{FLOW_ID.upper()}.json"

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
    </RootComponents>
    <MissingDependencies />
  </SolutionManifest>
</ImportExportXml>
"""

customizations_xml = f"""<?xml version="1.0" encoding="utf-8"?>
<ImportExportXml xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" OrganizationVersion="9.2.26094.160" OrganizationSchemaType="Standard">
  <Entities />
  <Roles />
  <Workflows>
    <Workflow WorkflowId="{{{FLOW_ID}}}" Name="{FLOW_NAME}">
      <JsonFileName>/{flow_file}</JsonFileName>
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
        <LocalizedName languagecode="1033" description="{FLOW_NAME}" />
      </LocalizedNames>
    </Workflow>
  </Workflows>
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
    z.writestr(flow_file, json.dumps(flow_json, indent=2))
print(zip_path)
