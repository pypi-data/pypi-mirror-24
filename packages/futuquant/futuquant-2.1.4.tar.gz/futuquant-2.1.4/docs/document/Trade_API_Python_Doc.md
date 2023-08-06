#接口概要
**交易接口有频率限制，30秒内不能超过20次交易请求**


#港股交易接口

**实例化上下文对象**

```python
tradehk_ctx = OpenHKTradeContext(host='127.0.0.1', sync_port=11111)
```

**功能**：创建上下文，建立网络连接

**参数**:

**host**：网络连接地址。

**sync_port**：网络连接端口，用于同步通信。



**解锁接口 unlock_trade**

```python
ret_code, ret_data = tradehk_ctx.unlock_trade(password)
```

**功能**：

港股交易解锁。港股模拟交易不需要解锁，真实交易需要解锁

**参数**：

**password**: 用户交易密码。

**返回**：

ret_code失败时，ret_data返回为错误描述字符串；
正常情况下，ret_code为0, ret_data返回None。

**失败情况**：

1.  交易密码错误

2.  客户端内部或网络错误



**下单接口 place_order**

```python
ret_code, ret_data = tradehk_ctx.place_order(price, qty, strcode, orderside, ordertype=0, envtype=0)
```

**功能**：港股下单接口。

**参数**：

**price**: 交易价格。

**qty**: 交易数量。

**strcode**: 股票代码。例如：“HK.00700”。

**orderside**: 交易方向。如下表所示。

**ordertype**: 交易类型。**与美股不同！**如下表所示。

**envtype**: 交易环境参数。如下表所示。

| orderside | 交易方向 |
| --------- | ---- |
| 0         | 买入   |
| 1         | 卖出   |

| ordertype | 交易方向        |
| --------- | ----------- |
| 0         | 增强限价单(普通交易) |
| 1         | 竞价单(竞价交易)   |
| 3         | 竞价限价单(竞价限价) |

| envtype | 交易环境参数 |
| ------- | ------ |
| 0       | 真实交易   |
| 1       | 仿真交易   |

**返回:**

ret_code失败时，ret_data返回为错误描述字符串；
正常情况下，ret_code为0，ret_data为一个dataframe, 其中包括：

**envtype**: 交易环境参数。0是真实交易，1是仿真交易

**orderid**: 订单ID。


**失败情况**：

1. 参数错误

2. 客户端内部或网络错误

3. 不满足下单条件



**设置订单状态 set_order_status**

```python
ret_code, ret_data = tradehk_ctx.set_order_status(status, orderid=0, envtype=0)
```

**功能**：更改某指定港股订单状态。

**参数**：

**status**: 更改状态的类型。如下表所示。

**orderid**: 订单ID。

**envtype**: 交易环境参数。如下表所示。


| status | 更改状态的类型 |
| ------ | ------- |
| 0      | 撤单      |
| 1      | 失效      |
| 2      | 生效      |
| 3      | 删除      |

| envtype | 交易环境参数 |
| ------- | ------ |
| 0       | 真实交易   |
| 1       | 仿真交易   |

**返回:**

ret_code失败时，ret_data返回为错误描述字符串；
正常情况下，ret_code为0，ret_data为一个dataframe, 其中包括：

**envtype**: 交易环境参数。0是真实交易，1是仿真交易

**orderid**: 订单ID。

**失败情况**：

1. 参数错误
2. 客户端内部或网络错误
3. 订单不存在



**修改订单 change_order**

```python
ret_code, ret_data = tradehk_ctx.change_order(price, qty, orderid=0, envtype=0)
```

**功能**：修改某指定港股订单。

**参数**：

**price**: 交易价格。

**qty**: 交易数量。

**orderid**: 订单ID。

**envtype**: 交易环境参数。如下表所示。

| envtype | 交易环境参数 |
| ------- | ------ |
| 0       | 真实交易   |
| 1       | 仿真交易   |

**返回:**

ret_code失败时，ret_data返回为错误描述字符串；
正常情况下，ret_code为0，ret_data为一个dataframe, 其中包括：

