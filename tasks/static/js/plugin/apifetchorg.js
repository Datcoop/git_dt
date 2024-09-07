
// get the CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {

        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));

                break;
            }

        }
    }
    return cookieValue;

} 

const csrftoken = getCookie('csrftoken');
 
let selected = [];

function llenarfld(frm,url){
    
    //alert(url);
    //apps/password/vertext/
    let arrruta = url.split("/");
    //alert("arrruta="+arrruta[0]+", "+arrruta[1]+", "+arrruta[2]+", "+arrruta[3]);
    //arrruta=frmsignin, tasks, password, vertext 
    //arrruta=, tasks, text, vertext frm+'/'+page+'/'+idpsw+'/vertext/'+div_eye
    let ruta = arrruta[3];
    document.getElementById("ruta").value = ruta;
    
    let form = new FormData(document.getElementById(frm));
    
    fetch(url, {
        method: "POST",

        body: form,
        headers: {        
            "X-CSRFToken": getCookie('csrftoken'),

        }
        
    }).then(
        function( response ) {
            return response.json();
        }
    ).then(
        function(res) {
        
            console.log(res);
            
            let ruta = res.data["ruta"];
            
            document.getElementById('ruta').value = ruta;
            
            if (ruta == "listado_autor") {

                document.getElementById("ruta").value = "listado_autor"; 
                
                let divres = document.getElementById('idvo').value;

                
                let array_autores = res.data["data"];
                var div = document.getElementById(divres);
                div.innerHTML = array_autores;


                let paginacion = res.data["pagedat"];
            
                var divpage = document.getElementById("paginas");
                divpage.innerHTML = paginacion;

/*
                let column = document.getElementById("column");
                var selectcolumn = res.data["column"];
                column.innerHTML = selectcolumn;
*/
                let subnav3 = document.getElementById("subnav3");
                var selectsubnav3 = res.data["column"];
                subnav3.innerHTML = selectsubnav3;
            
                let subnav31 = document.getElementById("SwitchCheck");
                var selectsubnav31 = res.data["columnswitch"];
                subnav31.innerHTML = selectsubnav31;

                document.getElementById("columnswitch").value = res.data["columnswitch"];

                document.getElementById("arrcolSwitch").value = res.data["arrcolSwitch"];

                let mostrando = document.getElementById("mostrar");
                mostrando.innerHTML = res.proyectos["limite"];

                document.getElementById("numpags").value = res.data["numpags"];


                let pagant = res.data["indice"];
        
                document.getElementById('pagant').value = pagant;

                let orderby = res.data["orderby"];
        
                document.getElementById('orderby').value = orderby;


                let direc = res.data["direc"];
        
                document.getElementById('direc').value = direc;


                let cmdtext = res.data["cmdtext"];
        
                document.getElementById('cmdtext').value = cmdtext;

                let iglike = res.data["iglike"];
        
                document.getElementById('iglike').value = iglike;

                let arrwer = res.data["arrwer"];
                
                document.getElementById("arrwer").value = arrwer;

                let numCheck = res.data["numCheck"];
                
                document.getElementById("numCheck").value = numCheck;

                let crearcolumnswitch = res.data["crearcolumnswitch"];
                
                document.getElementById("crearcolumnswitch").value = crearcolumnswitch;
                
            } else if (ruta == "select_col") {
                
                let colopt = document.getElementById("subnav3content1");

                var selectopt = res.data["tuplas"];
                colopt.innerHTML = selectopt;
                
                document.getElementById("numoper").value = res.data["numoper"]; 
                
                document.getElementById("inxopt0").value = res.data["inxopt0"];  
                
                document.getElementById("arrnumtbl").value = res.data["arrnumtbl"];             

            } else if (ruta == "ir_datos") {  

                let subnav3contentres = document.getElementById("subnav3contentres");
                var selectoptsi = res.data["boxes"];
                subnav3contentres.innerHTML = selectoptsi;    
                
                document.getElementById("arrwery").value = res.data["arrwery"];             
                
            } else if (ruta == "in_datinp") {         

                let orderby = res.data["orderby"];
        
                document.getElementById("orderby") = orderby;     
                
            } else if (ruta == "bus_filtrar") {
    
        //arrchk = ['Filtro inicial', 'Mayor o igual a', 'Menor o igual a']  

                let orderby = res.data["orderby"];
                
                document.getElementById('orderby').value = orderby;

                let arrcolSwitch = res.data["arrcolSwitch"];
        
                document.getElementById("arrcolSwitch").value = arrcolSwitch;  

                let arrwer = res.data["arrwer"];
        
                document.getElementById("arrwer").value = arrwer;                   

                let arrwery = res.data["arrwery"]; 
        
                document.getElementById("arrwery").value = arrwery;  
    
                ruta = 'listado_autor';
                
                num = document.getElementById("numero").value;
                
                llenarfld('frmparam','/'+num+'/coop/'+ruta+'/');
                
            } else if (ruta == "inxpagina") {

                document.getElementById('indice').value = res.data["indice"]; 
    
                ruta = 'listado_autor';
                
                num = document.getElementById("numero").value;
                
                llenarfld('frmparam','/'+num+'/coop/'+ruta+'/');
                
            } else if (ruta == "ordenar") {

                var idsel = res.data["idsel"];  
            
                let idselvoid = document.getElementById(idsel);
                var titcol = res.data["titascdesc"];
                idselvoid.innerHTML = titcol;      
                
                document.getElementById("direc").value = res.data["direc"];      
                
                document.getElementById("critsearch").value = res.data["direc"];
                
                num = res.data["numero"];
                
                llenarfld('frmparam','/'+num+'/coop/listado_autor/');
            
            } else if (ruta == "recargar") {
            
                let arrdtbl = res.data["valini"];
                
                for (var dtbl in arrdtbl){
                    document.getElementById(dtbl).value = arrdtbl[dtbl];
                }
                
                llenarfld('frmparam','/'+num+'/coop/listado_autor/');
            
            } else if (ruta == "select_opt1") {
            
                let idselopt = document.getElementById(res.data["numopt"]);
                
                for (const valor of res.data["tuplas"]) {
                    let option = document.createElement("option");
                    option.text = valor;
                    idselopt.add(option);
                }

                document.getElementById("inxopt").value = res.data["inxopt"];
                
            } else if (ruta == "addact") {
                
                var accion = res.data["accion"];
                
                if ( accion == 'regadd' ) {
                    y = 2;
                } else if ( accion == 'regact' ) {

                    let formulario = document.getElementById("resform");
                    var selectform = res.data["formulario"];
                    formulario.innerHTML = selectform;
                
                }
                /*
                let selchk = res.data["selected"];
                /document.getElementById("ruta").value = "listado_autor";
                const lenselchk = selchk.length;
                
                for (let i = 0; i < lenselchk; i++) {
                    selected.push(selchk[i]);
                }
                */
                
            } else if (ruta == "cbocomb") {
                
                let titbtn = res.data["titbtn"];
                let spantit = document.getElementById(titbtn);
                var titopt = res.data["titulo"];
                spantit.innerHTML = titopt;      
                
                let tipcbo = res.data["tipcbo"];       

                document.getElementById("codnew").value = res.data["codnew"]; 
                
                if (tipcbo == 'lastcbo') {
                
                    document.getElementById("inxopt0").value = res.data["inxopt0"];  
                
                    document.getElementById("inxbus").value = res.data["inxbus"];    
                    
                    document.getElementById("orderby").value = res.data["orderby"];        

                    document.getElementById("arrwery").value = res.data["arrwery"]; 
                 
                    document.getElementById("numero").value = document.getElementById("numtblurl").value;
                    
                    var num = document.getElementById("numero").value;
                    
                    llenarfld('frmparam','/'+num+'/coop/listado_autor/');
                    
                } else {
                    let nomid = res.data["idsel"];
                    let divopciones = document.getElementById(nomid);
                    var selectopt = res.data["selfilanv"];
                    divopciones.innerHTML = selectopt;
                }                
                
            } else if (ruta == "fillauto") {
                
                let nomid = res.data["numsel"];
                let divopciones = document.getElementById(nomid);
                var selectopt = res.data["selfilanv"];
                divopciones.innerHTML = selectopt;
            
            } else if ( ruta == "savewer") {
            
                let arrfiltros = res.data["arrfiltrosswitch"];
                
                var strhtml = "";
                
                var selcheckfiltro = "selcheckfiltro";
                
                var num_tbl = document.getElementById("numero").value;
                
                let filtros = document.getElementById("Switchfiltros");
                var strhtml = res.data["strhtml"];
                filtros.innerHTML = strhtml;
                
                document.getElementById("arrwer").value = res.data["arrwer"];
                
                document.getElementById("filtrosswitch").value = res.data["filtrosswitch"];
                
                document.getElementById("orderby").value = '';
               
            } else if ( ruta == "selcheck") {
            
                document.getElementById("arrcolSwitch").value = res.data["arrcolSwitch"]; 
                              
            } else if ( ruta == "selcheckfiltro") {
            
                document.getElementById("arrcolSwitch").value = res.data["arrcolSwitch"];
               
            } else if ( ruta == "exportar") {
            
                let resexport = document.getElementById("resexport");
                var filexport = res.data["mensaje"];
                resexport.innerHTML = filexport;
               
            } else if ( ruta == "bus_global") {
    
                document.getElementById('critsearch').value = res.data["critsearch"];    

                document.getElementById("cons").value = res.data["cons"];

                llenarfld('frmparam','/'+num+'/coop/listado_autor/'); 
               
            } else if ( ruta == "pop_up") {
            
                var selcbo = res.data["selcbo"];
                let resselcbo = document.getElementById(selcbo);
                resselcbo.innerHTML = res.data["opciones"];
            
            } else if ( ruta == "col_u") {
            
                var idinp = res.data["idinp"];
                document.getElementById(idinp).value = res.data["codigo"];
            
            } else if ( ruta == "vertext") {            
                
                var frm = res.data["frm"];
                
                var nomdiv_eye = document.getElementById("nomdiv_eye").value; 
                
                var nomdiv_eye2 = document.getElementById(nomdiv_eye).value;
                
                let resspan = document.getElementById(nomdiv_eye2);
                var resdiv = res.data["span"];
                resspan.innerHTML = resdiv;
                
            } else if ( ruta == "genpassw") {
            
                document.getElementById("password1").value = res.data["valpassw"];
            
                document.getElementById("password2").value = res.data["valpassw"];
            
            }
    });

}

