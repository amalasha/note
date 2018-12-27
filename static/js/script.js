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

    $('body').on('click','.add_new_tag',function(){
            var type = $(this).attr('data-type')
            var tag = prompt("Enter the tag name?");
            if (tag != null) {
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
                            var str = '<a href="/tag_action/'+data.id+'">'+data.tag+'</a>'
                            str += '<button type="button" class="text-danger delete_tag" data-id="'+data.id+'">X</button>'
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