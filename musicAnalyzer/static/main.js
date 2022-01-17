function toggleDiv(divId) {
    $('#' + divId).toggle();
}

function refreshDiv(divId) {
    $('#' + divId).load(location.href + ' #' + divId);
}

function createSong(albumId) {
    $.post('song_create', {
        id_ : albumId,
        title : $('#songName').val()
    },
    function(data) {
        refreshDiv('allSongs');
        $('#songName').val('');
    });
}

function rateSong(songId, rating) {
    $.get('song_rate', {
        id_ : songId,
        rating : rating
    },
    function(data) {
        refreshDiv('allSongs');
    });
}

function deleteSong(songId) {
    $.get('song_delete', {
        id_ : songId
    },
    function(data) {
        refreshDiv('allSongs');
    });
}

function createArtist() {
    $.post('artist_create', {
        name : $('#artistName').val()
    },
    function(data) {
        refreshDiv('allArtists');
        $('#artistName').val('');
    });
}

function deleteArtist(artistId) {
    $.get('artist_delete', {
        id_ : artistId
    },
    function(data) {
        refreshDiv('allArtists');
    });
}

function createAlbum(artistId, albumId) {
    $('#loading' + albumId).show()
    $.post('album_create', {
        id_ : artistId,
        title : $('#albumName' + albumId).val(),
        genius_id : $('#albumGeniusId' + albumId).val(),
        cover_url : $('#albumCoverUrl' + albumId).val(),
        release_date : $('#albumReleaseDate' + albumId).val()
    },
    function(data) {
        $('#loading' + albumId).hide()
    });
}

function deleteAlbum(albumId) {
    $.get('album_delete', {
        id_ : albumId
    },
    function(data) {
        refreshDiv('allAlbums');
    });
}