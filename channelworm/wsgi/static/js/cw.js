var cw = cw || {};

cw.notify = (function () {
    var options = {
        "closeButton": true,
        "debug": false,
        "newestOnTop": false,
        "progressBar": false,
        "positionClass": "toast-top-right",
        "preventDuplicates": false,
        "onclick": null,
        "showDuration": "300",
        "hideDuration": "1000",
        "timeOut": "5000",
        "extendedTimeOut": "1000",
        "showEasing": "swing",
        "hideEasing": "linear",
        "showMethod": "fadeIn",
        "hideMethod": "fadeOut"
    };

    function success(message, title, option) {
        option = this.option;
        toastr.success(message, title, option);
    }

    function error(message, title, option) {
        option = this.option;
        toastr.error(message, title, option);
    }

    function warning(message, title, option) {
        option = this.option;
        toastr.warning(message, title, option);
    }

    function info(message, title, option) {
        option = this.option;
        toastr.info(message, title, option);
    }

    return {
        info: info,
        success: success,
        warning: warning,
        error: error
    }
})();

cw.ajax = (function () {
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    function defaultErrorCallBack(response, form) {
        cw.notify.error(response.responseJSON.message);
        clearFormErrors(form)
        showFormErrors(response)
    }

    function clearFormErrors(form) {
        $("#" + form + " .ajax-error").remove();
    }

    function showFormErrors(response) {
        response = response.responseJSON;
        var validationErrors = response.validation;

        $.each(validationErrors, function (elementId, errors) {
            var errorMessages = $('<div class="ajax-error" id="' + elementId + '_errors"></div>');
            var element = $("#id_" + elementId).after();

            $.each(errors, function (index, error) {
                var message = $('<span class="text-red"></span>').html('<i class="fa fa-times-circle-o"></i>' + error)
                message.appendTo(errorMessages)
            });

            element.after(errorMessages);
        });
    }

    function submit(config) {
        var form = $("#" + config.form);
        var csrftoken = $.cookie('csrftoken');
        var loadingMask = config.loadingMask || 'cw-loading';
        var successCallBack = config.success;
        var errorCallBack = config.error || defaultErrorCallBack;

        var ajaxOptions = {
            type: "POST",
            url: form.attr('action'),
            data: form.serialize(),
            beforeSend: function (xhr, settings) {
                $("#" + loadingMask).css("display", "block");
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },
            success: function (response) {
                if (response.status == 'success') {
                    cw.notify.success(response.result);
                } else {
                    cw.notify.error(response.result);
                }
                $("#" + loadingMask).css("display", "none");
                successCallBack(response);
            },
            error: function (response) {
                errorCallBack(response ,form.attr('id'));
                $('#loading').css("display","none")
            }
        };

        if (config.containFile){
            ajaxOptions.data = new FormData(form[0]);
            ajaxOptions.cache= false;
            ajaxOptions.contentType= false;
            ajaxOptions.processData= false;
        }

        $.ajax(ajaxOptions);

    }

    return {
        submit: submit,
        clearFormErrors : clearFormErrors,
        showFormErrors: showFormErrors
    };
})();

cw.initApp = (function () {});


$(document).ready(cw.initApp);