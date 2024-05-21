$(document).ready(() => {
    $("button.add-to-cart").click((e) => {
        let id = $(e.target).attr("id")
        console.log(id)
        let ingrs = []
        $("input[type='checkbox']:checked").each((i, el) => {
            ingrs.push($(el).attr("id"))
        })
        let food = {
            goods: id,
            ingridients: ingrs
        }
        let cart = localStorage.getItem("cart")
        if (cart) {
            let cart_json = JSON.parse(cart)
            cart_json.push(food)
            localStorage.setItem('cart', JSON.stringify(cart_json))
        } else {
            localStorage.setItem("cart", JSON.stringify([food]))
        }
        window.location.replace("/")
    })
})