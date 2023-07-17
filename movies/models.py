from django.db import models

class Rating_Choice(models.TextChoices):
  GENERAL_AUDIENCES = "G"
  PARENTAL_GUIDANCE_SUGGESTED = "PG"
  PARENTS_STRONGLY_CAUTIONED = "PG-13"
  RESTRICTED = "R"
  ADULTS_ONLY = "NC-17"

class Movie(models.Model):
  title     = models.CharField(max_length=127)
  duration  = models.CharField(max_length=10, null=True, default=None)
  rating    = models.CharField(
    choices=Rating_Choice.choices,
    null=True,
    default=Rating_Choice.GENERAL_AUDIENCES,
    max_length=20
  )
  synopsis  = models.TextField(null=True, default=None)

  user      = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="movies")

  orders    = models.ManyToManyField("users.User", through="MovieOrder", related_name="ordersUser")

class MovieOrder(models.Model):
  user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="user_movie_orders")

  movie = models.ForeignKey("Movie", on_delete=models.CASCADE, related_name="movie_orders")

  buyed_at = models.DateTimeField(auto_now_add=True)

  price = models.DecimalField(max_digits = 8, decimal_places = 2)
