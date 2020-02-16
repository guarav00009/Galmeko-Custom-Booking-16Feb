/*global showAddAnotherPopup, showRelatedObjectLookupPopup showRelatedObjectPopup updateRelatedObjectLinks*/

(function ($) {
    'use strict';
    $(document).ready(function () {
        var modelName = $('#django-admin-form-add-constants').data('modelName');
        $('body').on('click', '.add-another', function (e) {
            e.preventDefault();
            var event = $.Event('django:add-another-related');
            $(this).trigger(event);
            if (!event.isDefaultPrevented()) {
                showAddAnotherPopup(this);
            }
        });

        if (modelName) {
            $('form#' + modelName + '_form :input:visible:enabled:first').focus();
        }
    });

    //User Add Form Js

    var getUrlParameter = function getUrlParameter(sParam) {
        var sPageURL = window.location.search.substring(1),
            sURLVariables = sPageURL.split('&'),
            sParameterName,
            i;

        for (i = 0; i < sURLVariables.length; i++) {
            sParameterName = sURLVariables[i].split('=');

            if (sParameterName[0] === sParam) {
                return sParameterName[1] === undefined ? true : decodeURIComponent(sParameterName[1]);
            }
        }
    };

    // for Edit form changes
    var url = $(location).attr('href'),
        parts = url.split("/"),
        edit_case = parts[parts.length - 2];
    if(edit_case == 'change')
    {
        $('.field-type').hide();
    }

    //Code for Dynamic user add bassed on type
    var user_type = getUrlParameter('type');

    var type = $("#id_type").val();
    if (type == 1 || user_type == 1) {
        show_hide_by_id(type)
    } else if (type == 2 || user_type == 2) {
        show_hide_by_id(type)
    }
    else if (type == 4 || user_type == 4) {
        show_hide_by_id(type)
    }
    else if (type == 3 || user_type == 3) {
        show_hide_by_id(type)
    }
    $("#id_type").on('change', function (e) {
        $('.custom_error').css('display','none');
        var type = $("#id_type").val();
        if (type == 1) {
            show_hide_by_id(type)
        } else if (type == 2) {
            show_hide_by_id(type)
        } else if (type == 3) {
            show_hide_by_id(type)
        }
        else if (type == 4) {
            show_hide_by_id(type)
        }
    });

    // Type 1 = Hospial , 2 = Vendor , 3 = User , 4 = Admin
    function show_hide_by_id(type) {
        if (type == 1) {         
            $('#id_is_staff').attr('checked', false);              
            $('.dynamic-title').text('Add Hospital');
            $('#hospital-group').show();
            $('#vehicle_set-group').hide();
            $('#vendor-group').hide();
        } else if (type == 2) {
            $('#id_is_staff').attr('checked', false);
            $('.dynamic-title').text('Add Vendor');
            $('#hospital-group').hide();
            $('#vendor-group').show();
            $('#vehicle_set-group').show();
        } else if (type == 3) {
            $('#id_is_staff').attr('checked', false);
            $('.dynamic-title').text('Add User');
            $('#hospital-group').hide();
            $('#vendor-group').hide();
            $('#vehicle_set-group').hide();
        } else if (type == 4) {
            $('#id_is_staff').attr('checked', true);
            $('.field-is_staff,.field-is_active').hide();
            $('.dynamic-title').text('Add User');
            $('#hospital-group').hide();
            $('#vendor-group').hide();
            $('#vehicle_set-group').hide();
        }
    }
})(django.jQuery);
