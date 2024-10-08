import os
import glob
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import MasterData
from .forms import MasterForm
from .controller.util import MakeCSV

# ホーム画面のビュー
def home(request):
    return render(request, 'app/home.html')

def download_sample(request):
    file_path = os.path.join(settings.BASE_DIR, 'sample', 'sampledeta.xlsx')

    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename="sampledeta.xlsx"'
            return response
    else:
        return HttpResponse("サンプルデータが存在しません。")

# マスタ設定画面のビュー
def master(request):
    master_list = MasterData.objects.all()

    if request.method == 'POST':
        form = MasterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('master')
    else:
        form = MasterForm()

    return render(request, 'app/master.html', {'form': form, 'master_list': master_list})

# マスタ設定画面-削除機能のビュー
def delete_master(request, pk):
    master = get_object_or_404(MasterData, pk=pk)
    master.delete()
    return redirect('master')

# マスタ設定画面-編集機能のビュー
def edit_master(request, pk):
    master = get_object_or_404(MasterData, pk=pk)

    if request.method == 'POST':
        form = MasterForm(request.POST, instance=master)
        if form.is_valid():
            form.save()
            return redirect('master')

    else:
        form = MasterForm(instance=master)

        if master.project_name == "自社作業":
            form.fields['project_name'].widget.attrs['readonly'] = True

    return render(request, 'app/edit_master.html', {'form': form})

# 確認画面のビュー
def confirm_master(request):
    internal_task_exists = MasterData.objects.filter(project_name="自社作業").exists()
    master_list = MasterData.objects.all()
    if request.method == "POST":
        form = MasterForm(request.POST)
        if form.is_valid():
            MasterData.objects.create(
                project_name=form.cleaned_data['project_name'],
                project_number=form.cleaned_data['project_number'],
                phase_number=form.cleaned_data['phase_number'],
                search_text=form.cleaned_data['search_text'],
            )
        if 'output' in request.POST:
            input_book = request.FILES.get('input_book')
            year_month = request.POST.get('year_month')
            if input_book:
                make_csv = MakeCSV(input_book)
                make_csv.operation_record_export(year_month)
                return redirect('output')  # 出力実行画面へ遷移
        elif 'edit_master' in request.POST:
            return redirect('master')  # マスタ設定画面へ遷移

    return render(request, 'app/confirm_master.html', {
        'master_list': master_list,
        'internal_task_exists': internal_task_exists
    })

# 出力実行画面のビュー
def output(request):
    if request.method == 'POST':
        output_dir = os.path.join(settings.BASE_DIR, 'output')
        csv_files = glob.glob(os.path.join(output_dir, '*.csv'))
        if csv_files:
            file_path = csv_files[0]
        else:
            return HttpResponse("CSVファイルが存在しません。")

        if os.path.exists(file_path):
            response = HttpResponse(
                open(file_path, 'rb').read(),
                content_type='text/csv'
            )
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'

            for csv_file in csv_files:
                os.remove(csv_file)

            return response
        else:
            return HttpResponse("CSVファイルが存在しません。")

    # POSTリクエストでない場合の通常画面表示
    return render(request, 'app/output.html')