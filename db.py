import sqlite3


class Database:
    def __init__(self):
        # 连接数据库
        self.conn = sqlite3.connect('flask-layui.sqlite')
        # 设置数据的解析方法，有了这个设置，就可以像字典一样访问每一列数据
        self.conn.row_factory = sqlite3.Row

        # connect('服务器名称', '用户名', '密码', '库名')

        # import pymysql #MySQL
        # self.conn = pymysql.connect(host='localhost', user='root', password='root', database='School', charset='utf8')

        # import pymssql #SQLServer
        # self.conn = pymssql.connect('(local)','sa','123456','School')

        # 创建游标对象
        self.cursor = self.conn.cursor()

    def create_table(self):
        sql = """  create table  IF NOT EXISTS user
            (
                id       integer primary key,
                nickname varchar(255),
                mobile   varchar(50),
                password varchar(50)    
            );
            """
        self.cursor.execute(sql)
        self.conn.commit()

    def insert(self, nickname, mobile, password):
        sql = 'insert into user(nickname, mobile, password) values (?, ?, ?);'
        self.cursor.execute(sql, (nickname, mobile, password))
        self.conn.commit()

    def search(self, mobile):
        sql = 'select * from user where mobile=?;'
        self.cursor.execute(sql, (mobile,))
        return self.cursor.fetchone()

    def search_uid(self, uid):
        sql = 'select nickname from user where id=?;'
        self.cursor.execute(sql, (uid,))
        return self.cursor.fetchone()

    def create_blog(self):
        sql = """
        create table IF NOT EXISTS blog
        (
            id integer primary key,
            uid integer(32),
            created timestamp not null default current_timestamp,
            title text not null,
            content text not null,
            tags varchar(50),
            category varchar(50)  
        );  
        """

        self.cursor.execute(sql)
        self.conn.commit()

    def insert_blog(self, uid, title, content, tags, category):
        sql = 'insert into blog(uid, title, content, tags, category) values (?, ?, ?, ?, ?);'
        self.cursor.execute(sql, (uid, title, content, tags, category))
        self.conn.commit()

    def search_blogs(self, uid):
        sql = 'select * from blog where uid=?;'
        self.cursor.execute(sql, (uid,))
        return self.cursor.fetchall()

    def search_bid(self, bid):
        sql = 'select * from blog where id=?;'
        self.cursor.execute(sql, (bid,))
        return self.cursor.fetchone()

    def delete_bid(self, bid):
        sql = 'delete from blog where id=?;'
        self.cursor.execute(sql, (bid,))
        self.conn.commit()

    def update_bid(self, title, content, tags, category, id):
        sql = 'update blog set title=?, content=?, tags=?, category=? where id=?;'
        self.cursor.execute(sql, (title, content, tags, category, id))
        self.conn.commit()


db = Database()

if __name__ == '__main__':
    db.create_table()
    db.insert('博主', '13838383838', '123456')
    ret = db.search('13838383838')
    print(ret['password'])

    import hashlib

    def md5_encryption(data):
        md5 = hashlib.md5()  # 创建一个md5对象
        md5.update(data.encode('utf-8'))  # 使用utf-8编码数据
        return md5.hexdigest()  # 返回加密后的十六进制字符串

    print(md5_encryption(ret['password']))
    db.create_blog()
    db.insert_blog(1, '学习Flask1', 'Python课程设计学习flask第一部分', 11, 111)
    db.insert_blog(1, '学习Flask2', 'Python课程设计学习flask第二部分', 22, 222)
