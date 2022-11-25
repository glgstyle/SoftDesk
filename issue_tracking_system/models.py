from django.db import models
from django.conf import settings


class Project(models.Model):
    title = models.fields.CharField(max_length=128)
    description = models.fields.CharField(max_length=255, blank=True)
    TYPE_CHOICES = (
        ('Back-end', 'Back-end'),
        ('Front-end', 'Front-end'),
        ('IOs', 'IOs'),
        ('Android', 'Android'),
    )
    type = models.fields.CharField(max_length=128, choices=TYPE_CHOICES)
    author_user_id = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Contributor(models.Model):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ManyToManyField(to=Project)
    PERMISSION_CHOICES = (
        ('Author', 'Author'),
        ('Manager', 'Manager'),
        ('Creator', 'Creator'),
    )
    permission = models.CharField(
        max_length=200, choices=PERMISSION_CHOICES)
    role = models.CharField(max_length=128, blank=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return "Le contributeur du projet : " + self.project.title \
            + " est : " + self.user.username


class Issue(models.Model):
    title = models.fields.CharField(max_length=128)
    desc = models.fields.CharField(max_length=128, blank=True)
    TAG_CHOICES = (
        ('Bug', 'Bug'),
        ('Amélioration', 'Amélioration'),
        ('Tâche', 'Tâche')
    )
    tag = models.fields.CharField(max_length=128, choices=TAG_CHOICES)
    PRIORITY_CHOICES = (
        ('Faible', 'Faible'),
        ('Moyenne', 'Moyenne'),
        ('Élevée', 'Élevée'),
    )
    priority = models.fields.CharField(
        max_length=128, choices=PRIORITY_CHOICES)
    project_id = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    STATUS_CHOICES = (
        ('À faire', 'À faire'),
        ('En cours', 'En cours'),
        ('Terminé', 'Terminé')
    )
    status = models.fields.CharField(max_length=128, choices=STATUS_CHOICES)
    author_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    assignee_user = models.ForeignKey(to=Contributor, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)


class Comment(models.Model):
    description = models.fields.CharField(max_length=128, blank=True)
    author_user_id = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    issue_id = models.ForeignKey(to=Issue, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)