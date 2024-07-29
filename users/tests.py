# tests.py

from django.db.models.query import IntegrityError
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .managers import CustomUserManager
from .models import Profile

class CustomUserManagerTests(TestCase):
    def setUp(self):
        self.User = get_user_model()

    def test_create_user(self):
        user = self.User.objects.create_user(email='test@example.com', password='testpass', username='testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpass'))

    def test_create_user_no_email(self):
        with self.assertRaises(ValueError) as context:
            self.User.objects.create_user(email='', password='testpass', username='testuser')
        self.assertEqual(str(context.exception), 'Users must have an email address')

    def test_create_user_with_duplicate_username(self):
        # Create the first user
        self.User.objects.create_user(email='first@example.com', password='testpass', username='duplicateuser')

        # Attempt to create a second user with the same username
        with self.assertRaises(ValidationError) as context:
            self.User.objects.create_user(email='second@example.com', password='testpass', username='duplicateuser')

        # Validate that a ValidationError is raised
        self.assertEqual(str(context.exception), 'UNIQUE constraint failed: users_customuser.username')

    def test_create_superuser(self):
        superuser = self.User.objects.create_superuser(email='admin@example.com', password='testpass', username='adminuser')
        self.assertEqual(superuser.email, 'admin@example.com')
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_create_superuser_no_staff(self):
        with self.assertRaises(ValueError) as context:
            self.User.objects.create_superuser(email='admin@example.com', password='testpass', username='adminuser', is_staff=False)
        self.assertEqual(str(context.exception), 'Superuser must have is_staff=True.')

    def test_create_superuser_no_superuser(self):
        with self.assertRaises(ValueError) as context:
            self.User.objects.create_superuser(email='admin@example.com', password='testpass', username='adminuser', is_superuser=False)
        self.assertEqual(str(context.exception), 'Superuser must have is_superuser=True.')

class CustomUserTests(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_user(email='test2@example.com', password='testpass', username='duplicateUser')

    def test_str_method(self):
        self.assertEqual(str(self.user), 'test2@example.com')

    def test_required_fields(self):
        with self.assertRaises(ValidationError):
            user = self.User(email='test@example.com', username='testuser')
            user.full_clean()  # This will raise a ValidationError because password is required

    def test_unique_email_constraint(self):
        self.User.objects.create_user(email='unique@example.com', password='testpass', username='uniqueuser')
        with self.assertRaises(ValidationError):
            user = self.User(email='unique@example.com', username='anotheruser')
            user.full_clean()  # This should raise a ValidationError due to unique constraint

    def test_user_manager_assignment(self):
        self.assertIsInstance(self.user.__class__.objects, CustomUserManager)  # Correct way to access the manager

    def test_profile_creation(self):
        profile1 = Profile.objects.create(user=self.user)
        self.assertEqual(profile1.user, self.user)
        self.assertIsInstance(profile1, Profile)
        # Attempt to create a second profile for the same user
        with self.assertRaises(IntegrityError):
            profile2 = Profile.objects.create(user=self.user)

    def test_user_password_hashing(self):
        self.assertNotEqual(self.user.password, 'testpass')  # Password should be hashed
        self.assertTrue(self.user.check_password('testpass'))  # Check that the password is correct