**envtype**: 交易环境参数。0是真实交易，1是仿真交易

**orderid**: 订单ID。

**失败情况**：

1.  参数错误
2.  客户端内部或网络错误
3.  订单不存在



**查询账户信息 accinfo_query**

```python
ret_code, ret_data = tradehk_ctx.accinfo_query(envtype=0)
```

**功能**：查询港股账户信息。

**参数**：

**envtype**: 交易环境参数。如下表所示。

| envtype | 交易环境参数 |
| ------- | ------ |
| 0       | 真实交易   |
| 1       | 仿真交易   |

**返回:**

ret_code失败时，ret_data返回为错误描述字符串；
正常情况下，ret_code为0，ret_data为一个dataframe, 其中包括：

| 返回字符串 | 说明    | 返回字符串 | 说明    |
| ----- | ----- | ----- | ----- |
| ZQSZ  | 证券市值  | XJJY  | 现金结余  |
| KQXJ  | 可取现金  | DJZJ  | 冻结资金  |
| ZSJE  | 追收金额  | ZGJDE | 最高借贷额 |
| YYJDE | 已用借贷额 | GPBZJ | 股票保证金 |
| ZCJZ  | 资产净值  |
| Power | 现金账号的购买力，不适用于融资账号(因每支股票的融资额不同，融资账户的购买力由购买的股票决定)| 

**失败情况**：

1. 参数错误
2. 客户端内部或网络错误



**查询订单列表 order_list_query**

```python
ret_code, ret_data = tradehk_ctx.order_list_query(statusfilter="", envtype=0)
```

**功能**：查询港股今日订单列表。

**参数**：

**statusfilter**: 状态过滤字符串，为空返回全部订单，","分隔需要返回的状态，如"1,2,3"返回的是等待成交，部分成交以及全部成交的订单，状态如下表所示

| statusfilter | 返回订单的状态                  | statusfilter | 返回订单的状态  |
| :----- | :------------------------------------ | :----- | :---- |
| 0      | 服务器处理中                          | 1      | 等待成交  |
| 2      | 部分成交                              | 3      | 全部成交  |
| 4      | 已失效                                | 5      | 下单失败  |
| 6      | 已撤单                                | 7      | 已删除   |
| 8      | 等待开盘                              | 21     | 本地已发送 |
| 22     | 本地已发送，服务器返回下单失败、没产生订单 |        |       |
| 23     | 本地已发送，等待服务器返回超时       |        |       |

**envtype**: 交易环境参数。如下表所示。

| envtype | 交易环境参数 |
| ------- | ------ |
| 0       | 真实交易   |
| 1       | 仿真交易   |

**返回:**

ret_code失败时，ret_data返回为错误描述字符串；
正常情况下，ret_code为0，ret_data为一个dataframe, 其中包括：

| 返回字符串           | 说明           | 返回字符串         | 说明   |
| :-------------- | :----------- | :------------ | :--- |
| code      | 股票ID                 | stock_name    | 股票名称 |
| dealt_avg_price | 成交均价         | dealt_qty     | 成交数量 |
| localid         | 订单本地标识       | orderid       | 订单ID |
| order_type      | 交易类型         | price         | 交易价格 |
| status          | 订单状态(具体状态如下) | submited_time | 提交时间 |
| updated_time    | 更新时间         | order_side    | 交易方向 |
| qty    | 订单数量         | 

| status | 订单类型                  | status | 订单类型  |
| :----- | :-------------------- | :----- | :---- |
| 0      | 服务器处理中                | 1      | 等待成交  |
| 2      | 部分成交                  | 3      | 全部成交  |
| 4      | 已失效                   | 5      | 下单失败  |
| 6      | 已撤单                   | 7      | 已删除   |
| 8      | 等待开盘                  | 21     | 本地已发送 |
| 22     | 本地已发送，服务器返回下单失败、没产生订单 |        |       |
| 23     | 本地已发送，等待服务器返回超时       |        |       |

| order_side | 交易方向 |
| :--------- | :--- |
| 0          | 买入   |
| 1          | 卖出   |