function cboemerg(numcol,nomid) {

    var num = document.getElementById("numero").value
    
    var valinp = document.getElementById(nomid).value
    
    document.getElementById('valinp').value = valinp;

    document.getElementById("inxopt").value = numcol;

    llenarfld('frmparam','/'+num+'/'+numcol+'/pop_up/');    

}

function nuevolimite() {

    document.getElementById("indice").value = "1";

    document.getElementById("move").value = "page";


    let limite = document.getElementById("limite")
    limite.value = document.getElementById("regxpag").value

    let num = document.getElementById("numero").value


    llenarfld('frmparam','/'+num+'/coop/listado_autor/');

}

function buspor(frm,idvo,url,idbus,cons) {

    document.getElementById("indice").value = "1";

    let elemcrit = document.getElementById(idbus);

    let val = elemcrit.value;
    
    document.getElementById('critsearch').value = val;  

    document.getElementById('idvo').value = idvo;

    llenarfld(frm,url);

}
            
function fnt_col_u(ruta,idsel,move,inbus) {

    var selectElemt = document.getElementById(idsel);

    selectElemt.addEventListener('change', () => {
    
        var index = selectElemt.selectedIndex;  
    
        let num = document.getElementById("numero").value;
          
        document.getElementById("numcbo").value = inbus;
            
        document.getElementById("fila").value = index;

        llenarfld('frmparam','/'+num+'/coop/col_u/');
        
    });
    
}

