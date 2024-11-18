// Fetch subcategories based on the selected category
$('#id_category').change(function() {
    var categoryId = $(this).val();
    if (categoryId) {
        $.ajax({
            url: '/fetch-subcategories/', // Adjust the endpoint if needed
            data: { 'category_id': categoryId },
            success: function(response) {
                var subcategorySelect = $('#id_subcategory');
                subcategorySelect.empty(); // Clear existing options
                subcategorySelect.append(new Option('Select Subcategory', '')); // Default option
                response.subcategories.forEach(function(subcategory) {
                    subcategorySelect.append(new Option(subcategory.name, subcategory.id));
                });
            },
            error: function() {
                alert('Failed to fetch subcategories. Please try again.');
            }
        });
    } else {
        $('#id_subcategory').empty().append(new Option('Select Subcategory', ''));
    }
});

// Submit form via AJAX
$('#newsForm').submit(function(event) {
    event.preventDefault(); // Prevent the default form submission
    var formData = new FormData(this);

    $.ajax({
        url: '/submit-news/', // Ensure this matches your Django URL pattern
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        headers: { 'X-CSRFToken': getCookie('csrftoken') }, // CSRF token for security
        success: function(response) {
            if (response.success) {
                alert(response.success);
                location.reload(); // Reload the page or redirect to another page
            }
        },
        error: function(xhr) {
            var errors = xhr.responseJSON.error;
            if (errors) {
                alert('Errors: ' + JSON.stringify(errors));
            } else {
                alert('An unexpected error occurred.');
            }
        }
    });
});

// Utility function to get CSRF token
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === name + '=') {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
