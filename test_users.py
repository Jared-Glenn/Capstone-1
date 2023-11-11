import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Code

os.environ['DATABASE_URL'] = "postgresql:///qrcoder"

from app import app

db.create_all()

class UserModelTestCase(TestCase):
    """Test users."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Code.query.delete()

        self.client = app.test_client()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            first_name="first",
            last_name="last",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.codes), 0)
        
    def test_repr(self):
        """Does the repr function work?"""
        
        u = User(
            email="test@test.com",
            username="testuser",
            first_name="first",
            last_name="last",
            password="HASHED_PASSWORD"
        )
        
        db.session.add(u)
        db.session.commit()
        
        self.assertEqual(u.email, "test@test.com")
        self.assertEqual(u.username, "testuser")
        self.assertEqual(u.first_name, "first")
        self.assertEqual(u.last_name, "last")
        self.assertEqual(u.password, "HASHED_PASSWORD")
        
    
    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()
        
