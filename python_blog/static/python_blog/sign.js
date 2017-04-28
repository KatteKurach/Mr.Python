function save_user() {
    var username = $('#user_name').val();
    var email = $('#in_email').val();
    var pass = $('#in_password').val();
    var conf = $('#in_conf').val();

    if (pass !== conf) {
    	swal({
  			title: "Wrong data",
  			text: "Please, check your password and confirm password!",
  			type: "error",
			timer: 2500,
  			showConfirmButton: false
		});
		$('#in_password').addClass('highlight');
    	$('#in_conf').addClass('highlight');
		setTimeout(function() {
			$('#in_password').removeClass('highlight');
			$('#in_conf').removeClass('highlight');},
       		5500
    	);
	} else if (username == '' || email == ''){
        swal({
  			title: "Wrong data",
  			text: "You have empty fields.",
  			type: "error",
			timer: 2500,
  			showConfirmButton: false
		});
    } else {
        $.ajax({
            url: '',
            type: 'GET',
            data: {
                user_name: username,
                in_email: email,
                in_password: pass,
                in_conf: conf,
                btn_sign: true
            },
            success: function(data) {
                if (data['status'] === 'bad_email') {
                    swal({
                          title: "Wrong email address",
                          text: "This email already exists in our database.",
                          type: "warning",
                          timer: 3000
                    });
                    $('#in_email').addClass('highlight');
                            setTimeout(function() {
                                $('#in_email').removeClass('highlight');}, 
                                5500
                            );
                }
                if (data['status'] === 'ok') {
                    swal({
                        title: "Good job, " + username + "!", 
                        timer: 3000, 
                        type: "success"
                    },
                    function(){
                        window.location.href = 'https://mr-python.herokuapp.com/home/log/#';
                    });
				}
            },
            error: function(data) {
                alert("error");
            }
        });
    }
}

function setHandlers() {
    $('#btn_sign').click(function() {
        save_user();
    });
}

$(document).ready(function() {
    setHandlers();
});
