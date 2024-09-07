from django.urls import path
from . import views

app_name = 'gallery'

urlpatterns = [
    path('upload_image/<str:redir>', views.upload_image, name='upload_image'),
    path('upload_file/<str:redir>', views.upload_file, name='upload_file'),
    path('image_gallery/', views.image_gallery, name='image_gallery')
]
