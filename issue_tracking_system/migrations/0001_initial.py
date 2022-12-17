# Generated by Django 4.1.3 on 2022-12-17 11:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Contributor",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "permission",
                    models.CharField(
                        choices=[
                            ("Lecture", "read"),
                            ("Ecriture", "write"),
                            ("Modification / Suppression", "update_and_delete"),
                        ],
                        max_length=200,
                    ),
                ),
                ("role", models.CharField(blank=True, max_length=200)),
                ("active", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="Project",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=128)),
                ("description", models.CharField(blank=True, max_length=255)),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("Back-end", "Back-end"),
                            ("Front-end", "Front-end"),
                            ("IOs", "IOs"),
                            ("Android", "Android"),
                        ],
                        max_length=128,
                    ),
                ),
                ("active", models.BooleanField(default=False)),
                (
                    "author_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Issue",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=128)),
                ("desc", models.CharField(blank=True, max_length=128)),
                (
                    "tag",
                    models.CharField(
                        choices=[
                            ("Bug", "bug"),
                            ("Amélioration", "ameliorate"),
                            ("Tâche", "task"),
                        ],
                        max_length=128,
                    ),
                ),
                (
                    "priority",
                    models.CharField(
                        choices=[
                            ("Faible", "small"),
                            ("Moyenne", "medium"),
                            ("Élevée", "high"),
                        ],
                        max_length=128,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("À faire", "to_do"),
                            ("En cours", "on_progress"),
                            ("Terminé", "done"),
                        ],
                        max_length=128,
                    ),
                ),
                ("created_time", models.DateTimeField(auto_now_add=True)),
                ("active", models.BooleanField(default=False)),
                (
                    "assignee_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="issue_tracking_system.contributor",
                    ),
                ),
                (
                    "author_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="issue_tracking_system.project",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="contributor",
            name="project",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="issue_tracking_system.project",
            ),
        ),
        migrations.AddField(
            model_name="contributor",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("description", models.CharField(blank=True, max_length=128)),
                ("created_time", models.DateTimeField(auto_now_add=True)),
                ("active", models.BooleanField(default=False)),
                (
                    "author_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "issue",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="issue_tracking_system.issue",
                    ),
                ),
            ],
        ),
    ]
