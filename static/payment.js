$(document).ready(function() {
    $('.payWithRazorpay').click(function (e) { 
        e.preventDefault();
        var amount = $("[name='amount']").val();
        var cart = $("[name='cart']").val();
        var address = $("[name='address']").val();
        var payment = "Razorpay"
        var token = $("input[name='csrfmiddlewaretoken']").val()
        
        $.ajax({
            type: "GET",
            url: "razorpay",
            success: function (response) {
                console.log(response);
                var options={
                    "key": "rzp_test_rVlBh4uxr1y4Nd", // Enter the Key ID generated from the Dashboard
                    "amount": 1*100,//response.total, // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
                    "currency": "INR",
                    "name": "cart",
                    "description": "Thank you for shopping with us",
                    "image": "https://example.com/your_logo",
                    // "order_id": response.id, //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
                    "handler": function (response){
                        // alert(response.razorpay_payment_id);
                        data = {
                            "razorpay_payment_id": response.razorpay_payment_id,
                            "amount" : amount,
                            "cart" : cart,
                            "address" : address,
                            "payment" : payment,
                            csrfmiddlewaretoken: token
                        }
                        $.ajax({
                            type: "POST",
                            url: "payment",
                            data: data,
                            success: function (responsec) {
                                swal("Congratulations!", responsec.status, "success").then((value) => {
                                    window.location.href = "myorder"
                                });
                            }
                        });
                    },
                    "prefill": {
                        "name": "Gaurav Kumar",
                        "email": "",
                        "contact": "9999999999",
                    },
                    "notes": {
                        "address": "Razorpay Corporate Office"
                    },
                    "theme": {
                        "color": "#3399cc"
                    },
                };
                var rzp1 = new Razorpay(options);
                rzp1.open();
            }
        });
    });
});