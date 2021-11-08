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

function updateSong(songId) {
    $.post('song_update', {
        id_ : songId,
        title : $('#songTitle' + songId).val(),
        rating : $('#songRating' + songId).val(),
        track_num : $('#songTrackNum' + songId).val()
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

function updateArtist(artistId) {
    $.post('artist_update', {
        id_ : artistId,
        name : $('#artistName' + artistId).val(),
        genius_url : $('#artistGenius' + artistId).val()
    },
    function(data) {
        refreshDiv('allArtists');
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

function createAlbum(artistId) {
    $.post('album_create', {
        id_ : artistId,
        title : $('#albumName').val()
    },
    function(data) {
        refreshDiv('allAlbums');
        $('#albumName').val('');
    });
}

function updateAlbum(albumId) {
    $.post('album_update', {
        id_ : albumId,
        title : $('#albumTitle' + albumId).val(),
        release_date : $('#albumDate' + albumId).val(),
        release_type : $('#albumReleaseType' + albumId).val()
    },
    function(data) {
        refreshDiv('allAlbums');
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