function fnt_subirarch(archivo) {
//aq

    document.getElementById("indice").value = "1";

    let elemcrit = document.getElementById(idbus);

    let val = elemcrit.value;
    
    document.getElementById('critsearch').value = val;  

    document.getElementById('idvo').value = idvo;

    llenarfld(frm,url);

}

function pgindex(frm,idvo,url,idel,indice,move) {

    //alert(frm+','+idvo+','+url+','+idel+','+indice+','+move);
    //frmparam,listado,/138/coop/listado_autor/,indice,1,Next

    let irpg = document.getElementById(idel);

    let val = irpg.value;

    document.getElementById("move").value = move;

    document.getElementById('indice').value = indice;

    document.getElementById("irpg").value = val;

    document.getElementById('idvo').value = idvo;

    llenarfld(frm,url);

}

function fntord(num,numcol,idth,titcol,numcolbus) {

    let inxord = document.getElementById("inxord");

    inxord.value = numcol;  

    let titulocol = document.getElementById("titulocol");

    titulocol.value = titcol; 

    let idsel = document.getElementById("idsel");

    idsel.value = idth;  
    
    llenarfld('frmparam','/'+num+'/coop/ordenar/');

}

function fnt_recar() {
    num = document.getElementById("numero").value;
            
    var divfiltros = document.getElementById("Switchfiltros");
    divfiltros.innerHTML = "";
    
    var divpage = document.getElementById("subnav3content1");
    divpage.innerHTML = "";
            
    llenarfld('frmparam','/'+num+'/coop/recargar/');
}

