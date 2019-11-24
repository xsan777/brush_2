from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import View
from brush.models import *
import time, json, datetime
from .forms import *
import django_excel as excel
import os
from wine_2.settings import MEDIA_ROOT
from .excel_validator import excel_validator
from .pivottable_2 import da_financial_statements
from .pivottable import da_shop_paytype
from django.db.models import Sum


# Create your views here.
# 将时间2018-08-29 16:18:53.986855转换成2018年08月29日 16:18
def t(times):
    times = str(times)
    time1 = times.split(' ')
    time2 = time1[0].split('-')
    year1 = time2[0]
    if time2[1][0] == '0':
        mouth1 = time2[1][1]
    else:
        mouth1 = time2[1]
    day1 = time2[2]
    if day1[0] == '0':
        day1 = str(day1)[1]
    times = '%s年%s月%s日 ' % (year1, mouth1, day1)
    time3 = time1[1].split(':')
    hours = time3[0]
    minits = time3[1]
    timess = '%s:%s' % (hours, minits)
    end_time = times + timess
    return end_time


# 获取前n天的日期
def get_nday_list2(n, now_time):
    dd = datetime.datetime.strptime(now_time, '%Y-%m-%d')
    print_time = dd - datetime.timedelta(days=n - 1)
    return_time = str(print_time).replace(' 00:00:00', '')
    return return_time


# 获取下载的月份
def t_mouth(search_time):
    search_time = search_time.split('-')
    mouths = search_time[1]
    if mouths[0] == '0':
        return mouths[1]
    else:
        return mouths


#
def t_mouth_2(search_time):
    search_time = search_time.split('-')
    years = search_time[0]
    mouths = search_time[1]
    mouths = years + '-' + mouths + '-'
    return mouths


# 验证成交日期格式是否正确
def is_vaild_date(date):
    import datetime
    try:
        datetime.datetime.strptime(date, "%Y-%m-%d")
        return True
    except Exception as e:
        return False


