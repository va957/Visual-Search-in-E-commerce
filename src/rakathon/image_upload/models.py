from django.db import models
from django.contrib.auth.models import User
from s3direct.fields import S3DirectField

class QueryImage(models.Model):
    user_id  = models.IntegerField(default=1, null=False)
    image_id = models.IntegerField(default=1)
    image_file = models.ImageField(upload_to='images/')
    image = S3DirectField(dest='primary_destination', blank=True)

    def __str__(self):
        return f"User{str(self.user_id)} QueryImage {str(self.image_id)}"