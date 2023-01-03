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

                    // subtotal, tax and grand total
                    applyCartAmount(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax'],
                        response.cart_amount['grand_total']
                    )
                }
            }
        })
    })

    // place the cart item quantity on load
$('.item_qty').each(function(){
    let the_id = $(this).attr('id')
    let qty = $(this).attr('data-qty')
    $('#'+the_id).html(qty)
})


    $('.decrease_cart').on('click',function(e) {
        e.preventDefault();
        
        food_id = $(this).attr('data-id');
        url = $(this).attr('data-url');
        item_id = $(this).attr('id');
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
                    if(window.location.pathname == '/cart/'){
                    applyCartAmount(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax'],
                        response.cart_amount['grand_total']
                        )
                    delete_cart(response.qty, item_id);
                    checkempty();
                }
            }
        }
    })
    })


    $('.delete_cart').on('click',function(e) {
        e.preventDefault();
        
        cart_id = $(this).attr('data-id');
        url = $(this).attr('data-url');

        $.ajax({
            type: 'GET',
            url: url,
            success: function(response){
                console.log(response)
            
                if(response.status == 'Failed'){
                    swal(response.message, '', 'error')
                }else{
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    swal(response.status, response.message, 'success')
                    applyCartAmount(
                            response.cart_amount['subtotal'],
                            response.cart_amount['tax'],
                            response.cart_amount['grand_total']
                    )
                    delete_cart(0, cart_id);
                    checkempty();
                }
            }
        })
    })

    function delete_cart(cartItem, cart_id){
        if (cartItem <= 0){
            document.getElementById("cart-item-"+cart_id).remove()

        }

    }
    function applyCartAmount(subtotal, tax, grand_total){
        if(window.location.pathname == '/cart/'){
            $("#subtotal").html(subtotal)
            $("#tax").html(tax)
            $("#total").html(grand_total)
        }
    }
    function checkempty(){
        cart_counter = document.getElementById("cart_counter").innerHTML
        if(cart_counter == 0){
            document.getElementById("empty-cart").style.display = "block"

        }
    }
});
