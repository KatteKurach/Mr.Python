function log_user() {
    var email = $('#email_s').val();
    var password = $('#password_s').val();
    var flag1 = true;
    var flag2 = true;

    if (email === '') {
        $('#email_s').addClass('highlight');
		setTimeout(function() {
		$('#email_s').removeClass('highlight');},
       		3000
    	);
        flag1 = false;
        alert("flag1");
    }
    if (password == '') {
       $('#password_s').addClass('highlight');
        setTimeout(function() {
            $('#password_s').removeClass('highlight');},
            3000
        );
        flag2 = false;
        alert("flag2");
    }
    if (flag1 == true && flag2 == true) {
        $.ajax({
            url: '',
            type: 'GET',
            data: {
                email_s: email,
                password_s: password,
                btn_log: true
            },
            success: function(data) {
                if (data['status'] === 'ok') {
                    swal({
                        title: 'Welcome!',
                        type: 'success',
                        timer: 3000
                    },
                    function() {
                        window.location.href = 'https://mr-python.herokuapp.com/home/';
                    });
                }
                if (data['status'] === 'error') {
                    swal({
                        title: 'Wrong',
                        text: 'The email and password you entered did not match our records. Please double-check and try again.',
                        type: "warning",
                        timer: 3000
                    });
                }
                if (data['status'] === 'admin') {
                    window.location.href = 'https://mr-python.herokuapp.com/hadmin/';
                }
            },
            error: function(data) {
                alert("error");
            }
        });
    }
}


$(document).ready(function() {
    $('#btn_log').click(function(){
        log_user();
    });
});
