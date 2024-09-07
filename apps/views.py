
# -*- encoding: utf-8 -*-
"""
Copyright (c) 2023 - AIBOT 
"""

import random
import itertools
from random import randint
from statistics import mean
#from reportlab.lib.pagesizes import A4, letter
#from reportlab.pdfgen import canvas
from django.template.loader import render_to_string
import psycopg2
from ast import Mod
import json, math, ast
from posixpath import split
from django import template
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic import ListView
from django.core.paginator import Paginator
from collections import namedtuple
from django.db import connection
from django.template import loader
from django.urls import reverse
#from apps import fnt_js
#from io import BytesIO
#from xhtml2pdf import pisa
#from .poo import *
#from .PDF import *

@login_required
def pages(request):
    context = {}
    contextajax = {}
    comi = "'"
    url = request.path.split('/')
    #['', 'apps', 'password', 'vertext', '']
    metodo = request.method
    
    try:
        metodo = request.method
        url = request.path.split('/')
        load_template = request.path.split('/')[-1]
        
        if metodo == 'POST':
        
            print(request.POST)
            
            ruta = request.path.split('/')
                    
            if ruta[-2] == 'listado_autor':
                print('rqorder =',request.POST.get("orderby"))
                dataobj = QueryDic(request.POST, ruta[-2]) 
                            
                context['limite'] = f' {request.POST.get("limite")} filas'
                
                return JsonResponse({'data': dataobj, 'proyectos':context})
            
            elif ruta[-2] == 'exportar':     
                
                try:
                
                    nomfile = request.POST.get("nomfile")
                
                    nomarchivo = reporte(nomfile,'letter')
                    #nomarchivo = export_pdf(request.POST)
                    data = [["N°", "ID", "Código", "Nombre"]]      
 
                    commandtext = f'select * from codlike(136,{comi}13{comi});'
                    
                    rawData = exe_sp(commandtext)
                    
                    strdata = []
                    for i, fila in enumerate(rawData):
                        thisdict = {}
                        thisdict = rawData[i][0]
                        for j,vj in thisdict.items():  
                            if j == 'numrows':
                                strdata.append(vj)      
                            elif j == 'id':
                                strdata.append(vj)   
                            elif j == 'codigo':  
                                strdata.append(vj)   
                            elif j == 'nombre':  
                                strdata.append(vj)   
                                data.append((strdata))
                                strdata = []
                                
                    print(data) 
                                
                    #imgpdf(data)                                 
                    #imgpdf() 
                    
                    #platipdf() 
                    platipdf(data) 
                    
                    dataobj = {
                        "mensaje": f'<div class="alert alert-success alert-dismissible fade show" role="alert">Archivo <strong>{nomarchivo}</strong><button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>',
                    "ruta": 'exportar',
                    }
                
                    return JsonResponse({'data': dataobj})
                    
                except Exception as e:
                    print(e)
                    print('Error al unir los pdf')
                    return False
            
            elif ruta[-2] == 'exportar2': 
                '''
                listpdf = [
                           '/home/js/Descargas/rafPDVSA5/Acta Constitutiva Venetek.pdf',
                           '/home/js/Descargas/rafPDVSA5/Cambio Razon.pdf',
                           '/home/js/Descargas/rafPDVSA5/Ultima Acta de Asamblea.PDF',
                           '/home/js/Descargas/rafPDVSA5/RIFe.pdf',
                           '/home/js/Descargas/rafPDVSA5/cedula.pdf',
                           '/home/js/Descargas/rafPDVSA5/RIFp.pdf',
                           '/home/js/Descargas/rafPDVSA5/RIFp2.pdf',
                           '/home/js/Descargas/rafPDVSA5/certificadoDeuda.pdf',
                           '/home/js/Descargas/rafPDVSA5/facturas.pdf'
                          ]                
                
                print(listpdf)          
                
                unpdf = Lista()
                
                nombre_archivo_salida = "/home/js/Descargas/rafPDVSA5/Recaudos PACIFIC LOGGING VENEZUELA, C.A.pdf"
                 
                unpdf = unpdf.unirpdf(listpdf, nombre_archivo_salida)                 
                
                print(unpdf)
                '''    
                
                print('ToPDF')      
                
                try:
                    exppdf = ezmPDF(request.POST)
                
                    pdf = exppdf.render_to_pdf('home/dtblbase.html', 140, url[2], request.POST.get)
                    
                    print('Creación satisfactoria')
                    
                    return HttpResponse(pdf, content_type='application/pdf')
                    
                except Exception as e:
                    print(e)
                    print('Error al unir los pdf')
                    return False
            
            elif ruta[-2] == 'exportar3':     
                
                try:
                
                    nomfile = request.POST.get("nomfile")
                
                    nomarchivo = reporte(nomfile,'letter')
                    #nomarchivo = export_pdf(request.POST)
                    data = [("N°", "ID", "Código", "Nombre")]      
 
                    commandtext = f'select * from codlike(134,{comi}13{comi});'
                    
                    rawData = exe_sp(commandtext)
                    
                    strdata = []
                    for i, fila in enumerate(rawData):
                        thisdict = {}
                        thisdict = rawData[i][0]
                        for j,vj in thisdict.items():  
                            if j == 'numrows':
                                strdata.append(vj)      
                            elif j == 'id':
                                strdata.append(vj)   
                            elif j == 'codigo':  
                                strdata.append(vj)   
                            elif j == 'nombre':  
                                strdata.append(vj)   
                                data.append((strdata))
                                strdata = []
                                
                    #print(data) 
                                
                    export_to_pdf(data) 
                    
                    dataobj = {
                        "mensaje": f'<div class="alert alert-success alert-dismissible fade show" role="alert">Archivo <strong>{nomarchivo}</strong><button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>',
                    "ruta": 'exportar',
                    }
                
                    return JsonResponse({'data': dataobj})
                    
                except Exception as e:
                    print(e)
                    print('Error al unir los pdf')
                    return False
                    
            else:  
                
                print('ruta = ',ruta[-2])
                
                inxopt = int(request.POST.get("inxopt"))
                
                inxopt0 = int(request.POST.get("inxopt0"))
                
                arrwer = request.POST.get("arrwer") 
                
                numoper = request.POST.get("numoper")      
                
                fillopt = Rutas(request.POST)
                
                dataobj = fillopt.fnt_rutas(ruta[-2],inxopt0,inxopt,arrwer)
                
                #print('dataobj = ',dataobj,' ruta =',dataobj['ruta'])
                
                return JsonResponse({'data': dataobj})
                       
        else:

            rutatot = request.path  
          
            if url[-1] == 'org.html':
                ruta = url[4]
                num_tbl = url[3]
            elif url[-1] == 'unirpdf.html':
                ruta = url[4]
                num_tbl = url[3]
            elif url[-1] == 'dtblbase.html':
                ruta = url[2]
                num_tbl = url[1]
                context['numtblurl'] = num_tbl 
            else:
                ruta = 'home'
                num_tbl = 130
                
            carpin = f'{ruta}/'

            if load_template == 'admin':
                return HttpResponseRedirect(reverse('admin:index'))
            
            poshtml = url[-1].find(".html")
            
            if poshtml != -1:
            
                html_template = loader.get_template(carpin + load_template)
                html_temp = carpin + load_template
                
                comi = "'"
                
                commandtext = f"select * from sp_selectuno ({num_tbl},{comi}ASC{comi},1,0,5,1,1,10,{comi}0 > 0{comi},{comi}0{comi});"
                
                rawDatauno = exe_sp(commandtext)
                
                for i, fila in enumerate(rawDatauno):
                    thisdict = {}
                    thisdict = rawDatauno[i][0]
                    for i,vi in thisdict.items():
                        if i == 'numreg':
                            numreg=vi
                        if i == 'numpags':
                            numpags=vi
                        if i == 'titulotbl':
                            titulotbl=vi
                        if i == 'row_to_json':
                            camposselect=vi['fldselect']
                            campostitulos=vi['fldtitulos']
                            camposrelacional=vi['relacional']
                
                dict_titrel = Lista()
                 
                dict_titrel = dict_titrel.dicttitrel(campostitulos,camposrelacional)  
                
                context['dict_titrel'] = dict_titrel
                    
                context['recordsTotal'] = numreg
                context['recordsFiltered'] = numreg   
                context['numpags'] = numpags
                context['campostitulos'] = campostitulos.split(", ")
                arrdirec = context['campostitulos']
                arrcamposselect = camposselect.split(", ")
                
                arrcolSwitch = ''
                for i in range(len(arrcamposselect)):
                    arrcolSwitch += ', '
                arrcolSwitch += ','
                arrcolSwitch = arrcolSwitch.replace(', ,','')
                context['arrcolSwitch'] = arrcolSwitch                
                
                context['num'] = int(num_tbl)
                context['tittbl'] = titulotbl
                context['idorg'] = url[2]
                context['nomorg'] = f'{request.session.get("nomorg")}'
                context['limite'] = 10 
                context['critsearch'] = 'ASC' 
                context['titulos'] = campostitulos
                
                html_temp = 'home/' + load_template
                
            return render(request, html_temp, {'proyectos':context})
            
    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))

