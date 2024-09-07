import json
import datetime
from datetime import datetime
import time
from datetime import date
from datetime import timedelta
from django.utils import timezone
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.files.storage import default_storage    
from django.core.files.base import ContentFile
import os
from pathlib import Path
import smtplib
import random
from django.core.mail import send_mail
from django.conf import settings

from .models import Task, Contacto, Fichero, Socios, Cooperativas, Tasas

from .forms import TaskForm, ContacForm, SignUpForm, LoginForm, PhotoForm, FicheroForm

from .pootask import *

from .clases import *

import requests
from bs4 import BeautifulSoup

# Create your views here.

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {"form": SignUpForm})
    else:

        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    request.POST["username"], password=request.POST["password1"])
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'signup.html', {"form": SignUpForm, "error": "Nombre de Usuario ya existe."})

        return render(request, 'signup.html', {"form": SignUpForm, "error": "Las contraseñas no coinciden."})

@login_required
def usuario(request):
    request.session['subir'] = 2
    return render(request, 'usuario.html')
    
@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html', {"tasks": tasks})

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'tasks.html', {"tasks": tasks})

@login_required
def eximport(request):

    request.session['subir'] = 1

    usuario=request.user
    user=User.objects.filter(username=usuario).values('id','first_name')
    user_list = list(user)
    
    userID = int(user_list[0]['id'])  
    
    tipuser = int(user_list[0]['first_name'])
    
    context = {'usuario': usuario, 'tipuser': tipuser}
       
    return render(request, 'eximport.html', {'context': context})

@login_required
def convertir(request):

    usuario=request.user
    user=User.objects.filter(username=usuario).values('id','first_name')
    user_list = list(user)
    
    userID = int(user_list[0]['id'])  
    
    tipuser = int(user_list[0]['first_name'])
    
    context = {'usuario': usuario, 'tipuser': tipuser}
    
    operfile = Archivo(request)
              
    return render(request, 'eximport.html', {'context': context})
    
@login_required
def my_image(request, image_name):
    # user upload file
    folder_path = 'path_to_your_file_folder/'
    fs = FileSystemStorage(location=folder_path, base_url=folder_path)    
    
    image_data = open(folder_path + image_name, "rb").read() #set file as variable
    fs.delete(folder_path + image_name)# delete the file from folder
    return HttpResponse(image_data, content_type="image")
    
@login_required
def create_task(request):
    if request.method == "GET":
        return render(request, 'create_task.html', {"form": TaskForm})
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {"form": TaskForm, "error": "Error creating task."})


def home(request):
    return render(request, 'home.html')

def contacto(request):
    if request.method == "GET":
        return render(request, 'contacto.html', {"form": ContacForm})
    else:
        try:
            form = ContacForm(request.POST)
            new_msg = form.save(commit=False)
            new_msg.save()
            
            subject = request.POST['asunto']
            message = request.POST['mensaje'] + " " + request.POST['correo']
            from_email = settings.EMAIL_HOST_USER
            recipient_list = ['javsalas@gmail.com', 'intalgos@gmail.com']
            send_mail(subject, message, from_email, recipient_list)
            
            return redirect('home')
        except ValueError:
            return render(request, 'contacto.html', {"form": ContacForm, "error": "Error al enviar formulario de Contacto."})


@login_required
def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {"form": LoginForm})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        login(request, user)
        
        if user is None:
            return render(request, 'signin.html', {"form": LoginForm, "error": "Usuario o contraseña incorrecto."})
        else:
            #eliminar archivos pdf
            delfile('media/Archivos/')
            usuario=request.POST['username']
            userlogin=User.objects.filter(username=usuario).values('id','first_name','username')
            user_obj = list(userlogin)
            user_list = [int(user_obj[0]['id']),int(user_obj[0]['first_name']),user_obj[0]['username']]
            
            if user_obj[0]['id']:
                userID = user_list[0]
                tipuser = user_list[1]
                Fichero.objects.filter(user_id=userID).delete()
            
            #Tasa BCV   .latest('testfield') 
            dictasa = tasachnge(request,98,tipuser) 
            
            valtasa = dictasa['tasa']
            fechant = dictasa['fecha'] 
        
            valdolar = float(valtasa)       
            valtasa = round(valdolar, 2)
            tasacambio = str(valtasa).split('.')
            dec = tasacambio[1]
            if len(dec) < 2:
                dec = f'{dec}0'
            tasacambio = f'{tasacambio[0]}.{dec}'
                         
            user_list.append(tasacambio)
            #eliminar archivos pdf
            delfile('media/Archivos/')
            
            dictnumtbl = {1: 103, 2: 140, 5: 103}
            
            msg = ''
            clase = ''
            monto = 0
            if tipuser == 5:
            
                fechnow = str(datetime.now()).split(' ')[0]
        
                fechult = tasachnge(request,103,5).split('T')[0]
                
                delta = dif_mes(datetime.strptime(fechnow, '%Y-%m-%d'),datetime.strptime(fechult, '%Y-%m-%d'))
                msg = f'No tiene cuotas vencidas'
                clase = 'alert alert-success'
                if int(delta) > 0:
                    if int(delta) == 1:
                        msg = f'Usted tiene 1 cuota vencida'
                    else:
                        msg = f'Usted tiene {delta} cuotas vencidas'
                    
                    clase = 'alert alert-danger'
                    monto = 4*delta*valtasa
                    
            user_list.append(dictnumtbl[tipuser])
            
            user_list.append(clase)
            user_list.append(msg)
            user_list.append(monto)
            user_list.append(fechant)
            request.session['user_list'] = user_list
            
            return redirect(f'/tasks/pages/{dictnumtbl[tipuser]}/1')

