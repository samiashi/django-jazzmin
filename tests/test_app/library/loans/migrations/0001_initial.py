# Generated by Django 2.2.15 on 2020-10-14 12:37

import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("books", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Library",
            fields=[
                (
                    "id",
                    models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID"),
                ),
                ("address", models.CharField(max_length=255)),
                (
                    "librarian",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, related_name="library", to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="BookLoan",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        help_text="Unique ID for this particular book across whole library",
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("imprint", models.CharField(max_length=200)),
                ("due_back", models.DateField(blank=True, null=True)),
                ("loan_start", models.DateTimeField()),
                ("duration", models.DurationField(blank=True)),
                (
                    "status",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("m", "Maintenance"),
                            ("o", "On loan"),
                            ("a", "Available"),
                            ("r", "Reserved"),
                        ],
                        default="m",
                        help_text="Book availability",
                        max_length=1,
                    ),
                ),
                (
                    "book",
                    models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to="books.Book"),
                ),
                (
                    "borrower",
                    models.ForeignKey(
                        blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
            options={
                "ordering": ("due_back",),
            },
        ),
    ]
