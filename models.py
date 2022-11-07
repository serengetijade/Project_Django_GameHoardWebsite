from django.db import models

platform_choices = [
    ('Board Game', 'Board_Game'),
    ('PlayStation', 'PlayStation'),
    ('Nintendo', 'Nintendo'),
    ('PC', 'PC'),
    ('Puzzle', 'Puzzle'),
    ('XBox', 'XBox'),
    ('Other', 'Other'),
]

rating_choices= [
    ('⭐','⭐'),
    ('⭐⭐','⭐⭐'),
    ('⭐⭐⭐','⭐⭐⭐'),
    ('⭐⭐⭐⭐','⭐⭐⭐⭐'),
    ('⭐⭐⭐⭐⭐','⭐⭐⭐⭐⭐'),
]
class Game(models.Model):
    #Define class attributes:
    Name = models.CharField(max_length=80, primary_key=True)
    Platform = models.CharField(max_length=40, choices=platform_choices)
    Rating = models.CharField(max_length=100, choices=rating_choices)
    Notes = models.CharField(max_length=200, default="", null=True, blank=True)
    #Object manager:
    GameModel = models.Manager()

    ##Define a function or multiple functions that will run when this function is called.

    # Returns values (of the attributes) to the admin
    def __str__(self):
        return self.Name

class WishList(models.Model):
    Name = models.CharField(max_length=80, primary_key=True)
    Thumb = models.CharField(max_length=80, default="", null=True, blank=True)
    Price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, default="00.00")
    #Object manager:
    WishListModelMgr = models.Manager()

    def __str__(self):
        return self.Name
