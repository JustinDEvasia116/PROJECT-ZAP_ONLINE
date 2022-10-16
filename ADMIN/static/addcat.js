var catnameError = document.getElementById("catname-error")
var uploadError = document.getElementById("image-error")
var submiterror = document.getElementById("submit-error")

function validateCatname() {
    var catname = document.getElementById('catname').value.trim();

    if( (catname.length == 0)  ){
        catnameError.innerHTML = 'Category name is required';
        return false
       }

  else{
    catnameError.innerHTML = '<i class="fa-solid fa-check"></i>';
    return true;
  }
   
    
}

function validateFile(){
    var inp = document.getElementById('upload');
    if(inp.files.length === 0){
        uploadError.innerHTML = 'image file is required';
        inp.focus();

        return false;
        }

  else{
        uploadError.innerHTML = '<i class="fa-solid fa-check"></i>';
        return true;
      }
}
function validateform(){
    validateCatname()
    validateFile()
    
    
    if(!validateCatname() || !validateFile() ){
        
        {
            return false;
        }
      
    
     }  

}
