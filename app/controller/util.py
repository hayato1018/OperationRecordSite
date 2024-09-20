import csv
from django.http import HttpResponse
from ..models import MasterData
import openpyxl

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

def operation_record_export(input_book):
    wb = openpyxl.load_workbook(input_book, data_only=True)
    ws = wb['澤村']

    # TODO ここに処理を追加