| order_type | 交易类型        |
| ---------- | ----------- |
| 0          | 增强限价单(普通交易) |
| 1          | 竞价单(竞价交易)   |
| 3          | 竞价限价单(竞价限价) |

**失败情况**：

1. 参数错误
2. 客户端内部或网络错误



**查询持仓列表 position_list_query**

```python
ret_code, ret_data = tradehk_ctx.position_list_query(envtype=0)
```

**功能**：查询港股持仓列表。

**参数**：

**envtype**: 交易环境参数。如下表所示。

| envtype | 交易环境参数 |
| :------ | :----- |
| 0       | 真实交易   |
| 1       | 仿真交易   |

**返回:**

ret_code失败时，ret_data返回为错误描述字符串；
正常情况下，ret_code为0，ret_data为一个dataframe, 其中包括：

| 返回字符串          | 说明      | 返回字符串            | 说明             |
| :------------- | :------ | :--------------- | :------------- |
| code     | 股票ID            | stock_name       | 股票名称           |
| qty            | 持有数量    | can_sell_qty     | 可卖数量           |
| cost_price     | 成本价     | cost_price_valid | 成本价是否有效(非0有效)  |
| market_val     | 市值      | nominal_price    | 市价             |
| pl_ratio       | 盈亏比例    | pl_ratio_valid   | 盈亏比例是否有效(非0有效) |
| pl_val         | 盈亏金额    | pl_val_valid     | 盈亏金额是否有效(非0有效) |
| today_buy_qty  | 今日买入数量  | today_buy_val    | 今日买入金额         |
| today_pl_val   | 今日盈亏金额  | today_sell_qty   | 今日卖出数量         |
| today_sell_val | 今日卖出金额  |                  |                |

**失败情况**：

1. 参数错误
2. 客户端内部或网络错误



**查询成交列表 deal_list_query**

```python
ret_code, ret_data = tradehk_ctx.deal_list_query(envtype=0)
```

**功能**：查询港股今日成交列表。

**参数**：

**envtype**: 交易环境参数。如下表所示。

| envtype | 交易环境参数 |
| ------- | ------ |
| 0       | 真实交易   |
| 1       | 仿真交易   |

**返回:**

ret_code失败时，ret_data返回为错误描述字符串；
正常情况下，ret_code为0，ret_data为一个dataframe, 其中包括：

**code**: 股票代码。

**stock_name**: 股票名称。

**dealid**: 成交ID。

**orderid**: 订单ID。

**price**: 交易价格。

**qty**: 交易数量。

**orderside**: 交易方向，0表示买入，1表示卖出。

**time**: 成交时间。


**失败情况**：

1. 参数错误
2. 客户端内部或网络错误




#美股交易接口

**实例化上下文对象**

```python
tradeus_ctx = OpenUSTradeContext(host='127.0.0.1', sync_port=11111)
```

**功能**：创建上下文，建立网络连接。
**参数**:
**host**：网络连接地址
**sync_port**：网络连接端口，用于同步通信。



**解锁接口 unlock_trade**

```python
ret_code, ret_data = tradeus_ctx.unlock_trade(password)
```

**功能**：交易解锁。

**参数**：

**password**: 用户交易密码。

**返回**：
ret_code失败时，ret_data返回为错误描述字符串；
正常情况下，ret_code为0, ret_data返回None。

**失败情况**：

1.  交易密码错误
2.  客户端内部或网络错误



**下单接口 place_order**

```python
ret_code, ret_data = tradeus_ctx.place_order(price, qty, strcode, orderside, ordertype=2, envtype=0)
```

**功能**：美股下单接口。美股暂时不支持仿真交易。

**参数**：

**price**: 交易价格。

**qty**: 交易数量

**strcode**: 股票ID。例如：“US.AAPL”。

**orderside**: 交易方向。如下表所示。

**ordertype**: 交易类型。**与港股不同！**如下表所示。

**envtype**: 环境参数，0是真实环境，1是仿真环境。

| orderside | 交易方向 |
| --------- | ---- |
| 0         | 买入   |
| 1         | 卖出   |

