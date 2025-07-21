from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Task, DailySession
from services.openai_service import analyze_task
from django.utils import timezone
from django.contrib.auth.models import User
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy

class IndexView(View):
    def get(self, request):
        user = request.user if request.user.is_authenticated else None
        today = timezone.now().date()
        session = DailySession.objects.filter(user=user, date=today).first()
        
        if session:
            tasks = session.tasks.filter(parent__isnull=True)
            total_tasks = tasks.count()
            completed_tasks = tasks.filter(is_completed=True).count()
            in_progress_tasks = total_tasks - completed_tasks
            total_palaces = tasks.filter(palace_image__isnull=False).count()
            recent_tasks = tasks.order_by('-id')[:5]
            
            # Calculate progress for each task
            for task in recent_tasks:
                subtasks = task.sub_tasks.all()
                total_subtasks = subtasks.count()
                completed_subtasks = subtasks.filter(is_completed=True).count()
                if total_subtasks > 0:
                    task.progress_percentage = (completed_subtasks / total_subtasks) * 100
                else:
                    task.progress_percentage = 0
                task.total_subtasks = total_subtasks
                task.completed_subtasks = completed_subtasks
        else:
            total_tasks = completed_tasks = in_progress_tasks = total_palaces = 0
            recent_tasks = []
        
        context = {
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'in_progress_tasks': in_progress_tasks,
            'total_palaces': total_palaces,
            'recent_tasks': recent_tasks,
        }
        return render(request, 'index.html', context)

class TasksView(View):
    def get(self, request):
        user = request.user if request.user.is_authenticated else None
        today = timezone.now().date()
        session = DailySession.objects.filter(user=user, date=today).first()
        tasks = session.tasks.filter(parent__isnull=True) if session else []
        return render(request, 'tasks/dashboard.html', {'tasks': tasks})

class TaskCreateView(View):
    def post(self, request):
        user = request.user if request.user.is_authenticated else None
        today = timezone.now().date()
        session, _ = DailySession.objects.get_or_create(user=user, date=today, defaults={"palace_theme": "Default"})
        # Get task description from form
        task_description = request.POST.get('task_description', '').strip()
        if not task_description:
            return redirect('dashboard')
        # Analyze with OpenAI
        ai_result = analyze_task(task_description)
        print('AI Result:', ai_result)
        # Create main Task with AI results
        main_task = Task.objects.create(
            session=session,
            title=task_description,
            category=ai_result.get('category', ''),
            complexity=ai_result.get('complexity', 1),
            is_completed=False
        )
        # Generate the base image for the palace
        from services.palace_generator import generate_palace_image
        generate_palace_image(main_task)
        print(f"Created main task: {main_task.title} (category: {main_task.category}, complexity: {main_task.complexity})")
        # Create sub-tasks if present
        for sub in ai_result.get('sub_tasks', []):
            sub_task = Task.objects.create(
                session=session,
                title=sub.get('title', ''),
                category=sub.get('category', ''),
                complexity=sub.get('complexity', 1),
                is_completed=False,
                order=sub.get('order', 0),  # Add order from LLM
                parent=main_task,
                time_estimate=sub.get('time_estimate')  # Save time_estimate if present
            )
            print(f"Created sub-task: {sub_task.title} (order: {sub_task.order}, category: {sub_task.category}, complexity: {sub_task.complexity}, time_estimate: {sub_task.time_estimate})")
        return redirect('dashboard')

class TaskCompleteView(View):
    def post(self, request, task_id):
        # Placeholder: mark task as complete
        return redirect('dashboard')

class TaskToggleCompleteView(View):
    def post(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        task.is_completed = not task.is_completed
        task.save()
        # If this is a sub-task and is now completed, trigger palace image generation
        if task.parent and task.is_completed:
            from services.palace_generator import trigger_palace_generation_async
            trigger_palace_generation_async(task.parent)
        return redirect('dashboard') 

class TaskDeleteView(View):
    def post(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        # Optionally: delete all sub-tasks as well
        task.delete()
        return redirect('dashboard')

class SubTaskEditView(View):
    def post(self, request, subtask_id):
        subtask = get_object_or_404(Task, id=subtask_id)
        subtask.title = request.POST.get('title', subtask.title)
        subtask.complexity = request.POST.get('complexity', subtask.complexity)
        time_estimate = request.POST.get('time_estimate')
        subtask.time_estimate = int(time_estimate) if time_estimate else None
        subtask.save()
        return redirect('dashboard') 