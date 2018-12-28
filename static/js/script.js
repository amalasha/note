$(document).ready(function() {
    // To delete notes
    $('body').on('click','.delete_note',function(){
        if(confirm("Are you sure you want to delete this item?")){
            var id = $(this).attr('data-id')
            window.location.href = '/delete_note/' + id
        }
    });
    // To delete tag
    $('body').on('click','.delete_tag',function(){
        if(confirm("Are you sure you want to delete this item?")){
            var id = $(this).attr('data-id')
            window.location.href = '/delete_tag/' + id
        }
    });
    // To add tag
    $('body').on('click','.add_new_tag',function(){
            var type = $(this).attr('data-type')
            var tag = prompt("Please enter the tag name");
            if (tag != null || tag != '') {
                $.ajax({
                    type: "POST",
                    url: '/ajax/addtag',
                    data: {
                        'tag': tag,
                        'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
                    },
                    dataType: 'json',
                    success: function(data) {
                        if(type = 'note'){
                            var str = '<option value="' + data.id + '">' + data.tag + '</option>'
                            $('#id_tags').append(str)
                            }
                         if(type = 'tag'){

                                var str = '    <div class="panel col-lg-4 mt-5">'
                                   str += ' <div class="btn-group" role="group">'
                                   str += ' <button style="min-width:150px" class="btn btn-outline-primary">'+data.tag+'</button>'
                                    str += '<a href="/tag_action/'+data.id+'" class="btn btn-success">'
                                    str += '<span class="glyphicon glyphicon-pencil"></span>'
                                    str += '</a>'
                                    str += '<button type="button" class=" btn btn-danger delete_tag" data-id="'+data.id+'">X</button>'
                                    str += '</div></div>'

                            $('#tags').prepend(str)
                            }

                    },
                    error: function(jqXHR, exception) {
                        alert("Ajax loading Error");
                    }
                });
            }
        });
        // For the selected tag value
        $('body').on('change','#tag_id',function(){
            window.location.href = '/home/' + this.value
        });
    });