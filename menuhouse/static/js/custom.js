let autoComplete;

$(document).ready(function() {
    $('.add_to_cart').on('click',function(e) {
        e.preventDefault();
        
        food_id = $(this).attr('data-id');
        url = $(this).attr('data-url');
        data = {
            food_id:food_id,
        }
        $.ajax({
            type : 'GET',
            url : url,
            data : data,
            success : function(response) {  
                console.log(response)
                $('#cart_counter').html(response.cart_counter['cart_count']);
                $('#qty-'+food_id).html(response.qty);
            }
        })
    })

    // place the cart item quantity on load
$('.item_qty').each(function(){
    let the_id = $(this).attr('id')
    let qty = $(this).attr('data-qty')
    $('#'+the_id).html(qty)
})

});


$(document).ready(function() {
    $('.decrease_cart').on('click',function(e) {
        e.preventDefault();
        
        food_id = $(this).attr('data-id');
        url = $(this).attr('data-url');
        data = {
            food_id:food_id,
        }
        $.ajax({
            type: 'GET',
            url: url,
            success: function(response){
                console.log(response)
                if(response.status == 'login_required'){
                    swal(response.message, '', 'info').then(function(){
                        window.location = '/login';
                    })
                }else if(response.status == 'Failed'){
                    swal(response.message, '', 'error')
                }else{
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    $('#qty-'+food_id).html(response.qty);
                }
            }
        })
    })
});
