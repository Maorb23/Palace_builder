from django.shortcuts import render
from django.views import View

class PalaceGenerateView(View):
    def post(self, request):
        # Placeholder: generate palace layer
        return render(request, 'tasks/dashboard.html', {})

class PalaceProgressView(View):
    def get(self, request):
        # Placeholder: show palace progress
        return render(request, 'tasks/dashboard.html', {}) 