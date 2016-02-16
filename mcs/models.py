from django.db import models


# Create your models here.
class Files(models.Model):
    Name = models.CharField(max_length=255, db_index=True)
    Type = models.CharField(max_length=5, db_index=True)
    Size = models.CharField(max_length=255)
    Source = models.CharField(max_length=30)
    Destination = models.CharField(max_length=30)
    lon = models.FloatField()
    lat = models.FloatField()
    DateTime = models.DateTimeField(db_index=True)

    def __str__(self):
        return self.Name


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


class UnstructuredTXT(models.Model):
    Content = models.TextField()
    File = models.ForeignKey(Files)
    SentimentPolarity = models.FloatField()

    def __str__(self):
        return (self.File.__str__() + " | SentimentPolarity: " +
                str(self.SentimentPolarity))