def dif_mes(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month
              
def tasachnge(request, num_tbl, tipuser): 
        
    comi = "'"
    paramfil = '1,0,5,1,1,2' 
    valwhere = f'0 > 0'      
    cmdtext = f"{num_tbl},{comi}DESC{comi},{paramfil},{comi}{valwhere}{comi},{comi}0{comi},{comi}0{comi}"
    fldcombos = Util(cmdtext) 
    listtasa = fldcombos.dict_selectodo(cmdtext)
    print(listtasa)
    dictasa = listtasa[1]
    fechval = dictasa['fecha'].split('T')[0]
    strfechval = f'{fechval} 09:00:00'
    
    fechval = datetime.strptime(strfechval, '%Y-%m-%d %H:%M:%S')
    print(fechval)
    
    print(datetime.now())
    if datetime.now() >= fechval:
        dictasa = listtasa[0]
        print('simayor =',listtasa[0])
        
    if num_tbl == 98:  
        return dictasa
    elif num_tbl == 103: 
        lastfecha = dictasa['fecha']  
        return lastfecha
  
def actualizartasa(request,tasa,fechant,fldcombos):
    
  r = requests.get('https://www.bcv.org.ve/glosario/cambio-oficial')
  s = BeautifulSoup(r.content, 'html.parser')
    
  try:  
    if r.status_code == 200:
        
        listfechval = []
        for text in s.find_all('span',{'class':'date-display-single'}):
            b = text
            listfechval.append(b)
            fechval = str(listfechval[0]) 
            fechval = fechval.split(' content="')
            fechavallocal = fechval[1].split('">')[1].replace('</span>','')
            
            fechval = fechval[1].split('T')[0]
            strfechval = f'{fechval} 09:00:00'
            #print('fechval',fechval)
        request.session['fechval'] = fechavallocal 
          
        fechnow = str(datetime.now()).split(' ')[0]
        strfechant = fechant.split('T')[0]
        if fechval != strfechant and datetime.now() > datetime.fromisoformat(strfechval):
            valdolar = []
            for text in s.find_all('div',{'class':'col-sm-6 col-xs-6 centrado'}):
                b = text
                valdolar.append(b)    
            valdolar = str(valdolar[4]).replace(' ', '')
            valdolar = valdolar.split('<strong>')
            valdolar = valdolar[1].split('</strong>')
            valdolar = valdolar[0].replace(',', '.') 
            valdolar = float(valdolar)       
            valdolar = round(valdolar, 2)
        
            dictval = {"tasa": valdolar, "fecha": strfechval}
                    
            insvaldolar = fldcombos.fnt_insert(98,dictval)
    
            return valdolar
        else:     
            return tasa
    else:
        return tasa
  except:    
    return tasa

def util(request, nrut, prm):
    print(request.POST)
    
    comi = "'"
    
    metodo = request.method
    
    if metodo == 'POST':  
            print(request.POST, nrut, prm)     
                             
            param = request.POST['param']      
                             
            frm = request.POST['frm']   
        
            dictidpass = {0: 'password', 1: 'new_password1', 2: 'new_password2'}  
        
            dictiddivpw = {0: 'pw', 1: 'pw1', 2: 'pw2'}  
        
            dictfaeye = {0: 'faeye', 1: 'faeye1', 2: 'faeye2'}  
            
            dictcontra = {0: 'Contraseña', 1: 'Contraseña nueva', 2: 'Repetir Contraseña'}
            
            dicteyeslash = {'fas fa-eye': 'fas fa-eye-slash', 'fas fa-eye-slash': 'fas fa-eye'}   
              
            dicttype = {'fas fa-eye': 'text', 'fas fa-eye-slash': 'password'}    
            
            valpass = request.POST[dictidpass[nrut]]
            print(dictidpass[nrut],valpass)
            pwinp = f'<input type="{dicttype[param]}" id="{dictidpass[nrut]}" name="{dictidpass[nrut]}" placeholder="Password" class="form-control" value="{valpass}" required ><label for="{dictidpass[nrut]}">{dictidpass[nrut]}</label>'             
            resspan = f'<span class="input-group-text btn btn-secondary" style="padding: 15px; font-size: 17px; cursor: pointer;" data-bs-toggle="tooltip" data-bs-placement="top" title="Mostrar Contraseña" onclick="llenarfld({comi}/util/{nrut}/{dicteyeslash[param]}{comi},{comi}{frm}{comi}, {comi}{dicteyeslash[param]}{comi})"><i class="{dicteyeslash[param]}"></i></span>'
                    
            dicteye = {}
            
            dicteye['idpw']  = dictiddivpw[nrut]
                    
            dicteye['pwinp'] = pwinp  
            
            dicteye['idfaeye'] = dictfaeye[nrut] 
            
            dicteye['eyeslash'] = resspan
                    
            dicteye['ruta'] = 'eye'   
                
            return JsonResponse({'data': dicteye}) 
     
@login_required
def pages(request, redirh, ruta):
    
    context = {}
    
    comi = "'"
    
    url = request.path.split('/')
    
    userID = request.session['user_list'][0]
    tipuser = request.session['user_list'][1]
    
    metodo = request.method
    print(url,metodo,redirh,ruta)
    
    try:
        if metodo == 'POST':         
            
            num_tbl = redirh  
                
            if ruta == '1':    
                
                onfnt = Llenar(num_tbl, ruta, request.POST)
             
                dataobj1 = onfnt.cmdtextfnt()
                print('dataobj1', dataobj1)
                fldcombos = Fntsql(dataobj1['cmdtext']) 
        
                user_list = fldcombos.dict_selectuno()
                
                indicepag = Util(dataobj1['cmdtext'])
                pagi = indicepag.paginacion(dataobj1['paramfil'], num_tbl, user_list['fldtitulos'], user_list['numreg'], user_list['numpags'], dataobj1['argprm'], dataobj1['irpag'])
                
                dataobj = indicepag.tbl(num_tbl,pagi,dataobj1['paramfil'],dataobj1['arrprm'],dataobj1['ordpage']) 
                
                dataobj['ruta'] = ruta                
                dataobj['textbox'] = ''                
                dataobj['argprm'] = dataobj1['argprm']                
                dataobj['pagant'] = dataobj1['indice']                
                dataobj['numpags'] = user_list['numpags']                 
                dataobj['paramfil'] = dataobj1['paramfil']                   
                dataobj['ordpage'] = dataobj1['ordpage']                   
                dataobj['valwhere'] = dataobj1['valwhere']                       
                context['limite'] = f' {dataobj["limite"]} filas'  
               
                return JsonResponse({'data': dataobj, 'proyectos':context}) 
                
            elif ruta == '100':            
                print(request.POST)
                ordpage = request.POST['ordpage']
                argprm = request.POST['argprm']
                arrprm = request.POST['param'].split('-')
                indice = request.POST['indice']
                pagant = int(request.POST['pagant'])
                numpags = int(request.POST['numpags'])
                irpagen = int(request.POST['irpag']) 
                irpag = irpagen 
                if irpagen > numpags:
                    irpag = numpags    
                elif irpagen <= 1:
                    irpag = 1                                    
                paramfil = request.POST['paramfil']
                arrparamfilaux = paramfil.split(',')
                arrparamfil = []
                for fil in arrparamfilaux: 
                    arrparamfil.append(int(fil))
                accion = arrparamfil[2]  
                limite = int(request.POST['regxpag']) 
                
                logfirst = str(arrprm[0])
                
                ascdesc = 'ASC'
                inxcol = 0
                valor1 = ''
                valor2 = ''
                #----------- ini if 1.1
                if logfirst != 'ini': 
                  fldbus = arrparamfil[0]
                  fldord = arrparamfil[1]
                  if logfirst == 'avan' and arrprm[-1] == '0': 
                    fldbus = int(arrprm[1])+1
                    logfirst = arrprm[2]
                    inxcol=fldbus
                  elif logfirst == 'ord':
                    if arrprm[2] != 'reset':
                        fldord = int(arrprm[1])+1
                        logfirst = arrprm[0]                    
                        dictascdesc = {'sort': 'asc', 'asc': 'desc', 'desc': 'asc'}
                        arrordpage = ordpage.split('-')
                        ascdesc = dictascdesc[arrordpage[2]]
                        ordpage = f'{logfirst}-{fldord}-{ascdesc}'
                        arrprm = ordpage.split('-') 
                  else: 
                    logfirst = arrprm[2]
                    
                    indice = arrparamfil[4]
                    
                    dictmov = {'page': int(arrprm[-2]),'Previous': -1, 'Next': 1, 'pgfin': int(arrprm[-2]), 'Extremos': [0, numpags+1], 'irpag': irpag}
                    indiceorig = indice
                    
                    if arrprm[-1] == 'page' or arrprm[-1] == 'pgfin':
                        indice = 0 
                    if arrprm[-1] != 'lim':
                        indice += dictmov[arrprm[-1]]
                    if arrprm[-1] == 'irpag':
                        indice = dictmov[arrprm[-1]]
                    if indice in dictmov['Extremos']:
                        indice = indiceorig
                        pagant = indice
                        
                  if arrprm[2] == 'reset':
                      paramfil = f'1,0,5,1,1,{limite}'
                  else:                       
                      dictparamfil = {0: fldbus, 1: fldord, 2: accion, 3: pagant, 4: indice, 5: limite}
                  
                      paramfil = ''
                      c = 0
                      for parfil in arrparamfil:
                          if c < 5:
                              paramfil += f'{dictparamfil[c]},'
                          else:
                              paramfil += f'{dictparamfil[c]}'
                          c += 1
                              
                  accion = arrparamfil[2]
                  valor1 = request.POST['boxizq1']
                  valor2 = request.POST['boxder1'] 
                  inxcol = int(fldbus)
                
                else:
                  key = logfirst  
                werlog = Dictoperador() 
                 
                valwhere = str(request.POST['valwhere'])
                
                listfil = request.POST['listfil'].split(',')
                print(len(listfil),listfil)  
                
                werfil = ''
                valwhereaux = ''
                if arrprm[0] == 'avan':
                    valwhereaux = valwhere
                    werfil = werlog.fnt_dictoperval(inxcol, logfirst, valor1, valor2) 
                    if len(listfil) == 1:
                        arrwer = request.POST['arrwer']
                        valwhere = f'{arrwer} AND {werfil}'
                        valwhereaux = valwhere
                    else:
                        arrvalwhere = valwhere.split(' AND ')
                        valwhere = ''
                        trfl = {"true": " AND ", "false": ""} 
                        c=0
                        for tf in listfil:
                            if c == len(listfil)-1: 
                                if trfl[tf] != '':     
                                    valwhere += f'{arrvalwhere[c]}'
                            else:  
                                if trfl[tf] != '':  
                                    valwhere += f'{arrvalwhere[c]}{trfl[tf]}'
                            print(tf, valwhere)
                            c += 1 
                        valwhere += 'zz'
                        valwhere = valwhere.replace(' AND zz', '')
                        valwhere = valwhere.replace('zz', '')
                        valor1 = str(request.POST['boxizq1'])
                        print("valor1",valor1)
                        if valor1 != "": 
                            valwhere += f' AND {werfil}'
                            arrwer = request.POST['arrwer']
                            valwhereaux = f'{arrwer} AND {werfil}'
                            print("valwhereaux",valwhereaux)
                else:
                    arrwer = request.POST['arrwer']
                    valwhereaux = arrwer
                    argprm = 'page'
                    
                if valwhere != '':    
                    cmdtext = f"{num_tbl},{comi}{ascdesc}{comi},{paramfil},{comi}{valwhere}{comi},{comi}0{comi},{comi}0{comi}"
                else:  
                    cmdtext = f"{num_tbl},{comi}{ascdesc}{comi},{paramfil},{comi}0 = 0{comi},{comi}0{comi},{comi}0{comi}" 
                
                if arrprm[0] == 'edit':  
                    valwhere = request.POST['valwhere']  
                    cmdtext = f"{num_tbl},{comi}{ascdesc}{comi},{paramfil},{comi}{valwhere}{comi},{comi}0{comi},{comi}0{comi}"
                    print('---------------',cmdtext)
                
                fldcombos = Diccionario(request,cmdtext) 
        
                user_list = fldcombos.dict_selectuno()
                
                pagi = paginacion(paramfil, num_tbl, user_list['fldtitulos'], user_list['numreg'], user_list['numpags'], argprm, irpag)
            
                dataobj = fldcombos.tbl(num_tbl,pagi,paramfil,arrprm,ordpage) 
                
                valwhere = valwhereaux
                
                dataobj['ruta'] = ruta                
                dataobj['textbox'] = ''                
                dataobj['argprm'] = argprm                
                dataobj['pagant'] = indice                
                dataobj['numpags'] = user_list['numpags']                 
                dataobj['paramfil'] = paramfil                   
                dataobj['ordpage'] = ordpage                   
                dataobj['valwhere'] = valwhere                       
                context['limite'] = f' {dataobj["limite"]} filas'  
               
                return JsonResponse({'data': dataobj, 'proyectos':context}) 
            #Actualizar      
            elif ruta == '2':
                print(request.POST)
                arrprm = request.POST['param'].split('-')
                
                prm = int(arrprm[0])
                
                prm2 = int(arrprm[1])+1
                
                context = request.session['selectuno']
                
                arrrel = context['relacional'].split(", ") 
                             
                posrel = arrrel[prm].split('u')[0]
                
                if posrel == '10' or posrel == '11':
                    posrel = '1'
                try:
                 operlog = Util('') 
                
                 dictoperlogdescri = operlog.fnt_dictoperdescri(posrel)
                except Exception as e:
                 print(e)
                print('dictoperlogdescri',dictoperlogdescri)
                resRes = ''
                key=0
                for log in dictoperlogdescri['listoperdescri']:
                    resRes += f'<li><a href="#" class="link-dark d-inline-flex text-decoration-none rounded" onclick="llenarfld({comi}/tasks/pages/{num_tbl}/3{comi},{comi}frmparam{comi},{comi}{key}-{log}-{prm}-0{comi})">{log}</a></li>'
                    key += 1
                    
                dictoperlogdescri['divRes'] = f'rescrit{int(arrprm[1])}'
                
                dictoperlogdescri['resRes'] = resRes
                
                dictoperlogdescri['ruta'] = ruta
                
                dictoperlogdescri['textbox'] = ''
                
                return JsonResponse({'data': dictoperlogdescri})
                      
            elif ruta == '3':
              try:
                print(request.POST)
                arrprm = request.POST['param'].split('-')
                
                fldbus = arrprm[2]
                
                textlog = arrprm[1]
                
                arrval = textlog.split(' y ')
                
                context = request.session['selectuno']
                
                arrfld = context['fldtitulos'].split(", ") 
                
                inxfld = int(arrprm[2])
                             
                nomcol = arrfld[inxfld].upper()
                
                dicttextbox = {}
                
                textbox = f'<div><p class="text-white bg-dark text-center rounded" id="valcol">Introduzca valore(s) de {nomcol}</p> <div class="row p-2">'
                if len(arrval) == 1:
                    textbox += f'<div class="form-floating mb-3 col-12"><input type="text" class="form-control" id="boxizq" name="boxizq" value="" placeholder="{arrval[0]}" onchange="fillbox({comi}boxizq{comi},{comi}boxizq1{comi})"><label for="boxizq" class="p-3">{arrval[0]}</div></div>'
                else:
                    textbox += f'<div class="form-floating mb-3 col-12"><input type="text" class="form-control" id="boxizq" name="boxizq" value="" placeholder="{arrval[0]}" onchange="fillbox({comi}boxizq{comi},{comi}boxizq1{comi})"><label for="boxizq" class="p-3">{arrval[0]}</div><div class="form-floating mb-3 col-12"><input type="text" class="form-control" id="boxder" name="boxder" value="" placeholder="{arrval[1]}" onchange="fillbox({comi}boxder{comi},{comi}boxder1{comi})"><label for="boxder" class="p-3">{arrval[1]}</div></div>'
                argprm = f'{comi}avan-{inxfld}-{textlog}-0{comi}'
                dicttextbox['textbox'] = f'{textbox}<div class="row"><div id="addfil"></div><button class="btn btn-primary col-4" onclick="llenarfld({comi}/tasks/pages/{num_tbl}/1{comi},{comi}frmparam{comi},{argprm})">Filtrar</button><p class="col-1"></p><button class="btn btn-primary col-6" onclick="llenarfld({comi}/tasks/pages/{num_tbl}/4{comi},{comi}frmparam{comi},{comi}avan-{inxfld}-{textlog}-addfil{comi})">Agregar filtro</button></div></div>'
                
                dicttextbox['argprm'] = argprm
                
                dicttextbox['fldbus'] = fldbus
                
                dicttextbox['ruta'] = ruta
                
                return JsonResponse({'data': dicttextbox})
                
              except Exception as e:
                print(e)   
                      
            elif ruta == '4':
              try:
                print(request.POST)
                paramfil = request.POST['paramfil']
                
                arrwer = request.POST['arrwer']
                
                valwhere = request.POST['valwhere']
                
                valor1 = str(request.POST['boxizq1'])
                
                if valor1 != '':
                    arrwer = valwhere
                    
                listparam = request.POST['param'].split('-')
                criterio = listparam[2]
                arrcrit = criterio.split(' y ')
                
                context = request.session['selectuno']
        
                arrtit = context['fldtitulos'].split(", ")
                
                arrfiltros = arrwer.split(' AND ')
                
                filval = Llenar(num_tbl, ruta, request.POST)
                
                chk = '<ul class="btn-toggle-nav list-unstyled fw-normal pb-1 small"><div class="col-12 text-center text-light bg-dark">Filtros</div>'
                i = 0
                for filtro in arrfiltros:
                    prm = f'{comi}/tasks/pages/{num_tbl}/5{comi},{comi}frmparam{comi}, {comi}{comi}' 
                    if i == 0:
                        chk += f'<li class="row"><p class="col-8 mt-1">Todos los registros</p><div class="form-check form-switch col-1 mt-2"><input class="form-check-input" type="checkbox" id="chkfil{i}" name="chkfil" onclick="filchk({comi}listfil{comi},{comi}chkfil{comi},{prm})" checked /></div></li>'
                    else: 
                        listfiltro = filtro.split(' ')
                        print(listfiltro)
                        titulo = arrtit[int(listfiltro[0])-1].upper()
                        criterio = filval.fnt_dictoperkey(filtro)
                        valor = f'"{listfiltro[2].replace("%","")}"'    
                        chk += f'<li class="row"><p class="col-8 mt-1">{titulo} {criterio} {valor}</p><div class="form-check form-switch col-1 mt-2"><input class="form-check-input" type="checkbox" id="chkfil{i}" name="chkfil" onclick="filchk({comi}listfil{comi},{comi}chkfil{comi},{prm})" checked /></div></li>' 
                    i += 1
                    
                chk += '</ul>'
                
                dicttextbox = {}
                
                dicttextbox['addfil'] = chk
                
                dicttextbox['arrwer'] = arrwer
                
                dicttextbox['ruta'] = ruta
                
                return JsonResponse({'data': dicttextbox})
                
              except Exception as e:
                print(e)   
                      
            elif ruta == '5':
              try:
                print(request.POST)
                
                listfil = request.POST['listfil'].split(',')
                print(listfil[1])
                
                dicttextbox = {}
                
                dicttextbox['listfil'] = listfil
                
                dicttextbox['ruta'] = ruta
                
                return JsonResponse({'data': dicttextbox})
                
              except Exception as e:
                print(e)  
                      
            elif ruta == '7':    
                print("Tasas =",request.POST)       
                cmdtext = ''
                
                candias = request.POST['candias']
                
                fldcombos = Util(cmdtext) 
                
                dictval = fldcombos.actualizartasa(candias)  
                
                tasacambio = f'Tasa de cambio BCV: { dictval["tasa"] } Bs/$.' 
                
                valhasta = f'Válida hasta las 9:00am del dia { dictval["fecha"] }'
                
                dicttasa = {}
                
                dicttasa['valhasta'] = valhasta
                
                dicttasa['tasacambio'] = tasacambio
                
                dicttasa['ruta'] = ruta
                
                return JsonResponse({'data': dicttasa})
                      
            elif ruta == '8':
              try: 
                comi = "'"
                print(request.POST)
                
                paramfil = request.POST['paramfil']
                
                arrprm = request.POST['param'].split('-')
                
                if tipuser == 2:    
                    cmdtext = f"{num_tbl},{comi}ASC{comi},1,0,5,1,1,10,{comi}0 > 0{comi},'0','0'"
                else:
                    valwhere = request.POST['valwhere']
                    cmdtext = f"{num_tbl},{comi}ASC{comi},1,0,5,1,1,10,{comi}{valwhere}{comi},'0','0'"
                
                fldcombos = Diccionario(request,cmdtext)
        
                context = fldcombos.dict_selectuno()
                
                arrtit = context['fldtitulos'].split(", ")
        
                arrfld = context['fldselect'].split(", ")
        
                arrrel = context['relacional'].split(", ")
                
                valinp = Diccionario('', '')
                
                numrow = 0
                
                rowval = 0
                
                fldedit = Util('')
                inpbox = f'<form method="post" id="frmup" enctype="multipart/form-data">'
                if arrprm[0] == 'add':
                
                    numrow = context['numreg']+1
                    
                    arrfltg = context['row_to_json']['tiggers'].split(", ")
                    
                    arrvaltigg = context['row_to_json']['valtiggers'].split(", ")
                    print('arrvaltigg =',arrvaltigg)
                    
                    arrcampinsshow = context['row_to_json']['camposinsshow'].split(", ")
                    
                    inpbox += f'<input type="hidden" id="param" name="param">'
                    
                    inpbox += f'<div class="p-2"><div>Agregar el registro número {numrow}</div>'
                    
                    inpbox += buildinputbox(self, arrfltg, arrcampinsshow, arrrel)
                    j=0
                    for tit in range(len(arrfltg)):
                        if arrcampinsshow[j] != 'vacio':
                            tp = arrrel[j].split('u')[0]
                            if tp == '10':
                                arrtbl = arrrel[j].split('u')[1].split('x')
                                for tbl in arrtbl:
                                    cmdtext = f"{tbl},'ASC',1,0,7,3,1,10,'0 > 0','0','0'"
                                    fldcombos = Diccionario(request,cmdtext) 
                                    contextodo = fldcombos.dict_selectodo()
                                    sel = f'<div class="form-floating p-1"><select class="form-select bg-light" id="inp-{j}" name="inp-{j}" aria-label="Floating label select">'
                                    for dictcbo in contextodo:
                                        for key,opt in dictcbo.items():
                                            if key == 'numrows':
                                                numrows = dictcbo["numrows"]
                                            else:
                                                sel += f'<option value="{numrows}">{opt}</option>'
                                    titulo = fldcombos.get_titulotbl(tbl)
                                    sel += f'</select><label for="floatingSelect">{titulo}</label></div>'
                                inpbox += sel 
                            elif tp == '11':
                                cmdtext = f"{num_tbl},'ASC',1,0,7,3,1,10,'0 > 0','0','0'"
                                fldcombos = Diccionario(request,cmdtext) 
                                contextodo = fldcombos.dict_selectodo()
                                sel = f'<div class="col-md p-1"><div class="form-floating"><input list="dtl-{j}" type="number" class="form-control bg-light" id="inp-{j}" name="inp-{j}" placeholder="{arrtit[j]}" aria-describedby="basic-addon1" value="" style="font-size: 14px; color: #5b5b68"><label for="inp-{j}">{arrtit[j]}</label></div></div>'
                                sel += f'<datalist id="dtl-{j}">'
                                for dictcbo in contextodo:
                                  for key,opt in dictcbo.items():
                                    if key == 'codigo':
                                        sel += f'<option value="{opt}"></option>'
                                titulo = fldcombos.get_titulotbl(tbl)
                                sel += f'</datalist>'
                                inpbox += sel 
                                    
                            else: 
                                tp = arrrel[j] 
                                valdefault = fldedit.fnt_dattype(tp)
                                inpbox += fldedit.fnt_dictcontrolhtml(arrrel[j], arrtit, j, valdefault)
                      
                        else:
                            if arrfltg[j] != 'vacio':  
                                if str(arrvaltigg[j]) == '20':
                                    numid = request.session['user_list'][0]
                                    inpbox += fldedit.fnt_dictcontrolhtml('20', arrtit, j, numid)
                                elif str(arrvaltigg[j]) == '21':
                                    dtnow = str(datetime.now())
                                    dtnow = f"{dtnow.split(' ')[0]} 09:00:00"
                                    print("dtnow =",dtnow)
                                    inpbox += fldedit.fnt_dictcontrolhtml('21', arrtit, j, dtnow)
                          
                        j += 1
                              
                    inpbox += f'<div class="row p-2"><span class="col-6"><button type="button" class="btn btn-primary" data-bs-dismiss="offcanvas" aria-label="Close">Cancelar</button></span><span class="col-6"><button class="btn btn-primary" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasRight" aria-controls="offcanvasRight" onclick="llenarfld({comi}/tasks/pages/{num_tbl}/9{comi},{comi}frmup{comi},{comi}add-{numrow}-insert-0{comi})">Agregar<i class="fa fa-plus-circle p-1"></i></button></span></div></div>'
                else:                    
                
                    numrow = int(request.POST['valup'])
                
                    rowval = int(request.POST['valup'])
                
                    paramfilorig = request.POST['paramfil']
                                
                    arrprf = paramfil.split(',')
                    
                    arrwer = request.POST['arrwer']
                
                    paramfil = f'{arrprf[0]},{arrprf[1]},9,{arrprf[3]},{arrprf[4]},{numrow}'
                    cmdtext8 = f"{num_tbl},'ASC',{paramfil},{comi}{arrwer}{comi},'0','0'"
                    fldcombos = Diccionario(request,cmdtext8) 
                    contextodo = fldcombos.dict_selectodo()
                    arrvalinp = contextodo[0]
                    
                    inpbox += f'<input type="hidden" id="param" name="param">'
                              
                    inpbox += f'<div>Actualizar el registro número {numrow}</div>'
                    
                    arrfldup = context['row_to_json']['camposupdate'].split(", ")
                    j=0
                    for tit in range(len(arrfldup)):
                      if arrfldup[j] != 'vacio':
                        tp = arrrel[j].split('u')[0]
                    
                        if tp == '10':
                            arrtbl = arrrel[j].split('u')[1].split('x')
                            for tbl in arrtbl:
                                cmdtext = f"{tbl},'ASC',1,0,7,3,1,10,'0 > 0','0','0'"
                                fldcombos = Diccionario(request,cmdtext) 
                                cbotodo = fldcombos.dict_selectodo()
                                sel = f'<div class="form-floating p-1"><select class="form-select bg-light" id="inp-{j}" name="inp-{j}" aria-label="Floating label select">'
                                valfld = arrvalinp[arrfld[j]]
                                arrvalinprow = valinp.dict_findnumrow(tbl,valfld)[0]
                                seleccionado = ''
                                for dictcbo in cbotodo:
                                  for key,opt in dictcbo.items():
                                    if key == 'numrows':
                                        numrows = dictcbo["numrows"]
                                    else:
                                        if str(opt) == str(arrvalinprow[arrfld[j]]):
                                            seleccionado = 'selected'
                                        else:
                                            seleccionado = ''
                                        sel += f'<option value="{numrows}" {seleccionado}>{opt}</option>'
                                titulo = fldcombos.get_titulotbl(tbl)
                                sel += f'</select><label for="floatingSelect">{titulo}</label></div>'
                            inpbox += sel 
                        elif tp == '11':
                                cmdtext = f"{num_tbl},'ASC',1,0,7,3,1,10,'0 > 0','0','0'"
                                fldcombos = Diccionario(request,cmdtext) 
                                contextodo = fldcombos.dict_selectodo()
                                sel = f'<div class="col-md p-1"><div class="form-floating"><input list="dtl-{j}" type="number" class="form-control bg-light" id="inp-{j}" name="inp-{j}" placeholder="{arrtit[j]}" aria-describedby="basic-addon1" value="{arrvalinp[arrfld[j]]}" style="font-size: 14px; color: #5b5b68"><label for="inp-{j}">{arrtit[j]}</label></div></div>'
                                sel += f'<datalist id="dtl-{j}">'
                                for dictcbo in contextodo:
                                  for key,opt in dictcbo.items():
                                    if key == 'codigo':
                                        sel += f'<option value="{opt}"></option>'
                                titulo = fldcombos.get_titulotbl(tbl)
                                sel += f'</datalist>'
                                inpbox += sel 
                        else:
                            inpbox += fldedit.fnt_dictcontrolhtml(arrrel[j], arrtit, j, arrvalinp[arrfld[j]])
                        j += 1
                    cmdtext = cmdtext8.replace("'","|")     
                    inpbox += f'<div class="row p-2"><span class="col-6"><button type="button" class="btn btn-primary" data-bs-dismiss="offcanvas" aria-label="Close">Cancelar</button></span><span class="col-6"><button class="btn btn-primary" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasRight" aria-controls="offcanvasRight" onclick="llenarfld({comi}/tasks/pages/{num_tbl}/9{comi},{comi}frmup{comi},{comi}edit-{numrow}-{cmdtext}-{paramfilorig}{comi})">Actualizar<i class="fa fa-refresh p-1"></i></button></span></div></div>'
               
                dicttextbox = {}
                     
                dicttextbox['rowval'] = rowval
                     
                dicttextbox['ruta'] = ruta
                
                dicttextbox['inpbox'] = f'{inpbox}</form>'
                
                return JsonResponse({'data': dicttextbox})
              except Exception as e:
                print(e)    
                      
            elif ruta == '9':
                try:
                    print(request.POST)
                    cmdtext = f"{num_tbl},{comi}ASC{comi},1,0,5,1,1,10,{comi}0 > 0{comi},{comi}0{comi},{comi}0{comi}"
                    fldcombos = Diccionario(request,cmdtext)
        
                    context = fldcombos.dict_selectuno()
                
                    arrprm = request.POST['param'].split('-')
                    
                    cmdtext = arrprm[2].replace("|", "'")
                    print(cmdtext)
                    
                    dictval = dict(request.POST)
                    
                    fldcombos = Diccionario(request,cmdtext)
                    
                    fila = int(arrprm[1])
                    
                    paramjson = {}
                                                
                    if cmdtext == 'insert':
                        arrfld = context['row_to_json']['fldselect'].split(", ")
                        print(arrfld)
                        j=0
                        for key,value in dictval.items():
                            print(key,value[0])
                            if key != 'param':
                                value = value[0]
                                paramjson[arrfld[j]] = value
                                j += 1
                        
                        fldcombos = Util(cmdtext) 
                
                        upreg = fldcombos.insertdata(num_tbl,paramjson)
                        
                        fila += 1
                         
                    else:
                        arrparamfil = arrprm[-1].split(',')
                        
                        indice = int(arrparamfil[4])
                    
                        limite = int(arrparamfil[5])
                    
                        arrfld = context['row_to_json']['fldselect'].split(", ")
                        arrhcol = context['row_to_json']['chup'].split(", ")
                        listcolhidden = []
                        for inx in arrhcol:
                            listcolhidden.append(arrfld[int(inx)])
                        print(listcolhidden)
                        
                        upreg = []
                        for key,value in dictval.items():
                            if key != 'param' and int(arrfld[j]) not in listcolhidden:
                                value = value[0]
                                key = int(key.split('-')[-1])
                                paramjson[arrfldup[key]] = value
                                upreg.append(value)
                                
                        paramjson=json.dumps(paramjson)        
                        fldcombos = Diccionario(request,cmdtext) 
                        contextodo = fldcombos.dict_selectodo()  
                        arrvalinp = contextodo[0]
                             
                        cmdtextup = f'{num_tbl}, {arrvalinp["id"]}, {comi}[{paramjson}]{comi}'
                        rawData = fldcombos.dict_update_filas(cmdtextup)
                            
                        fila = fila-(indice-1)*limite
                                           
                    dicttextbox = {}
                
                    dicttextbox['upreg'] = upreg
                
                    dicttextbox['fila'] = fila
                
                    dicttextbox['ruta'] = ruta
                
                    return JsonResponse({'data': dicttextbox})
                except Exception as e:
                    print(e)       
                
                
        elif metodo == 'GET': 
            #['', 'tasks', 'pages', '103']
            num_tbl = redirh 
            comi = "'"
            cmdtext = f"{num_tbl},{comi}ASC{comi},1,0,5,1,1,10,{comi}0 > 0{comi},{comi}0{comi},{comi}0{comi}"
            fldcombos = Diccionario(request,cmdtext)
        
            context = fldcombos.dict_selectuno()
            
            request.session['selectuno'] = context
        
            arrtit = context['fldtitulos'].split(", ")
        
            numreg = context['numreg']
            numreg = int(numreg)+1
               
            dicttit = {}
            for i in range(len(arrtit)):
                dicttit[i] = arrtit[i]
               
            context['dicttit'] = dicttit        
            context['titulos'] = context['fldtitulos'].split(", ")
            context['num'] = num_tbl
            context['url'] = request.path
            context['titulotbl'] = context['titulotbl']
            context['numreg'] = numreg
            
            valwhere = f'0 > 0'
            if request.session["user_list"][1] == 5:
                valwhere = f'0 > 0 AND 5 = {request.session["user_list"][2]}'
                
            context['valwhere'] = valwhere
            
            cmdtext = f"99,{comi}ASC{comi},1,0,5,3,1,10,{comi}1 = {tipuser}{comi},{comi}0{comi},{comi}0{comi}"
            
            fldcombos = Diccionario(request,cmdtext)
            
            context['tbladmin'] = fldcombos.gentbladmin(tipuser, ruta)
            print(request.session["user_list"])
            fechahasta = datetime.fromisoformat(request.session["user_list"][8])
            arrymdiasig = str(fechahasta).split(' ')[0].split('-')
            print('arrymdiasig',arrymdiasig)
            
            nummes = arrymdiasig[1]
            dictmes = {'01': 'Enero', '02': 'Febrero', '03': 'Marzo', '04': 'Abril', '05': 'Mayo', '06': 'Junio', '07': 'Julio', '08': 'Agosto', '09': 'Septiembre', '10': 'Octubre', '11': 'Noviembre', '12': 'Diciembre'}
            ymdiasig = f'{arrymdiasig[2]} de {dictmes[nummes]} de {arrymdiasig[0]}'
            print('ymdiasig',ymdiasig)
            
            context['ymdiasig'] = ymdiasig
            
            return render(request, 'tasks.html', {"proyectos": context})
                       
    except template.TemplateDoesNotExist:

        html_template = loader.get_template('page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('page-500.html')
        return HttpResponse(html_template.render(context, request))

def paginacion(paramfil, numtbl, arrtitulos, numreg, numpags, argprm, irpag):
    #'['1', '0', '5', '1', '1', '10']'
   
  if int(numpags) > 0:
    comi = "'"
    paramfil = paramfil.split(',')
    
    pagant = int(paramfil[3])    
    indice = int(paramfil[4])   
    limite = int(paramfil[5])
    valder = indice*limite
    if indice == int(numpags):
        valder = int(numreg)
        
    pagi = f'<div class="col-3"><p style="font-size: 13px">(Mostrando {(indice-1)*limite+1} al {valder} de {numreg})</p></div><div class="col-7"><ul class="pagination pg-primary" style="cursor: pointer;"><li class="page-item" onclick="llenarfld({comi}/tasks/pages/{numtbl}/1{comi},{comi}frmparam{comi},{comi}page-{indice}-Previous{comi})"><a class="page-link" style="background-color: rgb(31, 36, 46);color: white;"><i class="fas fa-angle-double-left"></i></a></li>'
           
    active = ''
    for i in range(int(numpags)):
        inx = i + 1 
                
        if inx < 8:
            if inx == indice:
                active = 'active'
            pagi += f'<li class="page-item {active}" onclick="llenarfld({comi}/tasks/pages/{numtbl}/1{comi},{comi}frmparam{comi},{comi}page-{inx}-page{comi})"><a class="page-link">{inx}</a></li>'
        elif inx == 8:
            if indice == 8:
                active = 'active'
            pagi += f'<li class="page-item {active}" onclick="llenarfld({comi}/tasks/pages/{numtbl}/1{comi},{comi}frmparam{comi},{comi}page-{inx}-page{comi})"><a class="page-link">{inx}</a></li>'
            if numpags == 8:
                break
        elif indice > 8 and indice < numpags:
            pagi += f'<li class="page-item"><a class="page-link">...</a></li><li class="page-item active" onclick="llenarfld({comi}/tasks/pages/{numtbl}/1{comi},{comi}frmparam{comi},{comi}page-{indice}-page{comi})"><a class="page-link" >{indice}</a></li><li class="page-item"><a class="page-link">...</a></li><li class="page-item" onclick="llenarfld({comi}/tasks/pages/{numtbl}/1{comi},{comi}frmparam{comi},{comi}page-{numpags}-pgfin{comi})"><a class="page-link">{numpags}</a></li>'
            break
        else:
            if indice == numpags:
                active = 'active'
            pagi += f'<li class="page-item"><a class="page-link">...</a></li><li class="page-item"><a class="page-link">...</a></li><li class="page-item {active}" onclick="llenarfld({comi}/tasks/pages/{numtbl}/1{comi},{comi}frmparam{comi},{comi}page-{numpags}-pgfin{comi})"><a class="page-link">{numpags}</a></li>'
            break
        active = ''
          
    pagi += f'<li class="page-item" onclick="llenarfld({comi}/tasks/pages/{numtbl}/1{comi},{comi}frmparam{comi},{comi}page-{indice}-Next{comi})"><a class="page-link" style="background-color: rgb(31, 36, 46);color: white;"><i class="fas fa-angle-double-right"></i></a></li></ul></div><div class="col-2 m-auto"><div class="input-group mb-3"><input type="text" id="irpagnum" name="irpagnum" class="form-control" placeholder="Ir a pág..." aria-label="Ir a pág..." aria-describedby="ir-pag" onchange="fillbox({comi}irpagnum{comi},{comi}irpag{comi})"><span class="input-group-text" id="ir-pag"><i class="fa fa-search" style="cursor: pointer;" onclick="llenarfld({comi}/tasks/pages/{numtbl}/1{comi},{comi}frmparam{comi},{comi}page-{irpag}-irpag{comi})"></i></span></div></div>'
    
  else:
    pagi = '' 
  
  return pagi
              
@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {'task': task, 'form': form})
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {'task': task, 'form': form, 'error': 'Error updating task.'})

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')

