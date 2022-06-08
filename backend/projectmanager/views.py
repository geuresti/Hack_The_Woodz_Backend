from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action, permission_classes

from .models import Project
from .serializers import ProjectSerializer, UserSerializer

from django.contrib.auth.models import User

from django.shortcuts import get_object_or_404

from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    @action(detail=False, methods=['get'])
    def users(self, request):
        users = User.objects.all()

        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def create_account(self, request):
        serializer = UserSerializer(data=request.data)

        # this line is required before acessing serialized data
        if serializer.is_valid():

            # this validation system feels inefficient
            req_username = serializer.validated_data.get('username')
            req_email = serializer.validated_data.get('email')
            req_password = serializer.validated_data.get('password')

            if req_username and req_email and req_password:
                username = serializer.validated_data['username']
                email = serializer.validated_data['email']
                password = serializer.validated_data['password']

                user = User.objects.create_user(username, email, password)
                user.save()
                return Response({"status":"user successfully created"}, status=status.HTTP_200_OK)

        return Response({"status":"required fields missing"}, status=status.HTTP_400_BAD_REQUEST)


# request will only be allowed if the person making it
# is authenticated. authentication is confirmed by putting
# "Authorization : Token <insert token>" as the header for
# the request
@permission_classes([IsAuthenticated])
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
                    return Response({"error":"project with that title already exists"}, status=status.HTTP_409_CONFLICT)

            else:
                return Response({"error":"project not found"}, status=status.HTTP_404_NOT_FOUND)

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
                return Response({"error":"required fields missing"}, status=status.HTTP_400_BAD_REQUEST)

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
                # if it's new then why would it be found?
                return Response({"error":"project not found"}, status=status.HTTP_404_NOT_FOUND)

            #id is not passed in serializer due to being "read only"
            #project_id = (serializer.validated_data['id'])

        # UNCOMMENT THIS ONCE DONE TESTING WITH POSTMAN
        # header token == request.user.token*
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

            return Response({"images":img}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
