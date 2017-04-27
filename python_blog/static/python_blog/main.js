
function parseQuery() {
    return $('#search_s').val();
}


function settleResponse(data) {
    $('#search_results').empty();
    for (var i = 0; i < data.length; i++) {
        var name = data[i][0];
        var date = data[i][1];
        var text = data[i][2];
        var id = data[i][3];
        var container = '<div>';
            container += '<a href="blog/' + id + '">' + name + '</a>';
            container += '<p><span>' + date + '</span></p>';
            container += text;
        container += '<hr></div>';
        $('#search_results').append(container);
    }
}


function searchRequest() {
    var request = parseQuery();
    if (request !== ''){
        $.ajax({
            url: '',
            type: 'GET',
            data: {
                query: request
            },
            success: function(data) {
                settleResponse(data);
            }
        });
    }
}


function setHandlers() {
    var flag = true;
    $('#search_btn').click(function() {
        var x = $('.move').position();
        if (flag) {
            flag = false;
            $('.move').animate({
                'margin-top' : "-=250px"
            });
        }
        searchRequest(); 
    });
    $('#log_out').click(function() {
        $.ajax({
            url: '',
            type: 'GET',
            data: {
                log_out: true
            },
            success: function(data) {
                location.reload();
            }
        });
    });
    $('#log').click(function() {
        window.location.href = 'http://127.0.0.1:8000/home/log/#';
    });
    $('#sign').click(function() {
        window.location.href = 'http://127.0.0.1:8000/home/sign/#';
    });
}


$(document).ready(function() {
    setHandlers();
});
