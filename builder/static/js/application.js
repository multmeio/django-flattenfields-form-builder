function fill_form(form, data) {
    $.each(data, function(key, value){
        var $ctrl = $('#id_' + key);
        if (!$ctrl || !$ctrl[0]) return;

        var input_type = $ctrl.attr("type") || 
                         $ctrl[0].tagName.toLowerCase();
        switch(input_type) {
            case "text":
            case "hidden":
            case "textarea":
            case "select":
                $ctrl.val(value);
                break;
            case "radio":
            case "checkbox":
                $ctrl.each(function(){
                    if($(this).attr('value') == value) {
                        $(this).attr("checked",value);
                    }
                });
                break;
        }
    });
}

function clean_form(form){
    form.find('input:text, input:password, input:file, select, textarea').val('');
    form.find('input:radio, input:checkbox').removeAttr('checked').removeAttr('selected');
    return true;
};

$(function() {
	// Bootstrap tabs
    $('#tabs').tab();


    // JqueryUI handle Events
    $("#id_form_sortable").sortable({
        revert: true,
        receive: function(event, ui) {
            var item = $(this).data().sortable.currentItem;
            var element = item.children('.controls').children();

            if(element.length > 1){
                element = element.children();
            }

            $('#id_typo').val(element.attr('data-typo'));
            
            var modal_id = "#id_" + element.attr('data-typeconfig');
            $(modal_id).modal();
        }
    });

    $(".tab-pane form .control-group").draggable({
        connectToSortable: "#id_form_sortable",
        helper: "clone",
        revert: false,
    });

    $("#id_form_sortable_trash").droppable({
        drop: function(event, ui) {
            var element = $(ui.helper).find('.controls').children();
            var field_name =  element.attr('name').split('-')[2];
            if (field_name) {
                var url = '/delete/dynamic/field/' + field_name;
                $.getJSON(url, function(data) {});
            };

            $(ui.draggable).remove();
        }
    });


    // Edit fields handles
    $('#id_form_sortable .control-group').live({
        click: function() {
            var element_id = $(this).find('label').attr('for');
            var element = $("#" + element_id);
            if (element) {
                var url = '/get/dynamic/field/' + element.attr('name').split('-')[2];
                $.getJSON(url, function(data) {
                    form = $("#id_form_" + data.typeconfig);
                    var modal_id = "#id_" + data.typeconfig;
                    fill_form(form, data);
                    form.attr('action', '/update/dynamic/field/' + data.name);
                    $(modal_id).modal();
                });
            };
        },
    });

    // Override Forms events
    $(".form-field-configs").submit(function(){
        var action = $(this).attr('action');
        var these = this;
        
        var result = $.ajax({
            async: false,
            data: $(this).serialize(),
            type: 'POST',
            url: action,
            dataType: 'json',
        }).success(function(data) {
            // Update the field
            var update_url = 'update/dynamic/field/';
            if ($(these).attr('action').search(update_url) != -1) {
                var old_name = $(these).attr('action').split(update_url)[1];
                var element = $('[name$=' + old_name +']');
                element.val(data.default_value);
                label = $('[for=' + element.attr('id') + ']');
                label.html(data.verbose_name);
                
                var old_id = element.attr('id');
                var old_name = old_id.split(old_id.match('-[0-9]-'))[1]
                if (old_name != data.name) {
                    var new_id = (old_id.split(old_id.match('-[0-9]-'))[0] + 
                                  old_id.match('-[0-9]-')) + data.name;
                    
                    element.attr('id', new_id);
                    new_id = element.attr('id');
                    label.attr('for', new_id);
                    element.attr('name', new_id.replace('id_', ''));
                };
            }; 
        });

        $(this).parents('.modal').modal('hide');
        return false;
    });


    // Validade forms
    $('.modal').on('hidden', function () {
        clean_form($(this).find('form'));
    });

    $(".form-field-configs").validate({
        rules:{
            refer:{
                required: true
            },
            name:{
                required: true
            },
            verbose_name:{
                required: true
            },
            typo:{
                required: true
            },
            category:{
                required: true
            },
        },
        errorClass: "help-block",
        errorElement: "span",
        highlight:function(element, errorClass, validClass) {
            $(element).parents('.control-group').addClass('error');
        },
        unhighlight: function(element, errorClass, validClass) {
            $(element).parents('.control-group').removeClass('error');
        }
    });
});