| ordertype | 交易类型    |
| --------- | ------- |
| 1         | 市价单     |
| 2         | 限价      |
| 51        | 盘前交易、限价 |
| 52        | 盘后交易、限价 |

**返回:**

ret_code失败时，ret_data返回为错误描述字符串；
正常情况下，ret_code为0，ret_data为一个dataframe, 其中包括：

**envtype**: 环境参数，0是真实环境，1是仿真环境。
**orderid**: 订单ID。

**失败情况**：

1. 参数错误
2. 客户端内部或网络错误
3. 不满足下单条件



**设置订单状态 set_order_status**

```python
ret_code, ret_data = tradeus_ctx.set_order_status(status=0, orderid=0, envtype=0)
```

**功能**：更改某指定美股订单状态。美股暂时不支持仿真交易。

**参数**：

**status**: 美股暂时只支持撤单，status的值只能为0。

**orderid**: 订单ID。

**envtype**: 环境参数，0是真实环境，1是仿真环境。

**返回:**

ret_code失败时，ret_data返回为错误描述字符串；
正常情况下，ret_code为0，ret_data为一个dataframe, 其中包括：

**envtype**: 环境参数，0是真实环境，1是仿真环境。

**orderid**: 订单ID。

**失败情况**：

1. 参数错误
2. 客户端内部或网络错误
3. 订单不存在




**修改订单 change_order**

```python
ret_code, ret_data = tradeus_ctx.change_order(price, qty, orderid=0, envtype=0)
```

**功能**：修改某指定美股订单。美股暂时不支持仿真交易。

**参数**：

**price**: 交易价格。

**qty**: 交易数量。

**orderid**: 订单ID。

**envtype**: 环境参数，0是真实环境，1是仿真环境。

**返回:**

ret_code失败时，ret_data返回为错误描述字符串；
正常情况下，ret_code为0，ret_data为一个dataframe, 其中包括：

**envtype**: 环境参数，0是真实环境，1是仿真环境。

**orderid**: 订单ID。

**失败情况**：

1.  参数错误
2.  客户端内部或网络错误
3.  订单不存在



**查询账户信息 accinfo_query**

```python
ret_code, ret_data = tradeus_ctx.accinfo_query(envtype=0)
```

**功能**：查询美股账户信息。美股暂时不支持仿真环境

**参数**：

**envtype**: 环境参数，0是真实环境，1是仿真环境。

**返回:**

ret_code失败时，ret_data返回为错误描述字符串；
正常情况下，ret_code为0，ret_data为一个dataframe, 其中包括：

| 返回字符串 | 说明    | 返回字符串 | 说明    |
| ----- | ----- | ----- | ----- |
| Power | 购买力   | ZCJZ  | 资产净值  |
| ZQSZ  | 证券市值  | XJJY  | 现金结余  |
| KQXJ  | 可取现金  | DJZJ  | 冻结资金  |
| ZSJE  | 追收金额  | ZGJDE | 最高借贷额 |
| YYJDE | 已用借贷额 | GPBZJ | 股票保证金 |

**失败情况**：

1. 参数错误
2. 客户端内部或网络错误



**查询订单列表 order_list_query**

```python
ret_code, ret_data = tradeus_ctx.order_list_query(statusfilter="", envtype=0)
```

**功能**：查询美股今日订单列表。美股暂时不支持仿真环境。

**参数**：

**statusfilter**: 状态过滤字符串，默认为空返回全部订单，","分隔需要返回的状态，如"1,2,3"返回的是等待成交，部分成交以及全部成交的订单，如下表所示

| statusfilter | 返回订单的状态                  | statusfilter | 返回订单的状态  |
| :----- | :------------------------------------ | :----- | :---- |
| 0      | 服务器处理中                          | 1      | 等待成交  |
| 2      | 部分成交                              | 3      | 全部成交  |
| 4      | 已失效                                | 5      | 下单失败  |
| 6      | 已撤单                                | 7      | 已删除   |
| 8      | 等待开盘                              | 21     | 本地已发送 |
| 22     | 本地已发送，服务器返回下单失败、没产生订单 |        |       |
| 23     | 本地已发送，等待服务器返回超时       |        |       |

