$('.addtocartbtn').click(function (e) { 
    e.preventDefault();

    var product_id = $(this).closest('.product_data').find('.prod_id').val();
    var product_qty = $(this).closest('.product_data').find('.qty-input').val();
    var token = $('input[name=csrfmiddlewaretoken]').val();

    $.ajax({
        type: "POST",
        url: "mycart",
        data: {
            'product_id':product_id,
            'product_qty':product_qty,
            csrfmiddlewaretoken:token



        },
        dataType: "dataType",
        success: function (response) {
            console.log(response)
            alertify.success(response.status)
        }
    });
    
});