@login_required
def subir_archivo(request):
    
    html = 'eximport.html'
    
    if request.session['subir'] == 2:
        html = 'usuario.html'
    
    usuario = request.session['user_list'][2]
    
    if request.method == 'POST':
               
        num_tbl = int(request.session['user_list'][4])
        
        nomtitulos = {'nomunir': request.POST["nomunir"],'convexcel': request.POST["convexcel"],'convedacoop': request.POST["convedacoop"]}
        
        valid = request.POST['archi']
        titulo = nomtitulos[valid]
        if titulo != '':
            titulo = request.POST[valid]
    
        if request.POST['archi'] == 'nomunir':
        
            comi = "'" 
            
            cmdtext = f"100,'ASC',0,1,5,1,1,10,'3 = {titulo}','0',{comi}{usuario}{comi}"
            
            archput = Archivo(request, cmdtext, ['.pdf']) 
        
            output = archput.get_arch(titulo, num_tbl)  
            
            for key, value in output.items():
                if key == 'is_valid':
                    if value == True:
                        context = {'archivo': archivo, 'msg': 'PDFs unidos satisfactoriamente'}
                    else:
                        context = {'archivo': '', 'msg': 'Error al unir los archivos'}
                else:
                    archivo = value
                    
        elif request.POST['archi'] == 'convexcel':
        
            comi = "'" 
            
            cmdtext = f"100,'ASC',0,1,5,1,1,10,'3 = {titulo}','0',{comi}{usuario}{comi}"
            
            archput = Archivo(request, cmdtext, ['.xls', '.xlsx', '.pdf', '.csv'])
        
            output = archput.get_arch(titulo, num_tbl)  
            
            for key, value in output.items():
                if key == 'is_valid':
                    if value == True:
                        context = {'archivo': output['archivo'], 'msg': 'PDF convertido a datacoop satisfactoriamente'}
                    else:
                        context = {'archivo': '', 'msg': 'Error al convertir archivo'}
                else:
                    archivo = value
                    
        elif request.POST['archi'] == 'convedacoop':
        
            comi = "'" 
            
            cmdtext = f"100,'ASC',0,1,5,1,1,10,'3 = {titulo}','0',{comi}{usuario}{comi}"
            
            archput = Archivo(request, cmdtext, ['.xls', '.xlsx', '.csv'])
        
            output = archput.get_arch(titulo, num_tbl)  
            
            for key, value in output.items():
                if key == 'is_valid':
                    if value == True:
                        context = {'archivo': archivo, 'msgx': msgx, 'msg': 'Actualización realizada satisfactoriamente', 'dt': 1}
                    else:
                        context = {'archivo': archivo, 'msg': 'Error al actualizar', 'dt': 0}
                elif key == 'archivo':
                    archivo = value
                elif key == 'msgx':
                    msgx = value
                elif key == 'dt':
                    dt = value
    
    else:
        context = {}
            
    return render(request, html, context)

