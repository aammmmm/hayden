from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from api.serializers.user_serializer import UserSerializer

User = get_user_model()

class UserViewSet(viewsets.ViewSet):
    """ User API with soft delete & restore functionality """

    def list(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path="register")
    def register(self, request):
        """ Register a new user (default role: user) """
        username = request.data.get('username')
        phone_number = request.data.get('phone_number')
        email = request.data.get('email')
        password = request.data.get('password')
        role = request.data.get('role', 'user')  # Default role is 'user'

        if role not in ['user', 'admin']:
            return Response({"error": "Invalid role"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({"error": "Email already registered"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already taken"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create(
            username=username,
            phone_number=phone_number,
            email=email,
            role=role  # Allow assigning the admin role
        )
        user.set_password(password)
        user.save()
        return Response({"message": f"{role.capitalize()} registered successfully"}, status=status.HTTP_201_CREATED)


    @action(detail=False, methods=['post'], url_path="login")
    def login(self, request):
        """ Login user """
        email = request.data.get('email')
        password = request.data.get('password')

        user = User.objects.filter(email=email).first()
        if user and user.check_password(password):
            if user.is_deleted:
                return Response({"error": "Account is deactivated"}, status=status.HTTP_403_FORBIDDEN)

            refresh = RefreshToken.for_user(user)
            return Response({
                "username": user.username,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'role': user.role
            })

        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['post'], url_path="delete-user")
    def soft_delete_user(self, request):
        """ Soft delete a user """
        email = request.data.get('email')

        try:
            user = User.global_objects.get(email=email)
            user.delete()
            return Response({"message": "User soft deleted successfully"})
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'], url_path="restore")
    def restore_user(self, request):
        """ Restore a soft-deleted user """
        email = request.data.get('email')

        try:
            user = User.deleted_objects.get(email=email)
            user.restore()
            return Response({"message": "User restored successfully"})
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
