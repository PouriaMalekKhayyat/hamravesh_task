from django.http import JsonResponse
from .models import App, Run
from .serializers import AppSerializer, RunSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .docker_manager import DockerManager

@api_view(['POST'])
def app_build(request):
    serializer = AppSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def app_list(request):
    apps = App.objects.all()
    serializer = AppSerializer(apps, many=True)
    return JsonResponse({'apps:': serializer.data})

@api_view(['GET', 'DELETE', 'PUT'])
def app_detail(request, id):
    try:
        app = App.objects.get(pk=id)
    except App.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    match request.method:
        case 'GET':
            serializer = AppSerializer(app)
            return Response(serializer.data, status=status.HTTP_200_OK)
        case 'DELETE':
            app.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        case 'PUT':
            serializer = AppSerializer(app, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data ,status=status.HTTP_202_ACCEPTED)
            else:
                return Response(serializer.errors ,status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def app_run(request, id):
    try:
        app = App.objects.get(pk=id)
    except App.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    try:
        img_id = DockerManager.run_docker_command(app.image, app.envs, app.command)
        # create run object in db
        serializer = RunSerializer(data={
            'status': 'running',
            'running_time': 0,
            'name': app.name,
            'image': app.image,
            'envs': app.envs,
            'command': app.command,
            'app': id,
            'img_id': img_id
            })
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(status=status.HTTP_409_CONFLICT)
        return Response(status=status.HTTP_200_OK)
    except Exception:
        return JsonResponse({'msg': 'Error running command'}, status=status.HTTP_406_NOT_ACCEPTABLE)
    
@api_view(['GET'])
def run_list(request, id):
    runs = Run.objects.all().filter(app_id=id)
    for run in runs:
        running_time, cont_status = DockerManager.reload_docker_cont(run.img_id)
        run.running_time = running_time
        run.status = cont_status
        run.save()
    runs = Run.objects.all().filter(app_id=id).filter(status='finished')
    serializer = RunSerializer(runs, many=True)
    return JsonResponse({'runs': serializer.data}, status=status.HTTP_200_OK)

@api_view(['GET'])
def run_status(request, id):
    try:
        run = Run.objects.get(pk=id)
        _, cont_status = DockerManager.reload_docker_cont(run.img_id)
        run.status = cont_status
        return JsonResponse({'status': cont_status}, status=status.HTTP_200_OK)
    except Run.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
