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

    // Click "Done" button
    $('.panel > .button').click(function() {
        var orderid = this.id;

        // Mark order as complete
        jQuery.post("/kitchen/completeorder", { order: orderid }, function() {
            // Remove order
            $('#' + orderid + '.panel').fadeOut();
        });
    });
});
