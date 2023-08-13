



## 项目结构

~~~~~~
.
├── controllers                  # 控制层 目录
│   ├── auth_controllers.py      # 从HTTP请求中获取信息,提取参数
├── logs                         # 日志存放 目录
├── main.py                      # 入口主方法将请求分发给不同的控制层
├── modules                      # 实体模型 目录 
│   ├── db_client.py             # db_client 连接实例化
│   ├── module_route.py          # 关系映射及数据操作
├── public                       # 公共 目录
│   ├── metadata.py              # 定义接口 metadata 提示
│   ├── sys_logs.py              # 封装日志
│   ├── system.py                # 系统级别配置
│   └── utils.py                 # 公共算法
├── README.md
├── run.sh                       # 运行脚本
├── shell                        # 脚本目录
│   ├── Dockerfile               # 项目制作镜像
│   ├── haikang
│   │   ├── Dockerfile
│   │   ├── haikangapi.py
│   │   ├── requirements.txt
│   │   └── test.py
├── sql                          # sql 脚本目录
│   └── user.sql
└── test                         # test 脚本目录
    ├── alert_message_ddl.sql
    └── test_hmac.py

~~~~~~


_ main 文件主要是程序入口,将其他方法注册到主文件中.其他层托管其他地方处理.
- 添加接口 需要在 main 文件中注册 *控制层中的具体方法*
- 如：将controllers 目录下的auth_controllers文件中 auth_controllers_ping 方法注册到主方法中

~~~~~~

## controllers
from controllers import auth_controllers
# 将controllers文件的函数注册到当前全局命名空间中
globals()[auth_controllers.auth_controllers_ping.__name__] = auth_controllers.auth_controllers_ping

~~~~~~

- 将 auth_controllers_ping 绑定到接口中 (interfaces) 

~~~~~~
INSERT INTO `interfaces` (transaction_id,name,path, method, controller,system_id,tags, description)
VALUES ('ZR00001','探针','/api/ping', 'GET', 'auth_controllers_ping','ZR0001','ping','测试系统探针');
~~~~~~

- 以上添加 服务探针接口, 请求方式是 GET 请求路径为 /api/ping.具体请求参数在 auth_controllers_ping 方法中处理.
- 关于 controllers 层命名以文件名_具体方法名.禁止 controllers 中有重复的方法名及整改项目禁止方法名重复[原因工程使用方法名注入]


## 关于项目单个文件如何测试
# 在工程目录的下的测试文件 ./test/test_hmac.py
  - 请注意,不需要包括 .py 扩展名,并且使用点号 . 替代目录路径中的斜杠 /
  - 进入项目目录 执行
    ~~~~~~
    # ./test/test_hmac.py
    python3 -m test.test_hmac
    # ./modules/module_route.py
    python3 -m modules.module_route
    ~~~~~~

## 关于日志

### 使用 logure 中的 logger
   - 系统环境变量定义 LOG_LEVEL 设置logs 日志级别 debug info success error 默认DEBUG
   ~~~~~~
   echo "LOG_LEVEL=info">> ~/.bashrc
   ~~~~~~
   - 日志存放位置在项目下的logs文件中


## 关于关系型数据库

### 关系数据库使用sqlalchemy orm 
   - 需要依赖pymysql
   - 需要创建 MySQLdb 别名以便与 SQLAlchemy 兼容 ORM
   ~~~~~~ 
   # 以便与 SQLAlchemy 兼容 ORM
   import pymysql
   pymysql.install_as_MySQLdb() 
   ~~~~~~ 
### 简单操作

~~~~~~
# # 插入数据
 new_entry = Route(transaction_id='xx',name='yy',……)
 session.add(new_entry)
 session.commit()
# # 查询数据
 results = session.query(Route).all()
# # 更新数据
 entry = session.query(Route).filter_by(transaction_id=1).first()
 entry.name = 'Updated Name'
 session.commit()
# # 删除数据
 entry = session.query(Route).filter_by(transaction_id=1).first()
 session.delete(entry)
 session.commit()
# # 分页查询
page_size = 20  # 每页的记录数
page_number = 1  # 页码,从1开始
# 计算偏移量
offset = (page_number - 1) * page_size
# 查询数据并进行分页
results = session.query(Route).offset(offset).limit(page_size).all()
# # 原生sql
 result = session.execute("SELECT * FROM interfaces WHERE name = :name", {"name": "张三"})
# # 查询关联表数据
 users_with_addresses = session.query(User, Address).filter(User.id == Address.user_id).all()
~~~~~~

## 关于非系型数据库

### 关系数据库使用 redis

## 文件名、类名和方法名的规范
### 文件名：

   文件名应该使用全小写字母.
   如果文件名包含多个单词,可以使用下划线(_)进行分隔.
### 类名：

   类名应使用驼峰命名法,即每个单词的首字母大写,不包含下划线.
   类名应该是一个名词或名词短语,而且应该具有描述性.
### 方法名：

   方法名应使用小写字母.
   如果方法名包含多个单词,可以使用下划线(_)进行分隔.

* 列如:

~~~~~~
# 文件名：my_module.py
class MyClass:
    def do_something(self):
        # 方法体
        pass

def my_function():
    # 函数体
    pass

~~~~~~

* 其他注意事项：
* 尽量避免使用缩写或简写,除非在广泛接受的情况下.使用有意义的名称来描述变量、常量和参数.
