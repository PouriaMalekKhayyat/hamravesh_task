import docker
import time 

def time_convert(t):
    p = '%Y-%m-%dT%H:%M:%S'
    idx = t.rfind('.')
    t = t[:idx]
    a = int(time.mktime(time.strptime(t, p)))
    return a

class DockerManager():
    client = docker.from_env()

    @classmethod
    def run_docker_command(cls, image, envs, cmd):
        img = cls.client.images.pull(image)
        #container = cls.client.containers.run(img, detach=True)

        container = cls.client.containers.run(img, command=cmd, environment=envs, detached=True)
        return container.attrs['Id']

    @classmethod
    def pull_docker_image(cls, image):
        image = cls.client.images.pull(image)
        return image

    @classmethod
    def reload_docker_cont(cls, id):
        cont = cls.client.containers.get(id)
        cont.reload()
        running_time = time_convert(cont.attrs['State']['FinishedAt']) - time_convert(cont.attrs['State']['StartedAt'])
        status = cont.attrs['State']['Running']
        if status == False:
            status = 'finished'
        else:
            status = 'running'
        return running_time, status

