from django.shortcuts import render
from rest_framework import viewsets, permissions, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from .models import Task, TaskHistory
from .serializers import TaskSerializer, TaskHistorySerializer
from rest_framework.decorators import action
from rest_framework.response import Response

# Create your views here.

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'priority_level']
    ordering_fields = ['due_date', 'priority_level']

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        task = self.get_object()
        task.mark_as_completed()
        return Response({'status': 'task marked as complete'})
    
    @action(detail=True, methods=['post'])
    def incomplete(self, request, pk=None):
        task = self.get_object()
        task.mark_as_pending()
        return Response({'status': 'task marked as incomplete'})
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        if instance.status == 'COMPLETED' and not partial:
            return Response({"detail": "Completed tasks cannot be fully updated."}, status=status.HTTP_400_BAD_REQUEST)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def completed(self, request):
        completed_tasks = self.get_queryset().filter(status='COMPLETED')
        page = self.paginate_queryset(completed_tasks)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(completed_tasks, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def history(self, request, pk=None):
        task = self.get_object()
        history = task.history.all()
        serializer = TaskHistorySerializer(history, many=True)
        return Response(serializer.data)


