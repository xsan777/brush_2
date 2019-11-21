from django import forms
from brush.models import *
from django.core.exceptions import ValidationError


# 修改密码
class Updata_passwd(forms.Form):
    passwd = forms.CharField(label='新密码', widget=forms.PasswordInput(attrs={'placeholder': '新密码', 'class': 'form-control', 'id': 'passwd', }))
    passwd2 = forms.CharField(label='确认新密码', widget=forms.PasswordInput(attrs={'placeholder': '确认新密码', 'class': 'form-control', 'id': 'passwd2', }))


# 创建总账户
class Total_brank_account_form(forms.Form):
    total_brank_account_name = forms.CharField(label='总账户名', widget=forms.TextInput(
        attrs={'placeholder': '总账户名', 'class': 'form-control', 'id': 'total_brank_account_name',
               'onchange': 'verification_total_brank_account()'}))
    brank_name = forms.CharField(label='银行名', widget=forms.TextInput(
        attrs={'placeholder': '银行名', 'class': 'form-control', 'id': 'brank_name'}))
    brank_number = forms.CharField(label='开户行号', widget=forms.TextInput(
        attrs={'placeholder': '开户行号', 'class': 'form-control', 'id': 'brank_number', }))
    brank_card_number = forms.CharField(label='银行卡号',
                                        widget=forms.TextInput(attrs={'placeholder': '银行卡号', 'class': 'form-control', 'id': 'brank_card_number'}))


# 修改总账户
class Edit_total_brank_account_form(forms.Form):
    total_brank_account_name = forms.CharField(label='总账户名', widget=forms.TextInput(
        attrs={'placeholder': '总账户名', 'class': 'form-control', 'id': 'edit_total_brank_account_name', 'disabled': 'True'}))
    brank_name = forms.CharField(label='银行名', widget=forms.TextInput(
        attrs={'placeholder': '银行名', 'class': 'form-control', 'id': 'edit_brank_name'}))
    brank_number = forms.CharField(label='开户行号', widget=forms.TextInput(
        attrs={'placeholder': '开户行号', 'class': 'form-control', 'id': 'edit_brank_number', }))
    brank_card_number = forms.CharField(label='银行卡号',
                                        widget=forms.TextInput(
                                            attrs={'placeholder': '银行卡号', 'class': 'form-control', 'id': 'edit_brank_card_number'}))


# 添加用户
class Add_user(forms.Form):
    username = forms.CharField(label='用户名', widget=forms.TextInput(
        attrs={'placeholder': '用户名', 'class': 'form-control', 'id': 'username', 'onchange': 'verification_username()'}))
    passwd = forms.CharField(label='密码', widget=forms.PasswordInput(attrs={'placeholder': '密码', 'class': 'form-control', 'id': 'passwd', }))
    passwd2 = forms.CharField(label='确认密码', widget=forms.PasswordInput(attrs={'placeholder': '确认密码', 'class': 'form-control', 'id': 'passwd2', }))
    description = forms.CharField(label='职位描述', widget=forms.TextInput(
        attrs={'placeholder': '职位描述', 'class': 'form-control', 'id': 'description', }))

    def clean_username(self):
        v = self.cleaned_data['username']
        if Userinfo.objects.filter(username=v):
            raise ValidationError("用户名已存在")
        return v


# 修改用户信息
class Edit_user(forms.Form):
    username = forms.CharField(label='用户名', widget=forms.TextInput(
        attrs={'placeholder': '用户名', 'class': 'form-control', 'id': 'eidt_username', 'onchange': 'edit_verification_username()', 'disabled': 'True'}))
    passwd = forms.CharField(label='密码', widget=forms.PasswordInput(attrs={'placeholder': '密码', 'class': 'form-control', 'id': 'eidt_passwd', }))
    passwd2 = forms.CharField(label='确认密码',
                              widget=forms.PasswordInput(attrs={'placeholder': '确认密码', 'class': 'form-control', 'id': 'eidt_passwd2', }))
    description = forms.CharField(label='职位描述', widget=forms.TextInput(
        attrs={'placeholder': '职位描述', 'class': 'form-control', 'id': 'eidt_description', }))


# 添加店铺
class Add_shop_form(forms.Form):
    shop_name = forms.CharField(label='店铺名', widget=forms.TextInput(
        attrs={'placeholder': '店铺名', 'class': 'form-control', 'id': 'shop_name', 'onchange': 'verification_shopname()'}))


# 查找店铺
class Search_shop(forms.Form):
    search_shop_name = forms.CharField(label='店铺名', widget=forms.TextInput(
        attrs={'placeholder': '店铺名', 'class': 'form-control', 'id': 'shop_name', }))


# 修改店铺名
class Edit_shop_form(forms.Form):
    shop_name = forms.CharField(label='店铺名', widget=forms.TextInput(
        attrs={'placeholder': '店铺名', 'class': 'form-control', 'id': 'edit_shop_name', 'disabled': 'True'}))


