from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ContactPageSerializer, FooterSerializer


class ContactPageView(APIView):
    def get(self, request):
        serializer = ContactPageSerializer(instance={}, context={"request": request})
        return Response(serializer.data)


class FooterView(APIView):
    def get(self, request):
        serializer = FooterSerializer(instance={}, context={"request": request})
        return Response(serializer.data)
    

from .serializers import AboutPageSerializer

class AboutPageView(APIView):
    def get(self, request):
        serializer = AboutPageSerializer(instance={}, context={"request": request})
        return Response(serializer.data)    