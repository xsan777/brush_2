def excel_validator(file, range_validator={}, length_validator={}, rename={}):
    """
    excel 验证函数 （空值处理， tips信息顺序调整）
    :param file: excel绝对路径
    :param range_validator: 可用范围验证：key：excel字段名；value<list>：字段所有可能取值
    :param length_validator: (默认不传）长度限制处理：key：excel字段名；value<int>：字段限制长度
    :param rename: （默认不传）重命名参数: key：excel原字段名；value<int>：字段显示名称
    :return: data, response
    data<list-dict>: 默认数据列表
    response<dict>: 返回信息
        - error<str>: 错误显示的信息，有错误才会返回的信息，错误后将返回空 data 值
        - tips<str>: 为常规提示信息，html格式，非出错状态总会返回值
        - del_col<list>: 因错误被删除的行列表
    """
    import pandas as pd

    # 定义空值的显示内容
    naShow = "* 空值 *"

    # 定义日期索引值的字段
    date_validator_list = ["付款日期"]

    # 长度限制处理
    length_dict = {"店铺": 32, "付款日期": 16, "付款类型": 16, "付款账户": 64}
    length_dict.update(length_validator)

    # 重命名参数
    rename_dict = {"店铺": "shopname", "付款日期": "transaction_date", "付款类型": "payment_type", "付款账户": "payment_account"}
    rename_dict.update(rename)

    # 读取类型限制
    dtype = {i: "str" for i in rename_dict.keys()}

    # 可用范围验证
    range_dict = range_validator

    # 返回内容
    data = {}
    response = {"error": "", "tips": "", "del_col": []}

    def is_vaild_date(date):
        """
        验证日期类型
        :param date: 待验证的日期
        :return: True 或 False
        """
        import datetime
        try:
            datetime.datetime.strftime(date, "%Y-%m-%d")
            return True
        except:
            return False

    def drop_nan(s):
        """
        将空值替换为指定的显示内容
        :param s: 待判断处理的值
        :return: 替换后的值
        """
        if s == "nan":
            s = s.replace("nan", naShow)
        return s

    def replace_nan(s):
        """
        将显示的空值再替换为空字符串
        :param s: 待判断处理的值
        :return: 替换后的值
        """
        if s == naShow:
            s = s.replace(naShow, "")
        return s

    # 读取Excel文件
    try:
        df = pd.read_excel(file, dtype=dtype)
        # response['tips'] += '<p>识别excel文件，并从Excel文件中获取数据{}行</p>'.format(len(df))
    except:
        # 情况一：数据读取失败
        response["error"] += "<h3>文件读取失败！</h3>"
        return {}, response

    # 空值替换
    df.loc[:, rename_dict.keys()] = df.loc[:, rename_dict.keys()].applymap(drop_nan)

    # 验证标题
    for title in rename_dict.keys():
        if title not in df.columns.tolist():
            # 情况二：标题不符
            response["error"] += "<h3>文件格式错误！[{}] 字段未找到！</h3>".format(title)
            return {}, response

    # 验证数据
    for line in range(len(df)):
        # 日期验证
        for col in date_validator_list:
            if not is_vaild_date(df.loc[line, col]):
                response["tips"] += "<p>第{}行 [{}] 字段日期格式验证失败！本条数据被忽略！</p>".format(line+2, col)
                response["del_col"].append(line)

        # 范围验证
        for col in range_dict.keys():
            if df.loc[line, col] not in range_dict[col]:
                response["tips"] += "<p>第{}行 [{}] 字段为 [{}] 超域非法！本条数据被忽略！</p>".format(line+2, col, df.loc[line, col])
                response["del_col"].append(line)

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
    df.loc[:, rename_dict.keys()] = df.loc[:, rename_dict.keys()].applymap(replace_nan)

    # 字段截取
    df = df.loc[:, rename_dict.keys()]
    titleTips = "<p>经验证共取得合法数据共 {} 行".format(len(df))
    if len(response["del_col"]) > 0:
        response["tips"] = titleTips + "，非法未载入数据 {} 行".format(len(response["del_col"])) + response["tips"]
    else:
        response["tips"] = titleTips + "</p>" + response["tips"]

    # 处理返回值
    df.rename(columns=rename_dict, inplace=True)
    data = df.to_dict(orient="records")
    return data, response


if __name__ == "__main__":

    data, response = excel_validator("E:\数据表\销售部售后返现转账记录.xlsx")

    print(data)
    print(response)