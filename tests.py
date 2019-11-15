from datetime import datetime, timedelta
import unittest

from app import flask_app, db
from app.models import User, Post


class UserModelCase(unittest.TestCase):
    def setUp(self):
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        user = User(username='test')
        user.set_password('password')
        self.assertFalse(user.check_password('pass'))
        self.assertTrue(user.check_password('password'))

    def test_follow(self):
        user1 = User(username='john', email='john@email.com')
        user2 = User(username='susan', email='susan@email.com')
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
        self.assertEqual(user1.followed.all(), [])
        self.assertEqual(user2.followed.all(), [])

        user1.follow(user2)
        db.session.commit()
        self.assertTrue(user1.is_following(user2))
        self.assertEqual(user1.followed.count(), 1)
        self.assertEqual(user1.followed.first().username, 'susan')
        self.assertEqual(user2.followers.count(), 1)
        self.assertEqual(user2.followers.first().username, 'john')

        user1.unfollow(user2)
        db.session.commit()
        self.assertFalse(user1.is_following(user2))
        self.assertEqual(user1.followed.count(), 0)
        self.assertEqual(user2.followers.count(), 0)

    def test_follow_posts(self):
        user1 = User(username='john', email='john@example.com')
        user2 = User(username='susan', email='susan@example.com')
        user3 = User(username='mary', email='mary@example.com')
        user4 = User(username='david', email='david@example.com')
        db.session.add_all([user1, user2, user3, user4])

        now = datetime.utcnow()
        post1 = Post(body='post from john', author=user1, timestamp=now + timedelta(seconds=1))
        post2 = Post(body='post from susan', author=user2, timestamp=now + timedelta(seconds=4))
        post3 = Post(body='post from mary', author=user3, timestamp=now + timedelta(seconds=2))
        post4 = Post(body='post from david', author=user4, timestamp=now + timedelta(seconds=5))
        db.session.add_all([post1, post2, post3, post4])
        db.session.commit()

        user1.follow(user2)
        user1.follow(user4)
        user2.follow(user3)
        user3.follow(user4)
        db.session.commit()

        f1 = user1.followed_posts().all()
        f2 = user2.followed_posts().all()
        f3 = user3.followed_posts().all()
        f4 = user4.followed_posts().all()

        self.assertEqual(f1, [post4, post2, post1])
        self.assertEqual(f2, [post2, post3])
        self.assertEqual(f3, [post4, post3])
        self.assertEqual(f4, [post4])


if __name__ == '__main__':
    unittest.main(verbosity=2)
