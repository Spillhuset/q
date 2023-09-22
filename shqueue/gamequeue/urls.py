from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('queue/<int:queue_id>', views.view_queue, name='queue'),
    path('queue/<int:queue_id>/toggle', views.toggle_queue, name='queue_toggle'),
    path('queue/<int:queue_id>/clear_queue', views.clear_queue, name='queue_clear'),
    path('queue/<int:queue_id>/person/add', views.add_person, name='person_add'),
    path('queue/<int:queue_id>/person/<int:person_id>/start', views.start_person, name='person_start'),
    path('queue/<int:queue_id>/person/<int:person_id>/finish', views.finish_person, name='person_finish'),
    path('queue/<int:queue_id>/person/<int:person_id>/remove', views.remove_person, name='person_remove'),
    path('info/queue/<int:queue_id>', views.infoscreen_single, name='infoscreen_single'),
    path('info/queue/<int:queue_id>/data', views.infoscreen_data, name='infoscreen_data'),
]
