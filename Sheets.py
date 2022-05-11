import gspread

from oauth2client.service_account import ServiceAccountCredentials
def Transfer_to_sheet(string):
    print(string)
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

    creds = ServiceAccountCredentials.from_json_keyfile_name("angelic-digit-346111-0afa54abb91a.json", scope)

    client = gspread.authorize(creds)

    sheet = client.open("This_is_Gsheet").sheet1
    data = sheet.get_all_records()

    row = sheet.row_values(2)
    col = sheet.col_values(1)
    cell = sheet.cell(1,2).value
    l=[]
    l.append(string)
    print(l)
    sheet.insert_row(l ,2)
    print(data)
    print(row)
    print(col)
    print(cell)

