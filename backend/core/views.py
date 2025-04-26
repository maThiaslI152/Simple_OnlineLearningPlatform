# core/views.py
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from django.core.files.storage import default_storage

class FileUploadTestView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = []  # public for testing

    def post(self, request, format=None):
        file_obj = request.FILES.get("file")
        if not file_obj:
            return Response({"error": "No file"}, status=400)
        path = default_storage.save(f"test/{file_obj.name}", file_obj)
        url  = default_storage.url(path)
        return Response({"path": path, "url": url}, status=201)
