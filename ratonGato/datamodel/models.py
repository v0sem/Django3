from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Game(models.Model):
    cat_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cat_user")
    mouse_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mouse_user")
    cat1 = models.IntegerField(null=False)
    cat2 = models.IntegerField(null=False)
    cat3 = models.IntegerField(null=False)
    cat4 = models.IntegerField(null=False)
    mouse = models.IntegerField(null=False)
    cat_turn = models.BooleanField(null=False)

    CREATED = 'CREAT'
    ACTIVE = 'ACT'
    FINISHED = 'FIN'
    GameStatus = (
        (CREATED, "CREATED"),
        (ACTIVE, "ACTIVE"),
        (FINISHED, "FINISHED")
    )
    status = models.CharField(max_length=10, choices=GameStatus, default=CREATED, null=False)


class Move(models.Model):
    origin = models.IntegerField(null=False)
    target = models.IntegerField(null=False)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(null=False)