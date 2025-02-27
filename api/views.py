from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status

from leishimaniaapp.microscope_slide.models import MicroscopeSlide, TaskType
from .serializers import MicroscopeImageSerializer
from leishimaniaapp.microscope_slide.tasks import process_image, process_image_yolo


class ImageUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        serializer = MicroscopeImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            img_id = serializer.data["id"]
            microscope_slide = MicroscopeSlide.objects.get(
                id=serializer.data["microscope_slide"]
            )

            if microscope_slide.task_type == TaskType.YOLO:
                process_image_yolo.delay(img_id)
            else:
                process_image.delay(img_id)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
