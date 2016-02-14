from django.db import models


# Create your models here.
class Files(models.Model):
    Name = models.CharField(max_length=255)
    Type = models.CharField(max_length=5, db_index=True)
    Size = models.CharField(max_length=255)
    lon = models.FloatField()
    lat = models.FloatField()
    DateTime = models.DateTimeField(db_index=True)


class Victims(models.Model):
    Type = models.CharField(max_length=255, db_index=True)
    Quantity = models.IntegerField()
    File = models.ForeignKey(Files)


class Food(models.Model):
    Type = models.CharField(max_length=255, db_index=True)
    Quantity = models.IntegerField()
    File = models.ForeignKey(Files)


class Health(models.Model):
    Type = models.CharField(max_length=255, db_index=True)
    Quantity = models.IntegerField()
    File = models.ForeignKey(Files)


class Shelter(models.Model):
    Type = models.CharField(max_length=255, db_index=True)
    Quantity = models.IntegerField()
    File = models.ForeignKey(Files)


class Areas(models.Model):
    Type = models.CharField(max_length=255, db_index=True)
    Quantity = models.IntegerField()
    File = models.ForeignKey(Files)


class SMS(models.Model):
    Content = models.TextField()
    File = models.ForeignKey(Files)
