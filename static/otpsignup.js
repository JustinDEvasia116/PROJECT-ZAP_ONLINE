var otpError = document.getElementById("otp-error")
var submiterror = document.getElementById("submit-error")

function validateotp(){
    var otp = document.getElementById('otp').value.trim();
     
    if(otp.length == 0){
        otpError.innerHTML = 'OTP is Required'
        return false;
    }
    else{
        return true;
    }

}



function validateform(){
    validateotp()
 
    
    if(!validateotp() ){
        
        {
            return false;
        }
      
    
     }  

}