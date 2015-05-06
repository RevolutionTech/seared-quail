$(document).ready(function() {
    'use strict'

    function check_order_button_status () {
        var order_button = $( '.button.placeorder' );
        if (order_button.disabled) return;

        var disable = true;
        $( '.quantity' ).each(function() {
            var quantity = parseInt($(this).html());
            if (quantity > 0){
                order_button.removeAttr("disabled");
                disable = false;
                return;
            }
        })
        if (disable) order_button.attr("disabled", true);
    };

    // Adjust quantity on -/+ Buttons
    $( '.button.plus' ).click(function() {
        var quantity = parseInt($( '#' + this.id + '.quantity' ).html());
        quantity += 1;
        $( '#' + this.id + '.quantity' ).html(quantity);
        $( '.button.placeorder' ).removeAttr("disabled"); // order button should not be disabled anymore
    });
    $( '.button.minus' ).click(function() {
        var quantity = parseInt($( '#' + this.id + '.quantity' ).html());
        if ( quantity > 0 ){
            quantity -= 1;
        }
        $( '#' + this.id + '.quantity' ).html(quantity);
        if (quantity == 0) check_order_button_status(); // might need to disable order button
    });

    // Confirm order on Place Order button press
    $( '.button.placeorder' ).click(function() {
        // Determine the order being placed
        var order = [];
        $( '.quantity' ).each(function() {
            var quantity = parseInt($(this).html());
            if (quantity > 0){
                var name = $( '#' + this.id + '.name' ).html();
                var ordermenuitem = {
                    id: this.id,
                    name: name,
                    quantity: quantity,
                };
                order.push(ordermenuitem);
            }
        })

        // Request confirmation
        var ordertext = "Place this order?\n";
        jQuery.each(order, function() {
            ordertext += this.quantity + " " + this.name + "\n";
        })
        var r = confirm(ordertext);
        if (r == true){
            // Place Order
            // ...
            console.log("Order placed.");
        }
    });
});
