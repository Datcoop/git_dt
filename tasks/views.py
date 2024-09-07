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
def administrar(request):
    
    return redirect(f'/tasks/pages/103/1')

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
            
            correo = request.POST['correo']
            
            form = ContacForm(request.POST)
            new_msg = form.save(commit=False)
            new_msg.save()
            
            subject = request.POST['asunto']
            message = request.POST['mensaje'] + " " + request.POST['correo']
            from_email = settings.EMAIL_HOST_USER
            recipient_list = ['intalgos@gmail.com']
            send_mail(subject, message, from_email, recipient_list)
            
            return  render(request, 'home.html', {'msg': f'Hemos recibido su solicitud. En un plazo máximo de 48 horas, les estaremos respondiendo por el correo {correo}'})
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
            archdel = Archivo('', '', '') 
            archdel.delfile('media/Archivos/')
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
            archdel.delfile('media/Archivos/')
            
            dictnumtbl = {1: 103, 2: 101, 5: 103}
            
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
                
                dataobj = indicepag.tbl(num_tbl,pagi,dataobj1['paramfil'],dataobj1['arrprm'],dataobj1['ordpage'], tipuser) 
                
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
                
                fldcombos = Fntsql(cmdtext)
        
                context = fldcombos.dict_selectuno()
                
                arrtit = context['fldtitulos'].split(", ")
        
                arrfld = context['fldselect'].split(", ")
        
                arrrel = context['relacional'].split(", ")
                
                valinp = Diccionario('', '')
                
                numrow = 0
                
                rowval = 0
                
                inpbox = f'<form method="post" id="frmup" enctype="multipart/form-data">'
                if arrprm[0] == 'add':
                
                    numrow = context['numreg']+1
                    
                    arrfltg = context['row_to_json']['tiggers'].split(", ")
                    
                    arrvaltigg = context['row_to_json']['valtiggers'].split(", ")
                    print('arrvaltigg =',arrvaltigg)
                    
                    arrcampinsshow = context['row_to_json']['camposinsshow'].split(", ")
                    
                    inpbox += f'<input type="hidden" id="param" name="param">'
                    
                    fldcombos = Util(cmdtext)
                    inpbox += fldcombos.buildinputbox(inpbox, arrfltg, arrcampinsshow, arrrel, arrtit, arrvaltigg, arrfld, '')
                    inpbox += f'<div class="p-2"><div>Agregar el registro número {numrow}</div><div class="row p-2"><span class="col-6"><button type="button" class="btn btn-primary" data-bs-dismiss="offcanvas" aria-label="Close">Cancelar</button></span><span class="col-6"><button class="btn btn-primary" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasRight" aria-controls="offcanvasRight" onclick="llenarfld({comi}/tasks/pages/{num_tbl}/9{comi},{comi}frmup{comi},{comi}add-{numrow}-insert-0{comi})">Agregar<i class="fa fa-plus-circle p-1"></i></button></span></div></div></form>'                    
                
                elif arrprm[0] == 'edit':                    
                
                    numrow = int(request.POST['valup'])
                
                    rowval = int(request.POST['valup'])
                
                    paramfilorig = request.POST['paramfil']
                                
                    arrprf = paramfil.split(',')
                    
                    arrwer = request.POST['arrwer']
                
                    paramfil = f'{arrprf[0]},{arrprf[1]},9,{arrprf[3]},{arrprf[4]},{numrow}'
                    cmdtext8 = f"{num_tbl},'ASC',{paramfil},{comi}{arrwer}{comi},'0','0'"
                    fldcombos = Fntsql(cmdtext8) 
                    contextodo = fldcombos.dict_selectodo(cmdtext8)
                    arrvalinp = contextodo[0]
                    print(arrvalinp)
                    inpbox += f'<input type="hidden" id="param" name="param">'
                    
                    arrfltg = context['row_to_json']['tiggersup'].split(", ")
                    
                    arrfldup = context['row_to_json']['camposupdate'].split(", ")
                    
                    arrcampinsshow = context['row_to_json']['camposupshow'].split(", ")
                    
                    #arrvalinp[arrfld[j]]
                    fldcombos = Util(cmdtext8)
                    inpbox += fldcombos.buildinputbox(inpbox, arrfltg, arrcampinsshow, arrrel, arrtit, 'edit', arrfld, arrvalinp)  
                    inpbox += f'<div>Actualizar el registro número {numrow}<input type="hidden" id="cmdtext" name="cmdtext" value="{cmdtext}"><input type="hidden" id="paramfil" name="paramfil" value="{paramfilorig}"></div><div class="row p-2"><span class="col-6"><button type="button" class="btn btn-primary" data-bs-dismiss="offcanvas" aria-label="Close">Cancelar</button></span><span class="col-6"><button class="btn btn-primary" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasRight" aria-controls="offcanvasRight" onclick="llenarfld({comi}/tasks/pages/{num_tbl}/9{comi},{comi}frmup{comi},{comi}edit-{numrow}-update-0{comi})">Actualizar<i class="fa fa-refresh p-1"></i></button></span></div></div></form>'
               
                dicttextbox = {}
                     
                dicttextbox['rowval'] = rowval
                     
                dicttextbox['ruta'] = ruta
                
                dicttextbox['inpbox'] = f'{inpbox}</form>'
                
                return JsonResponse({'data': dicttextbox})
              except Exception as e:
                print(e)    
                      
            elif ruta == '9':
                try:
                    
                    cmdtext = f"{num_tbl},{comi}ASC{comi},1,0,5,1,1,10,{comi}0 > 0{comi},{comi}0{comi},{comi}0{comi}"
                    fldcombos = Util(cmdtext)
        
                    context = fldcombos.dict_selectuno()
                    
                    dictval = dict(request.POST)
                    print('dictval =',dictval)
                
                    arrprm = dictval['param'][0].split('-')
                    
                    fila = int(arrprm[1])
                    
                    accion = arrprm[2]
                    
                    paramjson = {}
                                     
                    arrfld = context['row_to_json']['fldselect'].split(", ")
                                   
                    print(accion)
                    if accion == 'insert':
                        paramjson = {}
                        for key,value in dictval.items():
                            nomcamp = key.split('-')
                            if nomcamp[0] == 'inp':
                                value = value[0]
                                key = int(key.split('-')[-1])
                                paramjson[arrfld[key]] = value
                                
                        paramjson=json.dumps(paramjson) 
                        upreg = fldcombos.insertdata(num_tbl,paramjson)
                        
                        msg = f'<div class="alert alert-danger text-center" role="alert">Registro N° {fila}. No se pudo insertado</div>'
                        if len(upreg): 
                            msg = f'<div class="alert alert-success text-center" role="alert">Registro {fila}. Insertado satisfactoriamente<span class=" p-2"><a class="btn btn-success" href="/tasks/pages/{ num_tbl }/11">Recargar<i class="fas fa-redo-alt"></i></a></span></div>' 
                         
                    else:
                 #select * from update_filas(98, 25, '[{"tasa": 36.53, "fecha": "2024-07-15 21:00:00"}]');
                        paramjson = {}
                        for key,value in dictval.items():
                            nomcamp = key.split('-')
                            if nomcamp[0] == 'inp':
                                value = value[0]
                                key = int(key.split('-')[-1])
                                paramjson[arrfld[key]] = value
                                
                        paramjson=json.dumps(paramjson)  
                        print(paramjson)      
                        fldcombos = Fntsql(cmdtext) 
                        arrvalinprow = fldcombos.dict_findnumrow(num_tbl,fila) 
                        print(arrvalinprow)   
                        cmdtextup = f'{num_tbl}, {arrvalinprow[0] ["id"]}, {comi}[{paramjson}]{comi}'
                        upreg = fldcombos.dict_update_filas(cmdtextup)
                        msg = f'<div class="alert alert-danger text-center" role="alert">Registro N° {fila}. No se pudo actualizar</div>'
                        if len(upreg): 
                            print('largo =',len(upreg))
                            msg = f'<div class="alert alert-success text-center" role="alert">Registro {fila}. Actualizado satisfactoriamente<span class=" p-2"><a class="btn btn-success" href="/tasks/pages/{ num_tbl }/11">Recargar<i class="fas fa-redo-alt"></i></a></span></div>'                 
                    dicttextbox = {}
                
                    dicttextbox['upreg'] = upreg
                
                    dicttextbox['fila'] = fila
                
                    dicttextbox['msg'] = msg
                
                    dicttextbox['ruta'] = ruta
                
                    return JsonResponse({'data': dicttextbox})
                    
                except Exception as e:
                    print(e)    
                      
            elif ruta == '11':   
                
                onfnt = Llenar(num_tbl, ruta, request.POST)
             
                dataobj1 = onfnt.cmdtextfnt()
                print('dataobj1', dataobj1)
                paramfil = dataobj1['paramfil']
                
                cmdtext = "98,'ASC',1,0,5,1,1,10,'0 > 0','0','0'"
                    
                fldcombos = Fntsql(cmdtext) 
        
                user_list = fldcombos.dict_selectuno()
                
                arrprm = dataobj1['arrprm']
                numpags = user_list['numpags']
                paramfil = f"1,0,5,{numpags},{numpags},10"   
                cmdtext = f"98,'ASC',{paramfil},'0 > 0','0','0'"
                    
                indicepag = Util(cmdtext)
                
                pagi = indicepag.paginacion(paramfil, num_tbl, user_list['fldtitulos'], user_list['numreg'], user_list['numpags'], dataobj1['argprm'], dataobj1['irpag'])
                
                dataobj = indicepag.tbl(num_tbl,pagi,paramfil,dataobj1['arrprm'],dataobj1['ordpage'],tipuser) 
                
                dataobj['ruta'] = '1'                
                dataobj['textbox'] = ''                
                dataobj['argprm'] = dataobj1['argprm']                
                dataobj['pagant'] = dataobj1['indice']                
                dataobj['numpags'] = user_list['numpags']                 
                dataobj['paramfil'] = dataobj1['paramfil']                   
                dataobj['ordpage'] = dataobj1['ordpage']                   
                dataobj['valwhere'] = dataobj1['valwhere']                       
                context['limite'] = f' {dataobj["limite"]} filas'  
               
                return JsonResponse({'data': dataobj, 'proyectos':context}) 
                
                
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
              
