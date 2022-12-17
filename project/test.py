import time
import docker
import models
from .docker_manager import DockerManager


"""
client = docker.from_env()


def time_convert(t):
    p = '%Y-%m-%dT%H:%M:%S.%f'
    idx = t.rfind('Z')
    t = t[:idx-3]
    a = float(time.mktime(time.strptime(t, p)))
    print(a)
    return a

img = client.images.pull('hello-world:latest')
container = client.containers.run(img, detach=True)
container.reload()
p = '%Y-%m-%dT%H:%M:%S.%f%Z'
running_time = time_convert(container.attrs['State']['FinishedAt']) - time_convert(container.attrs['State']['StartedAt'])
print(running_time)


client = docker.from_env()

img = client.images.pull('hello-world:latest')
container = client.containers.run(img, detach=True)
print('finished')

"""


#image 'nginx:latest'

try:
    app = models.App.objects.get(pk=15)
    img_id = DockerManager.run_docker_command(app.image, app.envs, app.command)
    print(app.image)
    print(app.image == 'nginx:latest')
except models.App.DoesNotExist:
    pass