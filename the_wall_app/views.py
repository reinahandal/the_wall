from django.shortcuts import render, redirect
from . import models
from .models import Message

# This method renders the wall page for logged in/registered users
def display_wall(request):
    if 'logged_user' in request.session:
        context = models.display_on_wall(request)
        return render(request, 'wall.html', context)
    else:
        return redirect('/')

def post_message(request):
    models.post_message(request)
    return redirect('/wall')

def add_comment(request):
    models.add_comment(request)
    return redirect('/wall')

def delete_message(request):
    models.delete_message(request)
    return redirect('/wall')
