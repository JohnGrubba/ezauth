function sendEmail() {
    console.log('Email sent')
    const html = tinymce.activeEditor.getContent()
    console.log(html)
}