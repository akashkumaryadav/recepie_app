from logging import Logger
import logging
from celery import shared_task
from decouple import config
from django.core.mail import send_mail
from django.utils import timezone
from .models import RecipeLike, Recipe

logger = logging.getLogger('recipe')

@shared_task
def send_email_like_notification(author_email, likes_count):
    subject = 'Your Recipe Received Likes!'
    message = f'Your recipe has received {likes_count} likes today!'
    logger.info(msg="Sending Email..")
    send_mail(subject, message, config("EMAIL_USER"), [author_email])


@shared_task
def notify_authors_about_likes():
    today = timezone.now().date()
    recipes = Recipe.objects.all()

    for recipe in recipes:
        likes_count = RecipeLike.objects.filter(recipe=recipe, created__date=today).count()
        if likes_count > 0:
            send_email_like_notification.delay(recipe.author.email, likes_count)