@login_required
def combos(request):
    
    if request.method == "GET":
        return render(request, 'combos.html')
    else:
        dataobj = tareas_combos(request)
        return render(request, 'combos.html', {'task': dataobj})
        
@login_required 
def tareas_combos(request):
              
    fillcombos = Cattbl(request,'')
    
    nomtbl = request.POST.get('nomtbl')

    dataobj = fillcombos.infoesquema(nomtbl)
    
    return dataobj
                
def insertJson():
                    
    with open('/home/js/Escritorio/appspython/pain.json', 'r') as f:
        array = json.load(f)
        dictpainjson = dict(array)
                   
        filljson = Rutas(request.POST)
        try:  
            dictcodpar = {'CodPar': CodPar, 'PaiIns': dictpartaux} 
            #print('<<<<<<<<<',dictcodpar)
            dictpart = {'codigo': dictcodpar}
            dataobj = filljson.fnt_insert(126, dictpart)
        except Exception as e:
            print(e)         

def delfile(filespath):        
    files = os.listdir(filespath)
    extfile = ['.pdf', '.xls', '.xlsx', '.tif', '.tiff', '.bmp', '.jpg', '.jpeg', '.gif', '.png', '.eps', '.json', '.csv']
    
    for file in files:
        if Path(file).suffix in extfile:
            fileruta = f'{filespath}{file}'
            os.remove(fileruta) # delete file based on their name or suffix 
          