**envtype**: 环境参数，0是真实环境，1是仿真环境。

**返回:**

ret_code失败时，ret_data返回为错误描述字符串；
正常情况下，ret_code为0，ret_data为一个dataframe, 其中包括：

| 返回字符串           | 说明           | 返回字符串         | 说明   |
| :-------------- | :----------- | :------------ | :--- |
| code      | 股票ID                 | stock_name    | 股票名称 |
| dealt_avg_price | 成交均价         | dealt_qty     | 成交数量 |
| localid         | 订单本地标识       | orderid       | 订单ID |
| order_type      | 交易类型         | price         | 交易价格 |
| status          | 订单状态(具体状态如下) | submited_time | 提交时间 |
| updated_time    | 更新时间         | order_side    | 交易方向 |
| qty    | 订单数量         | 

| status | 订单类型                  | status | 订单类型  |
| :----- | :-------------------- | :----- | :---- |
| 0      | 服务器处理中                | 1      | 等待成交  |
| 2      | 部分成交                  | 3      | 全部成交  |
| 4      | 已失效                   | 5      | 下单失败  |
| 6      | 已撤单                   | 7      | 已删除   |
| 8      | 等待开盘                  | 21     | 本地已发送 |
| 22     | 本地已发送，服务器返回下单失败、没产生订单 |        |       |
| 23     | 本地已发送，等待服务器返回超时       |        |       |

| order_side | 交易方向 |
| :--------- | :--- |
| 0          | 买入   |
| 1          | 卖出   |

| order_type | 交易类型    |
| ---------- | ------- |
| 1          | 市价单     |
| 2          | 限价      |
| 51         | 盘前交易、限价 |
| 52         | 盘后交易、限价 |

**失败情况**：

1. 参数错误
2. 客户端内部或网络错误



**查询持仓列表 position_list_query**

```python
ret_code, ret_data = tradeus_ctx.position_list_query(envtype=0)
```

**功能**：查询美股持仓列表。美股暂时不支持仿真环境。

**参数**：

**envtype**: 环境参数，0是真实环境，1是仿真环境。

**返回:**

ret_code失败时，ret_data返回为错误描述字符串；
正常情况下，ret_code为0，ret_data为一个dataframe, 其中包括：

| 返回字符串          | 说明      | 返回字符串            | 说明             |
| :------------- | :------ | :--------------- | :------------- |
| code     | 股票ID            | stock_name       | 股票名称           |
| qty            | 持有数量    | can_sell_qty     | 可卖数量           |
| cost_price     | 成本价     | cost_price_valid | 成本价是否有效(非0有效)  |
| market_val     | 市值      | nominal_price    | 市价             |
| pl_ratio       | 盈亏比例    | pl_ratio_valid   | 盈亏比例是否有效(非0有效) |
| pl_val         | 盈亏金额    | pl_val_valid     | 盈亏金额是否有效(非0有效) |
| today_buy_qty  | 今日买入数量  | today_buy_val    | 今日买入金额         |
| today_pl_val   | 今日盈亏金额  | today_sell_qty   | 今日卖出数量         |
| today_sell_val | 今日卖出金额  |                  |                |

**失败情况**：

1. 参数错误
2. 客户端内部或网络错误

**查询成交列表 deal_list_query**

```python
ret_code, ret_data = tradeus_ctx.deal_list_query(envtype=0)
```

**功能**：查询美股今日成交列表。美股暂时不支持仿真环境。

**参数**：

**envtype**: 环境参数，0是真实环境，1是仿真环境。

**返回:**

ret_code失败时，ret_data返回为错误描述字符串；
正常情况下，ret_code为0，ret_data为一个dataframe, 其中包括：

**code**: 股票代码。

**stock_name**: 股票名称。

**dealid**: 成交ID。

**orderid**: 订单ID。

**price**: 交易价格。

**qty**: 交易数量。

**orderside**: 交易方向，0表示买入，1表示卖出。

**time**: 成交时间。


**失败情况**：

1. 参数错误
2. 客户端内部或网络错误

