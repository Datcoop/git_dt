
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

function llenarfld(url, frm){
    //alert(document.getElementById("ruta").value);
    
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
                
            };         
        }
    );
};

const uploadButton = document.getElementById("uploadButton");
uploadButton.addEventListener("click", uploadFiles);

function uploadFiles(event) {
  event.preventDefault();
  const fileInput = document.getElementById("fileInput");
  const selectedFiles = fileInput.files;
  // Check if any files are selected
  if (selectedFiles.length === 0) {
    alert("Please select at least one file to upload.");
    return;
  }
}

function uploadFiles() {
  // ...
  // Create a FormData object to store the form data
  const formData = new FormData();
  // Append each selected file to the FormData object
  for (let i = 0; i < selectedFiles.length; i++) {
    formData.append("files[]", selectedFiles[i]);
  }
  
  for (const pair of formData.entries()) {
    console.log(
      pair[0],
      pair[1].name + ", " + pair[1].size + ", " + pair[1].type + ", " + pair[1].lastModifiedDate
    );
  }

  
}

const xhr = new XMLHttpRequest();
xhr.open("POST", "/uploadFiles", true);
xhr.onreadystatechange = function () {
  if (xhr.readyState === XMLHttpRequest.DONE) {
    if (xhr.status === 200) {
       // Handle successful response from the server
      console.log('Files uploaded successfully!');
      alert("Files uploaded successfully!");
    } else {
       // Handle error response from the server
      console.error('Failed to upload files.');
     alert("Error occurred during file upload. Please try again.");
    }
  }
};
xhr.send(formData);


