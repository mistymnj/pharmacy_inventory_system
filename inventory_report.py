import sqlite3
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
from openpyxl.worksheet.table import Table, TableStyleInfo


def export_inventory_report(role):

    if role != "admin":
        print("Access denied! Admin only.")
        return

    conn = sqlite3.connect("pharmacy.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            medicines.medicine_id,
            medicines.medicine_name,
            medicine_batches.batch_number,
            medicine_batches.quantity,
            medicines.unit_price,
            medicine_batches.manufacturing_date,
            medicine_batches.expiry_date,
            medicine_batches.purchase_date
        FROM medicines
        JOIN medicine_batches
        ON medicines.medicine_id = medicine_batches.medicine_id
        ORDER BY medicines.medicine_name
    """)

    records = cursor.fetchall()
    conn.close()

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Inventory Report"

    # Report Title
    sheet.merge_cells("A1:H1")
    sheet["A1"] = "PHARMACY INVENTORY REPORT"

    sheet["A1"].font = Font(
        name="Arial",
        size=18,
        bold=True,
        color="FFFFFF"
    )

    sheet["A1"].fill = PatternFill(
        fill_type="solid",
        fgColor="17365D"
    )

    sheet["A1"].alignment = Alignment(
        horizontal="center",
        vertical="center"
    )

    sheet.row_dimensions[1].height = 35

    # Column Headers
    headers = [
        "Medicine ID",
        "Medicine Name",
        "Batch Number",
        "Available Quantity",
        "Unit Price (₹)",
        "Manufacturing Date",
        "Expiry Date",
        "Purchase Date"
    ]

    sheet.append([])
    sheet.append(headers)

    header_fill = PatternFill(
        fill_type="solid",
        fgColor="4472C4"
    )

    for cell in sheet[3]:
        cell.font = Font(
            bold=True,
            color="FFFFFF",
            size=11
        )

        cell.fill = header_fill

        cell.alignment = Alignment(
            horizontal="center",
            vertical="center"
        )

    # Insert Inventory Records
    for record in records:
        sheet.append(record)

    # Table Formatting
    last_row = sheet.max_row

    if last_row >= 4:

        table = Table(
            displayName="PharmacyInventory",
            ref=f"A3:H{last_row}"
        )

        style = TableStyleInfo(
            name="TableStyleMedium2",
            showFirstColumn=False,
            showLastColumn=False,
            showRowStripes=True,
            showColumnStripes=False
        )

        table.tableStyleInfo = style
        sheet.add_table(table)

    # Column Widths
    widths = {
        "A": 15,
        "B": 25,
        "C": 20,
        "D": 22,
        "E": 18,
        "F": 22,
        "G": 18,
        "H": 18
    }

    for column, width in widths.items():
        sheet.column_dimensions[column].width = width

    # Cell Alignment and Borders
    thin_border = Border(
        left=Side(style="thin", color="D9E2F3"),
        right=Side(style="thin", color="D9E2F3"),
        top=Side(style="thin", color="D9E2F3"),
        bottom=Side(style="thin", color="D9E2F3")
    )

    for row in sheet.iter_rows(min_row=3):
        for cell in row:
            cell.border = thin_border
            cell.alignment = Alignment(
                horizontal="center",
                vertical="center"
            )

    # Price Formatting
    for row in range(4, last_row + 1):
        sheet[f"E{row}"].number_format = '₹#,##0.00'

    # Professional Report Settings
    sheet.freeze_panes = "A4"
    sheet.sheet_view.showGridLines = False
    sheet.auto_filter.ref = f"A3:H{last_row}"

    # Save Excel File
    filename = "pharmacy_inventory_report.xlsx"

    workbook.save(filename)

    print("\n" + "=" * 50)
    print("PHARMACY INVENTORY REPORT")
    print("=" * 50)
    print("Excel report generated successfully!")
    print("File Name:", filename)
    print("Total Records:", len(records))
    print("=" * 50)