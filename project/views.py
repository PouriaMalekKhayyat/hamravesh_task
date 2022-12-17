from django.http import JsonResponse
from .models import App, Run
from .serializers import AppSerializer, RunSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .docker_manager import DockerManager
from rest_framework.views import APIView

@api_view(['POST'])
def app_build(request):
    # to avoid wasting resources we pull image when running the app. (in run api)
    serializer = AppSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return JsonResponse({'msg': 'Invalid inputs, please check your inputs'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def app_list(request):
    apps = App.objects.all()
    serializer = AppSerializer(apps, many=True)
    return JsonResponse({'data:': serializer.data})

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
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'msg': 'Invalid inputs, please check your inputs'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def app_run(request, id):
    try:
        app = App.objects.get(pk=id)
    except App.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    try:
        try:
            image = DockerManager.pull_docker_image(app.image)
        except Exception:
            return JsonResponse({'msg': 'failed to pull image'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        cont_id = DockerManager.run_docker_command(image, app.envs, app.command)
        # create run object in db
        serializer = RunSerializer(data={
            'status': 'running',
            'running_time': 0,
            'name': app.name,
            'image': app.image,
            'envs': app.envs,
            'command': app.command,
            'app': id,
            'cont_id': cont_id,
        })
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)
    except Exception:
        return JsonResponse(
            {'msg': 'Error running command, you might want to check if your image, command or envoirment variables are valid.'},
             status=status.HTTP_406_NOT_ACCEPTABLE)
    
@api_view(['GET'])
def run_list(request, id):
    try:
        app = App.objects.get(pk=id)
    except App.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    runs = Run.objects.filter(app_id=id)
    for run in runs:
        running_time, cont_status = DockerManager.reload_docker_cont(run.cont_id)
        run.running_time = running_time
        run.status = cont_status
        run.save()
    runs = Run.objects.filter(app_id=id)
    serializer = RunSerializer(runs, many=True)
    return JsonResponse({'data': serializer.data}, status=status.HTTP_200_OK)

@api_view(['GET'])
def run_status(request, id):
    try:
        run = Run.objects.get(pk=id)
    except Run.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    _, cont_status = DockerManager.reload_docker_cont(run.cont_id)
    run.status = cont_status
    run.save()
    return JsonResponse({'data': cont_status}, status=status.HTTP_200_OK)
