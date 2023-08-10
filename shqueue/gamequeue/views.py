from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import *
from .forms import *

def home(request):
    if not request.user.is_authenticated: return redirect("/accounts/login")
    return render(request, "shqueue/home.html")

@login_required
def view_queue(request, queue_id):
    queue = GameQueue.objects.get(id=queue_id)
    context = {'queue': queue}
    return render(request, "shqueue/view_queue.html", context)

@login_required
def toggle_queue(request, queue_id):
    queue = GameQueue.objects.get(id=queue_id)
    if queue.active: queue.active = False
    else: queue.active = True
    queue.save()
    return redirect("/queue/" + str(queue_id))

@login_required
def clear_queue(request, queue_id):
    queue = GameQueue.objects.get(id=queue_id)
    people = QueuedPerson.objects.filter(queue=queue)
    people.delete()
    return redirect("/queue/" + str(queue_id))

@login_required
def add_person(request, queue_id):
    queue = GameQueue.objects.get(id=queue_id)
    if request.method == "POST":
        form = AddPersonForm(request.POST)
        if form.is_valid():
            person = form.save(commit=False)
            person.queue = queue
            person.queued_by = request.user
            person.save()
            return redirect("/queue/" + str(queue_id))
    else:
        form = AddPersonForm()
    context = {'form': form, 'queue': queue}
    return render(request, "shqueue/add_person.html", context)

@login_required
def start_person(request, queue_id, person_id):
    person = QueuedPerson.objects.get(id=person_id)
    person.playing_at = timezone.now()
    person.playing_by = request.user
    person.save()
    return redirect("/queue/" + str(queue_id))

@login_required
def finish_person(request, queue_id, person_id):
    person = QueuedPerson.objects.get(id=person_id)
    person.finished_at = timezone.now()
    person.finished_by = request.user
    person.save()
    return redirect("/queue/" + str(queue_id))

@login_required
def remove_person(request, queue_id, person_id):
    person = QueuedPerson.objects.get(id=person_id)
    person.delete()
    return redirect("/queue/" + str(queue_id))

def infoscreen_single(request, queue_id):
    queue = GameQueue.objects.get(id=queue_id)
    context = {'queue': queue}
    return render(request, "infoscreen/single.html", context)
