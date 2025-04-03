/**
 * 
 * @param {*} user_id 
 * @returns User Object
 * 
 *  Those fields are always returned:
 * {
  "_id": "67ee3a13affd83f823404ce6",
  "username": "string",
  "email": "user@example.com",
  "createdAt": "2025-04-03T07:34:43.351Z"
 }
 
    Additional fields should also be displayed and changeable.
 */
async function fetchUserDetail(user_id) {
    const data = await (await fetch(`../../internal/profile`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "internal-api-key": sessionStorage.getItem('apiKey')
        },
        body: JSON.stringify({
            user_id: user_id
        })
    })).json()
    return data
}

// Update user details
async function updateUserDetail(userData) {
    try {
        const response = await fetch(`../../internal/profile`, {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json",
                "internal-api-key": sessionStorage.getItem('apiKey')
            },
            body: JSON.stringify({
                internal_req: {
                    user_id: userData.user_id
                },
                update_data: userData
            })
        })

        return response
    } catch (error) {
        console.error("Error updating user:", error)
        throw error
    }
}

// Delete user
async function deleteUser(userId) {
    try {
        const response = await fetch(`../../internal/removeuser?user_id=${userId}`, {
            method: "DELETE",
            headers: {
                "internal-api-key": sessionStorage.getItem('apiKey')
            }
        })

        return await response.status === 204
    } catch (error) {
        console.error("Error deleting user:", error)
        throw error
    }
}

// Get URL parameters
function getUrlParams() {
    const queryString = window.location.search
    const urlParams = new URLSearchParams(queryString)
    return urlParams
}

// Display user data in form
function displayUserData(userData) {
    document.getElementById('user-id').value = userData._id || ''
    document.getElementById('username').value = userData.username || ''
    document.getElementById('email').value = userData.email || ''
    document.getElementById('created-at').value = new Date(userData.createdAt).toLocaleString() || ''

    // Handle additional fields
    const additionalFieldsContainer = document.getElementById('additional-fields')
    additionalFieldsContainer.innerHTML = '' // Clear existing fields

    Object.keys(userData).forEach(key => {
        // Skip the standard fields already displayed
        if (['_id', 'username', 'email', 'createdAt'].includes(key)) {
            return
        }

        const formGroup = document.createElement('div')
        formGroup.className = 'form-group'

        const label = document.createElement('label')
        label.setAttribute('for', key)
        label.textContent = key.charAt(0).toUpperCase() + key.slice(1) + ':'

        const input = document.createElement('input')
        input.setAttribute('type', 'text')
        input.setAttribute('id', key)
        input.setAttribute('name', key)
        input.value = userData[key]

        formGroup.appendChild(label)
        formGroup.appendChild(input)
        additionalFieldsContainer.appendChild(formGroup)
    })
}

// Collect form data
function collectFormData() {
    const formData = {
        user_id: document.getElementById('user-id').value,
        username: document.getElementById('username').value,
        email: document.getElementById('email').value
    }

    // Get values from additional fields
    const additionalFieldsContainer = document.getElementById('additional-fields')
    const additionalInputs = additionalFieldsContainer.querySelectorAll('input')

    additionalInputs.forEach(input => {
        formData[input.id] = input.value
    })

    return formData
}

// Show status message
function showStatusMessage(message, isError = false) {
    const statusElement = document.getElementById('status-message')
    statusElement.textContent = message
    statusElement.classList.remove('hidden', 'success', 'error')
    statusElement.classList.add(isError ? 'error' : 'success')

    // Hide message after 5 seconds
    setTimeout(() => {
        statusElement.classList.add('hidden')
    }, 5000)
}

// Initialize the page
async function initPage() {
    const loadingContainer = document.getElementById('loading-container')
    const errorContainer = document.getElementById('error-container')
    const userDetailsContainer = document.getElementById('user-details-container')

    try {
        const urlParams = getUrlParams()
        const userId = urlParams.get('user_id')

        if (!userId) {
            throw new Error('User ID is missing in URL parameters')
        }

        const userData = await fetchUserDetail(userId)

        if (!userData || userData.error) {
            throw new Error(userData.error || 'Failed to fetch user data')
        }

        displayUserData(userData)

        // Hide loading, show user details
        loadingContainer.style.display = 'none'
        userDetailsContainer.style.display = 'block'

        // Set up event listeners
        setupEventListeners(userId)

    } catch (error) {
        console.error('Error initializing page:', error)
        loadingContainer.style.display = 'none'
        errorContainer.style.display = 'block'
        document.querySelector('.error-message').textContent = error.message || 'Error loading user details.'
    }
}

// Set up event listeners
function setupEventListeners() {
    // Form submission
    document.getElementById('user-form').addEventListener('submit', async (e) => {
        e.preventDefault()

        try {
            const formData = collectFormData()
            const result = await updateUserDetail(formData)
            if (result.status !== 200) {
                const errorData = await result.json()
                showStatusMessage(errorData.detail, true)
            } else {
                showStatusMessage('User updated successfully!')
            }
        } catch (error) {
            console.error('Error updating user:', error)
            showStatusMessage(`Error updating user: ${error.message}`, true)
        }
    })

    // Delete button
    document.getElementById('delete-button').addEventListener('click', async () => {
        if (confirm('Are you sure you want to delete this user? This action cannot be undone.')) {
            try {
                const userId = document.getElementById('user-id').value
                await deleteUser(userId)
                showStatusMessage('User deleted successfully!')

                // Redirect back to admin page after a brief delay
                setTimeout(() => {
                    window.location.href = '/admin'
                }, 2000)
            } catch (error) {
                console.error('Error deleting user:', error)
                showStatusMessage(`Error deleting user: ${error.message}`, true)
            }
        }
    })

    // Retry button
    document.getElementById('retry-button').addEventListener('click', () => {
        document.getElementById('error-container').style.display = 'none'
        document.getElementById('loading-container').style.display = 'block'
        initPage()
    })
}

// Handle profile picture
document.addEventListener('DOMContentLoaded', function () {
    // Get user_id from URL parameters
    const urlParams = new URLSearchParams(window.location.search)
    const userId = urlParams.get('user_id')

    if (userId) {
        // Set the profile picture src
        const profilePicture = document.getElementById('user-profile-picture')
        if (profilePicture) {
            profilePicture.src = `../../cdn/${userId}.webp`
        }
    }
})

// Initialize the page when DOM is fully loaded
document.addEventListener('DOMContentLoaded', initPage)