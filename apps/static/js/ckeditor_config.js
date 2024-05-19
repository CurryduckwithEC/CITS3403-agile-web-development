document.addEventListener('DOMContentLoaded', function () {
    CKEDITOR.replace('content-editor', {
        enterMode: CKEDITOR.ENTER_BR,
        shiftEnterMode: CKEDITOR.ENTER_P
    });
});