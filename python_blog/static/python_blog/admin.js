function updateText(data) {
    $('#article_text').val(data);
}


function articleContentRequest(article_id) {
    $.ajax({
        url: '',
        type: 'GET',
        data: {
            id: article_id 
        },
        success: function(data) {
            updateText(data); 
        }
    });
}


function addNameClickHandler(id) {
    $('#' + id).click(function() {
        articleContentRequest($(this).attr('id'));
    });
}


function setHandlers() {
    var names = $('.articlename');
    for (var i = 0; i < names.length; i++) {
        addNameClickHandler(names[i].id);
    }
}


$(document).ready(function() {
    setHandlers();
});
