
import json
import psycopg2
import ast
from django.db import connection
import js2py
import ipywidgets as widgets
from IPython.display import Javascript, display

from fast_autocomplete import AutoComplete
import img2pdf
from PIL import Image
import os
from PyPDF2 import PdfMerger
from os import listdir
from os.path import isfile, join

from django.conf import settings
import reportlab
import io
from django.http import FileResponse

from reportlab.pdfgen import canvas
from django.http import HttpResponse
from io import BytesIO
from django.template.loader import get_template

from datetime import datetime, date

from xhtml2pdf import pisa

class Dictoperador:
    def __init__(self):
        self.dicexp = {'1': 'tblpdf', '2': 'tblexcel', '3': 'tblcsv', '4': 'fnt_bucle()'}
            
    def fnt_dictoperdescritext(self, numoperdict):
        return self.fnt_bucledictoper(numoperdict, 1)
            
    def fnt_dictopersymboltext(self, numoperdict):
        return self.fnt_bucledictoper(numoperdict, 2)
        
    def fnt_dattype(self, key): 
        comi = "'"
        fecha_actual = date.today()
        dattype = {"bigint": 0, "integer": 0, "character varying": f"{comi}{comi}", "date": f"{comi}{fecha_actual}{comi}", "double precision": 0.00}
        
        for i,vi in dattype.items():
            if i == key:
                return vi
        
    def fnt_dictoperdescri(self, numoperdict):
        
        operdescri = {"1": "0,Igual a,Mayor o igual a,Mayor que,Menor o igual a,Menor que,Mayor que y Menor que,Mayor o igual a y Menor o igual a,Mayor o igual a y Menor que,Mayor que y Menor o igual a,Comience en,Contenga a,Termine en,Distinto de,No comience en,No contenga a,No termine en","2": "0,Igual a,Comience en,Contenga a,Termine en,Distinto de,No comience en,No contenga a,No termine en","3": "0,Igual a,Mayor o igual a,Mayor que,Menor o igual a,Menor que,Mayor que y Menor que,Mayor o igual a y Menor o igual a,Mayor o igual a y Menor que,Mayor que y Menor o igual a,Comience en,Contenga a,Termine en,Distinto de,No comience en,No contenga a,No termine en","4": "opciones"}
        
        return operdescri[numoperdict]
        
    def fnt_dictopersymbol(self, numoperdict): 
    
        opersymbol = {"1": "0,=,>=,>,<=,<,>y<,>=y<=,>=y<,>y<=,y%s,%sy%s,%sy,y<>,y%n,%ny%n,%ny","2": "0,=,y%s,%sy%s,%y,y<>,y%n,%ny%n,%ny","3": "0,=,>=,>,<=,<,>y<,>=y<=,>=y<,>y<=,y%s,%sy%s,%sy,y<>,y%n,%ny%n,%ny","4": "opt"}
        
        return opersymbol[numoperdict]
        
    def fnt_dictoperlg(self, key): 
        
        operlg = {"Igual a": "=", "Mayor o igual a": ">=", "Mayor que": ">", "Menor o igual a": "<=", "Menor que": "<", "Distinto de": "<>", "Comience en": "y%s", "Contenga a": "%sy%s", "Termine en": "%sy", "No comience en": "y%n", "No contenga a": "%ny%n", "No termine en": "%ny"}
        
        for i,vi in operlg.items():
            if i == key:
                return vi
        
    def fnt_dictoperval(self, key, valor1): 
        
        operlg = {"Igual a": f"= {valor1}", "Mayor o igual a": f">= {valor1}", "Mayor que": f"> {valor1}", "Menor o igual a": f"<= {valor1}", "Menor que": f"< {valor1}", "Distinto de": f"<> {valor1}", "Comience en": f"ILIKE {valor1}%", "Contenga a": f"ILIKE %{valor1}%", "Termine en": f"ILIKE %{valor1}", "No comience en": f"NOT_ILIKE {valor1}%", "No contenga a": f"NOT_ILIKE %{valor1}%", "No termine en": f"NOT_ILIKE %{valor1}"}
        
        for i,vi in operlg.items():
            if i == key:
                return vi              
        
    def fnt_dictdirec(self, key): 
        direc = {'0': 'fa fa-sort', 'ASC': 'fa fa-sort-amount-up', 'DESC': 'fa fa-sort-amount-down'}
        
        for i,vi in direc.items():
            if i == key:
                return vi       
        
    def dictlgoperfnt(self, key): 
        
        lgoper = {"=": "Igual a", ">=": "Mayor o igual a", ">": "Mayor que", "<=": "Menor o igual a", "<": "Menor que", "<>": "Distinto de", "y%s": "Comience en", "%sy%s": "Contenga a", "%sy": "Termine en", "y%n": "No comience en", "%ny%n": "No contenga a", "%ny": "No termine en"}
        
        for i,vi in lgoper.items():
            if i == key:
                return vi  
        
    def fnt_bucledictoper(self,numoperdict,numbucle):
    
        if numbucle == 1:
            dictoper = self.fnt_dictoperdescri(numoperdict)
        elif numbucle == 2:
            dictoper = self.fnt_dictopersymbol(numoperdict)
            
        return dictoper
        
    def fnt_buclelistoper(self,listoper,numoperlist):
        i = 1
        for vi in numoperlist:
            if i == int(numoperlist):
                return vi
            i += 1     
        
    def fnt_dictjson(self, dictjson, key): 
        
        for i,vi in dictjson.items():
            if i == key:
                return vi  
        