@login_required
def subir_archivo(request):
    
    html = 'eximport.html'
    
    if request.session['subir'] == 2:
        html = 'usuario.html'
        
    userID = request.session['user_list'][0]
    usuario = request.session['user_list'][2]
    
    if request.method == 'POST':
               
        num_tbl = int(request.session['user_list'][4])
        print('xxxx =',request.POST)
        nomtitulos = {'nomunir': request.POST["nomunir"],'convecsv': request.POST["convecsv"],'convexcel': request.POST["convexcel"],'convedacoop': request.POST["convedacoop"]}
        
        valid = request.POST['archi']
        titulo = nomtitulos[valid]
        if titulo != '':
            titulo = request.POST[valid]
    
        if request.POST['archi'] == 'nomunir':
        
            comi = "'" 
            
            cmdtext = f"100,'ASC',0,1,5,1,1,10,'3 = {titulo}','0',{comi}{usuario}{comi}"
            
            archput = Archivo(request, cmdtext, ['.xls', '.xlsx', '.pdf', '.csv']) 
        
            output = archput.get_arch(request, titulo, num_tbl)  
            
            for key, value in output.items():
                if key == 'is_valid':
                    if value == True:
                        context = {'archivo': archivo, 'msg': 'PDFs unidos satisfactoriamente', 'ifpdf': True}
                    else:
                        context = {'archivo': '', 'msg': 'Error al unir los archivos'}
                else:
                    archivo = value
                    
        elif request.POST['archi'] == 'convecsv':
        
            comi = "'" 
            
            cmdtext = f"100,'ASC',0,1,5,1,1,10,'3 = {titulo}','0',{comi}{usuario}{comi}"
            
            output = f'media/Archivos/{titulo}.csv'
            
            archput = Archivo(request, cmdtext, ['.xls', '.xlsx', '.pdf', '.csv'])
        
            output = archput.get_arch(request, titulo, num_tbl)  
            
            for key, value in output.items():
                if key == 'is_valid':
                    if value == True:
                        context = {'archivo': output['archivo'], 'msg': 'PDF convertido a CSV satisfactoriamente'}
                    else:
                        context = {'archivo': '', 'msg': 'Error al convertir archivo'}
                else:
                    archivo = value
                    
        elif request.POST['archi'] == 'convexcel':
        
            comi = "'" 
            
            cmdtext = f"100,'ASC',0,1,5,1,1,10,'3 = {titulo}','0',{comi}{usuario}{comi}"
            
            output = f'media/Archivos/{titulo}.xlsx'
            
            archput = Archivo(request, cmdtext, ['.xls', '.xlsx', '.pdf', '.csv'])
        
            output = archput.get_arch(request, titulo, num_tbl)  
            
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
            print('xxxx =',request.session['user_list'])
            archput = Archivo(request, cmdtext, ['.xls', '.xlsx', '.csv'])
        
            output = archput.get_arch(request, titulo, num_tbl)  
            
            for key, value in output.items():
                if key == 'is_valid':
                    if value == True:
                        context = {'archivo': archivo, 'msg': 'Actualización realizada satisfactoriamente', 'dt': 1}
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







