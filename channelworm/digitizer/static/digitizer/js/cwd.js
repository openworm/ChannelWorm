var cwd = cwd || {};
cwd.modal = (function () {
    function show(id) {
        $('#' + id).modal('show');
    }

    function close(id) {
        $('#' + id).modal('hide');
    }

    function isModal(id) {
        var modal = $('#' + id);
        return (modal.hasClass("modal"));
    }

    return {
        show: show,
        close: close,
        isModal: isModal
    }
})();

cwd.notify = (function () {
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

cwd.alignAxes = (function () {
    function initiatePlotAlignment() {
        document.getElementById('r_xy').checked = true;
        wpd.alignAxes.start();
    }

    return {
        start: initiatePlotAlignment
    }
})();

cwd.toolbar = (function () {

    function show(tbid) { // Shows a specific toolbar
        clear();
        $('#' + tbid).collapse('show');
    }

    function clear() { // Clears all open toolbars
        $('.collapse').collapse('hide');
    }

    return {
        show: show,
        clear: clear
    };
})();

cwd.graphData = (function () {
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    function save(data) {
        var series = wpd.dataTable.getDataSet();
        var form = $("#frm_graph_data");
        var csrftoken = $.cookie('csrftoken');

        $("#series_name").val(series.name);
        $("#series_data").val(series.data);
        $("#save_data_graph_loading").css("display", "block");

        $.ajax({
            type: "POST",
            url: form.attr('action'),
            data: form.serialize(),
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },
            success: function (response) {
                if (response.status == 'success') {
                    cwd.notify.success(response.result);
                } else {
                    cwd.notify.error(response.result);
                }
                $("#save_data_graph_loading").css("display", "none");
            },
            error: function (response) {
                cwd.notify.error("System Error !!!");
            }
        });

    }

    return {
        save: save
    };

})();


cwd.initApp = (function () {
    wpd.browserInfo.checkBrowser();
    wpd.layoutManager.initialLayout();

    var graphUrl = $("#graph_url").val();
    wpd.graphicsWidget.loadImageFromURL(graphUrl);

    $('.cwd-loading').css("display", "none");
});


$(document).ready(cwd.initApp);