class Parametros:
    def __init__(self, _dictreq):
        """Esta clase se usa para todas las operaciones con diccionarios"""
        self._dictreq = _dictreq
            
    def paramcmdtext(self):
    
        comi = "'"
    
        textparam = f'{self._dictreq.get("numero")},{comi}{self._dictreq.get("critsearch")}{comi},{self._dictreq.get("inxbus")},{self._dictreq.get("inxord")},{self._dictreq.get("cons")},{self._dictreq.get("pagant")},{self._dictreq.get("indice")},{self._dictreq.get("limite")},{comi}{self._dictreq.get("arrwer")}{self._dictreq.get("orderby")}{comi},{comi}{self._dictreq.get("arrcolSwitch")}{comi}'
     
        return textparam
            
    def paramcmdtextparcial(self):
    
        comi = "'"
    
        textparamparcial = f'{self._dictreq.get("numero")},{comi}{self._dictreq.get("critsearch")}{comi},{self._dictreq.get("inxbus")},{self._dictreq.get("inxord")},{self._dictreq.get("cons")},{self._dictreq.get("pagant")},{self._dictreq.get("indice")},{self._dictreq.get("limite")},{comi}{self._dictreq.get("arrwer")},{comi}{self._dictreq.get("arrcolSwitch")}{comi}'
    
        return textparamparcial
        
    def dictformdatafnt(self, inxname):
        formdatafnt = {"1": "critsearch", "2": "inxbus", "3": "inxord", "4": "cons", "5": "pagant", "6": "indice", "7": "limite", "8": "orderby", "9": "columnswitch", "10": "stateCheck", "11": "arrcolSwitch", "12": "dict_titrel", "13": "numoper", "14": "numtblcbo", "15": "valinp", "16": "move", "17": "irpg", "18": "numpags", "19": "idvo", "20": "direc", "21": "ruta", "22": "idsel", "23": "inxopt0", "24": "inxopt", "25": "boxizq", "26": "boxder", "27": "numcbo", "28": "arrtuplas", "29": "arrnumtbl", "30": "cmdtext", "31": "arrchk", "32": "arrwer", "33": "numwer", "34": "iglike", "35": "nomfile", "36": "inpCheck", "37": "numCheck", "38": "dataobject", "39": "numcolswitch", "40": "numero", "41": "arrwery", "42": "filtrosswitch", "43": "numtblurl", "44": "titulocol", "45": "titulos", "46": "inxavan", "47": "codnew", "48": "fila", "49": "accion"}
        
        return formdatafnt[inxname]  
        
    def fnt_dictrecargar(self, num, dict_titrel):
        formdataini = {'numero': num, 'critsearch': 'ASC', 'inxbus': '0', 'inxord': '0', 'cons': '5', 'pagant': '1', 'indice': '1', 'limite': '10', 'orderby': '', 'columnswitch': '0', 'crearcolumnswitch': 'true', 'stateCheck': '', 'arrcolSwitch': '0', 'dict_titrel': dict_titrel, 'numoper': '0', 'inxavan': '0', 'paramfil': '0,0,1,1,1,10', 'move': 'page', 'irpg': '', 'numpags': '1', 'idvo': 'listado', 'direc': '0', 'ruta': 'coop', 'idsel': '', 'inxopt0': '0', 'inxopt': '0', 'boxizq': '', 'boxder': '', 'numcbo': '1', 'arrtuplas': '', 'arrnumtbl': '0', 'cmdtext': '', 'arrchk': '0', 'arrwery': '', 'arrwer': '0 > 0', 'numwer': '0', 'iglike': '', 'nomfile': '', 'inpCheck': 'false', 'numCheck': '', 'dataobject': '', 'numcolswitch': '', 'filtrosswitch': 'Filtro inicial', 'largo': '1', 'numtblurl': '140', 'titulocol': ''}
        
        return formdataini  
        
    def dict_selectuno(self, nomcampodict, textparam):
        
        commandtext = f'select * from sp_selectuno ({textparam});'
        
        rawDatauno = self.exe_sp(commandtext)
        
        for i, fila in enumerate(rawDatauno):
            thisdict = {}
            thisdict = rawDatauno[i][0]
            for i,vi in thisdict.items():                   
                if i == 'row_to_json':
                    if nomcampodict == 'fldselect':
                        return vi['fldselect']
                    elif nomcampodict == 'fldtitulos':
                        return vi['fldtitulos']  
                    elif nomcampodict == 'relacional':
                        return vi['relacional']                 
                elif i == nomcampodict:
                    return vi
      
    def dict_selectallu(self, textparam):
        commandtext = f'select * from sp_selectallu ({textparam});'
        
        return self.exe_sp(commandtext) 
           
    def dict_inxcolavanproc(self, nomcampodict, num_tblu):    
        commandtext = f'select * from inxcolavanproc({num_tblu});'  
        
        rawDatauno = self.exe_sp(commandtext)
        
        for i, fila in enumerate(rawDatauno):
            thisdict = {}
            thisdict = rawDatauno[i][0]
            for i,vi in thisdict.items():                   
                if i == nomcampodict:
                    return vi
           
    def dict_comboscombi(self, num_tblu):    
        commandtext = f'select * from comboscombi({num_tblu});'    
        
        return self.exe_sp(commandtext)
    
    def dict_findnumrow(self, num_tblu,num_row):  
        commandtext = f'select * from findnumrow({num_tblu},{num_row});'     
        
        return self.exe_sp(commandtext) 
    
    def dict_cbosidrel(self, num_tblu,id_rel):  
        commandtext = f'select * from cbosidrel({num_tblu},{id_rel});'     
        
        return self.exe_sp(commandtext) 
    
    def dict_findidbyrow(self, num_tblu, numfila):  
        commandtext = f'select * from findidbyrow({num_tblu},{numfila});'     
        
        return self.exe_sp(commandtext) 
    
    def dict_sp_information_schema(self, num_tblu, numfld):  
        commandtext = f'select * from sp_information_schema({num_tblu},{numfld});'     
        
        return self.exe_sp(commandtext) 
  
    def dict_inserttblall(self, num_tblu, textnumfld, textvalparam):  
        comi = "'"
        commandtext = f'select * from inserttblall({num_tblu},{comi}{textnumfld}{comi},{comi}{textvalparam}{comi});'     
        
        return self.exe_sp(commandtext) 
    
    def dict_sp_information_schematbl(self, num_tblu):  
        commandtext = f'select * from sp_information_schematbl({num_tblu});'     
        
        return self.exe_sp(commandtext) 
    
    def dict_sp_camposinsert(self, num_tblu):  
        commandtext = f'select * from sp_camposinsert({num_tblu});'     
        
        return self.exe_sp(commandtext) 
    
    def dict_selectall(self, num_tblu, numid):  
        commandtext = f'select * from selectall({num_tblu},{numid});'     
        
        return self.exe_sp(commandtext) 
    
    def dict_listtblselect(self, num_tblu):  
        commandtext = f'select * from listtblselect({num_tblu});'     
        
        return self.exe_sp(commandtext) 
    
    def dict_cboscod(self, num_tblu,cod):  
        commandtext = f'select * from cboscod({num_tblu},{cod});'     
        
        return self.exe_sp(commandtext) 
    
    def dict_codlike(self, num_tblu,cod):  
        commandtext = f'select * from codlike({num_tblu},{cod});'     
        
        return self.exe_sp(commandtext) 
    
    def dict_findid(self, num_tblu,id_rel,num_row):  
        commandtext = f'select * from findid({num_tblu},{id_rel},{num_row});'     
        
        return self.exe_sp(commandtext) 
    
    def dict_findcod(self, num_tblu,iglike,cod):  
        commandtext = f'select * from findcod({num_tblu},{iglike},{cod});'     
        
        return self.exe_sp(commandtext) 
          
    def exe_sp(self, commandtext):

        print(commandtext)
    
        try:
            with connection.cursor() as cursor:
            
                cursor.execute(commandtext)
                rawData= cursor.fetchall()
               
                return rawData

        finally:
            cursor.close() 
            
class Options(Parametros,Dictoperador):
    def __init__(self, _dictreq):
       super().__init__(_dictreq)
            
    def titulos(self, nomcampo):  
        
        textparam = super().paramcmdtext() 
        
        if nomcampo == 'fldtitulos':
            arrtitulos = super().dict_selectuno(nomcampo, textparam).split(", ")
        
            numCheck = ''
            for i in range(len(arrtitulos)):
                numCheck += f'{i}, '
            numCheck += ','
            numCheck = numCheck.replace(', ,', '')
            
            titnum = {'arrtitulos': arrtitulos, 'numCheck': numCheck}
            
            return titnum
            
        else:
            arrtitulos = super().dict_selectuno(nomcampo, textparam)
            
            return arrtitulos
        
    def operdescri(self, inxopt0): 
            
        arroperdescri = super().fnt_dictoperdescritext(inxopt0).split(",")
        
        options = ''            
        for oper in arroperdescri:
            options += f'<option>{oper}</option>'
            
        return options
        
    def numoper(self, inxopt0): 
         
        opcion = super().fnt_dictopersymboltext(inxopt0)
        
        textparam = super().paramcmdtext()
    
        arrrelacional = super().dict_selectuno('relacional', textparam).split(",") 
           
        c = 1
        for _elem in arrrel:
            if c == int(inxopt0):
                numoper = _elem[0]                
        
        return numoper
        
    def filtros(self): 
        
        comi = "'"
        
        nom_inpdtbl = super().dictformdatafnt("40")
        
        num_tbl = self._dictreq.get(nom_inpdtbl)
           
        nom_inpdtbl = super().dictformdatafnt("42")
        
        filtrosswitch = self._dictreq.get(nom_inpdtbl)  
        
        arrfiltrosswitch = filtrosswitch.split('xx')
        
        i = 0
        if len(arrfiltrosswitch) > 1:
            for namefiltro in arrfiltrosswitch:
                filtrosswitch += f'<li><div class="form-check form-switch"><input class="form-check-input" type="checkbox" id="fil-{i}" name="fil-{i}" onclick="fnt_changecheck({comi}selcheckfiltro{comi},{num_tbl},fil-{i})" checked><label class="form-check-label" for="fil-{i}">{namefiltro}</label></div></li>'
                i += 1
        else:
            filtrosswitch = f'<li><div class="form-check form-switch"><input class="form-check-input" type="checkbox" id="fil-{i}" name="fil-{i}" onclick="fnt_changecheck({comi}selcheckfiltro{comi},{num_tbl},fil-{i})" checked><label class="form-check-label" for="fil-{i}">{filtrosswitch}</label></div></li>'
                                
        return filtrosswitch
                 
