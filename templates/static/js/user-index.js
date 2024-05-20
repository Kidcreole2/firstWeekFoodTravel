$(document).ready(() => {
    $('.good-card').before().click((event) => {
        let id = $(event.target).attr('id')
        console.log('before', id)
    });
})