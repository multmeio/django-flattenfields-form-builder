$(function() {
	// Bootstrap tabs
    $('#tabs').tab();


    // JqueryUI handle Events
    $("#id_form_sortable").sortable({
        revert: true,
        receive: function(event, ui) {
            var item = $(this).data().sortable.currentItem;
            var rand_id = Math.floor(Math.random()*99999);
            item.attr('data-id', rand_id);

            var element = item.children('.controls').children();

            if(element.length > 1){
                element = element.children();
            }

            $(this).find('p').remove();
            var modal_id = "#id_" + element.attr('data-typeconfig');
            $(modal_id).modal();
            $(modal_id).attr('field-data-id', rand_id);
        }
    });

    $(".tab-pane form .control-group").draggable({
        connectToSortable: "#id_form_sortable",
        helper: "clone",
        revert: false,
    });

    $("#id_form_sortable_trash").droppable({
        drop: function(event, ui) {
            $(ui.draggable).remove();
        }
    });


    // Edit fields handles
    $('#id_form_sortable .control-group').live({
        click: function() {
            var element = $("#" + $(this).find('label').attr('for'));
            var modal_id = "#id_" + element.attr('data-typeconfig');
            $(modal_id).modal();
            $(modal_id).attr('field-data-id', rand_id);
        },
    });
});