// script.js

function previewImage(name, fileId) {
    var preview = document.getElementById(name);
    var fileInput = document.getElementById(fileId);
    var file = fileInput.files[0];
    var reader = new FileReader();

    reader.onloadend = function () {
        preview.innerHTML = '<img src="' + reader.result + '" alt="Selected Image">';
    }

    if (file) {
        reader.readAsDataURL(file);
    } else {
        preview.innerHTML = '';
    }
}

$(document).ready(function() {
    $('#uploadForm').submit(function(e) {
        e.preventDefault(); // Prevent page reload

        var formData = new FormData(this);

        $.ajax({
            type: 'POST',
            url: '/Secure-Data-Transfer-and-Information-Hiding/extracting/',
            data: formData,
            contentType: false,
            processData: false,
            success: function(response) {
                if ('name' in response && 'surname' in response && 'tcno' in response) {
                    console.log(response.name)
                    $('#name-output').text(response.name);
                    $('#surname-output').text(response.surname);
                    $('#tcno-output').text(response.tcno);

                    $('#result-message-output').text(response.success_message);
                    Swal.fire({
                        icon: 'success',
                        title: response.success_message,
                        text: response.success_message
                    });
                } else {
                    console.error('Invalid response format');
                }
            },
            error: function(error) {
                console.error(error);
            }
        });
    });

    $('#embedForm').submit(function(e) {
        e.preventDefault();

        var formData = new FormData(this);

        $.ajax({
            type: 'POST',
            url: '/Secure-Data-Transfer-and-Information-Hiding/embedding/',
            data: formData,
            contentType: false,
            processData: false,
            success: function(response) {
                if (response.embedded_image) {
                    var imagePath = response.embedded_image;
                    var imageUrl = '/static/' + encodeURIComponent(imagePath);

                    $('#embeddedImage').attr('src', imageUrl);
                    console.log(imagePath);       

                    $('#result-message-output').text(response.success_message);
                    Swal.fire({
                        icon: 'success',
                        title: response.success_message,
                        text: response.success_message
                    });

                    $('#imageContainer').show();
                } else {
                    console.error("Embedded image path not found in the response");
                }
            },
            error: function(error) {
                console.error(error);
            }
        });
    });

    document.getElementById('uploadForm').addEventListener('submit', function() {
        document.getElementById('uploadForm').target = 'uploadTarget';
    });

    document.getElementById('uploadTarget').addEventListener('load', function() {
        var iframeContent = document.getElementById('uploadTarget').contentDocument.body.textContent;
        console.log('iframe content:', iframeContent);
    });
});
