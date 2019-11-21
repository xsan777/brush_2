# 喝酒系统数据分析函数 王志平 2018-11-24：
# da_shop_paytype
# 参数 date_begin<str>: 起始查询日期（包含日期），例："2018-10-16"
# 参数 date_end<str>: 结束查询日期（不含日期），例："2018-10-17"
# 参数 aggfunc<str>: 运算函数，"sum"求和或"count"求数量
# 参数 rename_dict<dict>: 重命名参数: key：原始名；value：重命名；
# 返回值：result
# result<dict>: 返回json字典

# da_financial_statements
# 参数 date_begin<str>: 起始查询日期（包含日期），例："2018-10-16"
# 参数 date_end<str>: 结束查询日期（不含日期），例："2018-10-17"
# 参数 aggfunc<str>: 运算函数，"sum"求和或"count"求数量
# 参数 rename_dict<dict>: 重命名参数: key：原始名；value：重命名；
# 返回值：result
# result<dict>: 返回json字典

import pymysql
import numpy as np
import pandas as pd
import datetime

# 数据处理：格式化函数
def process_nan(s):
    try:
        if s == 0:
            return ""
        else:
            return float('%.2f' % float(s))
    except:
        return s

# 调用数据库函数
def return_mysql(date_begin, date_end, aggfunc="sum", values="payment_amount", index="shopname",
                 columns="payment_type", table="brush_brush_single_entry", type=[],
                 selector="id", field="add_time", value=""):
    conn = pymysql.connect(host="59.110.241.144",
                          user="panjin",
                          passwd="panjin456",
                          db="brush_wine",
                          port=3306,
                          charset="utf8")
    # type:"data" 返回值
    if "data" in type:
        sql = "SELECT {} FROM {} WHERE `{}`='{}'".format(selector, table, field, value)
    elif "finance" in type:
        sql = "SELECT * FROM {} WHERE `{}`>='{}' AND `{}`<'{}' AND `deletes`='False' AND `account_name_id`='{}';".format(table, field, date_begin, field, date_end, selector)
    else:
        sql = "SELECT * FROM {} WHERE `{}`>='{}' AND `{}`<'{}';".format(table, field, date_begin, field, date_end)
    try:
        df = pd.read_sql(sql, con=conn)
    except Exception as e:
        print(e)
    finally:
        conn.close()
    if "data" in type:
        return df.iloc[:, 0].tolist()
    df = df.loc[df["deletes"]=='False', :]
    df = df.applymap(process_nan)
    # type:"date" 针对日期处理 "date" for "add_time"
    if "date" in type:
        df["date"] = df[field].map(lambda s:str(s).split()[0])
    if "finance" in type:
        df["date"] = df[field].map(lambda s:str(s).split()[0])
        pivottable = df.loc[:, ["date", "start_money", "end_money"]]
        return pivottable
    pivottable = pd.pivot_table(df, values=values, index=index, columns=columns, aggfunc=aggfunc, fill_value=0, margins=True)
    pivottable = pivottable.reset_index()
    return pivottable

# pivot_table 格式化处理
def pivot_table_format(pivot_table, rename_dict={}):
    # 排序
    pivot_table.sort_values(by="All", ascending=False, inplace=True)
    pivot_table.reset_index(drop=True, inplace=True)
    # 重命名
    pivot_table.rename(columns=rename_dict, inplace=True)
    pivot_table = pivot_table.applymap(process_nan)
    return pivot_table

# columns_order_list
def order_list(origin_list=[], begin_list=[], end_list=[]):
    sort_list = []
    end_temporary_list = []
    for begin in begin_list:
        if begin in origin_list:
            sort_list.append(begin)
            origin_list.remove(begin)
    for end in end_list:
        if end in origin_list:
            end_temporary_list.append(end)
            origin_list.remove(end)
    sort_list.extend(origin_list)
    sort_list.extend(end_temporary_list)
    return sort_list

# 调用
def da_shop_paytype(date_begin, date_end, rename_dict={}, json=True):
    # sum
    pivot_table = return_mysql(date_begin, date_end, aggfunc='sum')
    pivot_table = pivot_table_format(pivot_table, rename_dict=rename_dict)
    # count
    pivot_table_count = return_mysql(date_begin, date_end, aggfunc='count')
    pivot_table_count = pivot_table_format(pivot_table_count, rename_dict=rename_dict)
    # concat
    dfx = pd.concat([pivot_table, pivot_table_count.rename(columns={"1": "count"}).loc[:, "count"]], axis=1)
    # order
    column_list = order_list(dfx.columns.tolist(), ["shopname", "count", "1", "2", "3"], ["All"])
    index_list = order_list(dfx.index.tolist(), [], [0])
    dfx = dfx.loc[index_list, column_list]
    # 输出
    if json:
        result = pivot_table.to_dict(orient="record")
        return result
    else:
        return dfx

def da_financial_statements(date_begin, date_end, total_account_name, rename_dict={}):
    id_list = return_mysql(date_begin, date_end, table="brush_total_brank_account", type=["data"], selector="id", field="total_account_name", value=total_account_name)
    if id_list:
        shop_list = return_mysql(date_begin, date_end, table="brush_shops", type=["data"], selector="shopname", field="own_total_brank_id", value=id_list[0])
    # 求和表
    df = return_mysql(date_begin, date_end, aggfunc='sum', index="date", columns=["shopname", "payment_type"], type=["date"])
    df.set_index("date", inplace=True)
    df_concat = ""
    for shopname in shop_list:
        df_component = df.loc[:, shopname].copy()
        df_component.columns = [shopname + "_" + i for i in df_component.columns.tolist()]
        if not len(df_concat):
            df_concat = df_component
        else:
            df_concat = pd.concat([df_concat, df_component], axis=1)
    # 数量表
    df = return_mysql(date_begin, date_end, aggfunc='count', index="date", columns=["shopname", "payment_type"] ,type=["date"])
    df.set_index("date", inplace=True)
    for shopname in shop_list:
        df_component = df.loc[:, ((shopname), ("本金"))].copy()
        df_component.name = shopname + "_" + "数量"
        df_concat = pd.concat([df_concat, df_component], axis=1)
    # 财务数据
    date_delta = datetime.datetime.strftime(datetime.datetime.strptime(date_begin, "%Y-%m-%d") - datetime.timedelta(1), "%Y-%m-%d")
    df = return_mysql(date_delta, date_end, table="brush_total_account_record", type=["finance"],
                        field="datess", index="date", selector=id_list[0])
    df["funds_to"] = df["start_money"] - df.shift(1)["end_money"]
#     df.drop(index=[0], inplace=True)
    df.set_index("date", inplace=True)
    df.loc["All", :] = df.sum(axis=0)
    df.rename(columns={"start_money": "初始金额", "end_money": "结束金额", "funds_to": "转账金额"}, inplace=True)
    df_concat = pd.concat([df_concat, df], axis=1, sort=True)
    df_concat.fillna("",inplace=True)
    #自己修改
    df_concat = df_concat.to_dict(orient="record")
    return df_concat

#测试
#########
# ab = da_financial_statements('2018-12-1','2018-12-2','芮丽娅总账户')
# print(ab)
# print(type(ab))