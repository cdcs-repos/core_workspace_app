/**
 * AJAX call to switch right
 */

switch_read = function() {
    var $recordRow = $(this).parent().parent().parent();
    call_ajax_switch_right($recordRow.attr("objectid"), action_read,  $(this))
};

switch_write = function() {
    var $recordRow = $(this).parent().parent().parent();
    call_ajax_switch_right($recordRow.attr("objectid"), action_write, $(this))
};

call_ajax_switch_right = function(selected, action, obj) {
    $.ajax({
        url : switchRightUrl,
        type : "POST",
        dataType: "json",
        data : {
            workspace_id: workspace_id,
            user_id: selected,
            action: action,
            value: obj.prop("checked")
        },
        success: function(data){},
        error:function(data){
            obj.prop("checked", !obj.prop("checked"));
            $("#switch_rights_errors").html(data.responseText);
            $("#switch_rights_banner_errors").show(50);
            $("#switch-rights-modal").modal("show");
        }
    });
};

$('#btn-read').on('change', switch_read);
$('#btn-write').on('change', switch_write);
