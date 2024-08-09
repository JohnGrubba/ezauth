document.addEventListener('DOMContentLoaded', () => {
    var elm = document.createElement("div")
    elm.id = "modal-backdrop"
    elm.className = "modal-backdrop"
    elm.innerHTML = `
    <div id="api-key-modal" class="modal">
        <h2>Enter API Key</h2>
        <input type="password" id="api-key-input" placeholder="Enter your API key">
            <button id="submit-api-key">Submit</button>
    </div>
    `
    document.body.append(elm)

    const modalBackdrop = document.getElementById('modal-backdrop')
    const apiKeyInput = document.getElementById('api-key-input')
    const submitButton = document.getElementById('submit-api-key')

    if (!sessionStorage.getItem('apiKey')) {
        modalBackdrop.style.display = 'flex'
    }

    submitButton.addEventListener('click', () => {
        const apiKey = apiKeyInput.value
        if (apiKey) {
            sessionStorage.setItem('apiKey', apiKey)
            modalBackdrop.style.display = 'none'
            location.reload()
        } else {
            alert('Please enter a valid API key.')
        }
    })
})