# ///////////////////////////////////////////////////////////////
def QueryDic(_dictreq, ruta):
    
    comi = "'"
    
    numtbl = int(_dictreq.get("numero"))
    
    indice = int(_dictreq.get("indice"))
    
    limite = int(_dictreq.get("limite"))
    
    direc = _dictreq.get("direc")
    
    orderby = _dictreq.get("orderby")
    
    columnswitch = _dictreq.get("columnswitch")
    
    arrcolSwitch = _dictreq.get("arrcolSwitch")
    
    numCheck = _dictreq.get("numCheck")
    
    crearcolumnswitch = _dictreq.get("crearcolumnswitch")
    #print("crearcolumnswitch =",crearcolumnswitch)
    
    paramfil = _dictreq.get("paramfil")
    
    cmdtext = _dictreq.get("cmdtext")
    
    arrwer = _dictreq.get("arrwer")
    
    numcolswitch = _dictreq.get("numcolswitch")  
    
    arrSwitch = numcolswitch.split(', ')
    #print("arrSwitch =",arrSwitch)  
    #print("orderby =",orderby)
    
    stateCheck = _dictreq.get("stateCheck")
    
    tablaini = Tabla(_dictreq)
    
    tabla = '<table id="tblmain" class="table table-striped">'
    
    tabla += tablaini.headtbl('<thead style="background: #36597a;color: azure;"><tr>')
    #print("tabla = ",tabla)
    
    tablaclass = tablaini.thtbl(numtbl, direc, 0)
    
    tabla += tablaclass["thc"]
    #print("tabla = ",tabla)
    tr = '</thead><tbody>'
    tr = tablaini.trtbl()
    #print(tr)  
