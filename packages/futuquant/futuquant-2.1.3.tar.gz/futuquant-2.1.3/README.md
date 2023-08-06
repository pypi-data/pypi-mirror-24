# FutuQuant - 富途量化投资平台 (Futu Quant Trading API)

### 简介

​**FutuQuant**开源项目可以满足使用[**富途牛牛**](http://www.futunn.com/)软件进行量化投资的需求, 提供包括Python接口、Json接口的行情及交易的API。

-------------------
### 安装
```
pip install futuquant
```

### 使用
```
import 
```

---

### 富途牛牛行情交易API入门指引
### [点击查看](https://github.com/FutunnOpen/futuquant/blob/master/docs/document/Futunn_API_Intro.md)

---

### 组织结构

![image](https://github.com/FutunnOpen/futuquant/raw/master/docs/resources/Structure.png)

​	最新版本在master分支。之前各版本在其他分支上。

---

### API与富途牛牛客户端架构

![image](https://github.com/FutunnOpen/futuquant/raw/master/docs/resources/API.png)

***

### 使用须知

- 限定使用有API后缀的安装包。不要去掉勾选“安装量化交易插件API”选项。
- 无需拷贝对应的dll插件。
- 安装成功后直接使用接口进行行情获取或者交易操作。

---

### 历史数据及除权除息下载问题
### [历史K线下载指引](https://github.com/FutunnOpen/futuquant/blob/master/docs/document/Hist_KLine_Download_Intro.md)

- 在富途牛牛安装目录的plugin文件夹内有历史数据下载配置文件(ftplugin.ini)，请先详细阅读再进行操作。
- 如果不想下载新数据、可以将开始时间和暂停下载时间设置为相同时间。
- 如果选择下载的数据越大，下载所需时间越长。如果中途退出，下次开启时将重新下载。请勿在下载过程中关闭牛牛客户端。

***

### 客户端下载及交流方式

* 富途开放API群(108534288)    群文件 >富途牛牛客户端(API接口专用版本)

  ![image](https://github.com/FutunnOpen/futuquant/raw/master/docs/resources/Download.png)

* <https://github.com/FutunnOpen/futuquant/issues>


***

### 使用说明

* 有任何问题可以到 issues  处提出，我们会及时进行解答。
* 使用新版本时请先仔细阅读接口文档，大部分问题都可以在接口文档中找到你想要的答案。
* 欢迎大家提出建议、也可以提出各种需求，我们一定会尽量满足大家的需求。