function bnt_click(ruta,num,move) {

    document.getElementById("move").value = move;
    
    llenarfld('frmparam','/'+num+'/coop/'+ruta+'/');
    
}

function fnt_colCheck() {
    
    document.getElementById("stateCheck").value = document.getElementById("colCheck").checked;

}

function select(ruta,idsel,move,inbus) {
    //alert("ruta="+ruta+", idsel="+idsel+", move="+move+", inbus="+inbus);
    document.getElementById("move").value = move;

    const selectElem = document.getElementById(idsel);

    const pElem = document.getElementById('inxbus');

    const pElemavan = document.getElementById('inxavan');
    
    document.getElementById("ruta").value = ruta;
    
    document.getElementById("idsel").value = idsel;

    selectElem.addEventListener('change', () => {


        let num = document.getElementById("numero").value;
    
        if ( move == "colinx" ) {    
    
            var arrruta = ruta.split("/");
            
            ruta = arrruta[0];
            
            var divpage = document.getElementById("subnav3content1");
            divpage.innerHTML = "";
                
            document.getElementById("numcbo").value = 1;

            const index = selectElem.selectedIndex;
            
            pElemavan.value = index;
            
            pElem.value = index;
            
            document.getElementById("inxopt0").value = index;
            
            document.getElementById("inxopt").value = index;

            llenarfld('frmparam','/'+num+'/coop/'+ruta+'/');
            
        } else if ( move == "opttexto") {   
    
            var arrruta = ruta.split("/");
            
            ruta = arrruta[0];
            
            const index = selectElem.selectedIndex;
       
            pElemavan.value = index;
            
            document.getElementById("inxopt").value = index;
            
            let subnav3 = document.getElementById("subnav3contentres");
            var selectsubnav3 = "";
            subnav3.innerHTML = selectsubnav3;  
            
            llenarfld('frmparam','/'+num+'/coop/'+ruta+'/');
            
        } else if ( move == "colinxavan") { 
       
            pElem.value = inbus;

            const index = selectElem.selectedIndex;
       
            pElemavan.value = index;

            
            if (idsel == 'col_avanUno') {
                ruta = 'listado_autor';

            }
            

            llenarfld('frmparam','/'+num+'/coop/'+ruta+'/');
            
        } else if ( move == "col_si") {
            
            document.getElementById("numcbo").value = inbus;

            const index = selectElem.selectedIndex;
       
            pElemavan.value = index;
            
            document.getElementById("fila").value = index;

            llenarfld('frmparam','/'+num+'/coop/col_u/');
            
        } else if ( move == "move_u") { 
    
            var arrruta = ruta.split("/");
            
            document.getElementById("ruta").value = arrruta[0];
            
            ruta = arrruta[0];

       
            pElem.value = inbus;

            const index = selectElem.selectedIndex;
       
            pElemavan.value = index;
            
            if (idsel == 'id_u') {
                ruta = 'listado_autor';
            }
            
            llenarfld('frmparam','/'+num+'/coop/'+ruta+'/');
            
        } else if ( move == "move_v") { 
    
            var arrruta = ruta.split("/");
            
            let len = arrruta.length;
            
            //alert("len="+len);//select_v/2/1
            
            ruta = arrruta[0];
        
            pElem.value = inbus;

            const index = selectElem.selectedIndex;
       
            pElemavan.value = index;
            
            if ( len > 1 ) {
            
                document.getElementById("numcbo").value = arrruta[2];
                
                llenarfld('frmparam','/'+num+'/coop/'+ruta+'/');

            
            }
            
        } else if ( move == "opt_cbo") { 
    
            var arrruta = ruta.split("/");

            document.getElementById("numcbo").value = arrruta[2];
            
            document.getElementById("ruta").value = arrruta[0];

            document.getElementById("cons").value = 5;
       
            pElem.value = inbus;

            const index = selectElem.selectedIndex;
       
            pElemavan.value = index;
            
            llenarfld('frmparam','/'+num+'/coop/'+ruta+'/');
            
        }

    });
}

