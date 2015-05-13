$(document).ready(function() {
    'use strict'

    // CSRF
    var csrftoken = $.cookie('csrftoken');
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    // Show "caught up" text if there are no incoming orders
    function check_caught_up() {
        if ($('.panel').length == 0) $('.caught-up').show();
    }

    // Click "Done" button
    $('.panel > .button').click(function() {
        var orderid = this.id;

        // Mark order as complete
        jQuery.post("/kitchen/completeorder", { order: orderid }, function() {
            // Remove order
            $.when($('#' + orderid + '.panel').fadeOut())
                .done(function() {
                    // Remove panel
                    $('#' + orderid + '.panel').remove();

                    // Check if empty
                    check_caught_up();
                });
        });
    });

    // Get new orders
    function update_orders() {
        // Most recent order
        var lastorderid = 0; // Just provide 0 if we don't have any orders on the page
        if ($('.panel').length > 0){
            lastorderid = parseInt($('.panel').last()[0].id);
        }

        // Get orders newer than what we have on the page
        jQuery.getJSON("/kitchen/update", { lastorder: lastorderid }, function(resp) {
            // Remove "caught up" text if there are incoming orders
            if (resp.length > 0) $('.caught-up').fadeOut();

            // Add each new order to the page
            $.each(resp, function() {
                var itemlist = "";
                $.each(this['items'], function() {
                    itemlist += "<li>" + this['quantity'] + " " + this['name'] + "</li>";
                });
                $('.orders').append(
                    "<div class=\"panel\" id=\"" + this['id'] + "\"><h4>Table: " + this['table'] +
                    "</h4><ul>" + itemlist + "</ul>" +
                    "<a href=\"#\" class=\"button small success\" id=\"" + this['id'] + "\">Done</a></div>"
                )
            });
        });
    }

    setInterval(function(){
        update_orders();
    }, 10000);
});
