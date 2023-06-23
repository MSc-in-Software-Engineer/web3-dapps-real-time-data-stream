$(document).ready(function () {
    $('#uploadForm').submit((event) => {
        event.preventDefault();

        const formData = new FormData();
        formData.append('file', $('#fileInput')[0].files[0]);

        const uploadConfig = {
            url: '/v1/api/ipfs_file_event/upload',
            type: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function (response) {
                $("#uploadResult").css("display", "block");
                $("#uploadResultJSON").text(JSON.stringify(response))
                $('#uploadForm')[0].reset();
            },
            error: function (jqXHR, textStatus, errorThrown) {
                alert('Error uploading file: ' + errorThrown);
                $('#uploadForm')[0].reset();
            }
        };

        $.ajax(uploadConfig);
    });

    $('#downloadForm').submit((event) => {
        event.preventDefault();

        const hashInput = $('#hashInput').val();
        const formData = new FormData();
        formData.append('hashInput', hashInput);

        const downloadConfig = {
            url: `/v1/api/ipfs_file_event/download`,
            type: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function (response) {
                $("#downloadLink").css("display", "block");
                $("#downloadLinkHref").attr("href", response.download_link);
                $("#streamLinkHref").attr("href", `/ipfs_video_feed/${hashInput}`);
                $('#downloadForm')[0].reset();
            },
            error: function (jqXHR, textStatus, errorThrown) {
                alert('Error uploading file: ' + errorThrown);
                $('#downloadForm')[0].reset();
            }
        };

        $.ajax(downloadConfig);
    });
});