#------    
    column = f'<select class="form-control input-solid bg-dark" id="columnas" style="color: white;cursor: pointer;" onclick="select({comi}select_col/1/1{comi},{comi}columnas{comi},{comi}colinx{comi},0)" required><option id="nomfiltro">Filtrar columna</option>' 
    
    arrtitulos = tablaclass["arrtitulos"]
    
    print("arrSwitch = ",arrSwitch," lenarrSwitch = ",len(arrSwitch))
    
    checked = []
    for item in range(len(arrtitulos)):
        if len(arrSwitch) > 1:
            if str(item) in arrSwitch:
                checked.append('checked')
            else:
                checked.append('')
        else:
            checked.append('')
        
    checkedini = ''
    if stateCheck == 'true':
        checkedini = 'checked'
            
    print("stateCheck = ",stateCheck," checkedini = ",checkedini)
        
    options = '' 
    if crearcolumnswitch == 'true':           
        for opt in arrtitulos:
            options += f'<option>{opt}</option>'
    
        columnswitch = f'<li><div class="p-1"></div><div class="form-check form-switch bg-dark p-2"><input class="form-check-input m-1" type="checkbox" role="switch" id="colCheck" onclick="fnt_colCheck()" {checkedini}><label class="form-check-label" for="colCheck">Seleccionar columnas</label></div></li><li><div class="bg-light p-3"><button class="w-100 btn btn-md btn-primary" onclick="bnt_click({comi}bus_filtrar{comi},{numtbl},{comi}filselcol{comi})" id="selcolcheck"><i class="fas fa-filter"></i>Filtrar</button></div></li><div class="p-1"></div>'    
        i = 1
        for j in arrtitulos:
            
            columnswitch += f'<li><div class="form-check form-switch"><input class="form-check-input" type="checkbox" id="{i}" name="colcheck" onclick="fnt_changecheck({comi}selcheck{comi},{numtbl},{i})" {checked[i-1]}><label class="form-check-label" for="{i}">{j}</label></div></li>'
            i += 1   
        #crearcolumnswitch = 'false'
        
    column += options
    column += '</select>'
    #print(columnswitch)  
