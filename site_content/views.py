from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ContactPageSerializer


class ContactPageView(APIView):
    def get(self, request):
        serializer = ContactPageSerializer(instance={}, context={"request": request})
        return Response(serializer.data)