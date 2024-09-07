
function nument(evt){
	
	var code = (evt.which) ? evt.which : evt.keyCode;
			
	if(code==8) { 
	    return true;
	} else if(code>=48 && code<=57) { 
		return true;
	} else { 
		return false;
	}
}

let resto = 0;

function numdbl(evt){
    
    let code = (evt.which) ? evt.which : evt.keyCode;
		
	if(code==8) { 
	    return true;
	} else if(code>=48 && code<=57) { 
		return true;
	} else if(code==190) { 
	    resto = parseFloat(valfld) - parseInt(valfld);	    
	    if ( resto > 0 ) {
		    return false;
	    } else {
		    return true;
		}
	} else { 
		return false;
	}
}
//https://uxsolutions.github.io/bootstrap-datepicker/?markup=input&format=&weekStart=&startDate=&endDate=&startView=0&minViewMode=0&maxViewMode=4&todayBtn=false&clearBtn=false&language=en&orientation=auto&multidate=&multidateSeparator=&keyboardNavigation=on&forceParse=on#sandbox
function numdate(evt){
    return false;    
}
