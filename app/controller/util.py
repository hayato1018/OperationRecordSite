import csv
from django.http import HttpResponse
import openpyxl.utils
from ..models import MasterData
import openpyxl
from datetime import datetime

# 入力ファイル、ワークブック、ワークシートの初期化
# input_book = None
# wb = None
# ws = None

class MakeCSV:
    
    def __init__(self, input_book):
        self.master_list = MasterData.objects.all()
        self.input_book = input_book
        self.wb = openpyxl.load_workbook(input_book, data_only=True)
        self.ws = self.wb['澤村']

    def export_master_data_to_csv(self):
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
    def search_start_date_col(self, keyword):
        result = 7
        for col in self.ws.columns:
            for cell in col:
                try:
                    value = str(cell.value)
                except:
                    continue
                if value == keyword:
                    result = cell.column
        return result

    # '01'の行を検索して、その行番号を返す
    def search_start_date_row(self, keyword):
        result = 2
        for row in self.ws.rows:
            for cell in row:
                try:
                    value = str(cell.value)
                except:
                    continue
                if value == keyword:
                    result = cell.row
        return result

    # 検索文字のある行を取得し、キーにプロジェクト番号、値にプロジェクト名、フェーズ番号、検索文字のある行を持つ辞書を作成
    def get_search_text_dict(self):
        search_text_dict = {}
    
        for row in self.ws.iter_rows(min_row=2, max_row=200, min_col=1, max_col=200):
            for col in row:
                for master_data in self.master_list:
                    if col.value == master_data.search_text:
                        project_number = master_data.project_number
                        project_name = master_data.project_name
                        phase_number = master_data.phase_number
                        search_text = openpyxl.utils.cell.coordinate_from_string(col.coordinate)[1]
                        search_text_dict.update({project_number: [project_name, phase_number, search_text]})
        return search_text_dict

    def create_csv_rows(self, row, col, work_day, order_no, phase_no):
        work_day_str = work_day.strftime('%Y/%m/%d')
        time_cell = self.ws.cell(row, col).value
        times = None

        if order_no != (self.master_list.filter(project_name='社内雑務').first()).project_number:
            if time_cell:
                times = time_cell
            else:
                return
    #else:
        
# 主な処理
    def operation_record_export(self, year_month_str):
        # TODO ここに処理を追加
        year_month = datetime.strptime(year_month_str, '%Y-%m').strftime('%Y_%m')
        start_date_col = self.search_start_date_col('01')
        start_date_row = self.search_start_date_row('01')
        search_text_dict = self.get_search_text_dict()
        print(search_text_dict)
        print(start_date_col, start_date_row)