class Tabla(Parametros,Dictoperador):

    def __init__(self, _dictreq):
        super().__init__(_dictreq)
        self.direc = {'0': 'fa fa-sort', 'ASC': 'fa fa-sort-amount-up', 'DESC': 'fa fa-sort-amount-down'}
        
    def headtbl(self, ccsthead):
        thead = ccsthead
        
        return thead
        
    def thtbl(self, numtbl, ascdesc, csn):
        
        comi = "'"
        
        th = f'<th>Acción</th><th>N°</th>'
        
        column = ''
           
        nom_inpdtbl = super().dictformdatafnt("3")
        
        inxord = self._dictreq.get(nom_inpdtbl)
           
        nom_inpdtbl = super().dictformdatafnt("20")
        
        direc = self._dictreq.get(nom_inpdtbl)
         
        nom_inpdtbl = super().dictformdatafnt("39")
        
        colsSwitch = self._dictreq.get(nom_inpdtbl)
        print("colsSwitch",colsSwitch)
            
        nom_inpdtbl = super().dictformdatafnt("10")
        
        stateCheck = self._dictreq.get(nom_inpdtbl)
            
        nom_inpdtbl = super().dictformdatafnt("45")
        
        arrtitulos = self._dictreq.get(nom_inpdtbl).split(', ')
        
        if stateCheck == 'true':
            arrcolSwitcharray = colsSwitch.split(', ')
        else:
            arrcolSwitcharray = []
            for j in range(len(arrtitulos)):
                arrcolSwitcharray.append(j) 
        
        print("arrcolSwitcharray",arrcolSwitcharray)
             
        for j in arrcolSwitcharray: 
        
            c = int(j)
            
            _titulo = arrtitulos[c]
            
            if c == int(inxord):          
                ascdesc = super().fnt_dictdirec(direc)
            else:
                ascdesc = 'fa fa-sort'  
                
            if csn == 0:  
                cssth = f'<th onclick="fntord({numtbl},{c},{comi}colu{c}{comi},{comi}{_titulo}{comi},{c+1})" style="cursor: pointer;" id="colu{c}">{_titulo}<span><i class="{ascdesc}" aria-hidden="true"></i></span></th>'
                th += cssth
                thc = th
            elif csn == 1:
                column += f'<option>{_titulo}</option>'
                thc = column
            
        dataobj = {
            'arrtitulos': arrtitulos,
            'thc': thc,
        }
                  
        return dataobj            
        
    def trtbl(self):
        
        comi = "'"
        
        textparam = super().paramcmdtext() 
        
        rawData = super().dict_selectallu(textparam)
        
        tr = ''
        for i,fila in enumerate(rawData):
        
            tr += f'<tr><td class="row"><div class="col"><span class="btn btn-primary btn-sm" data-bs-toggle="modal" data-bs-target="#addreg" data-bs-placement="top" title="Editar o modificar fila" id="btnedit{i}" onclick="clickbtn({comi}addact{comi},{comi}regact{comi},{i})"><i class="fas fa-edit"></i></span></div><div class="col"><span class="btn btn-danger btn-sm" data-bs-toggle="modal" data-bs-target="#addreg" data-bs-placement="top" title="Quitar toda la fila" id="btndel{i}" onclick="clickbtn({comi}addact{comi},{comi}regdel,{i})"><i class="fa fa-trash"></i></span></div></td>'
        
            thisdict = {}        
            thisdict = rawData[i][0]
            j = 0
            for key,value in thisdict.items():
                tr += f'<td>{value}</td>' 
            
        tr += f'</tr>'
        
        return tr

