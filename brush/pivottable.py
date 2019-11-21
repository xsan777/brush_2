# excel 取数排序函数 王志平 2018-10-31：
# 参数 date_begin<str>: 起始查询日期（包含日期），例："2018-10-16"
# 参数 date_end<str>: 结束查询日期（不含日期），例："2018-10-17"
# 参数 aggfunc<str>: 运算函数，"sum"求和或"count"求数量
# 参数 rename_dict<dict>: 重命名参数: key：原始名；value：重命名；
# 参数 order<list>: 列排序，需传入完整的排序列名列表；
# 返回值：result
# result<dict>: 返回字典
# -*- coding: UTF-8 -*-
def da_shop_paytype(date_begin, date_end, aggfunc="sum", rename_dict={}, order=[]):
    import pymysql
    import numpy as np
    import pandas as pd
    conn = pymysql.connect(host="59.110.241.144",
                          user="panjin",
                          passwd="panjin456",
                          db="brush_wine",
                          port=3306,
                          charset="utf8")
    sql = "SELECT * FROM brush_brush_single_entry WHERE `add_time`>='{}' AND `add_time`<'{}';".format(date_begin, date_end)
    try:
        df = pd.read_sql(sql, con=conn)
    except Exception as e:
        print(e)
    finally:
        conn.close()
    df = df.loc[df["deletes"]=='False', :]
    def process_nan(s):
        try:
            if s == 0:
                return ""
            else:
                return float('%.2f' % float(s))
        except:
            return s
    df = df.applymap(process_nan)
    pivottable = pd.pivot_table(df, values="payment_amount", index="shopname", columns="payment_type", aggfunc=aggfunc, fill_value=0, margins=True)
    pivottable = pivottable.reset_index()
    # 排序
    pivottable.sort_values(by="All", ascending=False, inplace=True)
    pivottable.reset_index(drop=True, inplace=True)
    if order:
        pivottable =  pivottable.loc[:, order]
    # 重命名
    pivottable.rename(columns=rename_dict, inplace=True)
    pivottable = pivottable.applymap(process_nan)
    result = pivottable.to_dict(orient="record")
    return result