#----- FILTROS
    filtrosswitch = Options(_dictreq)
                
    filtrosswitch = filtrosswitch.filtros()
    #print("filtrosswitch = ",filtrosswitch)
#-----       
    nomcamposelectuno = Options(_dictreq)
    
    numreg = nomcamposelectuno.titulos('numreg')  
     
    numpags = nomcamposelectuno.titulos('numpags')  
    #print("numpags = ",numpags)
    
    pagi = f'<div class="col-2"><p style="font-size: 13px">({(indice-1)*limite+1} al {(indice)*limite}) de {numreg}</p></div><div class="col-8"><ul class="pagination pg-primary" style="cursor: pointer;"><li class="page-item" onclick="pgindex({comi}frmparam{comi},{comi}listado{comi},{comi}/{numtbl}/coop/inxpagina/{comi},{comi}indice{comi},{indice},{comi}Previous{comi})"><a class="page-link" style="background-color: rgb(31, 36, 46);color: white;"><i class="fas fa-angle-double-left"></i></a></li>'
            
    active = ''
    for i in range(numpags):
        inx = i + 1
                
        if inx < 8:
            if inx == indice:
                active = 'active'
            pagi += f'''<li class="page-item {active}" onclick="pgindex('frmparam','listado','/{numtbl}/coop/inxpagina/','indice',{inx},'page')"><a class="page-link">{inx}</a></li>'''
        elif inx == 8:
            if indice == 8:
                active = 'active'
            pagi += f'''<li class="page-item {active}" onclick="pgindex('frmparam','listado','/{numtbl}/coop/inxpagina/','indice',{inx},'page')"><a class="page-link">{inx}</a></li>'''
            if numpags == 8:
                break
        elif indice > 8 and indice < numpags:
            pagi += f'''<li class="page-item"><a class="page-link">...</a></li><li class="page-item active" onclick="pgindex('frmparam','listado','/{numtbl}/coop/inxpagina/','indice',{indice},'page')"><a class="page-link" >{indice}</a></li><li class="page-item"><a class="page-link">...</a></li><li class="page-item" onclick="pgindex('frmparam','listado','/{numtbl}/coop/inxpagina/','indice',{numpags},'pgfin')"><a class="page-link">{numpags}</a></li>'''
            break
        else:
            if indice == numpags:
                active = 'active'
            pagi += f'''<li class="page-item"><a class="page-link">...</a></li><li class="page-item"><a class="page-link">...</a></li><li class="page-item {active}" onclick="pgindex('frmparam','listado','/{numtbl}/coop/inxpagina/','indice',{numpags},'pgfin')"><a class="page-link">{numpags}</a></li>'''
            break
        active = ''
            
    pagi += f'<li class="page-item" onclick="pgindex({comi}frmparam{comi},{comi}listado{comi},{comi}/{numtbl}/coop/inxpagina/{comi},{comi}indice{comi},{indice},{comi}Next{comi})"><a class="page-link" style="background-color: rgb(31, 36, 46);color: white;"><i class="fas fa-angle-double-right"></i></a></li></ul></div><div class="col-2"><div class="input-group mb-3"><input type="text" id="irpag" class="form-control" placeholder="Ir a página..." aria-label="Ir a página..." aria-describedby="ir-pag"><span class="input-group-text" id="ir-pag"><i class="fa fa-search" style="cursor: pointer;" onclick="pgindex({comi}frmparam{comi},{comi}listado{comi},{comi}/{numtbl}/coop/inxpagina/{comi},{comi}irpag{comi},1,{comi}irpag{comi})"></i></span></div></div>'
    #print("pagi = ",pagi)

            #colsp = len(fila)
    tf = f'</tbody><tfoot style="background: rgb(10, 10, 10);color: white;"><tr style="text-align: center;"><td>Acción</td><td>N°</td>'
    for i in range(len(arrtitulos)):
        tf += f'<td>{arrtitulos[i]}</td>'
        
    tf += f'</tr></tfoot>'
    #print("tf = ",tf)
            
    tabla += f'{tr}{tf}</table>'
    #print("tabla = ",tabla)
    dataobj = {
        "recordsTotal": numreg,
        'numpags': numpags,
        'indice': indice,
        'pagedat': pagi,
        'orderby': orderby,  
        'direc': direc,     
        'column': column,      
        'columnswitch': columnswitch,       
        'arrcolSwitch': arrcolSwitch,       
        'filtrosswitch': filtrosswitch, 
        'data': tabla,   
        'ruta': ruta,
        'paramfil': paramfil,  
        'cmdtext': cmdtext, 
        'arrwer': arrwer, 
        'numCheck': numCheck,  
        'crearcolumnswitch': crearcolumnswitch,             
    }
             
    return dataobj