# 登录
class Login(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('user')
        passwd = request.POST.get('passwd')
        user = Userinfo.objects.filter(username=username, deletes=False)
        if user:
            user = Userinfo.objects.filter(username=username, deletes=False).values('passwd', 'rouse', ).get()
            if passwd == user['passwd']:
                request.session['username'] = username
                request.session['rouse'] = user['rouse']
                request.session.set_expiry(0)
                if user['rouse'] == '运营':
                    return redirect('brushmanagement/')
                else:
                    return redirect(to=search_total_count)
        msg = '用户名或密码错误'
        return render(request, 'login.html', {'err_msg': msg})


# 修改密码
def update_passwd(request):
    user = request.session.get('username')
    rouse = request.session.get('rouse')
    if user == None:
        return redirect(to=Login)
    passwds = request.POST.get('passwd')
    passwd2s = request.POST.get('passwd2')
    if passwds and passwd2s:
        if passwds == passwd2s:
            user_id = Userinfo.objects.get(username=user, deletes=False)
            Userinfo.objects.filter(username=user, deletes=False).update(passwd=passwds)
            msg = ''
            msg = json.dumps(msg)
            operators = Userinfo.objects.get(username=user, deletes=False)
            operation_types = '用户自己修改密码'
            before_operations = '{id：%d，用户名：%s，旧密码：%s，角色：%s，职位描述：%s，}' % (
                user_id.id, user_id.username, user_id.passwd, user_id.rouse, user_id.description,)
            after_operations = '{id：%s，用户名：%s，新密码：%s，角色：%s，职位描述：%s，}' % (
                user_id.id, user, passwds, rouse, user_id.description,)
            Log.objects.create(operator=operators, operation_type=operation_types, after_operation=after_operations,
                               before_operation=before_operations)
        else:
            msg = '两次输入密码不一致，请重新修改'
            msg = json.dumps(msg)
        return HttpResponse(msg)


# 用户管理
class Adduser(View):
    def get(self, request):
        user = request.session.get('username')
        # rouse = request.session.get('rouse')
        # if user == None:
        #     return redirect(to=Login)
        # if rouse == '运营':
        #     return render(request, 'login.html', {'err_msg': '当前账户权限不足，请使用其他账号'})
        title = '用户管理'
        err_msg = ''
        msgs = ''
        users = request.GET.get('username')
        if users:
            user_id = Userinfo.objects.filter(username=users, deletes=False).all()
        else:
            user_id = Userinfo.objects.filter(deletes=False).all()
        table_list = []
        for i in user_id:
            tables = {}
            tables['id'] = i.id
            tables['username'] = i.username
            tables['rouse'] = i.rouse
            tables['description'] = i.description
            shops = ''
            if i.rouse == '财务':
                shops = '所有店铺'
            else:
                for user_shop in i.shop.filter(deletes=False).all():
                    shops += str(user_shop)
                    shops += '、'
            tables['shop'] = shops
            total_accounts = ''
            if i.rouse == '财务':
                total_accounts = '所有总账户'
            else:
                for user_total_accounts in i.total_brank_account.filter(deletes=False).all():
                    total_accounts += str(user_total_accounts.total_account_name)
                    total_accounts += '、'
            tables['total_accounts'] = total_accounts
            table_list.append(tables)
        shopss = Shops.objects.filter(deletes=False).all()
        total_account = Total_brank_account.objects.filter(deletes=False).all()
        add_form = Add_user()
        edit_form = Edit_user()
        now_time = time.strftime('%Y-%m-%d', time.localtime())
        now_time = get_nday_list2(2, now_time)
        all_account_makes = Total_account_record.objects.filter(datess__date=now_time, makes=False, deletes=False).all()
        if len(all_account_makes) == 0:
            admin_flog = 1
        else:
            admin_flog = 0
        update_passwd = Updata_passwd()
        return render(request, 'user.html',
                      {'title': title, 'tables': table_list, 'shops': shopss, 'add_form': add_form, 'edit_user': edit_form, 'err_msg': err_msg,
                       'msgs': msgs, 'user': user, 'admin_flog': admin_flog, 'total_account': total_account, 'update_passwd': update_passwd})

    def post(self, request):
        user = request.session.get('username')
        rouse = request.session.get('rouse')
        usernames = request.POST.get('username')
        passwds = request.POST.get('passwd')
        passwd2s = request.POST.get('passwd2')
        rouses = request.POST.get('rose')
        descriptions = request.POST.get('description')
        shop_list = request.POST.getlist('checkitem')
        total_accounts_list = request.POST.getlist('total_accounts')
        # 财务角色自动绑定所有店铺和所有总账户
        if rouses == '财务':
            shop_all = Shops.objects.filter(deletes=False).all()
            shop_list = []
            for j in shop_all:
                shop_list.append(j.shopname)
            total_account_all = Total_brank_account.objects.filter(deletes=False).all()
            total_accounts_list = []
            for m in total_account_all:
                total_accounts_list.append(m.total_account_name)
        if passwd2s == passwds:
            if len(shop_list) != 0:
                if len(total_accounts_list) != 0:
                    Userinfo.objects.create(username=usernames, passwd=passwds, rouse=rouses, description=descriptions, deletes=False)
                    user_ids = Userinfo.objects.filter(username=usernames, deletes=False).get()
                    # 将店铺与用户绑定
                    for shop in shop_list:
                        user_ids.shop.add(Shops.objects.get(shopname=shop, deletes=False))
                    # 将总账户与用户绑定
                    for accounts in total_accounts_list:
                        user_ids.total_brank_account.add(Total_brank_account.objects.get(total_account_name=accounts, deletes=False))
                    last_date = Userinfo.objects.last()
                    shops_clean = last_date.shop.all()
                    shops = ''
                    for user_shop in shops_clean:
                        shops += str(user_shop)
                        shops += '、'
                    total_account_names = ''
                    for total in total_accounts_list:
                        total_account_names += total
                        total_account_names += '、'
                    operators = Userinfo.objects.get(username=user, deletes=False)
                    operation_types = '创建新用户'
                    after_operations = '{id：%d，用户名：%s，密码：%s，角色：%s，职位描述：%s，所管店铺：%s，使用总账户：%s}' % (
                        last_date.id, usernames, passwds, rouse, descriptions, shops, total_account_names)
                    Log.objects.create(operator=operators, operation_type=operation_types, after_operation=after_operations)
                    msgs = "创建成功"
                else:
                    msgs = '必须选择总账户'
            else:
                msgs = '必须选择店铺'
        else:
            msgs = '两次密码输入不一致'
        return HttpResponse(json.dumps(msgs))


# 查看运营账户未确认情况
def check_child_count_status(user):
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
    account_unmakes = Userinfo.objects.get(username=user, deletes=False).brank_account_set.filter(deletes=False).all()
    for i in account_unmakes:
        check_countss = Account_record.objects.filter(datess__date=now_time, account_name__account_name=i.account_name, deletes=False).all()
        if check_countss:
            check_countss = Account_record.objects.filter(datess__date=now_time, account_name__account_name=i.account_name, deletes=False).get()
            if check_countss.makes == 'False':
                reminds = '(有账户未确认)'
                unmakes += 1
            if check_countss.makes == 'True':
                makes += 1
    return total_reminds, reminds, unmakes, makes


# 财务提示总账户未确认
def finance_point_total_account_status():
    now_time = time.strftime('%Y-%m-%d', time.localtime())
    now_time = get_nday_list2(2, now_time)
    all_account_makes = Total_account_record.objects.filter(datess__date=now_time, makes=False, deletes=False).exists()
    if all_account_makes:
        admin_flog = 0
    else:
        admin_flog = 1
    return admin_flog


# 按日期查询总账户记录
def search_total_count(request):
    search_date = request.GET.get('search_date')
    user = request.session.get('username')
    rouse = request.session.get('rouse')
    if user is None:
        return redirect(to='login/')
    title = '总账户记录管理'
    total_account_all = Userinfo.objects.filter(username=user, deletes=False).get().total_brank_account.filter(deletes=False).all()
    account2 = Userinfo.objects.filter(username=user, deletes=False).get().total_brank_account.filter(deletes=False).all()
    forms = Forms()
    edit_form = Edit_forms()
    now_time = time.strftime('%Y-%m-%d', time.localtime())
    if search_date:
        count = Total_account_record.objects.filter(datess__date=search_date, deletes=False).all()
    else:
        search_date = get_nday_list2(2, now_time)
        count = Total_account_record.objects.filter(datess__date=search_date, deletes=False).all()
    count_list = []
    last_date = get_nday_list2(2, search_date)
    for i in count:
        count_row = {}
        last_end_money_exists = Total_account_record.objects.filter(datess__date=last_date, account_name=i.account_name, deletes=False).values(
            'end_money').exists()
        if last_end_money_exists:
            last_end_money = Total_account_record.objects.filter(datess__date=last_date, account_name=i.account_name, deletes=False).values(
                'end_money').get()
            count_row['last_end_money'] = last_end_money['end_money']
        else:
            count_row['last_end_money'] = '该账户没有前一天的结余记录'
        count_row['id'] = i.id
        count_row['datess'] = i.datess
        count_row['account_name'] = i.account_name
        count_row['start_money'] = i.start_money
        count_row['end_money'] = i.end_money
        count_row['payment_money'] = '%.2f' % (float(i.start_money) - float(i.end_money))
        count_row['start_money_img'] = i.start_money_img
        count_row['end_money_img'] = i.end_money_img
        count_row['operator'] = i.operator.username
        count_row['makes'] = i.makes
        count_list.append(count_row)
    # 财务提示总账户未确认
    admin_flog = finance_point_total_account_status()
    # 查看运营账户未确认情况
    total_reminds, reminds, unmakes, makes = check_child_count_status(user)
    update_passwd = Updata_passwd()
    if rouse == '财务':
        return render(request, 'total_countmanagement.html',
                      {'title': title, 'count': count_list, 'nowss': search_date, 'user': user, 'admin_flog': admin_flog,
                       'update_passwd': update_passwd})
    else:
        return render(request, 'total_countmanagement2.html',
                      {'title': title, 'account': account2, 'count': count_list, 'nowss': search_date, 'formm': forms, 'edit_form': edit_form,
                       'user': user, 'total_reminds': total_reminds, 'total_account_all': total_account_all, 'reminds': reminds, 'unmakes': unmakes,
                       'update_passwd': update_passwd, 'makes': makes, 'now_time': search_date})
