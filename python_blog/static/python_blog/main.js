
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
            container += '<br>' + text;
        container += '</div>';
        $('#search_results').append(container);
    }
}


function searchRequest() {
    var request = parseQuery();
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


function setHandlers() {
    $('#search_btn').click(function() {
        searchRequest(); 
    });
}


$(document).ready(function() {
    setHandlers();
});
