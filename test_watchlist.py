import unittest

from watchlist import app, db
from watchlist.models import Movie, User
from watchlist.commands import forge, initdb


class WatchlistTestCase(unittest.TestCase):

    def setUp(self):
        # 更新配置
        app.config.update(
            TESTING=True,
            SQLALCHEMY_DATABASE_URI='sqlite:///:memory:'
        )
        # 创建数据库和表

        ctx = app.app_context()
        ctx.push()
        db.create_all()
        # 创建测试数据，一个用户，一个电影条目
        user = User(username='test',image_hash='default.png',)
        user.set_password('123')
        movie = Movie(name='Test person', sex='男',phone='12345678912',qq='123456789',user_id = 1)
        # 使用 add_all() 方法一次添加多个模型类实例，传入列表
        db.session.add_all([user, movie])
        db.session.commit()

        self.client = app.test_client()  # 创建测试客户端
        self.runner = app.test_cli_runner()  # 创建测试命令运行器

    def tearDown(self):
        db.session.remove()  # 清除数据库会话
        db.drop_all()  # 删除数据库表

    # 测试程序实例是否存在
    def test_app_exist(self):
        self.assertIsNotNone(app)

    # 测试程序是否处于测试模式
    def test_app_is_testing(self):
        self.assertTrue(app.config['TESTING'])


    def test_404_page(self):
        response = self.client.get('/nothing')  # 传入目标 URL
        data = response.get_data(as_text=True)
        self.assertIn('Page Not Found - 404', data)
        self.assertIn('Go Back', data)
        self.assertEqual(response.status_code, 404)  # 判断响应状态码

    # 测试主页
    def test_index_page(self):
        response = self.client.get('/')
        data = response.get_data(as_text=True)
        self.assertIn('通讯录', data)
        self.assertEqual(response.status_code, 200)
    
    def login(self):
        self.client.post('/login', data=dict(
            username='test',
            password='123'
        ), follow_redirects=True)


    def test_register(self):
        # 测试注册用户
        response = self.client.post('/register', data=dict(
            username='new_test',
            password='123',
            repeatpassword = '123'
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('登陆成功.', data)
        """
        #测试注册用户名存在
        response = self.client.post('/register', data=dict(
            username='test',
            password='123',
            repeatpassword = '123'
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('登陆成功.', data)
        self.assertIn('用户名已存在!', data)

        #测试注册两次密码不同
        response = self.client.post('/register', data=dict(
            username='new_test',
            password='123',
            repeatpassword = '124'
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('登陆成功.', data)
        self.assertIn('两次密码输入不同!', data)
        """
    def test_create_item(self):
        self.login()

        # 测试创建条目操作
        response = self.client.post('/', data=dict(
            name='New person',
            sex='男',
            phone = '123456789',
            qq = '123456777'
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('创建联系人成功.', data)

        # 测试创建条目操作，但电影标题为空
        response = self.client.post('/', data=dict(
            name='',
            sex='男',
            phone = '123456789',
            qq = '123456777'
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('创建联系人成功.', data)
        self.assertIn('Invalid input.', data)

        # 测试创建条目操作，但电影年份为空
        response = self.client.post('/', data=dict(
            name='New person',
            sex='',
            phone = '123456789',
            qq = '123456777'
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('创建联系人成功.', data)
        self.assertIn('Invalid input.', data)

    def test_update_item(self):
        self.login()

        # 测试更新页面
        response = self.client.get('/movie/edit/1')
        data = response.get_data(as_text=True)
        self.assertIn('Edit item', data)
        self.assertIn('Test person', data)
        self.assertIn('男', data)

        # 测试更新条目操作
        response = self.client.post('/movie/edit/1', data=dict(
            name='New person',
            sex='男',
            phone = '123456789',
            qq = '123456777'
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('更新联系人成功.', data)
    

        # 测试更新条目操作，但电影标题为空
        response = self.client.post('/movie/edit/1', data=dict(
            name='',
            sex='男',
            phone = '123456789',
            qq = '123456777'
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('更新联系人成功.', data)
        self.assertIn('Invalid input.', data)

        # 测试更新条目操作，但电影年份为空
        response = self.client.post('/movie/edit/1', data=dict(
            name='New person',
            sex='',
            phone = '123456789',
            qq = '123456777'
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('更新联系人成功.', data)
        self.assertNotIn('New Movie Edited Again', data)
        self.assertIn('Invalid input.', data)

    # 测试删除条目
    def test_delete_item(self):
        self.login()

        response = self.client.post('/movie/delete/1', follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('删除联系人成功.', data)
        self.assertNotIn('Test Movie Title', data)

    


    def test_login_protect(self):
        response = self.client.get('/')
        data = response.get_data(as_text=True)
        self.assertNotIn('退出', data)
        self.assertNotIn('设置', data)
        self.assertNotIn('<form method="post">', data)
        self.assertNotIn('Delete', data)
        self.assertNotIn('Edit', data)

    # 测试登录
    def test_login(self):
        response = self.client.post('/login', data=dict(
            username='test',
            password='123'
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('登陆成功.', data)
        self.assertIn('退出', data)
        self.assertIn('设置', data)
        self.assertIn('Delete', data)
        self.assertIn('Edit', data)
        self.assertIn('<form method="post">', data)
        """
        # 测试使用错误的密码登录
        response = self.client.post('/login', data=dict(
            username='test',
            password='456',
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('登陆成功.', data)
        self.assertIn('用户名错误或密码错误.', data)

        # 测试使用错误的用户名登录
        response = self.client.post('/login', data=dict(
            username='wrong',
            password='123'
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('登陆成功.', data)
        self.assertIn('用户名错误或密码错误.', data)

        # 测试使用空用户名登录
        response = self.client.post('/login', data=dict(
            username='',
            password='123'
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('登陆成功.', data)
        self.assertIn('Invalid input.', data)

        # 测试使用空密码登录
        response = self.client.post('/login', data=dict(
            username='test',
            password=''
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('登陆成功.', data)
        self.assertIn('Invalid input.', data)
        """
    # 测试登出
    def test_logout(self):
        self.login()

        response = self.client.get('/logout', follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Goodbye.', data)
        self.assertNotIn('退出', data)
        self.assertNotIn('设置', data)
        self.assertNotIn('Delelte', data)
        self.assertNotIn('Edit', data)
        self.assertNotIn('<form method="post">', data)

    # 测试设置
    def test_settings(self):
        self.login()

        # 测试设置页面
        response = self.client.get('/settings')
        data = response.get_data(as_text=True)
        self.assertIn('设置', data)
        self.assertIn('用户名', data)

        # 测试更新设置
        response = self.client.post('/settings', data=dict(
            name='Grey Li',
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('设置更改成功.', data)
        self.assertIn('Grey Li', data)

        # 测试更新设置，名称为空
        response = self.client.post('/settings', data=dict(
            name='',
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('设置更改成功.', data)
        self.assertIn('Invalid input.', data)

 

    # 测试初始化数据库
    def test_initdb_command(self):
        result = self.runner.invoke(initdb)
        self.assertIn('Initialized database.', result.output)

 
if __name__ == '__main__':
    unittest.main()