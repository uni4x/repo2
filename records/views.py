# mealtracker/records/views.py
import matplotlib
matplotlib.use('Agg')

from django.shortcuts import render, get_object_or_404, redirect
from .models import MealRecord
from .forms import MealRecordForm, SearchForm
from datetime import date, timedelta
import matplotlib.pyplot as plt
from io import BytesIO
from django.http import HttpResponse, JsonResponse
import matplotlib.dates as mdates
import matplotlib.font_manager as fm
from django.db.models import Q


def calendar_view(request):
    records = MealRecord.objects.all()
    return render(request, 'calendar.html', {'records': records})

def record_detail(request, pk):
    record = get_object_or_404(MealRecord, pk=pk)
    return render(request, 'record_detail.html', {'record': record})


def record_create(request):
    record_date = request.GET.get('date', date.today())
    try:
        # 既存のレコードがあるかチェック
        record = MealRecord.objects.get(date=record_date)
        return redirect('record_edit', pk=record.pk)
    except MealRecord.DoesNotExist:
        # 既存のレコードがない場合、新規作成フォームを表示
        if request.method == 'POST':
            form = MealRecordForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('calendar')
        else:
            form = MealRecordForm(initial={'date': record_date})
        return render(request, 'record_form.html', {'form': form})

def record_edit(request, pk):
    record = get_object_or_404(MealRecord, pk=pk)
    if request.method == 'POST':
        form = MealRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('record_detail', pk=record.pk)
    else:
        form = MealRecordForm(instance=record)
    return render(request, 'record_form.html', {'form': form})

def record_delete(request, pk):
    record = get_object_or_404(MealRecord, pk=pk)
    if request.method == 'POST':
        record.delete()
        return redirect('calendar')
    return render(request, 'record_confirm_delete.html', {'record': record})


def weight_trend_view(request):
    # 体重が記録されている日付と体重を取得
    records = MealRecord.objects.exclude(weight__isnull=True).order_by('date')
    dates = [record.date for record in records]
    weights = [record.weight for record in records]

    # 日本語フォントを設定
    font_path = '/Users/a/Library/Fonts/NotoSansJP-VariableFont_wght.ttf'
    prop = fm.FontProperties(fname=font_path)

    # グラフを作成
    fig, ax = plt.subplots()
    ax.plot(dates, weights, marker='o')

    # グラフのラベルとタイトルを設定
    ax.set(xlabel='日付', ylabel='体重 (kg)', title='体重推移グラフ')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # 日付フォーマットを設定
    fig.autofmt_xdate()  # 日付ラベルのフォーマットを自動調整
    ax.set_title('体重推移グラフ', fontproperties=prop)
    ax.set_xlabel('日付', fontproperties=prop)
    ax.set_ylabel('体重 (kg)', fontproperties=prop)
    ax.grid()

    # グラフをバッファに保存
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)

    graph_url = request.build_absolute_uri('/graph/')
    return render(request, 'weight_trend.html', {'graph_url': graph_url})

def graph_view(request):
    records = MealRecord.objects.exclude(weight__isnull=True).order_by('date')
    dates = [record.date for record in records]
    weights = [record.weight for record in records]

    font_path = '/Users/a/Library/Fonts/NotoSansJP-VariableFont_wght.ttf'
    prop = fm.FontProperties(fname=font_path)
    
    fig, ax = plt.subplots()
    ax.plot(dates, weights, marker='o')

    ax.set(xlabel='日付', ylabel='体重 (kg)', title='体重推移グラフ')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()
    ax.set_title('体重推移グラフ', fontproperties=prop)
    ax.set_xlabel('日付', fontproperties=prop)
    ax.set_ylabel('体重 (kg)', fontproperties=prop)
    ax.grid()

    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)

    return HttpResponse(buf, content_type='image/png')

def calculate_bmi(request):
    if request.method == 'POST':
        height = float(request.POST.get('height'))
        weight = float(request.POST.get('weight'))
        bmi = weight / (height / 100) ** 2
        return JsonResponse({'bmi': bmi})
    return JsonResponse({'error': 'Invalid request method'}, status=400)


def monthly_view(request, year, month):
    start_date = date(year, month, 1)
    end_date = (start_date + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    records = MealRecord.objects.filter(date__range=(start_date, end_date)).order_by('date')
    
    form = SearchForm(request.GET)
    filtered_records = []
    if form.is_valid():
        query = form.cleaned_data.get('query')
        if query:
            for record in records:
                record_data = {
                    'date': record.date,
                    'breakfast': record.breakfast if query in record.breakfast else None,
                    'lunch': record.lunch if query in record.lunch else None,
                    'dinner': record.dinner if query in record.dinner else None,
                    'snack': record.snack if query in record.snack else None,
                    'notes': record.notes if query in record.notes else None,
                }
                if any(record_data.values()):
                    filtered_records.append(record_data)
        else:
            filtered_records = records

    return render(request, 'monthly_view.html', {'records': filtered_records, 'month': month, 'year': year, 'form': form, 'query': query})
