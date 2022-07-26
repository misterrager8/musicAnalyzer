$(document).ready(function() {
    document.documentElement.setAttribute('data-theme', localStorage.getItem('musicAnalyzer'));
});

function changeTheme(theme) {
    localStorage.setItem('musicAnalyzer', theme);
    document.documentElement.setAttribute('data-theme', localStorage.getItem('musicAnalyzer'));
}

function toggleDiv(divId) {
    $('#' + divId).fadeToggle(150);
}

function refreshPage() {
    $('#pageContent').load(location.href + ' #pageContent');
}

function suggestTitle() {
    $.post("suggest_title", {
        url : $('#url').val()
    }, function(data) {
        $('#headline').val(data);
    });
}

function addNews() {
    $.post('add_news', {
        url: $('#url').val(),
        headline: $('#headline').val()
    }, function(data) {
        refreshPage();
    });
}

function addNewsFromScraper(idx) {
    $('#spinner' + idx).show();
    $.post('add_news', {
        url: $('#url' + idx).val(),
        headline: $('#headline' + idx).val()
    }, function(data) {
        refreshPage();
    });
}

function editNews(newsId) {
    $.post('edit_news', {
        id_: newsId,
        url: $('#url' + newsId).val(),
        headline: $('#headline' + newsId).val()
    }, function(data) {
        refreshPage();
    });
}

function deleteNews(newsId) {
    $.get('delete_news', {
        id_: newsId
    }, function(data) {
        refreshPage();
    });
}

function deleteBlog(blogId) {
    $.get('delete_blog', {
        id_: blogId
    }, function(data) {
        refreshPage();
    });
}