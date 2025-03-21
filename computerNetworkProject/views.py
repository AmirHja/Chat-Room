from django.shortcuts import render

def index_view(request):
    user = request.user
    return render(request, 'index.html', context={'sender': user})