class Rutas(Parametros,Dictoperador):
    def __init__(self, _dictreq):
       super().__init__(_dictreq)
        
    def fnt_rutas(self,ruta,inxopt0,inxopt,arrwer):
        print("rtanret =",ruta)
        comi = "'"
           
        nom_inpdtbl = super().dictformdatafnt("40")
        
        num_tbl = self._dictreq.get(nom_inpdtbl)
        
        textparam = super().paramcmdtext()
    
        arrtitulos = super().dict_selectuno('fldtitulos', textparam).split(", ")
    
        arrrelacional = super().dict_selectuno('relacional', textparam).split(",")
        
        if ruta == 'select_col':   
            
            numoperdict = int(inxopt0) -1
        
            numoperdict = arrrelacional[numoperdict][0]
                
            arrv = arrrelacional[int(inxopt0)-1].split('u')
            
            if int(numoperdict) != 4:
            
                arrnumtbl = arrv[0]
        
                arroperdescri = super().fnt_dictoperdescritext(numoperdict).split(",")
                
                arroption = '<option value="">Seleccionar opción</option><option>#</option>'
                for opcion in arroperdescri:
                    arroption += f'<option>{opcion}</option>'  
            
                idsel = "col_avanu"
                move = "opttexto"
                numcbo = 1
                inbus = numoperdict
            
                selfilanv = f'<li style="margin-top: 12px"><select class="form-control input-solid bg-dark" id="{idsel}" style="color: white;cursor: pointer;" onclick="select({comi}ir_datos/subnav3content1/{numcbo}{comi},{comi}{idsel}{comi},{comi}{move}{comi},{inbus})" required>'
                   
                selfilanv += f'{arroption}</select></li><li><div id="subnav3contentres" class="d-grid gap-3" style="color: #505050;"></div></li><li><div id="subnav4contentres" class="form-group form-floating-label"></div></li>'
                
            else:
                
                arrnumtbl = arrv[1].split('x')
                
                zoof = len(arrnumtbl)
                       
                selfilanv = ''
                
                c = 1
                for idtbl in arrnumtbl:
    
                    nombre = super().dict_inxcolavanproc('nombre', idtbl)
    
                    titulo = super().dict_inxcolavanproc('titulo', idtbl)
                    
                    rawData = super().dict_comboscombi(idtbl)
                    
                    inplist = f'<input list="aut{idtbl}" id="list-{idtbl}" onclick="autocomplete_click({comi}vacio{comi},{idtbl})" placeholder="Buscar por nombre" ><datalist id="aut{idtbl}"></datalist>'
                       
                    selfilanv += f'<option><div class="dropdown p-1"><button class="btn btn-secondary dropdown-toggle widthdrop boder" type="button" id="btn{c}" data-bs-toggle="dropdown" aria-expanded="false" onclick="clickulcbo({comi}#b_ul{c} li{comi},{idtbl},{zoof},{c})" ><span id="titbtn{c}">{titulo}</span></button><ul class="dropdown-menu" aria-labelledby="btn{c}" id="b_ul{c}"></option><li>{inplist}</li>' 
                    
                    if c == 1:
                        for i, fila in enumerate(rawData):
                            thisdict = {}
                            thisdict = rawData[i][0]
                            for i,vi in thisdict.items():   
                                if i == 'numrow':
                                    numrow = vi     
                                elif i == 'codigo':
                                    codi = vi     
                                elif i == 'nombre':
                                    selfilanv += f'<li><a class="dropdown-item" href="#" id=":{numrow}:{codi}:{vi}:">{vi}</a></li>'
                    
                    c += 1
                        
                    selfilanv += f'</ul></div>' 
            
            dataobjret = {           
                'ruta': ruta,      
                'tuplas': selfilanv, 
                'numoper': numoperdict, 
                'inxopt0': inxopt0, 
                'arrnumtbl': arrnumtbl, 
            }
            
            
            return dataobjret
        
        if ruta == 'select_col1':   
            
            numoperdict = int(inxopt0) -1
        
            numoperdict = arrrelacional[numoperdict][0]
                
            arrv = arrrelacional[int(inxopt0)-1].split('u')
            
            if int(numoperdict) != 4:
            
                arrnumtbl = arrv[0]
        
                arroperdescri = super().fnt_dictoperdescritext(numoperdict).split(",")
                
                arroption = '<option value="">Seleccionar opción</option><option>#</option>'
                for opcion in arroperdescri:
                    arroption += f'<option>{opcion}</option>'  
            
                idsel = "col_avanu"
                move = "opttexto"
                numcbo = 1
                inbus = numoperdict
            
                selfilanv = f'<li style="margin-top: 12px"><select class="form-control input-solid bg-dark" id="{idsel}" style="color: white;cursor: pointer;" onclick="select({comi}ir_datos/subnav3content1/{numcbo}{comi},{comi}{idsel}{comi},{comi}{move}{comi},{inbus})" required>'
                   
                selfilanv += f'{arroption}</select></li><li><div id="subnav3contentres" class="d-grid gap-3" style="color: #505050;"></div></li><li><div id="subnav4contentres" class="form-group form-floating-label"></div></li>'
                
            else:
                
                arrnumtbl = arrv[1].split('x')
                
                zoof = len(arrnumtbl)
                
                c = 1
                for idtbl in arrnumtbl:
    
                    nombre = super().dict_inxcolavanproc('nombre', idtbl)
    
                    titulo = super().dict_inxcolavanproc('titulo', idtbl)
                    
                    rawData = super().dict_comboscombi(idtbl)
                    
                    if c == 1:                
                        selfilanv = f'<option style="color: #747b7b;text-align: center;padding-top: 5px;">Seleccionar</option>'
                        inplist = ''
                    else:
                        inplist = f'<input list="aut{idtbl}" id="list-{idtbl}" onclick="autocomplete_click({comi}vacio{comi},{idtbl})" placeholder="Buscar por nombre" ><datalist id="aut{idtbl}"></datalist>'
                       
                    selfilanv += f'<option><div class="dropdown p-1"><button class="btn btn-secondary dropdown-toggle widthdrop boder" type="button" id="btn{c}" data-bs-toggle="dropdown" aria-expanded="false" onclick="clickulcbo({comi}#b_ul{c} li{comi},{idtbl},{zoof},{c})" style="width: 200px"><span id="titbtn{c}">{titulo}</span></button><span class="input-icon-addon btn btn-primary boizq" data-bs-toggle="tooltip" data-bs-placement="top" title="Filtrar según este nombre" id="lp-{c}" onclick="bnt_click({comi}bus_filtrar{comi},{idtbl},{comi}autocomp{comi})" ><i class="fa fa-filter"></i></span><ul class="dropdown-menu" aria-labelledby="btn{c}" id="b_ul{c}"></option><li>{inplist}</li>' 
                    # onclick="bntmodal_click("inpem",{idtbl})"
                    if c == 1:
                        for i, fila in enumerate(rawData):
                            thisdict = {}
                            thisdict = rawData[i][0]
                            for i,vi in thisdict.items():   
                                if i == 'numrow':
                                    numrow = vi     
                                elif i == 'codigo':
                                    codi = vi     
                                elif i == 'nombre':
                                    selfilanv += f'<li><a class="dropdown-item" href="#" id=":{numrow}:{codi}:{vi}:">{vi}</a></li>'
                    
                    c += 1
                        
                    selfilanv += f'</ul></div>' 
            
            dataobjret = {           
                'ruta': ruta,      
                'tuplas': selfilanv, 
                'numoper': numoperdict, 
                'inxopt0': inxopt0, 
                'arrnumtbl': arrnumtbl, 
            }
            
            
            return dataobjret
                
        elif ruta == 'ir_datos':   
            
            numoperdict = int(inxopt0) - 1
        
            numoperdict = arrrelacional[numoperdict][0]
            
            arrwerytext = super().fnt_dictoperdescritext(numoperdict)
                    
            print("arrwerytext =",arrwerytext)
            
            arroperdescri = arrwerytext.split(",") 
            
            c = 2
            for lg in arroperdescri:
                if c == int(inxopt):
                    print(f'lg ------------------------------ = {lg}')
                    break 
                c += 1
            
            arrwery = lg
            
            arrlg = arrwery.split(" y ")  
            
            boxes = '<div class="p-2" >'
                
            nomid = ['inpizq','inpder']
            c = 1
            for box in arrlg:
                boxes += f'<div class="form-floating bg-light"><input type="text" class="form-control" id="{nomid[c-1]}" placeholder="{arrlg[c-1]}" onchange="fnt_changeuno({comi}{nomid[c-1]}{comi})" required=""><label for="{nomid[c-1]}">{arrlg[c-1]}</label></div><li class="p-1"></li>' 
                c += 1
                    
            boxes += f'<div class="bg-light"><button class="w-100 btn btn-md btn-primary" onclick="bnt_click({comi}bus_filtrar{comi},{num_tbl},{comi}conbox{comi})"><i class="fas fa-filter"></i>Filtrar</button></div></div>'
                
            dataobj = {      
                    'boxes': boxes, 
                    'numoper': numoperdict, 
                    'inxopttext': inxopt0, 
                    'inxopt': inxopt, 
                    'arrwery': arrwery,
                    'ruta': ruta
                }
                
            return dataobj
        
        elif ruta == 'bus_filtrar':  
            
            numcol = int(inxopt0) - 1
            
            nom_inpdtbl = super().dictformdatafnt("16")        
            move = self._dictreq.get(nom_inpdtbl)  
            print("move =",move) 
            
            nom_inpdtbl = super().dictformdatafnt("10")        
            stateCheck = self._dictreq.get(nom_inpdtbl)   
            
            nomarrcolSwitch = super().dictformdatafnt("11")        
            arrcolSwitch = self._dictreq.get(nomarrcolSwitch)   
            
            nomarrcolSwitch = super().dictformdatafnt("39")        
            numcolswitch = self._dictreq.get(nomarrcolSwitch)   
            
            nom_inpdtbl = super().dictformdatafnt("41")        
            arrwery = self._dictreq.get(nom_inpdtbl)
            print("arrwery =//////////",arrwery) 
           
            nom_inpdtbl = super().dictformdatafnt("8")        
            orderby = self._dictreq.get(nom_inpdtbl)                 
            print("orderby ",orderby)
        
            arrwerytext = arrwery.split(' y ')
            print("arrwerytext =",arrwerytext)
            
            werytext = ''
                
            if move == 'conbox':
            
                nom_inpdtbl = super().dictformdatafnt("25")        
                valboxizq = self._dictreq.get(nom_inpdtbl)
           
                nom_inpdtbl = super().dictformdatafnt("26")        
                valboxder = self._dictreq.get(nom_inpdtbl)
            
                valbox = [valboxizq, valboxder]
                print("valbox =",valbox)
            
                esp = [' y ', '']
            
                c = 0
                for text in arrwerytext:
                
                    dictoperval = super().fnt_dictoperval(text,valbox[c])
                    
                    if c == 0:
                        orderby = f' AND {numcol+1} {dictoperval}'
                        print("orderby =",orderby)  
                    else:
                        orderby += f' AND {numcol+1} {dictoperval}'
                        print("orderby =",orderby)  
                
                    if len(arrwerytext) == 1:
                        esp = ['']
                    
                    werytext += f'{arrtitulos[numcol]} | {text} | {valbox[c]}{esp[c]}'
                    
                    c += 1
                print("werytext =",werytext)  
                              
            elif move == 'autocomp':
                pass            
            elif move == 'filselcol':
                pass   
             
            if stateCheck == 'false':
                arrcolSwitch = '0' 
            else:
                arrcolSwitch = numcolswitch 
        
            dataobj = {     
                    'arrwery': werytext, 
                    'orderby': orderby,
                    'arrcolSwitch': arrcolSwitch, 
                    'arrwer': arrwer, 
                    'ruta': 'bus_filtrar'
                }
                
            return dataobj  
        
        elif ruta == 'savewer':   
           
            nom_inpdtbl = super().dictformdatafnt("32")
        
            arrwer = self._dictreq.get(nom_inpdtbl)   
           
            nom_inpdtbl = super().dictformdatafnt("8")
        
            orderby = self._dictreq.get(nom_inpdtbl) 
           
            nom_inpdtbl = super().dictformdatafnt("41")
        
            arrwery = self._dictreq.get(nom_inpdtbl)  
                    
            print(f'arrwery =============== {arrwery}')
            
            print(f'arrwer =============== {arrwer}{orderby}')
            
            nom_inpdtbl = super().dictformdatafnt("42")
           
            filtrosswitch = self._dictreq.get(nom_inpdtbl)  
            
            filtrosswitch = f'{filtrosswitch}xx{arrwery}'
        
            arrfiltrosswitch = filtrosswitch.split('xx')
            
            print(f'filtrosswitch =============== {filtrosswitch}')
            
            print(f'arrfiltrosswitch =============== {arrfiltrosswitch}')
            
            strhtml = ''
            i = 0  
            for filtro in arrfiltrosswitch:
                strhtml += f'<li><div class="form-check form-switch"><input class="form-check-input" type="checkbox" id="fil-{i}" name="filtro" onclick="fnt_changecheck({comi}selcheckfiltro{comi},{num_tbl},{comi}fil-{i}{comi})" checked><label class="form-check-label" for="fil-{i}">{filtro}</label></div></li>'
                i += 1
                
            dataobj = {     
                    'arrwer': f'{arrwer}{orderby}', 
                    'filtrosswitch': filtrosswitch, 
                    'strhtml': strhtml, 
                    'ruta': 'savewer'
                }
                
            return dataobj
                
        elif ruta == 'cbocomb':   
            
            nom_inpdtbl = super().dictformdatafnt("14")
        
            numtblcbo = self._dictreq.get(nom_inpdtbl)  
            
            nom_inpdtbl = super().dictformdatafnt("47")
        
            codnew = self._dictreq.get(nom_inpdtbl)
           
            nom_inpdtbl = super().dictformdatafnt("29")
        
            arrnumtbl = self._dictreq.get(nom_inpdtbl).split(',')
            
            zoof = len(arrnumtbl)  
           
            nom_inpdtbl = super().dictformdatafnt("24")
        
            inxopt = self._dictreq.get(nom_inpdtbl)
            print(f'inxopt------------>>>> = {inxopt}') 
           
            nom_inpdtbl = super().dictformdatafnt("27")
        
            numcbo = self._dictreq.get(nom_inpdtbl)
           
            nom_inpdtbl = super().dictformdatafnt("30")
        
            arrinnerhtml = self._dictreq.get(nom_inpdtbl).split(':')
