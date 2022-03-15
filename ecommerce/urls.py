from django.urls import path
from . import views

urlpatterns = [
    path('create_disc', views.create_disc, name='create_disc'),
    path('get_disc', views.get_disc, name='get_disc'),
    path('delete_disc/<int:id_>', views.delete_disc, name='delete_disc'),
    path('put_disc/<int:id_>', views.put_disc, name='put_disc'),
]
