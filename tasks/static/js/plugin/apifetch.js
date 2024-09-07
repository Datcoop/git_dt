
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

function llenarfld(url, frm, prm){
    //alert(url, frm, prm);
    document.getElementById("param").value = prm;
     
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
            
            if (res.data['ruta'] == '1') {
                
                document.getElementById("argprm").value = res.data['argprm'];            
                document.getElementById("pagant").value = res.data['pagant'];            
                document.getElementById("numpags").value = res.data['numpags'];            
                document.getElementById("paramfil").value = res.data['paramfil'];           
                document.getElementById("ordpage").value = res.data['ordpage'];          
                document.getElementById("valwhere").value = res.data['valwhere']; 
            
                let div = document.getElementById('listado');
                div.innerHTML = res.data['tabla'];

                var divpage = document.getElementById("paginas");
                divpage.innerHTML = res.data["pagedat"];
                
            } else if (res.data['ruta'] == '2') {
            
                var divRes = res.data['divRes'];
                let div = document.getElementById(divRes);
                div.innerHTML = res.data['resRes'];
                
            } else if (res.data['ruta'] == '3') {
            
                let divbox = document.getElementById("resinpbox");
            
                divbox.innerHTML = res.data['textbox'];   
                       
                document.getElementById("fldbus").value = res.data['fldbus']; 
                
            } else if (res.data['ruta'] == '4') {
            
                document.getElementById("arrwer").value = res.data['arrwer'];        
                document.getElementById("valwhere").value = res.data['arrwer']; 
                document.getElementById("boxizq1").value = "";
                document.getElementById("boxder1").value = "";
            
                let divbox = document.getElementById("addfil");
            
                divbox.innerHTML = res.data['addfil'];
                
            } else if (res.data['ruta'] == '5') {
            
                document.getElementById("listfil").value = res.data['listfil'];
                
            } else if (res.data['ruta'] == '7') {
            
                let div = document.getElementById("tasacambio");
                div.innerHTML = res.data['tasacambio'];
            
                let divvalhasta = document.getElementById("valhasta");
                divvalhasta.innerHTML = res.data['valhasta'];
                
            } else if (res.data['ruta'] == '8') {
                        
                let div = document.getElementById("divedit");
                div.innerHTML = '';
                div.innerHTML = res.data['inpbox'];
                
            } else if (res.data['ruta'] == '9') {
                        
                let div = document.getElementById("divedit");
                div.innerHTML = '';
                        
                let divmsg = document.getElementById("msg");
                divmsg.innerHTML = res.data['msg'];
            
                //set_background(res.data['fila'],res.data['upreg']);
                
            } else if (res.data['ruta'] == 'eye') {
                
                var idpw = res.data['idpw']
                        
                let pwdiv = document.getElementById(idpw);
                pwdiv.innerHTML = "";
                pwdiv.innerHTML = res.data['pwinp'];
                
                var idfaeye = res.data['idfaeye']
                        
                let div = document.getElementById(idfaeye);
                div.innerHTML = res.data['eyeslash'];
                
            } else if (res.data['ruta'] == 'chgk') {
                        
                let div = document.getElementById("idresult");
                div.innerHTML = res.data['msg'];
                
            } 
            
        }
    );
};

function set_background(fila,upreg) {
  // get a list of all the body elements (there will only be one),
  // and then select the zeroth (or first) such element
  myBody = document.getElementsByTagName("body")[0];

  // now, get all the p elements that are descendants of the body
  myBodyElements = myBody.getElementsByTagName("tr");

  // get the second item of the list of p elements
  mytr = myBodyElements[fila];
  mytr.style.background = "#9ee394";
  
  celda = mytr.getElementsByTagName("td");
  
  const array1 = upreg;
  var i = 2;
  for (const element of array1) {
      celda[i].innerHTML = element;
      i++;
  }
}

function filinp(inp, valinp) {
    document.getElementById(inp).value = valinp;
}

function fillbox(inp, inp1) {
    document.getElementById(inp1).value = document.getElementById(inp).value;
}

function filchk(inpfrm, inp, url, frm, prm) { 

    var allElements = document.getElementsByName(inp);

    var mResult = [];

    allElements.forEach((v) => {
        mResult.push(v.checked);
    });

    document.getElementById(inpfrm).value = mResult;
    
    llenarfld(url, frm, prm);
    
    console.log(document.getElementById(inpfrm).value);
}

function validateNumber(event) {
    var key = window.event ? event.keyCode : event.which;
    if (event.keyCode === 8 || event.keyCode === 46) {
        return true;
    } else if ( key < 48 || key > 57 ) {
        return false;
    } else {
        return true;
    }
};
// Add event listener to the button element