#<a class="dropdown-item" id="1:679:13-08-01:Trinidad Samuel:">Trinidad Samuel</a> Index = 1              
        
            titulo = arrinnerhtml[-2]            
        
            codant = arrinnerhtml[-3]
        
            numrow = int(arrinnerhtml[-4])
               
            c = int(numcbo) + 1 
 
            if int(numcbo) == int(zoof):
                tipcbo = 'lastcbo'  
                num_tbl = arrnumtbl[int(zoof)-1] 
            else:
                tipcbo = 'nextcbo'   
                num_tbl = arrnumtbl[int(numcbo)]
 
            rawData = super().dict_codlike(num_tbl,f'{comi}{codant}{comi}') 
        
           #print(f'rawData = {rawData}') 
              
            selfilanv = '' 
                    
            for i, fila in enumerate(rawData):
                thisdict = {}
                thisdict = rawData[i][0]
                for j,vj in thisdict.items():                  
            
                    if j == 'id':
                        row_num = vj     
                    elif j == 'codigo':
                        codi = vj    
                    elif j == 'nombre':
                        selfilanv += f'<li><a class="dropdown-item" href="#"id="1:{row_num}:{codi}:{vj}:">{vj}</a></li>'
            #print(f'selfilanv = {selfilanv}')  
            
            codnew = codi
            
            orderby = f' AND {int(inxopt0)} = {codnew}' 
            
            numcol = int(inxopt0) - 1
            
            tblcbo = num_tbl
            
            text = super().dictlgoperfnt("=")
            
            werytext = f'{arrtitulos[numcol]} | {text} | {row_num}'
            
            inplist = f'<li><input list="aut{tblcbo}" id="list-{tblcbo}" onclick="autocomplete_click({comi}vacio{comi},{tblcbo})" placeholder="Buscar por nombre" ><datalist id="aut{tblcbo}"></datalist></li>'
            
            dataobj = {     
                'idsel': f'b_ul{c}',     
                'titbtn': f'titbtn{c-1}', 
                'titulo': titulo,
                'selfilanv': f'{inplist}{selfilanv}', 
                'tipcbo': tipcbo,
                'orderby': orderby,
                'numrow': numrow,
                'inxopt0': inxopt0,
                'inxbus': inxopt0,    
                'arrwery': werytext,   
                'codnew': codnew,
                'ruta': 'cbocomb'
            }
                
            return dataobj
                
        elif ruta == 'fillauto':  
            
            idtbl = num_tbl
            
            rawData = super().dict_comboscombi(idtbl);
                    
            selfilanv = '' 
                    
            for i, fila in enumerate(rawData):
                thisdict = {}
                thisdict = rawData[i][0]
                for i,vi in thisdict.items():  
                    if i == 'numrow':
                        numrow = vi      
                    elif i == 'codigo':
                        codi = vi     
                    elif i == 'nombre':
                        selfilanv += f'<option value=":{numrow}:{codi}:{vi}"></option>'
                
            dataobj = {  
                'selfilanv': selfilanv, 
                'numsel': f'aut{idtbl}', 
                'ruta': 'fillauto'
            }
                
            return dataobj  
                
        elif ruta == 'inxpagina': 
           
            nom_inpdtbl = super().dictformdatafnt("16")
        
            move = self._dictreq.get(nom_inpdtbl)
           
            nom_inpdtbl = super().dictformdatafnt("6")
        
            indice = int(self._dictreq.get(nom_inpdtbl))
           
            nom_inpdtbl = super().dictformdatafnt("17")
        
            irpg = int(self._dictreq.get(nom_inpdtbl))
           
            nom_inpdtbl = super().dictformdatafnt("19")
        
            idvo = self._dictreq.get(nom_inpdtbl)
           
            nom_inpdtbl = super().dictformdatafnt("18")
        
            numpags = int(self._dictreq.get(nom_inpdtbl))
            
            if move == 'Previous':
                inx = indice - 1
                if inx > 0:
                    indice = inx
            
            elif move == 'page':
                pass
            
            elif move == 'pgfin':
                pass
            
            elif move == 'Next':
                inx = indice + 1
                if inx <= numpags:
                    indice = inx
            
            elif move == 'irpag':
                indice = irpg
                
            dataobj = {  
                'indice': indice,
                'ruta': 'inxpagina'
            }
                
            return dataobj
                
        elif ruta == 'ordenar': 
           
            nom_inpdtbl = super().dictformdatafnt("22")
        
            idsel = self._dictreq.get(nom_inpdtbl)
           
            nom_inpdtbl = super().dictformdatafnt("44")
        
            _titulo = self._dictreq.get(nom_inpdtbl)
           
            nom_inpdtbl = super().dictformdatafnt("20")
        
            direc = self._dictreq.get(nom_inpdtbl)
            
            ascdesc = super().fnt_dictdirec(direc)
            
            if ascdesc == 'fa fa-sort':
                direc = 'ASC'
            elif ascdesc == 'fa fa-sort-amount-up':
                direc = 'DESC'
            elif ascdesc == 'fa fa-sort-amount-down':
                direc = 'ASC'
            
            ascdesc = super().fnt_dictdirec(direc)
            
            print(ascdesc)
               
            dataobj = {  
                'numero': num_tbl,
                'direc': direc,
                'idsel': idsel,
                'titascdesc': f'{_titulo}<span><i class="{ascdesc}" aria-hidden="true"></i></span>',
                'ruta': 'ordenar'
            }
                
            return dataobj
                
        elif ruta == 'recargar': 
           
            nom_inpdtbl = super().dictformdatafnt("40")
        
            num = self._dictreq.get(nom_inpdtbl)
            
            print(num)
            
            dict_titrel = {}
            
            valini = super().fnt_dictrecargar(num, dict_titrel)
            
            print(valini)
               
            dataobj = {  
                'valini': valini,
                'ruta': 'recargar'
            }
                
            return dataobj
                
        elif ruta == 'bus_global': 
            
            print(ruta)
           
            nom_inpdtbl = super().dictformdatafnt("1")
        
            critsearch = self._dictreq.get(nom_inpdtbl)
            
            print(critsearch)
           
            nom_inpdtbl = super().dictformdatafnt("4")
        
            cons = self._dictreq.get(nom_inpdtbl)
               
            dataobj = {  
                'critsearch': f'%{critsearch}%',
                'cons': 2,
                'ruta': 'bus_global'
            }
              
            return dataobj
                
        elif ruta == 'selcheckfiltro': 
            
            nom_inpdtbl = super().dictformdatafnt("37")
        
            numCheck = self._dictreq.get(nom_inpdtbl)
           
            nom_inpdtbl = super().dictformdatafnt("41")
        
            arrwery = self._dictreq.get(nom_inpdtbl)  
                    
            print(f'arrwery =============== {arrwery}')
            
            nom_inpdtbl = super().dictformdatafnt("42")
           
            filtrosswitch = self._dictreq.get(nom_inpdtbl)  
            
            arrfiltrosswitch = filtrosswitch.split('xx')
                    
            print(f'arrfiltrosswitch =============== {arrfiltrosswitch}')
            
            strhtml = ''
            i = 0  
            for filtro in arrfiltrosswitch:
                strhtml += f'<li><div class="form-check form-switch"><input class="form-check-input" type="checkbox" id="fil-{i}" name="filtro" onclick="fnt_changecheck({comi}selcheckfiltro{comi},{num_tbl},{comi}fil-{i}{comi})" checked><label class="form-check-label" for="fil-{i}">{filtro}</label></div></li>'
                i += 1
               
            dataobj = {  
                'critsearch': f'%{critsearch}%',
                'cons': 2,
                'ruta': 'bus_global'
            }
              
            return dataobj
               
            dataobj = {  
                'critsearch': f'%{critsearch}%',
                'cons': 2,
                'ruta': 'bus_global'
            }
             
            return dataobj
                
        elif ruta == 'addact': 
           
            nom_inpdtbl = super().dictformdatafnt("6")
        
            indice = int(self._dictreq.get(nom_inpdtbl))
           
            nom_inpdtbl = super().dictformdatafnt("7")
        
            limite = int(self._dictreq.get(nom_inpdtbl))
           
            nom_inpdtbl = super().dictformdatafnt("48")
        
            xfila = int(self._dictreq.get(nom_inpdtbl)) + 1
            
            if indice > 1:
                xfila += (indice-1)*limite
           
            nom_inpdtbl = super().dictformdatafnt("49")
        
            accion = self._dictreq.get(nom_inpdtbl) 
            
            numfld = ''
            valparam = ''
            constring = '{'
            if accion == 'addreg': 
            
                rawData = super().dict_sp_camposinsert(num_tbl) 
                
                for i,fila in enumerate(rawData):
                    thisdict = {}        
                    thisdict = rawData[i][0]
                    j = 0
                    for key,value in thisdict.items():
                        nominsert = value
                
                rawData = super().dict_sp_information_schematbl(num_tbl) 
                
                for i,fila in enumerate(rawData):
                    thisdict = {}        
                    thisdict = rawData[i][0]
                    j = 0
                    for key,value in thisdict.items():
                        if key == 'column_name':
                            nomcol = value
                        elif key == 'data_type':
                            datatype = super().fnt_dattype(value) 
                        elif key == 'is_nullable':
                            isnul = value
                            if i < len(rawData)-1:
                                poscol = nominsert.find(nomcol)
                                if poscol > -1:
                                    numfld += f'{i},'
                                    valparam += f'{datatype}, '
                                    constring += f'{comi}{nomcol}{comi}: {datatype}, '
                liz = "["
                lde = "]"
                numfld += '|'
                numfld = numfld.replace(',|','')
 
                valparam += '|'
                valparam = valparam.replace(', |','')
                valparam = f'[{valparam}]'
 
                constring += '|}'
                constring = constring.replace(', |','')
                constring = constring.replace("'",'"')
                print(constring)   
                            
                rawData = super().dict_inserttblall(num_tbl, numfld, valparam)              
            
            arrrelacional = super().dict_selectuno('relacional', textparam).split(",") 
            print(arrrelacional)
 
            rawData = super().dict_findidbyrow(num_tbl,xfila) 
            
            valid = 0
            for i,fila in enumerate(rawData):
                thisdict = {}        
                thisdict = rawData[i][0]
                j = 0
                for key,value in thisdict.items():
                    if key == 'id':
                        valid = value
            
            rawData = super().dict_selectall(num_tbl,valid)
            
            frm = '<form id="frmedit" class="form-control">'
            
            for i,fila in enumerate(rawData):
