$(document).ready(function() {
    $('#uploadForm').submit(function(event) {
        event.preventDefault();
        var formData = new FormData($(this)[0]);
        $.ajax({
            url: '/upload',
            type: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function(response) {
                $('#message').text(response.message);
                displayVideoList(response.urls);
            },
            error: function(xhr, status, error) {
                $('#message').text('Error: ' + error);
            }
        });
    });

    function displayVideoList(urls) {
        $('#videoList').empty();
        urls.forEach(function(url, index) {
            var listItem = $('<li class="video-item"></li>');
            var downloadLink = $('<a href="' + url + '" download>Download Part ' + (index + 1) + '</a>');
            var deleteButton = $('<button onclick="deleteVideo(\'' + url + '\')">Delete</button>');
            listItem.append(downloadLink, deleteButton);
            $('#videoList').append(listItem);
        });
    }

    window.deleteVideo = function(url) {
        $.ajax({
            url: '/delete',
            type: 'POST',
            data: { url: url },
            success: function(response) {
                $('#message').text(response.message);
                displayVideoList(response.urls);
            },
            error: function(xhr, status, error) {
                $('#message').text('Error: ' + error);
            }
        });
    };
});
