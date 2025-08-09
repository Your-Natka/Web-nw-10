from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from quotes.models import Quote, Tag, Author

class Command(BaseCommand):
    help = 'Додає тестові цитати і теги'

    def handle(self, *args, **kwargs):
        # Створюємо або беремо існуючі теги
        tag_inspiration, _ = Tag.objects.get_or_create(name='inspiration')
        tag_life, _ = Tag.objects.get_or_create(name='life')
        tag_funny, _ = Tag.objects.get_or_create(name='funny')

        # Створюємо або беремо автора
        author, _ = Author.objects.get_or_create(
            fullname='Albert Einstein',
            defaults={
                'born_date': '14 March 1879',
                'born_location': 'Ulm, Kingdom of Württemberg, German Empire',
                'description': 'German-born theoretical physicist who developed the theory of relativity.'
            }
        )

        # Створюємо або беремо користувача (потрібен для поля created_by)
        user, _ = User.objects.get_or_create(username='admin')
        # Якщо потрібно, можна задати й пароль (тоді треба додатково user.set_password('...') і user.save())

        # Додаємо цитати
        quotes_data = [
            ('Life is like riding a bicycle. To keep your balance you must keep moving.', [tag_life, tag_inspiration]),
            ('Imagination is more important than knowledge.', [tag_inspiration]),
            ("Two things are infinite: the universe and human stupidity; and I'm not sure about the universe.", [tag_funny]),
        ]

        for text, tags in quotes_data:
            quote, created = Quote.objects.get_or_create(
                quote=text,
                author=author,
                created_by=user,
            )
            if created:
                quote.tags.set(tags)
                quote.save()
                self.stdout.write(self.style.SUCCESS(f'Added quote: "{text[:50]}..."'))
            else:
                self.stdout.write(f'Quote already exists: "{text[:50]}..."')
