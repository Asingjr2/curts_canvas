from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
from base.models import BaseModel


class Picture(BaseModel): 
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.IntegerField(blank=True, default=50)

    # Determining average rating if at least one has been submitted
    def avg_rating(self):
        ratings_sum = 0
        all_ratings = Rating.objects.filter(picture=self)
        for rating in all_ratings:
            ratings_sum += rating.stars
        ratings_count = all_ratings.count()
        if ratings_count > 0:
            return ratings_sum / ratings_count
        else:
            return 0

    # Totaling filtered set for ratings of this movie
    def total_ratings(self):
        return Rating.objects.filter(picture=self).count()

    def __str__(self): 
        return "Picture name is {}".format(self.name)


class Rating(BaseModel):
    stars = models.IntegerField(default=1,
     validators = [MinValueValidator(1), MaxValueValidator(5)])
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    picture = models.ForeignKey(Picture, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("picture", "user"))
        index_together = (("picture", "user"))

    def _str__(self):
        return "{} picture got {} star(s)".format(self.picture.name, self.stars)