import openpyxl
import hunter

patch_to_excel = "C:\\Users\\Adam\\PycharmProjects\\Spider\\info.xlsx"

# Create workbook
wb = openpyxl.load_workbook(patch_to_excel)

# Feteches the current active workbook
ws = wb.active

headers = ["Emai", "First Name", "Last Name", "Phone Number", "Type"]
header_row = 1

for header in headers:
    ws.cell(1, header_row, value=header)
    header_row+= 1

row = 2
col = 1

company_info = hunter.get_company_data("https://dunhill.net/")
for data in company_info:
    ws.cell(row=row, column=col, value=data)


wb.save(patch_to_excel)