def send_email():
    try:
        username='****'
        password='***'
        mailServer = smtplib.SMTP('smtp.gmail.com', 587)
        mailServer.ehlo()
        mailServer.starttls()
        mailServer.ehlo()
        mailServer.login(username, password)
    except Exception as e:
        print(e)
'''
def cafe():
    
    cookie1 = Cookie()
    print(id(cookie1))
    print(type(cookie1))
    print(isinstance(cookie1, Cookie))
    
    small = Coffee('Small', 2)
    regular = Coffee('Regular', 5)
    big = Coffee('Big', 6)
    
    print('small',small)
    try:
        user_budget = float(input('What is your budget? '))
    except ValueError:
        exit('Please enter a number')
  
    for coffee in [big, regular, small]:
        coffee.sell(user_budget) 
        
def galleta():
    
    cookie2 = Cookie('Awesome cookie', 'Star')
    print(cookie2.name)
    print(cookie2.shape)
    print(cookie2.chips) 
    
    cookie3 = Cookie('Baked cookie', 'Tree')
    cookie3.bake()  
    
def forma():
    
    rec = Rectangle(1, 2)
    print(rec)
    sqr = Square(4)
    print(sqr)
    tri = Triangle(2, 3)
    print(tri)
    cir = Circle(4)
    print(cir)
    hex = Hexagon(3)
    print(hex)        

userInputDate = 'None'
alarmDate = ''
timeNow = datetime.now()

while userInputDate not in ('Y','N'):
    userInputDate = 'Y'
    if userInputDate == 'Y':
        userInput = '17:59'
        alarmDate = timeNow.strftime('%d/%m/%y')+ ' ' + userInput
        print(f'La alarma está configurada para las : {alarmDate}')
        
while True:
     
    if datetime.now().strftime('%d/%m/%y %H:%M') == alarmDate:

        for i in reversed(range (1, 11)):
            print(i)
            t = Timer(30,)
            t.start()
            valdolar = scrap()
            
def hello():
    print("hello, world")

    delta = timedelta(
        days=0,
        seconds=0,
        microseconds=0,
        milliseconds=0,
        minutes=1,
        hours=0,
        weeks=0
    )
    print(datetime.now())
    print(datetime.now()+delta)
delta = timedelta(
    days=50,
    seconds=27,
    microseconds=10,
    milliseconds=29000,
    minutes=5,
    hours=8,
    weeks=2
)

t = Timer(30.0, hello)
t.start() # after 30 seconds, "hello, world" will be printed
#wait(1)  
t = datetime(2024,6,12,9,1,0)
print(t)
 
delta = timedelta(days=1)
print(t+delta)

delta = timedelta(
    days=50,
    seconds=27,
    microseconds=10,
    milliseconds=29000,
    minutes=5,
    hours=8,
    weeks=2
)


user = User.objects.create_user(
                            'stdom',
                            email=None,
                            password='1234')
user.save()
user.first_name = '2'
user.save() 
u = User.objects.get(username="fsmith")
freds_department = u.employee.department 
-------------
user = User.objects.create_user('javsalas', email=None, password='1234')
user.save()
user.first_name = '5'
user.save()   

coop1 = Cooperativas(rif="J-30459078-4", nombre="Cooperativa Santo Domingo Brasil", direccion="Calle Lisboa con calle Zulia y entrada por la Carabobo", telefono="0252-4220170", estatus="Activa", user=user)
coop1.save()  

socio = Socios(coop = coop1, nombre="Javier Salas", sexo="M", estatus="Activo", user=user)
socio.save()   
'''







