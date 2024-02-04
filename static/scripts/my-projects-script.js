
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
    function showCustomPopup(icon, title, message) {
        Swal.fire({
            icon: icon,
            title: title,
            text: message
        });
    }

    $('#loanForm').submit(function(e) {
        e.preventDefault();

        var formData = new FormData(this);

        $.ajax({
            type: 'POST',
            url: '/loan-approval-prediction/',
            data: formData,
            contentType: false,
            processData: false,
            success: function(response) {
                if (response.prediction) {
                    $('#prediction-output').text(response.prediction);
                    $('#result-message-prediction').text(response.success_message);
                    showCustomPopup('success', response.success_message, response.success_message);
                } else {
                    console.error("Prediction Problem");
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

                    $('#result-message-embedding').text(response.success_message);
                    showCustomPopup('success', response.success_message, response.success_message);

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

    $('#uploadForm').submit(function(e) {
        e.preventDefault();

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

                    $('#result-message-extracting').text(response.success_message);
                    showCustomPopup('success', response.success_message, response.success_message);
                } else {
                    console.error('Invalid response format');
                }
            },
            error: function(error) {
                console.error(error);
            }
        });
    });

    

});