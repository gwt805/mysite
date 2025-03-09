from django.db import models

class Blog(models.Model):
    title = models.CharField(max_length=256, null=False)
    content = models.TextField(null=False)
    created_at = models.DateTimeField(null=False, auto_created=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=False, auto_created=True, auto_now=True)

    class Meta:
        db_table = "blog"

class Blogfile(models.Model):
    bid = models.BigIntegerField(null=False)
    file = models.JSONField()

    class Meta:
        db_table = "blogfile"