from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets, permissions, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from .models import Task, TaskHistory
from .serializers import TaskSerializer, TaskHistorySerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from .forms import TaskForm, TaskFilterForm
from django.contrib import messages

# Create your views here.
@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    filter_form = TaskFilterForm(request.GET)
    
    if filter_form.is_valid():
        status = filter_form.cleaned_data.get('status')
        priority_level = filter_form.cleaned_data.get('priority_level')
        due_date_from = filter_form.cleaned_data.get('due_date_from')
        due_date_to = filter_form.cleaned_data.get('due_date_to')
        ordering = filter_form.cleaned_data.get('ordering')
        
        if status:
            tasks = tasks.filter(status=status)
        if priority_level:
            tasks = tasks.filter(priority_level=priority_level)
        if due_date_from:
            tasks = tasks.filter(due_date__gte=due_date_from)
        if due_date_to:
            tasks = tasks.filter(due_date__lte=due_date_to)
        if ordering:
            tasks = tasks.order_by(ordering)
    
    return render(request, 'tasks/task_list.html', {'tasks': tasks, 'filter_form': filter_form})

@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    return render(request, 'tasks/task_detail.html', {'task': task})

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, 'Task created successfully.')
            return redirect('task_detail', pk=task.pk)
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})

@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully.')
            return redirect('task_detail', pk=task.pk)
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully.')
        return redirect('task_list')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})

@login_required
def task_complete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.mark_as_completed()
        messages.success(request, 'Task marked as complete.')
    return redirect('task_detail', pk=task.pk)

@login_required
def task_incomplete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.mark_as_pending()
        messages.success(request, 'Task marked as incomplete.')
    return redirect('task_detail', pk=task.pk)

@login_required
def completed_tasks(request):
    completed_tasks = Task.objects.filter(user=request.user, status='COMPLETED')
    return render(request, 'tasks/completed_tasks.html', {'completed_tasks': completed_tasks})


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


