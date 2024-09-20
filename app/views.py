from django.shortcuts import render, redirect, get_object_or_404
from .models import MasterData
from .forms import MasterForm

# ホーム画面のビュー
def home(request):
    return render(request, 'app/home.html')

# マスタ設定画面のビュー
def master(request):
    master_list = MasterData.objects.all()

    if request.method == 'POST':
        form = MasterForm(request.POST)
        if form.is_valid():
            MasterData.objects.create(
                project_name=form.cleaned_data['project_name'],
                project_number=form.cleaned_data['project_number'],
                phase_number=form.cleaned_data['phase_number'],
                search_text=form.cleaned_data['search_text'],
            )
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

    return render(request, 'app/edit_master.html', {'form': form})

# 確認画面のビュー
def confirm_master(request):
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
            return redirect('output')  # 出力実行画面へ遷移
        elif 'edit_master' in request.POST:
            return redirect('master')  # マスタ設定画面へ遷移

    return render(request, 'app/confirm_master.html', {'master_list': master_list})

# 出力実行画面のビュー
def output(request):
    return render(request, 'app/output.html')
