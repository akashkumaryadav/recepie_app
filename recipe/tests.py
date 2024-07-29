from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Recipe, RecipeCategory, RecipeLike, get_default_recipe_category
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

class RecipeCategoryModelTest(TestCase):
    def setUp(self):
        self.category = RecipeCategory.objects.create(name='Desserts')

    def test_recipe_category_creation(self):
        self.assertEqual(self.category.name, 'Desserts')
        self.assertEqual(str(self.category), 'Desserts')

    def test_get_default_recipe_category(self):
            default_category = get_default_recipe_category()
            self.assertEqual(default_category.name, 'Others')
            another_default_category = get_default_recipe_category()
            self.assertEqual(default_category.id, another_default_category.id)

class RecipeModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email="testuser@example.com", password='testpass')
        self.category = RecipeCategory.objects.create(name='Main Course')
        self.recipe = Recipe.objects.create(
            author=self.user,
            category=self.category,
            picture='uploads/test.jpg',
            title='Test Recipe',
            desc='This is a test recipe.',
            cook_time=timezone.now().time(),
            ingredients='Test ingredients',
            procedure='Test procedure'
        )

    def test_recipe_creation(self):
        self.assertEqual(self.recipe.author, self.user)
        self.assertEqual(self.recipe.category, self.category)
        self.assertEqual(self.recipe.title, 'Test Recipe')
        self.assertEqual(str(self.recipe), 'Test Recipe')

    def test_get_total_number_of_likes(self):
        self.assertEqual(self.recipe.get_total_number_of_likes(), 0)
        RecipeLike.objects.create(user=self.user, recipe=self.recipe)
        self.assertEqual(self.recipe.get_total_number_of_likes(), 1)


class RecipeLikeModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser',email="testuser@example.com", password='testpass')
        self.category = RecipeCategory.objects.create(name='Appetizers')
        self.recipe = Recipe.objects.create(
            author=self.user,
            category=self.category,
            picture='uploads/test.jpg',
            title='Test Recipe',
            desc='This is a test recipe.',
            cook_time=timezone.now().time(),
            ingredients='Test ingredients',
            procedure='Test procedure'
        )
        self.recipe_like = RecipeLike.objects.create(user=self.user, recipe=self.recipe)

    def test_recipe_like_creation(self):
        self.assertEqual(self.recipe_like.user, self.user)
        self.assertEqual(self.recipe_like.recipe, self.recipe)
        self.assertEqual(str(self.recipe_like), self.user.username)

    def test_recipe_like_str(self):
        self.assertEqual(str(self.recipe_like), self.user.username)
