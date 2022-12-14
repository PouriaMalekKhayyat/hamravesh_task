from django.db import models

class App(models.Model):
    name = models.CharField(max_length=100)
    image = models.CharField(max_length=100)
    envs = models.JsonField()
    command = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Run(models.Model):
    status = models.ChoiceField(choices= [('running', 'Running'), ('finished', 'Finished')])
    running_time = models.DurationField()
    name = models.CharField(max_length=100)
    image = models.CharField(max_length=100)
    envs = models.JsonField()
    command = models.CharField(max_length=100)
    app = models.ForeignKey(App, on_delete=models.SET_NULL)

    def __str__(self):
        return (self.status + ' ' + self.app)