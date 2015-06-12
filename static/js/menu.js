$(document).ready(function() {
    'use strict'

    // Order button should be enabled iff:
    // 1) Table is selected
    // 2) One or more menu items has quantity > 0
    function update_order_button_status () {
        var order_button = $( '.button.placeorder' );

        // A table must be selected
        var table_id = $( '.table' ).val();
        if (table_id == 0){
            order_button.attr("disabled", true);
            return;
        }

        // One or more menu items has quantity > 0
        var disable = true;
        $( '.quantity' ).each(function() {
            var quantity = parseInt($(this).html());
            if (quantity > 0){
                order_button.removeAttr("disabled");
                disable = false;
                return;
            }
        })

        // Set enabled/disabled
        if (disable) order_button.attr("disabled", true);
    };

    // Adjust quantity on -/+ Buttons
    $( '.button.plus' ).click(function() {
        var quantity = parseInt($( '#' + this.id + '.quantity' ).html());
        quantity += 1;
        $( '#' + this.id + '.hidden-quantity' ).val(quantity);
        $( '#' + this.id + '.quantity' ).html(quantity);
        if (quantity == 1) update_order_button_status(); // may have changed from disabled -> enabled
    });
    $( '.button.minus' ).click(function() {
        var quantity = parseInt($( '#' + this.id + '.quantity' ).html());
        if ( quantity > 0 ){
            quantity -= 1;
            $( '#' + this.id + '.hidden-quantity' ).val(quantity);
        }
        $( '#' + this.id + '.quantity' ).html(quantity);
        if (quantity == 0) update_order_button_status(); // may have changed from enabled -> disabled
    });

    // Read more if long description
    $( '.menuitem-description' ).readmore({
        collapsedHeight: 100
    });

    // Select table
    $( '.table' ).change(function() {
        update_order_button_status();
    });

    // Confirm order on Place Order button press
    $( '.button.placeorder' ).click(function() {
        // Determine the table placing the order
        var table_name = $( '.table :selected' ).text();

        // Determine the order being placed
        var order = [];
        $( '.quantity' ).each(function() {
            var quantity = parseInt($(this).html());
            if (quantity > 0){
                var name = $( '#' + this.id + '.name' ).html();
                var note = $( '#' + this.id + '.note' ).val();
                var ordermenuitem = {
                    id: this.id,
                    name: name,
                    note: note,
                    quantity: quantity,
                };
                order.push(ordermenuitem);
            }
        });


        // Request confirmation
        $('.orderconfirm > h2').html("Confirm order for table " + table_name + "?");
        var ordertext = "";
        $.each(order, function() {
            ordertext += "<li>" + this.quantity + " " + this.name + "</li>";
            if (this.note) ordertext += "<ul><li>" + this.note + "</li></ul>";
        });
        $('.orderconfirm > ul').html(ordertext);
        $('.orderconfirm').foundation('reveal', 'open');
    });

    // Place order on Confirm Order button press
    $( '.orderconfirm > button' ).click(function() {
        $( '.orderform' ).submit();
    });
});