function fnt_click(nomid,num) {

    let strnomid = "xx#"+nomid;

    let ruta = strnomid.split("#")[2];
    
    document.getElementById("ruta").value = ruta;

    document.getElementById("cons").value = 5;
    
    let y = document.getElementById("colCheck");
    
    document.getElementById("inpCheck").value = y.checked; 
    

    llenarfld('frmparam','/'+num+'/coop/'+ruta+'/');    

}

function fnt_changeuno(nomid) {
    
    if (nomid == "inpizq") {     

        document.getElementById("boxizq").value = document.getElementById(nomid).value;
        
    } else {    

        document.getElementById("boxder").value = document.getElementById(nomid).value;
        
    }
       
}

function fnt_changecheck(ruta,num,nomid) {

    if (ruta == "selcheck") {

        var colcheck_names = document.getElementsByName("colcheck"),tab = '', index;
        
        var sep = ", ";
        
        for(var i = 0; i < colcheck_names.length; i++){
            
            if (colcheck_names[i].checked) {
                tab = tab+i+sep;
            }
            
        }
        tab = tab+",";
        tab = tab.replace(", ,","");
    
        document.getElementById("arrcolSwitch").value = tab; 
    
        document.getElementById("numcolswitch").value = tab; 
        
    } else if (ruta == "selcheckfiltro") {

        var filtros_names = document.getElementsByName("filtro"),tab = '', index;
        
        var sep = ",";
        
        for(var i = 0; i < filtros_names.length; i++){
            
            if (i == parseInt(filtros_names.length) - 1) {
                sep = ""
            }  
            
            if (filtros_names[i].checked) {
                tab = tab+1+sep;
            } else {
                tab = tab+0+sep;
            }
        }
        
        console.log(tab);     

        document.getElementById("numCheck").value = tab; 
    
        llenarfld('frmparam','/'+num+'/coop/'+ruta+'/');
    } 
}

function orgper(nomid) {
    
    let valinput = document.getElementById("lblentrar");
    valinput.value = nomid;
    
    //llenarfld('frmentrar','/130/coop/auten/'+nomid);
       
}

function mospsw(tippsw, page, frm, div_eye, idpsw) {

    document.getElementById("nomdiv_eye").value = div_eye;
    
    llenarfld(frm,'/'+page+'/'+idpsw+'.'+tippsw+'/vertext/'+frm+'.'+div_eye);
    
} 

