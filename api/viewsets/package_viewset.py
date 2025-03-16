from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from api.serializers.package_serializer import PackageSerializer


class PackageViewSet(viewsets.ViewSet):
    """ User API with soft delete & restore functionality """

    def list(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)