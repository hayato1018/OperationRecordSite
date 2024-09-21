import csv
from django.http import HttpResponse
import openpyxl.utils
from ..models import MasterData
import openpyxl
from datetime import datetime

master_list = MasterData.objects.all()

def export_master_data_to_csv():
    # CSVのHTTPレスポンスを作成
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="master_data.csv"'

    writer = csv.writer(response)
    # ヘッダー行を書き込む
    writer.writerow(['プロジェクト名', 'プロジェクト番号', 'フェーズ番号', '検索文字'])

    # DBからマスタデータを取得してCSVに書き込む
    for data in MasterData.objects.all():
        writer.writerow([data.project_name, data.project_number, data.phase_number, data.search_text])

    return response

# '01'の列を検索して、その列番号を返す
def search_start_date_col(ws, keyword):
    result = 7
    for col in ws.columns:
        for cell in col:
            try:
                value = str(cell.value)
            except:
                continue
            if value == keyword:
                result = cell.column
    return result

# '01'の行を検索して、その行番号を返す
def search_start_date_row(ws, keyword):
    result = 2
    for row in ws.rows:
        for cell in row:
            try:
                value = str(cell.value)
            except:
                continue
            if value == keyword:
                result = cell.row
    return result

# 検索文字のある行を取得し、キーにプロジェクト番号、値にプロジェクト名、フェーズ番号、検索文字のある行を持つ辞書を作成
def get_search_text_dict(ws):
    search_text_dict = {}
    
    for row in ws.iter_rows(min_row=2, max_row=200, min_col=1, max_col=200):
        for col in row:
            for master_data in master_list:
                if col.value == master_data.search_text:
                    project_number = master_data.project_number
                    project_name = master_data.project_name
                    phase_number = master_data.phase_number
                    search_text = openpyxl.utils.cell.coordinate_from_string(col.coordinate)[1]
                    search_text_dict.update({project_number: [project_name, phase_number, search_text]})
    return search_text_dict

def create_csv_rows(ws, row, col, work_day, order_no, phase_no):
    work_day_str = work_day.strftime('%Y/%m/%d')
    time_cell = ws.cell(row, col).value
    times = None
    #if order_no != (社内雑務):
    #    if time_cell:
    #        times = time_cell
    #    else:
    #        return
    #else:
    

# 主な処理
def operation_record_export(input_book, year_month_str):
    wb = openpyxl.load_workbook(input_book, data_only=True)
    ws = wb['澤村']

    # TODO ここに処理を追加
    year_month = datetime.strptime(year_month_str, '%Y-%m').strftime('%Y_%m')
    start_date_col = search_start_date_col(ws, '01')
    start_date_row = search_start_date_row(ws, '01')

    
    search_text_dict = get_search_text_dict(ws)


