const cart = localStorage.getItem('cart')

if (cart) {
    $(".cart").show()
} else {
    $(".cart").hide()
}

$(document).ready(() => {
    $(".good-card").click((e) => {
        let id = $(e.target).attr("id")
        window.location.replace(`/goods/${id}`)
    })

    $(".cart").click((e) => {
        window.location.replace('/order/create')
    })
})

