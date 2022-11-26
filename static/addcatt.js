var catnameError = document.getElementById("catname-error")
var submiterror = document.getElementById("submit-error")

function validateCatname() {
    var catname = document.getElementById('catname').value.trim();

    if( (catname.length == 0)  ){
        catnameError.innerHTML = 'Category name is required';
        return false
       }

    else{
        catnameError.innerHTML = '<i class="fa-solid fa-check"></i>';
        return True;
    }
   
}


function validateform(){
    validateCatname()
    if (validateCatname) {

        catnameError.innerHTML = 'All fields required';
        return false;
        
    }

    
   
      
}
