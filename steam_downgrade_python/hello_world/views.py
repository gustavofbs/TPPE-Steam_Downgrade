from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response


def hello_world(request):
    """Simple Hello World view"""
    return HttpResponse("<h1>Hello, World! Welcome to Steam Downgrade Python</h1>")


class HelloWorldAPIView(APIView):
    """API view for Hello World"""
    def get(self, request, format=None):
        return Response({
            "message": "Hello, World!",
            "project": "Steam Downgrade Python",
            "status": "Running successfully"
        })
