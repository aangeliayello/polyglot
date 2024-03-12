var lastFocusedElement = null;

document.addEventListener('focus', function (e) {
    if ((e.target.tagName === 'INPUT' && e.target.type === 'text') || e.target.tagName === 'TEXTAREA') {
        lastFocusedElement = e.target;
    }
}, true);

// Function to insert character into the last focused text field or textarea
function insertChar(character) {
    if (lastFocusedElement !== null) {
        // Insert character at current cursor position in input field or textarea
        const start = lastFocusedElement.selectionStart;
        const end = lastFocusedElement.selectionEnd;
        lastFocusedElement.value = lastFocusedElement.value.substring(0, start) + character + lastFocusedElement.value.substring(end);
        // Move the cursor to right after the inserted character
        lastFocusedElement.selectionStart = lastFocusedElement.selectionEnd = start + character.length;
        // Return focus to the last focused element after inserting character
        lastFocusedElement.focus();
    }
}

// Global Variable
translationId = -1;

function closeEditModal() {
    document.getElementById('editModal').style.display = 'none';
}

function saveEdit() {
    const editedJson = document.getElementById('editData').value;

    const translationId = this.getAttribute('data-translation-id');
    try {
        const translation = JSON.parse(editedJson);

        // Example endpoint URL - adjust based on your actual URL structure and how you pass the translation ID
        const updateUrl = `/update-translation/${translationId}/`;

        fetch(updateUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                // Include CSRF token header if necessary; Django example shown below
                'X-CSRFToken': getCookie('csrftoken') // Function to get CSRF token from cookies
            },
            body: JSON.stringify(translation)
        })
        .then(response => {
            if (response.ok) {
                return response.json(); // or .text() if the response is not JSON
            }
            throw new Error('Network response was not ok.');
        })
        .then(data => {
            console.log(data); // Handle success; maybe close the modal and refresh part of your page
            closeEditModal();
            location.reload(); // Reload page to pull edited json again
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
        });
    } catch (error) {
        alert('Invalid JSON');
    }
}

// Function to get CSRF token, necessary if you are using Django
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function findTranslationIndex(translationsData, translationId) {
    return translationsData.findIndex(translation => translation.translation_id === translationId);
}

document.addEventListener('DOMContentLoaded', function() {

    console.log(translationsData);
    // Function to handle the edit action
    function editTranslation(event) {
        const button = event.target;
        const translationId = parseInt(button.getAttribute('data-translation-id'));
        
        // Retrieve the translation data using the passed ID
        translation_indx = findTranslationIndex(translationsData, translationId)
        if (translation_indx < 0) {
            console.error('Translation data not found for id:', translationId);
            return;
        }
        const translation = translationsData[translation_indx];
        const jsonText = JSON.stringify(translation, null, 4);
        document.getElementById('editData').value = jsonText;
        document.getElementById('editModal').style.display = 'block';
        document.getElementById('saveEditButton').setAttribute('data-translation-id', translationId);

    }
    
    // Attach the editTranslation function as an event listener to each edit button
    const editButtons = document.querySelectorAll('.edit-btn');
    editButtons.forEach(button => {
        button.addEventListener('click', editTranslation);
    });

    document.getElementById('saveEditButton').addEventListener('click', saveEdit);

});
