from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from .models import ReadDetail
from blog.models import Blog
import datetime
import pytz

# Create your views here.


def get_week_data(request):
    now = datetime.datetime.now()
    now_day = datetime.datetime(now.year, now.month, now.day, 0, 0, tzinfo=pytz.timezone('Asia/Shanghai'))
    days = []
    days_str = []
    counts = []
    ct = ContentType.objects.get_for_model(Blog)

    # 拼装日期
    for n in range(7, 0, -1):
        day = now_day - datetime.timedelta(n)
        days.append(day)

    # 拼装每日阅读数
    for day in days:
        count = ReadDetail.objects.filter(content_type=ct, requested_at__range=(day, day+datetime.timedelta(1))).count()
        counts.append(count)
        day_str = str(day)[6:10]
        days_str.append(day_str)

    context = {
        'read_num': counts,
        'days': days_str,
    }
    return render(request, 'data.html', context=context)