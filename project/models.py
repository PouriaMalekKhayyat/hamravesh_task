from django.db import models

class App(models.Model):
    name = models.CharField(max_length=100)
    image = models.CharField(max_length=100)
    envs = models.JSONField(null=True)
    command = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name

class Run(models.Model):
    class Status(models.TextChoices):
        running = ('running', 'Running')
        finished = ('finished', 'Finished')
    
    status = models.CharField(max_length=10, choices=Status.choices)
    running_time = models.IntegerField(default=0)
    name = models.CharField(max_length=100)
    image = models.CharField(max_length=100)
    envs = models.JSONField(null=True)
    command = models.CharField(max_length=100, null=True)
    app = models.ForeignKey(App, on_delete=models.SET_NULL, null=True)
    cont_id = models.CharField(max_length=100, default=None)

    def __str__(self):
        return (self.status + ' ' + self.name)