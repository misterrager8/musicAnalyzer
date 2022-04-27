function refreshPage() {
    $('#pageContent').load(location.href + ' #pageContent');
    $('#navContent').load(location.href + ' #navContent');
}

function toggleDiv(divId) {
    $('#' + divId).fadeToggle(150);
}

function userEdit() {
    $.post('user_edit', {
        username: $('#username').val(),
        password: $('#password').val()
    }, function(data) {
        refreshPage();
    });
}

function artistAdd() {
    $.post('artist_add', {
        name: $('#name').val()
    }, function(data) {
        refreshPage();
    });
}

function artistEdit(artistId) {
    $('#spinner').show();
    $.post('artist_edit', {
        id_: artistId,
        name: $('#name' + artistId).val()
    }, function(data) {
        refreshPage();
    });
}

function artistDelete(artistId) {
    $('#spinner').show();
    $.get('artist_delete', {
        id_: artistId
    }, function(data) {
        refreshPage();
    });
}

function albumAdd(artistId, idx) {
    $('#spinner').show();
    $.post('album_add', {
        id_: artistId,
        title: $('#title' + idx).val(),
        genius_id: $('#geniusId' + idx).val(),
        release_date : $('#released' + idx).val()
    }, function(data) {
        refreshPage();
    });
}

function albumEdit(albumId) {
    $('#spinner').show();
    $.post('album_edit', {
        id_: albumId,
        title: $('#title' + albumId).val(),
        release_date: $('#releaseDate' + albumId).val()
    }, function(data) {
        refreshPage();
    });
}

function albumDelete(albumId) {
    $('#spinner').show();
    $.get('album_delete', {
        id_: albumId
    }, function(data) {
        refreshPage();
    });
}

function albumTag(albumId, tagId) {
    $('#spinner').show();
    $.get('album_tag', {
        album_id: albumId,
        tag_id: tagId
    }, function(data) {
        refreshPage();
    });
}

function albumUntag(albumtagId) {
    $('#spinner').show();
    $.get('album_untag', {
        id_: albumtagId
    }, function(data) {
        refreshPage();
    });
}

function songAdd(albumId) {
    $.post('song_add', {
        id_: albumId,
        name: $('#name').val()
    }, function(data) {
        refreshPage();
    });
}

function songDelete(songId) {
    $('#spinner').show();
    $.get('song_delete', {
        id_: songId
    }, function(data) {
        refreshPage();
    });
}

function rateSong(songId, rating) {
    $.get('song_rate', {
        id_ : songId,
        rating : rating
    },
    function(data) {
        refreshPage();
    });
}

function tagDelete(tagId) {
    $('#spinner').show();
    $.get('tag_delete', {
        id_: tagId
    }, function(data) {
        refreshPage();
    });
}

function tagAdd() {
    $('#spinner').show();
    $.post('tag_add', {
        name: $('#name').val()
    }, function(data) {
        refreshPage();
    });
}