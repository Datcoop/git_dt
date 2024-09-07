import time, datetime
from django.shortcuts import render
from .models import *
from .forms import *
from django.http import HttpResponseRedirect# Create your views here.

def upload_image(request, redir):

    usuario=request.user
    user=User.objects.filter(username=usuario).values('id','first_name')
    user_list = list(user)
    
    userID = int(user_list[0]['id'])  
    
    tipuser = int(user_list[0]['first_name'])  
         
    html = 'upload_image.html'
                
    if request.method == 'GET':
        
        return render(request, html)
        
    elif request.method == 'POST':

        usuario=request.user
        user=User.objects.filter(username=usuario).values('id','first_name')
        user_list = list(user)
    
        userID = int(user_list[0]['id'])  
    
        tipuser = int(user_list[0]['first_name'])
        
        form = ImageForm(request.POST, request.FILES)
               
        if form.is_valid():
            
            for filename, file in request.FILES.items():
                image = request.FILES[filename].name
        
            strfec = timestamp(str(image))
            
            print(strfec)
            
            new_image = Image(  image = form.cleaned_data["image"],
                                name = form.cleaned_data["name"],
                                fecha = strfec,
                                user_id = userID)
            print(image)
            new_image.save()
                
            msg = 'Imágen subida satisfactoriamente.'
                
            return render(request, html, {'msg': msg, 'image': image}) 
 
def timestamp(image):
        
    try:    
        arrfecha = image.split('.')
        
        arrfecha = image.split('.')[-2]
        
        fecha = arrfecha.split('_')[0]
        
        hora = arrfecha.split('_')[1]
        
        strfec = ''
        i = 1
        for d in fecha:
            strfec += d
            if i == 4:
                year = strfec
                strfec = ''
            elif i == 6:
                mes = strfec
                strfec = ''
            elif i == 8:
                dia = strfec
                strfec = ''
            i += 1
        
        strfec = ''
        i = 1
        for d in hora:
            strfec += d
            if i == 2:
                h = strfec
                strfec = ''
            elif i == 4:
                m = strfec
                strfec = ''
            elif i == 6:
                s = strfec
                strfec = ''
            i += 1
        
        strfec = f'{year}-{mes}-{dia} {h}:{m}:{s}.0-04' 
        
        return strfec
        
    except Exception as e:
    
        now = datetime.datetime.now()
        
        return now
                  
def image_gallery(request):
    images = Image.objects.all()       
        
    context = {}
    context["brand"] = 'Surcoop'
                
    return render(request, 'image_gallery.html', {'images': images, "proyectos": context})
            
            
def upload_image1(request, redir):
    
    if request.method == 'GET':
                
        html_temp = 'upload_image.html'
    
        url = request.path.split('/')        
        
        context = {}
        context['redir'] = url[-1] 
        context["brand"] = 'Surcoop'
                
        return render(request, 'upload_image.html', {'pagina':context, "proyectos": context})
        
    elif request.method == 'POST':
        print(f'{request.POST}, {request.FILES}')
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            new_image = Image(  file = form.cleaned_data["file"],
                                title = form.cleaned_data["title"],
                                username = request.session["nomuser"]
                                )
            new_image.save()
            return redirect(request.POST.get("redir"))

def upload_file(request, redir):

    usuario=request.user
    user=User.objects.filter(username=usuario).values('id','first_name')
    user_list = list(user)
    
    userID = int(user_list[0]['id'])  
    
    tipuser = int(user_list[0]['first_name'])  
         
    html = 'upload_image.html'
                
    if request.method == 'GET':
        
        return render(request, html)
        
    elif request.method == 'POST':

        usuario=request.user
        user=User.objects.filter(username=usuario).values('id','first_name')
        user_list = list(user)
    
        userID = int(user_list[0]['id'])  
    
        tipuser = int(user_list[0]['first_name'])
        
        form = ImageForm(request.POST, request.FILES)
               
        if form.is_valid():
            
            for filename, file in request.FILES.items():
                image = request.FILES[filename].name
        
            strfec = timestamp(str(image))
            
            print(strfec)
            
            new_image = Image(  image = form.cleaned_data["image"],
                                name = form.cleaned_data["name"],
                                fecha = strfec,
                                user_id = userID)
            print(image)
            new_image.save()
                
            msg = 'Imágen subida satisfactoriamente.'
                
            return render(request, html, {'msg': msg, 'image': image}) 
        
class MultiValueDict(dict):
        
    def getlist(self, key, default=None):
        """
        Return the list of values for the key. If key doesn't exist, return a
        default value.
        """
        return self._getlist(key, default, force_list=True) 
                           
'''
<QueryDict: {'csrfmiddlewaretoken': ['DQQVzIxdOH2zwF3tU0vrFNTR0sTUeHtZGlNfrY11nOih00Kny7WrI3tOKysrzp9Q'], 'redir': ['home'], 'title': ['La Virgen'], 'user': ['']}>, <MultiValueDict: {'image': [<InMemoryUploadedFile: Contadores-Públicos.jpg (image/jpeg)>]}>

'''        
    
    
    
