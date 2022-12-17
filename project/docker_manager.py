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
        container = cls.client.containers.run(image, command=cmd, environment=envs, detach=True)
        return container.attrs['Id']

    @classmethod
    def pull_docker_image(cls, image):
        image = cls.client.images.pull(image)
        return image

    @classmethod
    def reload_docker_cont(cls, id):
        cont = cls.client.containers.get(id)
        cont.reload()
        status = cont.attrs['State']['Running']
        if status == False:
            running_time = time_convert(cont.attrs['State']['FinishedAt']) - time_convert(cont.attrs['State']['StartedAt'])
            status = 'finished'
        else:
            running_time = int(time.time()) - time_convert(cont.attrs['State']['StartedAt'])
            status = 'running'
        return running_time, status
