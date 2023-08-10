from .models import *

def queue(request):
    queues = GameQueue.objects.all()
    return {'queues': queues}
