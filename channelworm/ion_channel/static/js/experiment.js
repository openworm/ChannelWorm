cw.experiment = (function () {
    var experimentId = -1;

    var url = {
        experimentUpdateURL: '',
        experimentCreateURL: '',
        patchClampIndex: '',
        patchClampCreate: '',
        patchClampUpdate: '',
        graphIndex: '',
        graphCreate: '',
        graphUpdate: '',
    };

    function init(config) {
        url.experimentCreateURL = config.url.experimentCreateURL;
        url.experimentUpdateURL = config.url.experimentUpdateURL;

        url.patchClampIndex = config.url.patchClampIndex;
        url.patchClampCreate = config.url.patchClampCreate;
        url.patchClampUpdate = config.url.patchClampUpdate;

        url.graphIndex = config.url.graphIndex;
        url.graphCreate = config.url.graphCreate;
        url.graphUpdate = config.url.graphUpdate;



        $("#experiment_form").load(url.experimentCreateURL);
    }

    function loadPatchClamp() {
        $("#patch_clamp_loading").css("display", "block");
        $("#patch_clamp").load(url.patchClampIndex + experimentId, function () {
            $("#patch_clamp_loading").css("display", "none")
        });
    }

    function loadGraph() {
        $("#graph_loading").css("display", "block");
        $("#graph").load(url.graphIndex + experimentId, function () {
            $("#graph_loading").css("display", "none")
        });
    }

    function saveExperiment() {
        var experimentUpdateURL = url.experimentUpdateURL;

        cw.ajax.submit({
            form: 'frm_experiment',
            loadingMask: 'loading',
            success: function (response) {
                if (response.status == 'success') {
                    experimentId = response.pk;
                    var lastSlashIndex = experimentUpdateURL.lastIndexOf("/");
                    var updateURL = experimentUpdateURL.substring(0, lastSlashIndex) + "/" + experimentId;
                    $("#experiment_form_wrapper").load(updateURL);
                    $('#loading').css("display", "none");

                    loadPatchClamp();
                    loadGraph();
                }
            }
        });

        return false;
    }

    function savePatchClamp() {
        cw.ajax.submit({
            form: 'frm_patch_clamp',
            loadingMask: 'form_loading',
            success: function (response) {
                if (response.status == 'success') {
                    $('#form_loading').css("display", "block");
                    loadPatchClamp();
                    closeModal()
                }
            }
        });

        return false;
    }

    function deletePatchClamp(){
        return savePatchClamp();
    }

    function saveGraph() {
        cw.ajax.submit({
            form: 'frm_graph',
            loadingMask: 'form_loading',
            containFile: true,
            success: function (response) {
                if (response.status == 'success') {
                    $('#form_loading').css("display", "block");
                    loadGraph();
                    closeModal();
                }
            }
        });

        return false;
    }

    function deleteGraph(){
        return saveGraph();
    }

    function openModal(title){
        $('.modal-title').html(title)
        $('.modal').modal('show');
    }

    function openPatchClampCreateForm() {
        openModal('<i class="fa fa-pinterest-p"></i> Patch Clamp')
        $("#form-container").load(url.patchClampCreate + experimentId);
    }

    function openPatchClampUpdateForm(url) {
        openModal('<i class="fa fa-pinterest-p"></i> Patch Clamp')
        $("#form-container").load(url);
    }

    function confirmPatchClampDelete(url){
        openModal('<i class="fa fa-warning"></i> Confirm')
        $("#form-container").load(url);
    }

    function openGraphCreateForm() {
        openModal('<i class="fa fa-bar-chart"></i> Graph')
        $("#form-container").load(url.graphCreate + experimentId);
    }

    function closeModal(){
        $('.modal').modal('hide');
    }

    function openGraphUpdateForm(url) {
        $('.modal-title').html('<i class="fa fa-bar-chart"></i> Graph')
        $('.modal').modal('show');
        $("#form-container").load(url);
    }

    function confirmDeleteGraph(url){
        openModal('<i class="fa fa-warning"></i> Confirm')
        $("#form-container").load(url);
    }

    return {
        init: init,
        saveExperiment: saveExperiment,
        patchClamp: {
            openCreateForm: openPatchClampCreateForm,
            openUpdateForm: openPatchClampUpdateForm,
            confirmDelete: confirmPatchClampDelete,
            refresh: loadPatchClamp,
            save: savePatchClamp,
            delete: deletePatchClamp
        },
        graph: {
            openCreateForm: openGraphCreateForm,
            openUpdateForm: openGraphUpdateForm,
            confirmDelete: confirmDeleteGraph,
            refresh: loadGraph,
            save: saveGraph,
            delete: deleteGraph
        },
        modal: {
            close: closeModal
        }
    }
})();