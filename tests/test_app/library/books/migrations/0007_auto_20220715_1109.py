# Generated by Django 3.2.13 on 2022-07-15 10:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("books", "0006_auto_20220327_0814"),
    ]

    operations = [
        migrations.AlterField(
            model_name="book",
            name="last_print",
            field=models.DateField(auto_now_add=True),
        ),
    ]