#1217725 Camjust36%        
                thisdict = {}        
                thisdict = rawData[i][0]
                j = 0
                for key,value in thisdict.items():
                    tipfile = int(arrrelacional[j].split('u')[0])
            
                    try:
                        valinp = value
                    except:
                        valinp = ''
                        
                    if tipfile == 3:
                        frm += f'<div class="col-md p-1"><div class="form-floating"><input type="date" class="form-control" id="inp-{j}" placeholder="{arrtitulos[j]}" aria-describedby="basic-addon1" value="{valinp}" style="font-size: 14px; color: #5b5b68" onclick="cboemerg({j},{comi}inp-{j}{comi})"><label for="inp-{j}">{arrtitulos[j]}</label></div></div>'
                    else:
                        frm += f'<div class="col-md p-1"><div class="form-floating"><input type="text" class="form-control" id="inp-{j}" placeholder="{arrtitulos[j]}" aria-describedby="basic-addon1" value="{valinp}" style="font-size: 14px; color: #5b5b68" onclick="cboemerg({j},{comi}inp-{j}{comi})"><label for="inp-{j}">{arrtitulos[j]}</label></div></div><div class="p-1" id="selcbo{j}"></div>' 
                            
                    j += 1
                
            frm += '</form>'
               
            dataobj = {  
                'accion': accion,
                'formulario': frm,
                'ruta': 'addact'
            }
              
            return dataobj
                
        elif ruta == 'pop_up': 
           
            nom_inpdtbl = super().dictformdatafnt("15")
            
            valinp = self._dictreq.get(nom_inpdtbl)
                
            print(valinp)
            
            try:
                codant = valinp
            except:
                codant = ''
                
            print(valinp)
           
            nom_inpdtbl = super().dictformdatafnt("24")
        
            inxopt = int(self._dictreq.get(nom_inpdtbl))
    
            arrrelacional = super().dict_selectuno('relacional', textparam).split(",") 
            
            opt = ''
            
            j = 0
            for reltex in arrrelacional:
                arrreltex = reltex.split('u') 
                if int(arrreltex[0]) == 4:
                    xnumtbl = arrreltex[1]
                    if j == inxopt:
                        arrx = arrreltex[1].split('x')
                        opt = f'<select class="form-select form-select-sm" aria-label="Ejemplo de .form-select-sm" id="selemerg{inxopt}" onclick="fnt_col_u({comi}inp-{inxopt}{comi},{comi}selemerg{inxopt}{comi},{comi}col_u{comi},{arrx[0]})">' 
                        if len(arrx) == 1:
                            rawData = super().dict_listtblselect(xnumtbl)
                            print(rawData)
                            xselected = ''
            
                            for i,fila in enumerate(rawData):        
                                thisdict = {}        
                                thisdict = rawData[i][0]
                                k = 0
                                for key,value in thisdict.items():
                                    if k == inxopt:
                                        xselected = 'selected'
                                    if key == 'nombre':
                                        nombre = value
                                        opt += f'<option {xselected}>{nombre}</option>'  
                                k += 1
                                
                        else: 
                            arrcodant = codant.split('-')
                            
                            cod = ''    
                            c = 0
                            for num_x in arrx:
                                cod += arrcodant[c]
                                rawData = super().dict_codlike(num_x,f'{comi}{cod}{comi}') 
                                opt = f'<select class="form-select form-select-sm" aria-label="Listado emergente" id="selemerg{num_x}" onclick="fnt_col_u({comi}inp-{inxopt}{comi},{comi}selemerg{num_x}{comi},{comi}col_u{comi},{num_x})">' 
                                xselected = ''
                                for i,fila in enumerate(rawData):        
                                    thisdict = {}        
                                    thisdict = rawData[i][0]
                                    nombre = super().fnt_dictjson(thisdict, 'nombre')
                                    opt += f'<option {xselected}>{nombre}</option>' 
                                if c < len(arrx)-1:
                                     cod += '-'
                                     
                j += 1
                
            opt += '</select>'
                                 
            dataobj = {  
                'selcbo': f'selcbo{inxopt}',
                'opciones': opt,
                'ruta': 'pop_up'
            }
               
            return dataobj
                
        elif ruta == 'col_u': 
           
            nom_inpdtbl = super().dictformdatafnt("24")
        
            inxopt = int(self._dictreq.get(nom_inpdtbl))
           
            nom_inpdtbl = super().dictformdatafnt("27")
        
            numtbl = int(self._dictreq.get(nom_inpdtbl))
           
            nom_inpdtbl = super().dictformdatafnt("48")
        
            filaindex = int(self._dictreq.get(nom_inpdtbl))
 
            rawData = super().dict_findidbyrow(numtbl,filaindex+1) 
            
            for i,fila in enumerate(rawData):        
                thisdict = {}        
                thisdict = rawData[i][0]
                for key,value in thisdict.items():
                    if key == 'codigo':
                        cod = value
            #cod = super().fnt_dictjson(thisdict, 'codigo')
                                 
            dataobj = {  
                'codigo': cod,
                'idinp': f'inp-{inxopt}',
                'ruta': 'col_u'
            }
#nikolai patrushev               
            return dataobj
        
class Lista:
    
    def __init__(self):
        pass
        
    def dicttitrel(self, titulos, relacional):
    
        titrel = {}
    
        dicttitulos = {}
                
        arrtitulos = titulos.split(", ") 
                
        arrrelacional = relacional.split(",") 
        
        c = 0
        for titulo in arrtitulos:
            titrel[titulo] = arrrelacional[c]
            key = str(c)
            dicttitulos[key] = titulo
            c += 1
        
        dataobj = {"titrel": titrel, "dicttitulos": dicttitulos}
            
        return dataobj
        
    def unirpdf(self, listpdf, nombre_archivo_salida):
        
        try:
        
            merger = PdfMerger()
        
            for pdf in listpdf:
                merger.append(pdf)
            merger.write(nombre_archivo_salida)
            merger.close()
            return True
        except Exception as e:
            print(e)
            print('Error al unir los pdf')
            return False
        
    def imgTopdf(self, img_path, pdf_path):
  
