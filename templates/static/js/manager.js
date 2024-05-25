
$(document).ready(() => {
    $(".order-info").hide()
    $("h4.check").click((e) => {
        let id = e.target.id
        $(`#order-info_${id}`).toggle(250)
    })
})