import unittest
from apps import create_app, db
from apps.models import User, Post
from apps.config import TestConfig

class DataTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_registration(self):
        response = self.client.post('/registration', data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password',
            'confirmPassword': 'password'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sign In / Log In', response.data)
        self.assertIsNotNone(User.query.filter_by(username='testuser').first())
        self.assertIsNotNone(User.query.filter_by(email='test@example.com').first())

    def test_user_login(self):
        u = User(username='testuser', email='test@example.com')
        u.set_password('password')
        db.session.add(u)
        db.session.commit()

        response = self.client.post('/login', data={
            'email': 'test@example.com',
            'password': 'password'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Log Out', response.data)

    def test_create_post(self):
        u = User(username='testuser', email='test@example.com')
        u.set_password('password')
        db.session.add(u)
        db.session.commit()

        self.client.post('/login', data={
            'email': 'test@example.com',
            'password': 'password'
        }, follow_redirects=True)

        response = self.client.post('/create_post', data={
            'title': 'Test Post',
            'content': 'This is a test post content.'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'This is a test post content.', response.data)
        self.assertIsNotNone(Post.query.filter_by(title='Test Post').first())

    def test_display_posts(self):
        u = User(username='testuser', email='test@example.com')
        u.set_password('password')
        db.session.add(u)
        db.session.commit()

        post1 = Post(title='Test Post 1', content='This is the first test post.', user=u)
        post2 = Post(title='Test Post 2', content='This is the second test post.', user=u)
        db.session.add(post1)
        db.session.add(post2)
        db.session.commit()

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'This is the first test post.', response.data)
        self.assertIn(b'This is the second test post.', response.data)

if __name__ == '__main__':
    unittest.main()