# opening image
        image = Image.open(img_path)
  
# converting into chunks using img2pdf
        pdf_bytes = img2pdf.convert(image.filename)
  
# opening or creating pdf file
        file = open(pdf_path, "wb")
  
# writing pdf files with chunks
        file.write(pdf_bytes)
  
# closing image file
        image.close()
  
# closing pdf file
        file.close()
  
# output
        return "Successfully made pdf file"
         
    def abrir(self):
        ruta= 'fotos'
        archivos = ''     # ### nunca se usa
        fichero = QFileDialog.getOpenFileName(self, "Abrir fichero")
        with open(fichero, 'rb') as fsrc:
            a = fsrc.read()
        
        shutil.copyfile(fichero, ruta)

    def uploadFile(self):
        fileTitle = request.POST["fileTitle"]
        uploadedFile = request.FILES["uploadedFile"]

            # Saving the information in the database
        document = models.Document(
            title = fileTitle,
            uploadedFile = uploadedFile
        )
        document.save()

        documents = models.Document.objects.all()

        return render(request, "Core/upload-file.html", context = {
            "files": documents
        })

class ezmPDF(Parametros,Dictoperador):
    
    #print('ToPDF2') 
    
    def __init__(self, _dictreq):
       super().__init__(_dictreq)
        
    def reportpdf(self):
        comi = "'"
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="hello.pdf"'
        buffer = BytesIO()
        p = canvas.Canvas(buffer)
        p.setFont("Courier", 28)
        p.setFillColorRGB(0.14, 0.59, 0.74)
        p.drawString(60, 750, "Videojuegos")
        p.setFont("Helvetica", 16)
        p.setFillColorRGB(0, 0, 0)
 
        rawData = super().dict_codlike(134,f'{comi}13{comi}') 
              
        selfilanv = '' 
        
        positionY = 700            
        for i, fila in enumerate(rawData):
            thisdict = {}
            thisdict = rawData[i][0]
            for j,vj in thisdict.items():   
                if j == 'id':
                    row_num = vj     
                elif j == 'codigo':
                    codi = vj    
                elif j == 'nombre':
                    name = vj
                    selfilanv += f'<li><a class="dropdown-item" href="#"id="1:{row_num}:{codi}:{vj}:">{vj}</a></li>'
            p.drawString(60, positionY, name)
            positionY -= 25
            
        #print(f'selfilanv = {selfilanv}') 
        
        p.showPage()
        p.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        
        return response  
            
    def export_pdf(self):
    
        comi = "'"
        
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="/home/js/Descargas/exportdg/mydata.pdf"'

        # Create the PDF object, using the response object as its "file."
        p = canvas.Canvas(response)

        # Define the width and height of each row in the table
        row_height = 20
        column_width = 50

        # Define the data to be printed in the table
        data = [
            ['N°', 'ID', 'Código', 'Nombre'],
        ]  
 
        rawData = super().dict_codlike(134,f'{comi}13{comi}') 
        
        strdata = ''    
        for i, fila in enumerate(rawData):
            thisdict = {}
            thisdict = rawData[i][0]
            for j,vj in thisdict.items():  
                if j == 'numrows':
                    strdata += f'{vj},'      
                elif j == 'id':
                    strdata += f'{vj},'    
                elif j == 'codigo':
                    strdata += f'{vj},'   
                elif j == 'nombre':
                    strdata += f'{vj}' 
            
            arrdata = strdata.split(',')  
            data.append(arrdata)   
        #for obj in MyModel.objects.all():
            #data.append([obj.id, obj.codigo, obj.nombre])

        # Draw the table
        x = 50
        y = 750
        for row in data:
            for item in row:
                p.drawString(x, y, str(item))
                x += column_width
            x = 50
            y -= row_height

        # Close the PDF object cleanly, and we're done.
        p.showPage()
        p.save()
        
        return response   

    def render_to_pdf(self, template_src):
        
        comi = "'"
        
        context_dict={}
        
        template = get_template(template_src)        
 
        rawData = super().dict_codlike(134,f'{comi}13{comi}')  
        
        strdata = "{'0' : {'1': 'N°', '2': 'ID', '3': 'Código', '4': 'Nombre'}}, "
        
        xlxl = '{'
        
        lxlx = '}'
           
        for i, fila in enumerate(rawData):
            thisdict = {}
            thisdict = rawData[i][0]
            for j,vj in thisdict.items():  
                if j == 'numrows':
                    strdata += f'{xlxl}{comi}{i+1}{comi}: {xlxl}{comi}1{comi}: {vj}, '      
                elif j == 'id':
                    strdata += f'{comi}2{comi}: {vj}, '     
                elif j == 'codigo':  
                    strdata += f'{comi}3{comi}: {comi}{vj}{comi}, '   
                elif j == 'nombre': 
                    strdata += f'{comi}4{comi}: {comi}{vj}{comi}{lxlx}{lxlx}, ' 
        strdata += 'k'  
        strdata = strdata.replace(', k','')
            
        print(strdata)
            
        data = ast.literal_eval(strdata)
            
        print(data)
        
        html  = template.render(data)
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
        if not pdf.err:
            return HttpResponse(result.getvalue(), content_type='application/pdf')
        return None 
        
            
                   
class Move:
    def __init__(self):
        self.dictmove = {'move_u': 1, 'col_si': 2, 'page': 3, 'irpag': 4, 'pgfin': 5, 'Previous': 6, 'Next': 7, 'order': 8, 'ordorig': 9}

    def movi(self, value):
        return self.dictmove[value]

class ExportTo:
    def __init__(self):
        self.dicexp = {'1': 'tblpdf', '2': 'tblexcel', '3': 'tblcsv'}

    def fnt_bucle(self,codigo,n,idsel):
        
        if idsel == '4':
            arrcod = list(codigo)
            codigo = ''
            codtemp = ''
            t = 0
            for j in range(len(arrcod)):        
                for c in range(n):
                    codtemp += arrcod[t]
                    t += 1
                if t < len(arrcod):
                    codigo += f'{codtemp}-'
                    codtemp = ''
                else:
                    codigo += f'{codtemp}'
                    break
    
            return codigo
            
class Booleano:
    def __init__(self):
        self.ditbool = {'false': 0, 'true': 1}

    def isboolean(self, value):
        return self.ditbool[IsPresent.texto(self,value,1)]
            
class IsPresent:
    def __init__(self):
        self.arrswitchtextini = ''

    def texto(self, arrvalue, nt):
        
        not_its = 'false'
        arrswitchtextout = []
        for _elem in arrvalue:
            print(nt)
            if int(_elem) != 0:
                not_its = 'true'
                self.arrswitchtextout.append(_elem)
        if nt == 1:
            return not_its
        elif nt == 2:
            if len(arrswitchtextout):
                return arrswitchtextout

class PushCheck:
    def __init__(self):
        self.arrswitchtext = []

    def checkpush(self, value):
        self.arrswitchtext = IsPresent.texto(self,value, 2)
        
class Select_tblcombos:
    def __init__(self,numtbl,accion,nt):
        self.comi = "'"
        self.numtbl = numtbl
        self.accion = accion
        self.nt = nt
        
    def sp_select(self):
        self.nt = f'{comi}{self.nt}{comi}'
        
class Parametros1:
    def __init__(self,numtbl,accion,cmdtext,numSwitchtext,_dictreq):
        self.comi = "'"
        self.dictparamfiltros = {'1': f'{self.numtbl},{self.comi}%%{self.comi},1,0,1,1,1,10,{self.comi}{comi},{self.comi}{self.comi}', '5': f'{self.cmdtext()},{self.numSwitchtext()}'}
        self.dictruta = {'0': 'listado_autor', '1': 'ordenar', '2': 'select_cbo', '3': 'select_u', '4': 'regadd', '5': 'actualizar', '6': 'recargar', '7': 'select_col', '8': 'select_colsi', '9': 'select_v', '10': 'btn_enviar', '11': 'submenu', '12': 'regact', '13': 'cbocomb', '14': 'savewer', '15': 'selcheck', '16': 'exportar', '17': 'rutaget'}
        self.listruta = ['listado_autor', 'ordenar', 'select_cbo', 'select_u', 'regadd', 'actualizar', 'recargar', 'select_col', 'select_colsi', 'select_v', 'btn_enviar', 'submenu', 'regact', 'cbocomb', 'savewer', 'selcheck', 'exportar', 'rutaget']

    def paramfiltros(self, accion):
        return self.dictparamfiltros[accion]

    def cmdtext(self, accion):
        return self.dictparamfiltros[accion]

    def numSwitchtext(self, accion):
        return self.dictparamfiltros[accion]

    def listcmdtext(self, dictrequest):
        return self.dictparamfiltros[accion]
        