function passwordgen(page,frm,div_eye) {

    document.getElementById("nomdiv_eye").value = div_eye;

    llenarfld(frm,'/'+page+'/idpsw/genpassw/');
    
} 

function llenartip(tipuser) {

    document.getElementById("tipuser").value = tipuser;
}

function chkmul(namsel,namform) {

    let xcon = '#'+namsel;
    
    const x = document.querySelector(xcon);
    
    let posi = selected.indexOf(namsel);
    

    if (x.checked == true) {
        if ( posi == -1 ) {
            selected.push(namsel);
        }
    } else {
        var removed = selected.splice(posi, 1);
    }
    
    alert("selected="+selected);

    
}

function clickbtn(ruta,accion,idfila) {
    
    let num = document.getElementById("numero").value;
    
    document.getElementById("accion").value = accion;
    
    document.getElementById("fila").value = idfila;
    
    llenarfld('frmparam','/'+idfila+'/'+num+'/coop/'+ruta+'/');
    
}

function autocomplete_click(ruta,num) {

    document.getElementById("numero").value = num;
    
    if ( ruta == 'vacio') {
        
        ruta = 'fillauto';
    
        llenarfld('frmparam','/'+num+'/coop/'+ruta+'/');
        
    }
    
}

function autocompleteu_li(ruta,num) {

    document.getElementById("numero").value = num;
    
    llenarfld('frmparam','/'+num+'/coop/'+ruta+'/');
    
}

function clickulcbo(idbtnsel,num,zoof,numcbo) {
    
    document.getElementById("numcbo").value = numcbo;
    
    document.getElementById("idsel").value = zoof;
    
    document.getElementById("numtblcbo").value = num;

    var items = document.querySelectorAll(idbtnsel),tab = [], index;
        
        // add values to the array
    for(var i = 0; i < items.length; i++){
       tab.push(items[i].innerHTML);
    }
        
        // get selected element index
    for(var i = 0; i < items.length; i++)
    {    
        
        items[i].onclick = function(){
               
            index = tab.indexOf(this.innerHTML);
            
            if ( index == 0) {
                
                var content = this.innerHTML;
                nomid = "u_li"+num;
                let u_li = document.getElementById(nomid);
                var selectopt = '<input list="aut'+num+'" id="list-'+num+'" onclick="autocompleteu_li("fillcboant",'+num+')" placeholder="Buscar por nombre"><datalist id="aut'+num+'"></datalist>';
                console.log(selectopt);
                u_li.innerHTML = selectopt;
            
            } else {
                console.log(this.innerHTML + " Index = " + index);
    
                document.getElementById("inxopt").value = index;
    
                document.getElementById("cmdtext").value = this.innerHTML;
            
                llenarfld('frmparam','/'+num+'/coop/cbocomb/');
            }
        };
    }
    
}

function changeform(idsel) {
  alert("You must fill out the form!");
}

function valkey(tipo) {
    
    if (tipo == '2') {
        alert("You pressed a key inside the input field");
    }
}

function exportTableTo(ruta, nomid, nomfile, num) {

    document.getElementById("ruta").value = ruta;

    document.getElementById("idsel").value = nomid;

    document.getElementById("nomfile").value = nomfile;
    
    llenarfld('frmparam','/'+num+'/coop/'+ruta+'/');

}

function fntord1(ascdesc,frm,x,url,move) {

    //alert(x.cellIndex);
    const table = document.querySelector('table');

    const rows = document.querySelectorAll('tr');


    const rowsArray = Array.from(rows);

    table.addEventListener('click', (event) => {

        const rowIndex = rowsArray.findIndex(row => row.contains(event.target));
        const columns = Array.from(rowsArray[rowIndex].querySelectorAll('th'));
        const columnIndex = columns.findIndex(column => column == event.target);
        console.log(rowIndex,columnIndex);
        let direc = document.getElementById("direc");
        direc.value = ascdesc+"-"+columnIndex;
    });
    
    document.getElementById("move").value = move;

    llenarfld(frm,url);

}


























































