from django.urls import path

from recipe import views

app_name = 'recipe'

urlpatterns = [
    path('', views.RecipeListAPIView.as_view(), name="recipe-list"),
    path('<int:pk>/', views.RecipeAPIView.as_view(), name="recipe-detail"),
    path('create/', views.RecipeCreateAPIView.as_view(), name="recipe-create"),
    path('<int:pk>/like/', views.RecipeLikeAPIView.as_view(),
         name='recipe-like'),
    path('send-email/', views.test_email, name='test_email'),
    path('like-recipe/<int:recipe_id>/', views.like_recipe, name='like_recipe'),
]
