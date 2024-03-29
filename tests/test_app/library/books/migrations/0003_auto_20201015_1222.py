# Generated by Django 2.2.15 on 2020-10-15 11:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("books", "0002_book_library"),
    ]

    operations = [
        migrations.AlterField(
            model_name="book",
            name="isbn",
            field=models.CharField(
                help_text=(
                    '13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>',
                ),
                max_length=13,
                verbose_name="ISBN",
            ),
        ),
    ]
