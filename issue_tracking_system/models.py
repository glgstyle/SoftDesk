from django.db import models, transaction
from django.conf import settings


class Project(models.Model):
    title = models.fields.CharField(max_length=128)
    description = models.fields.CharField(max_length=255, blank=True)
    TYPE_CHOICES = (
        # first is displayed and second in database
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

    @property
    def author_user(self):
        if self.author_user_id != None:
            return self.author_user_id.id
        else:
            return None

class Contributor(models.Model):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ManyToManyField(to=Project)
    PERMISSIONS_CHOICES = (
        ('Lecture', 'read'),
        ('Ecriture', 'write'),
        ('Modification / Suppression', 'update_and_delete'),
    )
    permission = models.CharField(
        max_length=200, choices=PERMISSIONS_CHOICES)
    role = models.CharField(max_length=200, blank=True)
    active = models.BooleanField(default=False)

    # def __str__(self):
    #     return "Le contributeur du projet : " + self.project.title \
    #         + " est : " + self.user.username


class Issue(models.Model):
    title = models.fields.CharField(max_length=128)
    desc = models.fields.CharField(max_length=128, blank=True)
    TAG_CHOICES = (
        ('Bug', 'bug'),
        ('Amélioration', 'ameliorate'),
        ('Tâche', 'task')
    )
    tag = models.fields.CharField(max_length=128, choices=TAG_CHOICES)
    PRIORITY_CHOICES = (
        ('Faible', 'small'),
        ('Moyenne', 'medium'),
        ('Élevée', 'high'),
    )
    priority = models.fields.CharField(
        max_length=128, choices=PRIORITY_CHOICES)
    project_id = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    STATUS_CHOICES = (
        ('À faire', 'to_do'),
        ('En cours', 'on_progress'),
        ('Terminé', 'done')
    )
    status = models.fields.CharField(max_length=128, choices=STATUS_CHOICES)
    author_user_id = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    assignee_user = models.ForeignKey(to=Contributor, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    @property
    def author_user(self):
        if self.author_user_id != None:
            return self.author_user_id.id
        else:
            return None


    @transaction.atomic
    def disable(self):
        if self.active is False:
        # Ne faisons rien si la catégorie est déjà désactivée
            return
        self.active = False
        self.save()
        self.project.update(active=False)

class Comment(models.Model):
    description = models.fields.CharField(max_length=128, blank=True)
    author_user_id = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    issue_id = models.ForeignKey(to=Issue, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)