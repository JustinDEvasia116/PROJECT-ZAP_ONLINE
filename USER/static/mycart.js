$('.addtocartbtn').click(function (e) { 
    e.preventDefault();

    var product_id = $(this).closest('.product_data').find('.prod_id').val();
    var product_qty = $(this).closest('.product_data').find('.qty-input').val();
    var total = $(this).closest('.price_data').find('.total').val();
    
    var token = $('input[name=csrfmiddlewaretoken]').val();

    $.ajax({
        type: "POST",
        url: "mycart",
        data: {
            'total':total,
            'product_id':product_id,
            'product_qty':product_qty,
            csrfmiddlewaretoken:token
            },
        
        success: function (response) {
            location.reload();
            // alert("success")
            // console.log(response)
            // alertify.success(response.status)
            
        },
        error: function(err) {
            console.log(err.responseText);   // <-- printing error message to console
        }
    });


    
});


