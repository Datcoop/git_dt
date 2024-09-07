# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Create your views here.
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .forms import LoginForm, SignUpForm
from apps.home import views as vistahomeapps


def login_view(request,tipuser):

    form = LoginForm(request.POST or None)
    
    context = {}

    msg = None
    
    comi = "'"

    if request.method == "POST":

        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            #print(f'email={email}, password={password}') 
            nomproc = f"SELECT * from sp_abc(141, 2050, '', {comi}{email}{comi}, 5) as soc(idorg bigint, nomorg varchar, tipouser integer, username varchar);"
            rawData = vistahomeapps.exe_sp(nomproc)
            #[(1, 'Javier Salas', 1)]
            for i in rawData:
                idorg = i[0]
                nomorg = i[1]
                tipuser = i[2]
                username = i[3]
                
            user = authenticate(username=username, password=password)
                
            #print(f'user={user}  idorg = {i[0]}   nomorg = {i[1]}   tipuser = {i[2]}')
            
            request.session["nomorg"] = nomorg
            
            request.session["idorg"] = idorg
            
            request.session["tipuser"] = tipuser
            
            request.session["email"] = email
            
            '''1 	useradm
	           2 	autorizados
	           3 	userweb
	           4 	pageadmin'''    
            tbladmin = []      
            if tipuser == 1:
                commandtext = f'SELECT * from sp_abc(141,0,{comi}0{comi},{comi}{email}{comi},6) as soc(registro record);'
                rawData = vistahomeapps.exe_sp(commandtext) 
                for i, fila in enumerate(rawData):
                    strrawData = rawData[i][0].replace('(','')
                    strrawData = strrawData.replace(')','')
                    strrawData = strrawData.replace('"','')
                    arrrawData = strrawData.split(',')
                    tbladmin.append([arrrawData[0], arrrawData[1]])
                #print(f'tbladmin = {tbladmin}')
                        
            elif tipuser == 2:
                commandtext = f'CALL sp_abc(141,0,0,{comi}{email}{comi},7)'
                rawData = vistahomeapps.exe_sp(commandtext)  
                
                modificartbl = rawData[0][0].split(", ")
                
                for i in len(modificartbl):
                    rawData = modificartbl.split("xxx")
                    tbladmin.append([rawData[i][0],rawData[i][1]])
                
            elif tipuser == 3:
                tbladmin += f'<li><a href="/143/home/dtblbase.html">'     
                tbladmin += f'<span class="sub-item">Socio web</span></a></li>' 
	                  
                tbladmin += f'<li><a href="/158/home/dtblbase.html">'     
                tbladmin += f'<span class="sub-item">Socios terceros</span></a></li>' 
            request.session["tbladmin"] = tbladmin 
            #print(f'request_session={request.session["tbladmin"]}')    
                 
            if user is not None:
            #CALL sp_selectuno(135,'1',0,0,0,1,1,10)           
                login(request, user)
                return redirect(f"{idorg}/130/home/org.html")
            else:
                msg = 'Credenciales inválidas'
        else:
            msg = 'Formulario inválido'
            
    else:

        url = request.path.split('/')
        
        context['tipuser'] = url[-1]

    return render(request, "accounts/login.html", {"form": form, "msg": msg, 'proyectos': context})
    
def register_user(request,tipuserreg):
    context = {}
    msg = None
    success = False
    tabla = ()
    comi = "'"
    if request.method == "POST":
        ruta = request.path.split('/')
        num_tbl = ruta[1]
        current_dateTime = datetime.now()
        
        print(request.POST)
        
        tip_user = request.POST.get("tipuser")
        if tip_user == 'org':
            tipuser = 1
        elif tip_user == 'per':
            tipuser = 3
            
        #password, last_login, username, email, organizacion, tip_user
        idorg = int(request.POST.get("pag").split('g')[-1])
        commandtext = f'CALL sp_abc(130, {idorg}, {comi}pparam1{comi}, {tipuser}, 0)' 
        rawData = vistahomeapps.exe_sp(commandtext)        
        print(f'rawData={rawData}')
        idorg = rawData[0][0]
        
        commandtext = f'CALL sp_abc(141, {idorg}, {comi}pparam1{comi}, {tipuser}, 0)' 
        rawData = vistahomeapps.exe_sp(commandtext)        
        arrcamposselect = rawData[0][1].split(", ")
        
        request.POST = request.POST.copy()
        request.POST.update({
            "organizacion": idorg
        })
            
        request.POST.update({
            "tip_user": tipuser
        })
        request.POST.update({
            "pag": idorg
        })
        
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()            
            
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)           
            
            commandtext = f'CALL sp_abc(141,{idorg},{comi}{idorg}xxx{tipuser}{comi},{comi}{username}{comi},4)'
            rawData = vistahomeapps.exe_sp(commandtext)
            
            request.session["idorg"] = idorg
            
            login(request, user)
            
            msg = f'Usuario creado satisfactoriamente - ya puede entrar<a class="btn btn-primary btn-link" href="{idorg}/130/home/org.html">ENTRAR</a>.'
            success = True

            # return redirect("/login/")

        else:
            msg = 'Formulario no válido'
    else:

        url = request.path.split('/')
        
        context['tipuser'] = url[-1]
        form = SignUpForm()
        tabla = vistahomeapps.objall()
        print(f'url={url}')

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success, "tabla": tabla, 'proyectos': context})

