var currentPage = window.location.hash ? parseInt(window.location.hash.substring(1)) : 0

handleActivePageNumber = () => {
    window.location.hash = currentPage
    updateTable({}, currentPage)
    const pageButton = document.querySelector('#page-number')
    pageButton.innerHTML = currentPage + 1
}

const setCurrentPage = (pageNum) => {
    currentPage = pageNum
    handleActivePageNumber()
    handlePageButtonsStatus()
}


const handlePageButtonsStatus = () => {
    document.querySelector('#paginate-prev').disabled = currentPage === 0
}

const prevPage = () => {
    if (currentPage > 0) {
        setCurrentPage(currentPage - 1)
    }
}

const nextPage = () => {
    setCurrentPage(currentPage + 1)
}

document.addEventListener('DOMContentLoaded', () => {
    setCurrentPage(currentPage)
    handlePageButtonsStatus()
})