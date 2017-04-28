function add_like() {
    $.ajax({
        url: '',
        type: 'GET',
        data: {
            btn_like: true
        },
        success: function(data) {
            if (data['status'] === 'ok') {
                document.getElementById("count_likes").innerHTML = data['likes'];
            }
        }
    });
}

function add_comment() {
    var text = $('#text_comment').val();
    if (text == '') {
        swal({
            title: 'Wrong data!',
            text: 'Empty comment. Please, check your data input.',
            type: "info",
            timer: 3000
        });
    } else {
        $.ajax({
            url: '',
            type: 'GET',
            data: {
                btn_add: true,
                text_comment: text
            },
            success: function(data) {
                if (data['status'] == 'ok') {
                    $("#comment").append('<div id="one_comment"><p id="username">'+data['user']+'</p><p id="value_c">' +text+ '</p><hr></div><br>');
                } else {
                    swal({
                        title: 'Wrong',
                        text: 'If you want to add comment, please, log in.',
                        type: "warning",
                        timer: 3000,
                        confirmButtonText: "Log in",
                        showCancelButton: true,
                    },
                    function(isConfirm){
                        if (isConfirm) {
                            window.location.href = 'https://mr-python.herokuapp.com/home/log/#';
                        }
                    });
                }
            }
        });
    }
}

$(document).ready(function() {
    $('#btn_like').click(function() {
        add_like();
    });
    $('#btn_com').click(function() {
        add_comment();
    });
});
