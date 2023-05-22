# <center> FastAPI-Vue </center>

## 简介

> 在gitee平台好像看不到图片，可以去[CSDN(https://blog.csdn.net/sinat_34149445/article/details/127975155)](https://blog.csdn.net/sinat_34149445/article/details/127975155)查看图片 

[**GITHUB**:  https://github.com/JohnDoe1996/fastAPI-vue.git](https://github.com/JohnDoe1996/fastAPI-vue.git)

[**GITEE**:  https://gitee.com/zy1234500/fastAPI-vue](https://gitee.com/zy1234500/fastAPI-vue)

FastAPI-Vue是个人开发并使用的CURD模板之一，代码功能不难，主要是减少浪费时间在用户系统的开发。
fastAPI的性能在Python中还算挺不错的，使用起来也很方便。github上也有其他fastAPI和vue组合的代码，个人觉得不是很符合我自己，然后就自己开发了一套，现开源共享出来。
后端项目的目录结构借鉴了Django的目录结构。前端Vue代码使用了Ruoyi的Vue代码。
大部分功能和若依相似，但是在原基础上删除了我个人认为用得很少的 部门 模块。并在原基础上加上了用户注册功能。

### 运行截图


![登录页面](https://img-blog.csdnimg.cn/7547dcfaaf494d0e8136bf7bc4a6c717.png)

![仪表盘页面](https://img-blog.csdnimg.cn/f4d74fc8b3eb4c1a92e84d933f4f701a.png)

![菜单管理页面](https://img-blog.csdnimg.cn/b0e4f2c111724ed5b67a2792fc284780.png)


## Demo

### URL: 

- web: [http://fastapi-vue.beginner2020.top](http://fastapi-vue.beginner2020.top)
- api-doc: [http://fastapi-vue-api.beginner2020.top/docs](http://fastapi-vue-api.beginner2020.top/docs)

### 账号:

| 角色 | 用户名 | 密码 |
| ----| ---- | ---- |
| 管理员 | admin |  admin123 |
| 运维员 | opt |  opt123 |
| 普通用户 | user | 123456 |


## 更新日志  

> 感谢各个平台中给我问题反馈和优化方案的朋友们。

- 1.0.1 (20230514)
1. 修复sql_init.sql执行报错(sql语句建表顺序问题)
2. 修复requirements.txt中jinja拼写错误
3. 修复get_uuid函数生成uuid不带- 
4. 新增celery 异步处理函数的模板以及定时任务的支持
5. 新增flask jsonable_encoder  custom_encoder函数(dict直出，datatime直出，datatime输出格式化字符串)
6. 修复READMR.md中前端部署的错误部分
7. 修复登录页面记住密码报错的bug

- 1.0.0 (base)
1. 初始上传项目

## 项目部署

> 注意：
> 本源码中所有配置文件都使用 配置文件模板(.example)的形式上传, 目的是为了方便我自己的配置信息不被泄露。
> 部署项目时需要把.example后缀去掉才能使用。需要用到配置文件的地方均在后续说明有列出。

### FIRST
克隆项目主分支
```shell
git clone -b main https://github.com/JohnDoe1996/fastAPI-vue.git
```
数据库中创建DB
```sql
CREATE DATABASE fastapi_vue;  -- 仅供参考根据自己项目名和所用的数据库类型 修改SQL， 
```
导入初始化sql数据到数据库
```sql
USE fastapi_vue;
SOURCE init_data.sql;   -- 仅供参考
```

### APP

1. 安装python3、virtualenv、Nginx、 supervisor
```shell
# 略
```

2. 安装必要第三方库
```shell
cd ./fastAPI-vue/backend/app   # 进入到后端程序代码的根目录

python3 -m virtualenv venv     # 创建虚拟环境

source ./venv/bin/activate      # 进入虚拟环境

pip install -r requirements.txt   # 安装库  可使用谷内源：  -i https://pypi.tuna.tsinghua.edu.cn/simple
```

3. 准备程序配置文件 
```shell
cp ./configs/.env.example  ./configs.env    # 复制配置模板

vim ./configs/.env     # 拷贝配置文件

# python main.py   # 测试项目是否成功运行，
```
> 根据需要修改.env的配置内容，配置所有的参数参考 ./core/config.py -> class Settings

4. 使用supervisor管理项目(生产环境)
```shell
cp ./configs/supervisor.conf.example  ./configs/supervisor.conf   # 拷贝配置文件

sudo ln -s /home/ubuntu/opt/fastAPI-vue/backend/app/configs/supervisor.conf /etc/supervisor/conf.d/fastapi_vue_backend.conf   # 配置文件软链到supervisor的配置文件目录， 此处目录路径仅供参考

vim ./configs/supervisor.conf    # 编辑配置文件,已有参考配置，按需修改

sudo supervisorctl update     # 更新supervisor

sudo supervisorctl start fastapi-backend:   # 启动项目
```

### WEB
1. 安装node、npm
```shell
# 略
```

2. 安装相关第三方包
```shell
cd ./fastAPI-vue/frontend/dashborad   # 进入项目目录

npm i  # 安装包
```

3. 开发环境配置
```shell
cp .env.development.example .env.development  # 复制配置文件

vim .env.development  # 编辑配置文件

npm run dev    # 测试运行程序 
```

4. 生产环境配置
```shell
cp .env.production.example .env.production  # 复制配置文件

vim .env.production  # 编辑配置文件

npm run build:stage  # 打包项目文件 (可以考虑在本地打包后把dies文件上传服务器部署)
```


### NGINX
使用Nginx反向代理后端项目和前端文件夹。
```shell
cd ./fastAPI-vue  # 进入项目根目录，此处目录仅供参加

cp ./nginx.conf.example  ./nginx.conf   # 拷贝配置文件

sudo ln -s /home/ubuntu/opt/fastAPI-vue/nginx.conf /etc/nginx/sites-enabled/fastapi_vue.conf   # 配置文件软链到Nginx的配置文件目录， 此处目录路径仅供参考

vim ./nginx.conf    # 编辑配置文件,已有参考配置，按需修改

nginx -t   # 检查Nginx配置文件 

nginx -s reload   # 重启Nginx
```

## 写在最后

### 展望
本代码只是一个初始项目代码，用于防止重复造轮子，本人想用这个模板代码开发自己的物联网、数据处理等项目，有机会的话也分享给大家。后期打算加入 websocket celery 等相关代码，同事有打算增加Flask Tornado Sanic 以及TypeScrip版本。敬请期待。

### 捐赠
开发不容如果觉得源码对你有帮助可以帮我出那么一点服务器费用。一分钱也是爱噢，哈哈哈哈~
<div style="max-width: 100px; display: flex;">

<img style="padding: 3px"  src='http://fastapi-vue.beginner2020.top/alipay.jpg'/>

<img style="padding: 3px" src='http://fastapi-vue.beginner2020.top/wechatpay.jpg'/>


</div>



### 反馈
源码可能还存在着不完善的地方，欢迎加QQ群反馈或者直接提issue，也欢迎直接贡献代码。
![](http://fastapi-vue.beginner2020.top/qqqun.jpg)

### 版权
前端VUE代码使用若依修改vue-element-admin的进行修改，版权参照他们的版权。
后端FastAPI代码为个人开发，可供学习和商用，禁止直接转卖代码，转载代码请带上出处。

### 致谢
- FastAPI
- vue
- element
- vue-element-admin
- 若依Ruoyi
