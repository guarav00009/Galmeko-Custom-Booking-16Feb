var loc = window.location;
var server_url = "" + loc.protocol + "//" + loc.host + '/';


$(document).ready(function () {
    var user_types = $("#booking_type").val();
    if (user_types != '') {
        get_userType_ById(user_types);
        $('.user_div').show();
    } else {
        $('.user_div').hide();
    }

    $(document).on('change', '#booking_type', function () {
        var user_type = this.value;
        if (user_type != '') {
            get_userType_ById(user_type);
        } else {
            $('.user_div').hide();
        }

    });

    function get_userType_ById(user_type) {
        if ($('#id_user').val()) {
            var user_id = $('#id_user').val();
        } else {
            user_id = ''
        }
        var token = $('input[name="csrfmiddlewaretoken"]').attr('value')
        var formData = {
            'user_type': user_type,
            'csrfmiddlewaretoken': token
        }
        $.ajax({
            method: "POST",
            url: server_url + 'admin/get_user_data/',
            data: formData,
            cache: false,
            success: function (data) {
                $('.user_div').css('display', 'block');
                var selectbox = $('#id_user');
                selectbox.empty();
                var list = '';
                var selected = '';
                if (data.status == true) {
                    $.each(data.data, function (k, v) {
                        if (v.id == user_id) {
                            var selected = 'selected';
                        } else {
                            var selected = '';
                        }
                        var name = v['first_name'] + ' ' + v['last_name'];
                        list += "<option  class='cur_user_" + v.id + "' value='" + v.id + "' " + selected + ">" + name + "</option>";
                    })
                } else {
                    list += "<option value=''>" + data.data + "</option>";
                }
                selectbox.html(list);
            }
        });
    }

})

// Google Map Autocomplete Code
function initAutocomplete() {
    new google.maps.places.Autocomplete(
        (document.getElementById('origin_address')),
        { types: ['geocode'], componentRestrictions: { country: 'IN' }, }

    );

    new google.maps.places.Autocomplete(
        (document.getElementById('destination_address')),
        { types: ['geocode'], componentRestrictions: { country: 'IN' }, }

    );

}

$(document).ready(function () {
    
    $('#origin_address ,#destination_address').blur(function () {
        origin = $('#origin_address').val();
        destination = $('#destination_address').val();
        if (origin != '' && destination != '') {
            get_lat_long(origin, destination);
        }
    });

})

function get_lat_long(origin, destination) {
    var token = $('input[name="csrfmiddlewaretoken"]').attr('value')
    var formData = {
        'origin': origin,
        'destination': destination,
        'csrfmiddlewaretoken': token
    }
    $.ajax({
        method: "POST",
        url: server_url + 'admin/get_lat_long/',
        data: formData,
        cache: false,
        success: function (data) {
            var origin = data.origin;
            var destination = data.destination;
            $('#origin_geocode').val(origin);
            $('#destination_geocode').val(destination);

        }
    });
}
//Booking stop related Js 
$(document).ready(function () {
    $('.stops').hide();
    $('.show_stop_form').click(function (e) {
        e.preventDefault();
        $('.stops').toggle();
        $(this).text(function (i, v) {
            return v === 'Add Stop' ? 'Remove' : 'Add Stop'
        })
    });

})
$(document).on('click','.add-row',function(e){
    for(n = 1; n < 6; n++){
            new google.maps.places.Autocomplete(
                (document.getElementById('id_bookingstop_set-'+n+'-address')),
                { types: ['geocode'], componentRestrictions: { country: 'IN' }, }
        
            );
        }
    
});