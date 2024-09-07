from django.urls import path
from . import views

app_name = 'fichero'

urlpatterns = [
    path('upload_file/<str:redir>', views.upload_file, name='upload_file'),
]
