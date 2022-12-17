from django.http import JsonResponse
from project.models import App, Run
from project.serializers import AppSerializer, RunSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from project.docker_manager import DockerManager

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
