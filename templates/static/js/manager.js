
$(document).ready(() => {
    $(".order-info").hide()
    $("h4.check").click((e) => {
        let id = e.target.id
        $(`#order-info_${id}`).toggle(250)
        $(`h4#${id}`).toggleClass("active")
    })
    $('.order-others').click((e) => {
        let id = e.target.id
        $(`div[data-order-id="${id}"]`).toggle(250)
    })
})
