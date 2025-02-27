from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from user.decorators import perm_required
from user.models import CustomUser
from django.utils.decorators import method_decorator
from .models import Task, ReviseStack, FileStack, ImageStack, ReportStack
from .serializers import (
    TaskSerializer, ReviseStackSerializer, FileStackSerializer, ImageStackSerializer, ReportStackSerializer
)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(appointeds=user)

    # 📌 GÖREV GÜNCELLEME
    @method_decorator(perm_required('change_task'))
    def update(self, request, *args, **kwargs):
        """Görevi güncelleme"""
        return super().update(request, *args, **kwargs)

    # 📌 GÖREV DURUMU GÜNCELLEME
    
    @action(detail=True, methods=['patch'])
    @method_decorator(perm_required('change_task'))
    def update_status(self, request, pk=None):
        task = self.get_object()
        new_status = request.data.get('status')
        if new_status not in dict(Task.TASK_SITUATIONS):
            return Response({"error": "Geçersiz durum"}, status=status.HTTP_400_BAD_REQUEST)
        task.status = new_status
        task.save()
        return Response(TaskSerializer(task).data)

    # 📌 REVİZE EKLEME, GÜNCELLEME & SİLME
    @action(detail=True, methods=['post'])
    @method_decorator(perm_required('add_revisestack'))
    def add_revise(self, request, pk=None):
        task = self.get_object()
        serializer = ReviseStackSerializer(data=request.data)
        if serializer.is_valid():
            revise = serializer.save(creator=request.user)
            task.revises.add(revise)
            return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'])
    @method_decorator(perm_required('change_revisestack'))
    def update_revise(self, request, pk=None):
        revise_id = request.data.get('revise_id')
        revise = get_object_or_404(ReviseStack, id=revise_id)
        serializer = ReviseStackSerializer(revise, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    @method_decorator(perm_required('delete_revisestack'))
    def delete_revise(self, request, pk=None):
        revise_id = request.data.get('revise_id')
        revise = get_object_or_404(ReviseStack, id=revise_id)
        revise.delete()
        return Response({"message": "Revize silindi"}, status=status.HTTP_204_NO_CONTENT)

    # 📌 RESİM EKLEME, GÜNCELLEME & SİLME
    @action(detail=True, methods=['post'])
    @method_decorator(perm_required('add_filestack'))
    def add_image(self, request, pk=None):
        task = self.get_object()
        serializer = ImageStackSerializer(data=request.data)
        if serializer.is_valid():
            image = serializer.save()
            task.revises.all().update(images=image)
            return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'])
    @method_decorator(perm_required('change_filestack'))
    def update_image(self, request, pk=None):
        image_id = request.data.get('image_id')
        image = get_object_or_404(ImageStack, id=image_id)
        serializer = ImageStackSerializer(image, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    @method_decorator(perm_required('delete_filestack'))
    def delete_image(self, request, pk=None):
        image_id = request.data.get('image_id')
        image = get_object_or_404(ImageStack, id=image_id)
        image.delete()
        return Response({"message": "Resim silindi"}, status=status.HTTP_204_NO_CONTENT)

    # 📌 DOSYA EKLEME, GÜNCELLEME & SİLME
    @action(detail=True, methods=['post'])
    @method_decorator(perm_required('add_filestack'))
    def add_file(self, request, pk=None):
        task = self.get_object()
        serializer = FileStackSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.save()
            task.revises.all().update(files=file)
            return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'])
    @method_decorator(perm_required('change_filestack'))
    def update_file(self, request, pk=None):
        file_id = request.data.get('file_id')
        file = get_object_or_404(FileStack, id=file_id)
        serializer = FileStackSerializer(file, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    @method_decorator(perm_required('delete_filestack'))
    def delete_file(self, request, pk=None):
        file_id = request.data.get('file_id')
        file = get_object_or_404(FileStack, id=file_id)
        file.delete()
        return Response({"message": "Dosya silindi"}, status=status.HTTP_204_NO_CONTENT)

    # 📌 RAPOR EKLEME, GÜNCELLEME & SİLME
    @action(detail=True, methods=['post'])
    @method_decorator(perm_required('add_reportstack'))
    def add_report(self, request, pk=None):
        task = self.get_object()
        serializer = ReportStackSerializer(data=request.data)
        if serializer.is_valid():
            report = serializer.save(creator=request.user)
            return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'])
    @method_decorator(perm_required('change_reportstack'))
    def update_report(self, request, pk=None):
        report_id = request.data.get('report_id')
        report = get_object_or_404(ReportStack, id=report_id)
        serializer = ReportStackSerializer(report, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    @method_decorator(perm_required('delete_reportstack'))
    def delete_report(self, request, pk=None):
        report_id = request.data.get('report_id')
        report = get_object_or_404(ReportStack, id=report_id)
        report.delete()
        return Response({"message": "Rapor silindi"}, status=status.HTTP_204_NO_CONTENT)
