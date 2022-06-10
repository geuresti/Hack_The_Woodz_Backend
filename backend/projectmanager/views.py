from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action, permission_classes

from .models import Project
from .serializers import ProjectSerializer, UserSerializer

from django.contrib.auth.models import User

from django.shortcuts import get_object_or_404

from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    # display all users (only useful for testing)
    @action(detail=False, methods=['get'])
    def users(self, request):
        users = User.objects.all()

        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['delete'], permission_classes=[IsAuthenticated])
    def log_out(self, request):
        request.user.auth_token.delete()
        return Response({"status":"sucessfully logged out"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def create_account(self, request):
        serializer = UserSerializer(data=request.data)

        # this line is required before acessing serialized data
        if serializer.is_valid():

            # this validation system feels inefficient
            # skim thru request data and make sure it has
            # a username, email, and password field
            req_username = serializer.validated_data.get('username')
            req_email = serializer.validated_data.get('email')
            req_password = serializer.validated_data.get('password')

            # check that these fields are not None
            if req_username and req_email and req_password:
                username = serializer.validated_data['username']
                email = serializer.validated_data['email']
                password = serializer.validated_data['password']

                # creaate and save new user
                user = User.objects.create_user(username, email, password)
                user.save()
                return Response({"status":"user successfully created"}, status=status.HTTP_200_OK)

        return Response({"status":"required fields missing"}, status=status.HTTP_400_BAD_REQUEST)

    # display all projects by a specific user (username: <username>)
    @action(detail=False, methods=['get'])
    def profile(self, request):
        username = request.data['username']
        user = get_object_or_404(User, username=username)

        projects = Project.objects.filter(user=user)

        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# unathenticated users may only perform GET requests
# other request types only be allowed if authenticated
# authentication is done by putting
#   "Authorization : Token <insert token>" in the request header
#
# tokens are acquired by using the auth_token endpoint with
#   "username : <username>, password: <password>" in the req body
@permission_classes([IsAuthenticatedOrReadOnly])
class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    # display all projects in database (for testing)
    @action(detail=False, methods=['get'])
    def projects(self, request):
        projects = Project.objects.all()

        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # view a specific project (title: <project title>)
    @action(detail=False, methods=['get'])
    def view_project(self, request):
        serializer = ProjectSerializer(data=request.data, partial=True)

        if serializer.is_valid():
            # look for project by title
            if serializer.initial_data.get('title'):
                title_data = serializer.validated_data['title']
                project = get_object_or_404(Project, title=title_data)

                display = ProjectSerializer(project)
                return Response(display.data, status=status.HTTP_200_OK)
            else:
                return Response({"error":"project not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # create a new project
    @action(detail=True, methods=['post'])
    def create(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            project = Project()
            project.user = request.user

            if serializer.initial_data.get('title'):
                title_data = serializer.validated_data['title']

                # check if project with that title alreadu exists
                already_exists = Project.objects.filter(title=title_data)

                if already_exists:
                    return Response({"error":"project with that title already exists"}, status=status.HTTP_409_CONFLICT)

            # confirm that the request has the following fields
            req_has_title = serializer.validated_data.get('title')
            req_has_tools = serializer.validated_data.get('tools')
            req_has_desc = serializer.validated_data.get('description')
            req_has_image = serializer.validated_data.get('images')

            # if the request had all four fields filled out, create
            # the new project using the data from the request
            if req_has_title and req_has_tools and req_has_desc and req_has_image:
                project.title = serializer.validated_data['title']
                project.tools = serializer.validated_data['tools']
                project.description = serializer.validated_data['description']
                project.images = serializer.validated_data['images']

                project.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({"error":"required fields missing"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# id is not passed in serializer due to being "read only"
# project_id = (serializer.validated_data['id'])
# ^^^ DOES NOT WORK ^^^
# therefore, we have to grab a project to update by its
# title, not it's ID (which would be ideal)

    # update field(s) for a project
    @action(detail=False, methods=['patch'])
    def update(self, request):
        serializer = ProjectSerializer(data=request.data, partial=True)

        if serializer.is_valid():
            # look for project by title
            if serializer.initial_data.get('title'):
                title_data = serializer.validated_data['title']
                project = get_object_or_404(Project, title=title_data)
            else:
                return Response({"error":"project not found"}, status=status.HTTP_404_NOT_FOUND)

            # check if user sending the request is the owner of the project
            if project.user == request.user:

                # update anything that's changed been changed in request body
                if serializer.data.get('tools'):
                    project.tools = serializer.validated_data['tools']

                if serializer.data.get('description'):
                    project.description = serializer.validated_data['description']

                if serializer.validated_data.get('images'):
                    project.images = serializer.validated_data['images']

                project.save()
                return Response({"status":"sucessfully updated project"}, status=status.HTTP_202_ACCEPTED)
            else:
                return Response({"error":"you don't have permission"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"error":"bad request"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def delete_project(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.initial_data.get('title'):
                title_data = serializer.validated_data['title']
                project = get_object_or_404(Project, title=title_data)

                if request.user == project.user:
                    project.delete()
                    return Response({"status":"project successfully deleted"}, status=status.HTTP_200_OK)
                else:
                    return Response({"error":"you don't have permission"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({"error":"project not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error":"bad request"}, status=status.HTTP_400_BAD_REQUEST)

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