# 添加银行账户
class Add_brank_account(forms.Form):
    account_name = forms.CharField(label='账户名', widget=forms.TextInput(
        attrs={'placeholder': '账户名', 'class': 'form-control', 'id': 'account_name', 'onchange': 'verification_brank()'}))
    brank_name = forms.CharField(label='银行名', widget=forms.TextInput(
        attrs={'placeholder': '银行名', 'class': 'form-control', 'id': 'brank_name', 'onchange': 'verification_brank()'}))
    brank_number = forms.CharField(label='开户行号', widget=forms.TextInput(
        attrs={'placeholder': '开户行号', 'class': 'form-control', 'id': 'brank_number', 'onchange': 'verification_brank()'}))
    brank_card_number = forms.CharField(label='银行卡号',
                                        widget=forms.TextInput(attrs={'placeholder': '银行卡号', 'class': 'form-control', 'id': 'brank_card_number',
                                                                      'onchange': 'verification_brank()'}))


# 修改银行账户
class Edit_brank_account(forms.Form):
    account_name = forms.CharField(label='账户名',
                                   widget=forms.TextInput(
                                       attrs={'placeholder': '账户名', 'class': 'form-control', 'id': 'update_account_name', 'disabled': 'True'}))
    brank_name = forms.CharField(label='银行名',
                                 widget=forms.TextInput(attrs={'placeholder': '银行名', 'class': 'form-control', 'id': 'update_brank_name', }))
    brank_number = forms.CharField(label='开户行号',
                                   widget=forms.TextInput(attrs={'placeholder': '开户行号', 'class': 'form-control', 'id': 'update_brank_number', }))
    brank_card_number = forms.CharField(label='银行卡号',
                                        widget=forms.TextInput(
                                            attrs={'placeholder': '银行卡号', 'class': 'form-control', 'id': 'update_brank_card_number', }))


# 添加账户记录
class Forms(forms.Form):
    start_money = forms.CharField(label='今日转账收入资金', widget=forms.TextInput(attrs={'placeholder': '今日转账收入资金', 'class': 'form-control'}))
    end_money = forms.CharField(label='结余资金', widget=forms.TextInput(attrs={'placeholder': '结余资金', 'class': 'form-control'}))
    weixin_withdraw_money = forms.CharField(label='微信提现费用', widget=forms.TextInput(attrs={'placeholder': '微信提现费用', 'class': 'form-control'}))


# 修改账户记录
class Edit_forms(forms.Form):
    start_money = forms.CharField(label='初始资金',
                                  widget=forms.TextInput(attrs={'placeholder': '初始资金', 'class': 'form-control', 'id': 'eidt_start_money'}))
    end_money = forms.CharField(label='结余资金', widget=forms.TextInput(attrs={'placeholder': '结余资金', 'class': 'form-control', 'id': 'eidt_end_money'}))
    weixin_withdraw_money = forms.CharField(label='微信提现费用', widget=forms.TextInput(
        attrs={'placeholder': '微信提现费用', 'class': 'form-control', 'id': 'eidt_weixin_withdraw_money'}))


# 创建喝酒数据
class Add_brush_data(forms.Form):
    qq_or_weixin = forms.CharField(label='QQ或微信',
                                   widget=forms.TextInput(attrs={'placeholder': 'QQ或微信', 'class': 'form-control', 'id': 'qq_or_weixin'}))
    # wang_wang_number = forms.CharField(label='旺旺号',
    #                                    widget=forms.TextInput(attrs={'placeholder': '旺旺号', 'class': 'form-control', 'id': 'wang_wang_number','onchange':'search_wangwang_num_input()','data-container':'body','data-toggle':'popover','data-placement':'bottom'}))
    # wang_wang_number = forms.CharField(label='旺旺号', widget=forms.TextInput(
    #     attrs={'placeholder': '旺旺号', 'class': 'form-control', 'id': 'wang_wang_number', 'data-container': 'body', 'data-toggle': 'popover',
    #            'data-placement': 'bottom', 'data-html': 'true'}))
    wang_wang_number = forms.CharField(label='旺旺号', widget=forms.TextInput(
        attrs={'placeholder': '旺旺号', 'class': 'form-control', 'id': 'wang_wang_number'}))
    online_order_number = forms.CharField(label='线上订单号', widget=forms.TextInput(
        attrs={'placeholder': '线上订单号', 'class': 'form-control', 'id': 'online_order_number'}))
    payment_amount = forms.CharField(label='付款金额（收入为负）', widget=forms.TextInput(
        attrs={'placeholder': '付款金额（收入为负）', 'class': 'form-control', 'id': 'payment_amount'}))


# 修改喝酒数据
class Edit_brush_data(forms.Form):
    wang_wang_number = forms.CharField(label='旺旺号',
                                       widget=forms.TextInput(attrs={'placeholder': '旺旺号', 'class': 'form-control', 'id': 'update_wang_wang_number'}))
    qq_or_weixin = forms.CharField(label='QQ或微信',
                                   widget=forms.TextInput(attrs={'placeholder': 'QQ或微信', 'class': 'form-control', 'id': 'update_qq_or_weixin'}))
    online_order_number = forms.CharField(label='线上订单号', widget=forms.TextInput(
        attrs={'placeholder': '线上订单号', 'class': 'form-control', 'id': 'update_online_order_number'}))
    payment_amount = forms.CharField(label='付款金额（收入为负）', widget=forms.TextInput(
        attrs={'placeholder': '付款金额（收入为负）', 'class': 'form-control', 'id': 'update_payment_amount'}))
