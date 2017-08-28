/**
 * Remove rights
 */
removeRights = function() {
    $("#remove_rights_banner_errors").hide();
    var $recordRow = $(this).parent().parent();
    $('.remove-rights-id').val($recordRow.attr("objectid"));
    $("#remove-rights-modal").modal("show");
};

/**
 * AJAX call, remove rights
 */
remove_rights = function() {
    $.ajax({
        url : removeRightsUrl,
        type : "POST",
        dataType: "json",
        data : {
            workspace_id: workspace_id,
            user_id: $('.remove-rights-id').val()
        },
		success: function(data){
			location.reload();
	    },
        error:function(data){
            $("#remove_rights_errors").html(data.responseText);
            $("#remove_rights_banner_errors").show(500)
        }
    });
};

$('.remove-user-btn').on('click', removeRights);
$('#remove-user-yes').on('click', remove_rights);
