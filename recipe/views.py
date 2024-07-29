from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.core.mail import send_mail
from django.http import JsonResponse
from decouple import config
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

from .models import Recipe, RecipeLike
from .serializers import RecipeLikeSerializer, RecipeSerializer
from .permissions import IsAuthorOrReadOnly
from .tasks import send_email_like_notification

User = get_user_model()


class RecipeListAPIView(generics.ListAPIView):
    """
    Get: a collection of recipes
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (AllowAny,)
    filterset_fields = ('category__name', 'author__username')


class RecipeCreateAPIView(generics.CreateAPIView):
    """
    Create: a recipe
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class RecipeAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Get, Update, Delete a recipe
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthorOrReadOnly,)


class RecipeLikeAPIView(generics.CreateAPIView):
    """
    Like, Dislike a recipe
    """
    serializer_class = RecipeLikeSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        recipe = get_object_or_404(Recipe, id=self.kwargs['pk'])
        new_like, created = RecipeLike.objects.get_or_create(
            user=request.user, recipe=recipe)
        if created:
            new_like.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        recipe = get_object_or_404(Recipe, id=self.kwargs['pk'])
        like = RecipeLike.objects.filter(user=request.user, recipe=recipe)
        if like.exists():
            like.delete()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

def test_email(request):
    subject = 'Test Email'
    message = 'This is a test email sent from Django.'
    recipient_list = ['akash.kumar.yadav.cse@gmail.com']  # Replace with your recipient's email

    try:
        send_mail(subject, message, config("EMAIL_USER"), recipient_list)
        return JsonResponse({'status': 'Email sent successfully!'})
    except Exception as e:
        return JsonResponse({'status': 'Failed to send email', 'error': str(e)})

@csrf_exempt
def like_recipe(request, recipe_id):
    if request.method == 'POST':
        permission_classes = (IsAuthenticated,)
        user = User.objects.first()
        if not user.is_authenticated:
            return JsonResponse({'status': 'You must be logged in to like a recipe.'}, status=403)
        recipe = get_object_or_404(Recipe, id=recipe_id)
        print(recipe.author.email)
        if RecipeLike.objects.filter(recipe=recipe, user=user).exists():
            return JsonResponse({'status': 'You have already liked this recipe.'})
        RecipeLike.objects.create(recipe=recipe, user=user)
        likes_count = recipe.get_total_number_of_likes()
        send_email_like_notification.delay(recipe.author.email,likes_count)
        return JsonResponse({'status': 'Recipe liked successfully!'})
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)
