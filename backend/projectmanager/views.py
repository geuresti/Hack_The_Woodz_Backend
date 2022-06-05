from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from .models import Project
from .serializers import ProjectSerializer

from django.contrib.auth.models import User

from django.shortcuts import get_object_or_404

class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    @action(detail=False, methods=['get'])
    def projects(self, request):
        projects = Project.objects.all()

        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def create(self, request, *args, **kwargs):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            project = Project()
        # UNCOMMENT THIS ONCE DONE TESTING WITH POSTMAN
            #project.user = User.objects.get(pk=request.user.id)
            project.user = User.objects.get(pk=1)

            if serializer.initial_data.get('title'):
                title_data = serializer.validated_data['title']
                already_exists = Project.objects.filter(title=title_data)
                # UNCOMMENT THIS ONCE DONE TESTING WITH POSTMAN
                if already_exists: # and (already_exists.user == request.user):
                    return Response({"error":"project with that title already exists"})

            else:
                return Response({"error":"project not found"})

            req_has_title = serializer.validated_data.get('title')
            req_has_tools = serializer.validated_data.get('tools')
            req_has_desc = serializer.validated_data.get('description')
            req_has_image = serializer.validated_data.get('images')

            if req_has_title and req_has_tools and req_has_desc and req_has_image:
                project.title = serializer.validated_data['title']
                project.tools = serializer.validated_data['tools']
                project.description = serializer.validated_data['description']
                project.images = serializer.validated_data['images']

                project.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({"error":"required fields missing"})

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['patch'])
    def update(self, request, *args, **kwargs):
        serializer = ProjectSerializer(data=request.data, partial=True)

        if serializer.is_valid():
            # grab project by title
            if serializer.initial_data.get('title'):
                title_data = serializer.validated_data['title']
                project = get_object_or_404(Project, title=title_data)
            else:
                return Response({"error":"project not found"})

            #id is not passed in serializer due to being read only
            #project_id = (serializer.validated_data['id'])

        # UNCOMMENT THIS ONCE DONE TESTING WITH POSTMAN
            if project.user: # == request.user:

                # update anything that's changed been changed in request body
                if serializer.data.get('tools'):
                    project.tools = serializer.validated_data['tools']

                if serializer.data.get('description'):
                    project.description = serializer.validated_data['description']

                if serializer.validated_data.get('images'):
                    project.images = serializer.validated_data['images']

                project.save()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def get_image(self, request, *args, **kwargs):
        serializer = ProjectSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            title_data = (serializer.validated_data['title'])
            project = get_object_or_404(Project, title=title_data)
            img = "/media/" + str(project.images)

            return Response({"images":img})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
