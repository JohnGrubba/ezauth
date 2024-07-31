const users_table = document.querySelector('#users-table')
const tbody = users_table.querySelector('tbody')

const stats_table = document.querySelector('#stats-table')
const tbody_stats = stats_table.querySelector('tbody')

const no_icon = "🟥"
const ye_icon = "🟩"

function delete_modal(id) {
    const modal = document.getElementById('delete-modal')
    const confirmButton = modal.querySelector('.confirm')
    const cancelButton = modal.querySelector('.cancel')

    confirmButton.onclick = () => {
        fetch(`../internal/removeuser?user_id=${id}`, {
            method: "DELETE",
            headers: {
                "internal-api-key": sessionStorage.getItem('apiKey')
            }
        }).then(() => {
            updateTable({}, 0)
            modal.style.display = 'none'
        })
    }

    cancelButton.onclick = () => {
        modal.style.display = 'none'
    }

    modal.style.display = 'flex'
}

function restore_modal(id) {
    const modal = document.getElementById('restore-modal')
    const confirmButton = modal.querySelector('.confirm')
    const cancelButton = modal.querySelector('.cancel')

    confirmButton.onclick = () => {
        fetch(`../internal/restoreuser?user_id=${id}`, {
            method: "PUT",
            headers: {
                "internal-api-key": sessionStorage.getItem('apiKey')
            }
        }).then(() => {
            updateTable({}, 0)
            modal.style.display = 'none'
        })
    }

    cancelButton.onclick = () => {
        modal.style.display = 'none'
    }

    modal.style.display = 'flex'
}

async function updateTable(query, page) {
    fetch(`../internal/users`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "internal-api-key": sessionStorage.getItem('apiKey')
        },
        body: JSON.stringify({
            query: query,
            page: page,
            sort: { createdAt: -1 }
        })
    }).then(response => response.json())
        .then(data => {
            console.log(data)
            let tbody_new = document.createElement('tbody')
            data.forEach(user => {
                const tr = document.createElement('tr')
                tr.innerHTML = `
                    <td data-label="E-Mail">${user.email}</td>
                    <td data-label="Username">${user.username}</td>
                    <td data-label="Password">${user.password ? ye_icon : no_icon}</td>
                    <td data-label="OTP 2FA">${user["2fa_secret"] ? ye_icon : no_icon}</td>
                    <td data-label="Google Oauth">${user.google_uid ? ye_icon : no_icon}</td>
                    <td data-label="Github Oauth">${user.github_uid ? ye_icon : no_icon}</td>
                    <td data-label="Created At">${new Date(user.createdAt).toLocaleDateString(navigator.language, { weekday: "long", year: "numeric", month: "short", day: "numeric" })}</td>
                    <td data-label="Deletion on">${user.expiresAfter ?
                        new Date(user.expiresAfter).toLocaleDateString(navigator.language, { year: "numeric", month: "short", day: "numeric" })
                        : no_icon}</td>
                    <td data-label="Actions" class="actions">
                        <div>
                            <button class="delete" onclick="delete_modal('${user._id}')">Delete</button>
                            <button class="update" onclick="update_modal('${user._id}')">Update</button>
                            ${user.expiresAfter ? `<button class="restore" onclick="restore_modal('${user._id}')">Restore</button>` : ''}
                        </div>
                    </td>
                `
                if (user.expiresAfter) {
                    tr.style.backgroundColor = "#fff1db"
                }
                if (!user.password && !user.google_uid && !user.github_uid) {
                    tr.style.backgroundColor = "#ffdbdb"
                }
                tbody_new.appendChild(tr)
            })
            tbody.innerHTML = tbody_new.innerHTML
        })
}

async function update_stats() {
    fetch(`../internal/stats`, {
        method: "GET",
        headers: {
            "internal-api-key": sessionStorage.getItem('apiKey')
        }
    }).then(response => response.json())
        .then(data => {
            console.log(data)
            const html = `
            <tr>
                <td data-label="Total Users">${data.users}</td>
                <td data-label="Pending Users">${data.pending_users}</td>
                <td data-label="Total Sessions">${data.sessions}</td>
                <td data-label="Ø Sessions / User">${Number(data.avg_sess_per_usr).toFixed(2)}</td>
                <td data-label="Total Google OAuth">${data.google_oauth_count}</td>
                <td data-label="Total Github OAuth">${data.github_oauth_count}</td>
            </tr>
                `
            tbody_stats.innerHTML = html
        })
}

document.addEventListener('DOMContentLoaded', () => {
    const modalBackdrop = document.getElementById('modal-backdrop')
    const apiKeyInput = document.getElementById('api-key-input')
    const submitButton = document.getElementById('submit-api-key')

    if (!sessionStorage.getItem('apiKey')) {
        modalBackdrop.style.display = 'flex'
    } else {
        Promise.all([updateTable({}, 0), update_stats()])
    }

    submitButton.addEventListener('click', () => {
        const apiKey = apiKeyInput.value
        if (apiKey) {
            sessionStorage.setItem('apiKey', apiKey)
            modalBackdrop.style.display = 'none'
            updateTable({}, 0)
            update_stats()
        } else {
            alert('Please enter a valid API key.')
        }
    })
})