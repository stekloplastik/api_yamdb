from django.core.management.base import BaseCommand

from review.models import Comment, Review
from titles.models import Category, Genre, Title
from users.models import CustomUser
from utils.csv_to_db import fill_db


class Command(BaseCommand):
    help = 'Fill db'

    def handle(self, *args, **options):
        model_config = (
            ('data/users.csv', CustomUser),
            ('data/genre.csv', Genre),
            ('data/category.csv', Category),
            ('data/titles.csv', Title),
            ('data/genre_title.csv', Title.genre.through),
            ('data/review.csv', Review),
            ('data/comments.csv', Comment),
        )

        for config in model_config:
            fill_db(*config)
