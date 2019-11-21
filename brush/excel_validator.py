# excel 验证函数 王志平 2018-10-13 2018-10-14(空值处理, tips信息顺序调整)：
# 参数 file<str>: excel绝对路径
# 参数 range_validator<dict>: 可用范围验证：key：excel字段名；value<list>：字段所有可能取值
# 参数 length_validator<dict>: （默认不传）长度限制处理：key：excel字段名；value<int>：字段限制长度
# 参数 rename<dict>: （默认不传）重命名参数: key：excel原字段名；value<int>：字段显示名称
# 返回值：data, response
# data<list-dict>: 默认数据列表
# response<dict>: 返回信息(下详)
#   - error<str>: 错误显示的信息，有错误才会返回的信息，错误后将返回空 data 值
#   - tips<str>: 为常规提示信息，html格式，非出错状态总会返回值
#   - del_col<list>: 因错误被删除的行列表
def excel_validator(file, range_validator={}, length_validator={}, rename={}):
    import pandas as pd
    def is_vaild_date(date):
        import datetime
        try:
            datetime.datetime.strptime(date, "%Y-%m-%d")
            return True
        except:
            return False
    naShow = "* 空值 *"
    date_validator_list = ["成交日期"]
    length_dict = {
        "店铺名": 32,
        "旺旺号": 32,
        "QQ或微信号": 32,
        "线上订单号": 26,
        "成交日期": 16,
        "付款类型": 16,
        "付款金额": 10,
        "付款账户": 64,
        "备注": 64,
    }
    rename_dict = {
        "店铺名": "shopname",
        "旺旺号": "wang_wang_number",
        "QQ或微信号": "qq_or_weixin",
        "线上订单号": "online_order_number",
        "成交日期": "transaction_date",
        "付款类型": "payment_type",
        "付款金额": "payment_amount",
        "付款账户": "payment_account",
        "备注": "remarks",
    }
    dtype = {i:"str" for i in rename_dict.keys()}
    length_dict.update(length_validator)
    rename_dict.update()
    range_dict = range_validator
    data = {}
    response = {
        'error': '',
        'tips': '',
        'del_col': [],
        }
    try:
        df = pd.read_excel(file, dtype=dtype)
#         response['tips'] += '<p>识别excel文件，并从Excel文件中获取数据{}行</p>'.format(len(df))
    except:
        # 情况一，数据读取失败
        response['error'] += "<h3>文件读取失败！</h3>"
        return {}, response
    # 空值替换
    def drop_nan(s):
        if s=="nan":
            s = s.replace("nan", naShow)
        return s
    df.loc[:, rename_dict.keys()] = df.loc[:, rename_dict.keys()].applymap(drop_nan)
    # 验证标题
    for title in rename_dict.keys():
        if title not in df.columns.tolist():
            # 情况二，标题不符
            response['error'] += "<h3>文件格式错误！[{}] 字段未找到！</h3>".format(title)
            return {}, response
    # 验证数据
    for line in range(len(df)):
        # 日期验证
        for col in date_validator_list:
            if not is_vaild_date(df.loc[line, col]):
                response["tips"] += "<p>第{}行 [{}] 字段日期格式验证失败！本条数据被忽略！</p>".format(line+2, col)
                response['del_col'].append(line)
        # 范围验证
        for col in range_dict.keys():
            if df.loc[line, col] not in range_dict[col]:
                response["tips"] += "<p>第{}行 [{}] 字段为 [{}] 超域非法！本条数据被忽略！</p>".format(line+2, col, df.loc[line, col])
                response['del_col'].append(line)
        # 长度规整
        for col in length_dict.keys():
            df.loc[line, col] = str(df.loc[line, col])
            if len(df.loc[line, col]) > length_dict[col]:
                response["tips"] += "<p>第{}行 [{}] 字段超出最大长度，已截取！</p>".format(line+2, col)
                df.loc[line, col] = df.loc[line, col][:length_dict[col]]
    # 异常字段删除
    response["del_col"] = list(set(response["del_col"]))
    df.drop(response["del_col"], inplace=True)
    # 空值再替换
    def replace_nan(s):
        if s==naShow:
            s = s.replace(naShow, "")
        return s
    df.loc[:, rename_dict.keys()] = df.loc[:, rename_dict.keys()].applymap(replace_nan)
    # 字段截取
    df = df.loc[:, rename_dict.keys()]
    titleTips = "<p>经验证共取得合法数据共 {} 行".format(len(df))
    if len(response["del_col"]) > 0:
        response["tips"] = titleTips + "，非法未载入数据 {} 行".format(len(response["del_col"])) + response["tips"]
    else:
        response["tips"] = titleTips + "</p>" + response["tips"]
    df.rename(columns=rename_dict, inplace=True)
    data = df.to_dict(orient='records')
    return data, response