class Dictbucletext:
    def __init__(self):
        self.comi = "'"

    def paramfiltros(self, arr_, tarr):
        return self.dictparamfiltros[accion]
        
class Dataobjtbl:
    def __init__(self, tuplarequest):    
        self.comi = "'"    
        
    def dataobj(self, tuplarequest): 
    
        tabla1 = Tabla('id="tblmain"', ['Acción', 'N°']) 
        tabla2 = tabla1.headtbl('style="background: #36597a;color: azure;"')      
        tabla3 = tabla2.thtbl()       
        tabla = tabla3.tdtbl()  
        
        dataobj = {
            "recordsTotal": arrtuplassss(tuplarequest,'numreg',0),
            'numpags': arrtuplassss(tuplarequest,'numpags',1),
            'indice': indice,
            'pagedat': pagi,
            'orderby': orderby,  
            'direc': direc,     
            'column': column,      
            'columnswitch': columnswitch,       
            'arrcolSwitch': arrcolSwitch, 
            'data': tabla, 
            'ruta': ruta,
            'paramfil': paramfil,  
            'cmdtext': cmdtext, 
            'arrwer': arrwer,              
        }
        
        return dataobj
class Sp_fnt:

    def __init__(self, move): 
        self.move = move
        self.dictmove = {'1': 'move_u', '2': 'col_si', '3': 'page', '4': 'irpag', '5': 'pgfin', '6': 'Previous', '7': 'Next', '8': 'order', '9': 'ordorig'}
    
    def fnt_cmd(self, cmdtext, filini):
        if self.filini == 1:
            pass
    
class Dataobjtbluno:
    def __init__(self, tuplarequest, move, orderby):    
        self.comi = "'"
        self.paramfil = '0,0,1,1,1,10'
        self.arrcolSwitch = arrtuplassss(tuplarequest,'arrcolSwitch',2)
        self.dataobj = dataobj
        self.tuplarequest = tuplarequest
        self.move = move
        self.orderby = orderby        
          
        self.dataobj1 = {
            "recordsTotal": arrtuplassss(tuplarequest,'numreg',0),
            'numpags': arrtuplassss(tuplarequest,'numpags',1),
            'indice': indice,
            'pagedat': pagi,
            'orderby': orderby,  
            'direc': direc,     
            'column': column,      
            'columnswitch': columnswitch,       
            'arrcolSwitch': arrcolSwitch, 
            'data': tabla,   
            'ruta': ruta,
            'paramfil': paramfil,  
            'cmdtext': cmdtext, 
            'arrwer': arrwer,              
        }
        
        self.dataobj2 = {           
            'combos': combos, 
            'ruta': rutaorig,  
            'numcbo': -1, 
        }
        
        self.dataobj3 = {           
            'ruta': rutaorig,      
            'tuplas': arrsel[0],   
            'arrtuplas': arrtuplas,     
            'textcod': arrsel[1],       
            'critsearch': critsearch,       
            'cmdtext': cmdtext,            
            'numcbo': numcbo,   
        }
        #savewer
        self.dataobj4 = {
            "column": column,
            "columnswitch": columnswitch,
            "arrcolSwitch": arrcolSwitch,
            "arrwer": arrwer,
            "numwer": numwer,
            "mensaje": f'<div class="alert alert-success alert-dismissible fade show" role="alert">Total filtros agregados: <strong>{numwer}</strong><button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>',
                    "ruta": 'savewer',
        }
               
        return dataobj 
    
'''
 
        
            numoperdict = int(inxopt0) -1
        
            numoperdict = arrrelacional[numoperdict][0]
            
            if int(numoperdict) != 4:
                
                rawData = super().dict_comboscombi('136');
                    
                numrow = 1
                for f, fila in enumerate(rawData):
                    thisdict = {}
                    thisdict = rawData[f][0]
                    for i,vi in thisdict.items():  
                        if i == 'codigo':
                            c = 0
                            x = list(vi)
                            ls = x[c]
                            c += 1
                            ls += f'{x[c]}-'
                            c += 1
                            ls += f'{x[c]}'
                            c += 1
                            ls += f'{x[c]}-'
                            c += 1
                            ls += f'{x[c]}'
                            c += 1
                            ls += f'{x[c]}-'
                            c += 1
                            ls += f'{x[c]}'
                            c += 1
                            ls += f'{x[c]}'
                            c += 1
                            break
                    findid = super().dict_findid(136,numrow) 
                     
                    for r, row in enumerate(findid):
                        thisdictid = {}
                        thisdictid = findid[r][0]
                        for j,vj in thisdictid.items(): 
                            if j == 'id':
                                id = vj
                            elif j == 'tbl':
                                tbl = vj
                                break  
                        if numrow >= 961 and numrow <= 1340:  
                            print(f"UPDATE {tbl} SET codigo={comi}{ls}{comi} WHERE id={id};")
                                
                    numrow += 1
                    
<div class="form-check form-switch bg-dark p-2"><input class="form-check-input m-1" type="checkbox" role="switch" id="colCheck" onclick="fnt_colCheck()" checked=""><label class="form-check-label" for="colCheck">Seleccionar columnas</label></div>
                
        elif ruta == 'cbocomb':     
           
            nom_inpdtbl = super().dictformdatafnt("29")
        
            arrnumtbl = self._dictreq.get(nom_inpdtbl).split('x')
           
            nom_inpdtbl = super().dictformdatafnt("24")
        
            inxopt = self._dictreq.get(nom_inpdtbl)
           
            nom_inpdtbl = super().dictformdatafnt("27")
        
            numcbo = self._dictreq.get(nom_inpdtbl)
           
            nom_inpdtbl = super().dictformdatafnt("30")
        
            arrinnerhtml = self._dictreq.get(nom_inpdtbl).split(':')
        
            titulo = arrinnerhtml[-2]
        
            codigo = arrinnerhtml[-3]
        
            numrow = int(arrinnerhtml[-4])
            
            zoof = len(arrnumtbl)  
               
            c = int(numcbo) + 1 
            
            if len(arrnumtbl) > 1:
                cod = f'{comi}{codigo}%{comi}' 
                iglike = f'{comi}like{comi}'
            else:
                cod = f'{comi}{codigo}{comi}'
                iglike = f'{comi}={comi}'
                    
            print("c =",c,"; cod =",cod,"; iglike ",iglike,"; titulo =",titulo) 
                    
            print("numcbo =",numcbo,"; zoof =",zoof," arrnumtbl =",arrnumtbl) 
 
            if int(numcbo) == int(zoof):
                tipcbo = 'lastcbo'  
                num_tbl = arrnumtbl[int(zoof)-1] 
            else:
                tipcbo = 'nextcbo'
                numcbo = c            
                num_tbl = arrnumtbl[int(numcbo)]
                
            rawData = super().dict_findcod(num_tbl,iglike,cod) 
            print("rawData =",rawData)
                
            selfilanv = '' 
                    
            for i, fila in enumerate(rawData):
                thisdict = {}
                thisdict = rawData[i][0]
                for j,vj in thisdict.items():  
                    if j == 'id':
                        row_num = vj     
                    elif j == 'codigo':
                        codi = vj    
                    elif j == 'nombre':
                        selfilanv += f'<li><a class="dropdown-item" href="#"id=":{row_num}:{codi}:{vj}:">{vj}</a></li>'
            print("selfilanv =",selfilanv)
            
            orderby = f' AND {int(inxopt0)} = {row_num}' 
            
            numcol = int(inxopt0) - 1
            
            text = super().dictlgoperfnt("=")
            print("text =",text)
            
            werytext = f'{arrtitulos[numcol]} | {text} | {row_num}'
               
            dataobj = {     
                'idsel': f'b_ul{c}',     
                'titbtn': f'titbtn{c-1}', 
                'titulo': titulo,
                'selfilanv': selfilanv, 
                'tipcbo': tipcbo,
                'orderby': orderby,
                'numrow': numrow,
                'inxopt0': inxopt0,
                'inxbus': inxopt0,    
                'arrwery': werytext,
                'ruta': 'cbocomb'
            }
                
            return dataobj
'''



















