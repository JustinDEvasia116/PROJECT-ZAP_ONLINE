var fnameError = document.getElementById("fname-error")
var lnameError = document.getElementById("lname-error") 
var emailError = document.getElementById("email-error")
var unameError = document.getElementById("uname-error")
var submiterror = document.getElementById("submit-error")
var passwordError = document.getElementById("password-error");






function validatefname() {
    var fname = document.getElementById('fname').value.trim();

    if( (fname.length == 0)  ){
        fnameError.innerHTML = 'Name is Required';
       }

  else{
    fnameError.innerHTML = '<i class="fa-solid fa-check"></i>';
    return true;
  }
   
    
}

function validatelname() {
    var lname = document.getElementById('lname').value.trim();

    if( (lname.length == 0)  ){
        lnameError.innerHTML = 'Name is Required';
       }

  else{
    lnameError.innerHTML = '<i class="fa-solid fa-check"></i>';
    return true;
  }
   
    
}


function validateEmail() {
    var email = document.getElementById("email").value;
    if (email.length == 0) {
        emailError.innerHTML = "Email is required";
        return false;
    }
    if(!email.match(/^[A-Za-z\._\-[0-9]*[@][A-Za-z]*[\.][a-z]{2,4}$/)){
        emailError.innerHTML = "Invalid Email"


    }

    else {
        emailError.innerHTML = '<i class="fa-solid fa-check"></i>';
        return true;
    }



}
function validateform(){
    validatefname()
    validatelname()
    validateEmail()
    validateUname()
    validatePassword()

    if(!validatefname() || !validatelname() || !validateEmail() ||  !validateUname()){
        
        {

            submiterror.innerHTML = "fields can't be blank"
            return false;
        }
      
    
     }  
}
function validateUname() {
    var uname = document.getElementById('uname').value.trim();

    if( (uname.length == 0)  ){
        unameError.innerHTML = 'Username is Required';
       }

  else{
    unameError.innerHTML = '<i class="fa-solid fa-check"></i>';
    return true;
  }
   
    
}

function validatePassword(){
    var password = document.getElementById("password").value;
    var required = 5;
    var left = required - password.length;
    if(left>0){
        passwordError.innerHTML = left +' more character required';
        return false
    }
    else {
        passwordError.innerHTML ='<i class="fa-solid fa-check"></i>' ;
        return true;
    }


 }


