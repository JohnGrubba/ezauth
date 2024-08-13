function capitalizeName(name) {
    return name.replace(/\b(\w)/g, s => s.toUpperCase())
}

async function updateExtensions() {
    const data = await (await fetch(`../../internal/stats`, {
        method: "GET",
        headers: {
            "internal-api-key": sessionStorage.getItem('apiKey')
        }
    })).json()
    let exts_element = document.getElementById("extensions")
    let exts_elm_html = ""
    data.loaded_extensions.forEach(ext => {
        console.log(ext)
        exts_elm_html += `
        <li class="${ext.status ? `` : `down`}">
            <h3 style="display: flex; margin: 0;">
                <span style="line-height: 64px;">${capitalizeName(ext.name)}</span>
                <svg width="64" height="64" viewBox="0 0 100 100" style="display: ${ext.status ? `block` : `none`}; margin-left: auto;">
                    <circle cx="50" cy="50" r="10" fill="green"></circle>
                    <circle class="pulsing-dot" cx="50" cy="50" r="10" fill="green"></circle>
                    <circle class="pulsing-dot" cx="50" cy="50" r="10" fill="green"></circle>
                </svg>
            </h3>
            <div class="description" style="${ext.readme ? `` : `display: none`}">
                <p>${ext.readme ? marked.parse(ext.readme) : ""}</p>
            </div>
        </li>
        `
    })
    exts_element.innerHTML = exts_elm_html

    const extensionItems = document.querySelectorAll('#extensions li')

    extensionItems.forEach(item => {
        item.addEventListener('click', () => {
            item.classList.toggle('active')
        })
    })
}

document.addEventListener('DOMContentLoaded', () => {
    updateExtensions()
})