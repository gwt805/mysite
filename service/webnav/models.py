from django.db import models

class Webnav(models.Model):
    name = models.CharField(max_length=50, null=False, unique=True)
    weburl = models.CharField(max_length=100, null=False)
    imgurl = models.TextField(null=False)
    tooltip = models.CharField(max_length=100, null=False)
    tag = models.CharField(max_length=50, null=False)

    class Meta:
        db_table = 'webnav'

class Webnavlabel(models.Model):
    tag = models.CharField(max_length=50, null=False, unique=True)

    class Meta:
        db_table = 'webnavlabel'