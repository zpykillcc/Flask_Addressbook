# Python_QRCode

## 简介

Python实现的通讯录功能Flask_Addressbook @github.com](https://github.com/zpykillccdog/Flask_Addressbook) 

使用云平台 [PythonAnywhere](https://www.pythonanywhere.com/) 部署上线： http://zpykillcc.pythonanywhere.com/ 

## 环境

+ 操作系统：Ubuntu 20.04

+ python版本：3.8

+ 使用 内置的venv 模块，创建虚拟环境

  **ps: 建议使用Ubuntu系统可以直接使用仓库内的虚拟环境，win系统可能出现未知错误**  



## 使用

### Pre

```bash
$ . env/bin/activate  # 激活虚拟环境
(env) $ pip install -r requirements.txt  # 安装所有依赖
(env) $ flask initdb  # 初始化数据库
```

### Flaskenv

```bash
(env) $ vi .flaskenv
FLASK_ENV=development #可选，若上线则可删去
FLASK_APP=watchlist
```

### Pid问题

mac系统可能出现5000端口占用,修改flask运行端口号，如：

```bash
FLASK_RUN_PORT=8000
```



### 一、WebUI模式

```bash
(env) $ flask run
```

浏览器中打开127.0.0.1:5000

### 二、插件模式

直接作为python库引入watchlist包

## todo

### 用户账号功能

- [x] 用户注册功能
- [x] 用户登陆、退出功能
- [x] 用户修改密码
- [x] 用户修改头像
- [x] 用户改名
- [ ] QQ登陆接入
- [ ] 绑定邮箱功能

### 通讯录内容

- [x] 通讯录条目创建、删除、编辑
- [x] 通讯录条件查询功能
- [x] 外部接口查询电话

### 杂项

- [x] WebUI

- [x] 集成函数

- [x] 单元测试

- [x] 本地依赖检测脚本

  