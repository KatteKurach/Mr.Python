var selected_id = 1;


function updateText(data) {
    $('#article_title').val(data['title']);
    $('#article_text').val(data['article']);
}


function articleContentRequest(article_id) {
    selected_id = article_id;
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


function showFormattedText() {
    $('#view_blog').html($('#article_text').val()); 
}


function saveText() {
    var text = $('#article_text').val();
    var title = $('#article_title').val();
    $.ajax({
        url: '',
        type: 'GET',
        data: {
            id: selected_id,
            type: 'save',
            header: title,
            article: text
        },
        success: function(data) {
            alert('saved');
        },
        error: function(data) {
            alert(text + 'rrrr');
            alert('error');
        }
    });
}


function deleteArticle() {
    $.ajax({
        url: '',
        type: 'GET',
        data: {
            id: selected_id,
            type: 'delete'
        },
        success: function(data) {
            alert('delete');
        },
        error: function(data){
            alert('error');
        }
    });
}


function setHandlers() {
    var names = $('.articlename');
    for (var i = 0; i < names.length; i++) {
        addNameClickHandler(names[i].id);
    }
    selected_id = names[0].id;

    $('#view').click(function() {
        showFormattedText(); 
    });

    $('#save').click(function() {
        saveText();
    });

    $('#delete').click(function() {
        deleteArticle(); 
    });
}


$(document).ready(function() {
    setHandlers();
});
