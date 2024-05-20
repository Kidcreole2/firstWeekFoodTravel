$(document).ready(() => {
    $('.delete').click((e) => {
        let id = e.target.id
        $(`div[data-good-id="${id}"]`).hide(20)
        $.ajax({
            method: "POST",
            url: `/goods/delete/${id}`,
            dataType: "html",
        })
    })
})