# ///////////////////////////////////////////////////////////////     
def exe_sp(commandtext):

    print(commandtext)
    
    try:
        with connection.cursor() as cursor:
            
            cursor.execute(commandtext)
            rawData= cursor.fetchall()
               
            return rawData

    finally:
        cursor.close() 

# /////////////////////////////////////////////////////////////// 

def export_pdf(request):

    context = {}
    html = render_to_string("/home/dtblbase.html", context)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "inline; /home/js/Descargas/exportdg/report6.pdf"

    font_config = FontConfiguration()
    HTML(string=html).write_pdf(response, font_config=font_config)

    return response

def reporte(nomfile,hojasize):
    
    nomarchivo = f'/home/js/Descargas/exportdg/{nomfile}5.pdf'
    w, h = A4
    c = canvas.Canvas(nomarchivo, pagesize=A4)
    xlist = [10, 60, 110, 160]
    ylist = [h - 10, h - 60, h - 110, h - 160]
    c.grid(xlist, ylist)
    c.showPage()
    c.save()
    print(nomarchivo)
    
    return nomarchivo
    
def grouper(iterable, n):
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args)
    
def export_to_pdf(data):
    nomarchivo = '/home/js/Descargas/exportdg/nomfile11.pdf'
    c = canvas.Canvas(nomarchivo, pagesize=A4)
    w, h = A4
    max_rows_per_page = 45
    # Margin.
    x_offset = 50
    y_offset = 50
    # Space between rows.
    padding = 15
    
    xlist = [x + x_offset for x in [0, 200, 250, 300, 350, 400, 480]]
    ylist = [h - y_offset - i*padding for i in range(max_rows_per_page + 1)]
    
    print(data)
    for rows in grouper(data, max_rows_per_page):
        rows = tuple(filter(bool, rows))
        c.grid(xlist, ylist[:len(rows) + 1])
        for y, row in zip(ylist[:-1], rows):
            for x, cell in zip(xlist, row):
                c.drawString(x + 2, y - padding + 3, str(cell))
        c.showPage()
    
    c.save()






