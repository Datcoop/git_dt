import time, datetime
from django.shortcuts import render
from .models import *
from .forms import ImagesForm
from django.http import HttpResponseRedirect# Create your views here.

def upload_file(request, redir):

    usuario=request.user
    user=User.objects.filter(username=usuario).values('id','first_name')
    user_list = list(user)
    
    userID = int(user_list[0]['id'])  
    
    tipuser = int(user_list[0]['first_name'])  
         
    html = 'upload_file.html'
                
    if request.method == 'GET':
        
        return render(request, html)
        
    elif request.method == 'POST':

        usuario=request.user
        user=User.objects.filter(username=usuario).values('id','first_name')
        user_list = list(user)
    
        userID = int(user_list[0]['id'])  
    
        tipuser = int(user_list[0]['first_name'])
            
        form = ImagesForm(request.POST, request.FILES)
        
        is_valid = False
              
        if form.is_valid():
            is_valid = True
            images = request.FILES.getlist('pic')
            for image in images:
                image_ins = Fichas(pic = image)
                image_ins.save()
       
        context = {'form': form, 'is_valid': is_valid}
        print(context)
        return render(request, html, context)




