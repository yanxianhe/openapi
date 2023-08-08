## 关于项目单个文件如何测试
# 在工程目录的下的测试文件 ./test/test_hmac.py
  - 请注意，不需要包括 .py 扩展名，并且使用点号 . 替代目录路径中的斜杠 /
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
page_number = 1  # 页码，从1开始
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

   文件名应该使用全小写字母。
   如果文件名包含多个单词，可以使用下划线(_)进行分隔。
### 类名：

   类名应使用驼峰命名法，即每个单词的首字母大写，不包含下划线。
   类名应该是一个名词或名词短语，而且应该具有描述性。
### 方法名：

   方法名应使用小写字母。
   如果方法名包含多个单词，可以使用下划线(_)进行分隔。

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
* 尽量避免使用缩写或简写，除非在广泛接受的情况下。使用有意义的名称来描述变量、常量和参数。
