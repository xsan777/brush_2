from django.shortcuts import render, HttpResponse, redirect
from .views import login
from django.views.generic import View
from brush.models import *
import time, json, datetime
from .forms import *
import django_excel as excel
import os
from brush_system.settings import MEDIA_ROOT
from .excel_validator import excel_validator
from .pivottable_2 import da_financial_statements
from .pivottable import da_shop_paytype
from django.db.models import Sum
from erp.models import Taobao_buyer_information


# 上传销售部数据
def upload_excel_2(request):
    user = request.session.get('username')
    if user == None:
        return redirect(to=login)
    title = '上传喝酒数据'
    tables = ''
    msg = ''
    flog = 0
    if request.method == 'POST':
        now_time = time.strftime('%Y-%m-%d', time.localtime())
        excel_path = request.FILES.get('excels')
        if excel_path != None:
            Upload_excel.objects.create(excel_path=excel_path, operator=user)
            excel_path_database = Upload_excel.objects.filter(add_time__date=now_time, operator=user).last()
            excel_path_os = os.path.join(MEDIA_ROOT, str(excel_path_database.excel_path).replace('/', os.sep))
            # 准备验证信息
            account = Userinfo.objects.get(username=user, deletes=False).brank_account_set.filter(deletes=False).all()
            shops = Userinfo.objects.get(username=user, deletes=False).shop.filter(deletes=False).all()
            account_list = []
            for accs in account:
                account_list.append(accs.account_name)
            shop_list = []
            for shop in shops:
                shop_list.append(shop.shopname)
            payment_types = Payment_type.objects.values('types').all()
            payment_type_list = []
            for type in payment_types:
                payment_type_list.append(type['types'])
            verify_message = {'店铺名': shop_list, '付款账户': account_list, '付款类型': payment_type_list}
            # 调用验证函数（传入excel_path_os，verify_message)
            verify = excel_validator(excel_path_os, range_validator=verify_message)
            tables, msg = verify[0], verify[1]
            flog = 1
    # 总账户未确认提示运营
    total_reminds = ''
    user_total_account = Userinfo.objects.get(username=user, deletes=False)
    account__ = user_total_account.total_brank_account.filter(deletes=False).all()
    now_time = time.strftime('%Y-%m-%d', time.localtime())
    for m in account__:
        account2 = Total_account_record.objects.filter(datess__date=now_time, account_name=m, deletes=False).all()
        for i in account2:
            if i.makes == 'False':
                total_reminds = '(总账户未确认)'
    # 运营名下账户确认核对查询
    reminds = ''
    unmakes = 0
    makes = 0
    account = Userinfo.objects.get(username=user, deletes=False).brank_account_set.filter(deletes=False).all()
    for i in account:
        check_countss = Account_record.objects.filter(datess__date=now_time, account_name__account_name=i.account_name, deletes=False).all()
        if check_countss:
            check_countss = Account_record.objects.filter(datess__date=now_time, account_name__account_name=i.account_name, deletes=False).get()
            if check_countss.makes == 'False':
                reminds = '(有账户未确认)'
                unmakes += 1
            if check_countss.makes == 'True':
                makes += 1
    return render(request, 'supplemental_upload_excel.html',
                  {'user': user, 'title': title, 'tables': tables, 'msg': msg, 'flog': flog, 'reminds': reminds, 'unmakes': unmakes, 'makes': makes,
                   'total_reminds': total_reminds})
