function getIngridients(ingrsIdsArr) {
    let allhtml = ""
    ingrsIdsArr.forEach((e) => {
        $.ajax({
            method: "POST", async:false, dataType: "json", url: `/ingridient/${e}`, success: (data) => {
                console.log(data)
                allhtml += `<li>${data.title}</li>`
            }, error: (error) => {
                reject(error)
            }
        })
    })
    return allhtml
}
function getGoods(goodsId) {
    let resultData = {}
    $.ajax({
        method: "POST", async: false, dataType: "json", url: `/goods/${goodsId}`, success: (data) => {
            data = {
                html: `<li>${data.name} <span>${data.price}</span></li>`, price: Number(data.price),
            }
            resultData = data
        }
    })
    return resultData
}

 function getData() {
     const cart = localStorage.getItem("cart")
     let json_cart = JSON.parse(cart)
     let htmlCart = ""
     let totalPrice = 0
     json_cart.forEach((el) => {
         console.log(el)

         let goodsData = getGoods(el.goods)
         htmlCart += goodsData.html
         totalPrice += goodsData.price

         let ingridientsData = getIngridients(el.ingridients)
         htmlCart += `<ul> ${ingridientsData} </ul>`
     })

     let data = {
         html: htmlCart, price: totalPrice
     }
     return data
 }

 let data = getData()
$(".order-data > ul").html(data.html)
$("span.total-price").html(data.price)

$(document).ready(() => {
    $("#make-order").click((e) => {
        e.preventDefault()
        let cart = localStorage.getItem("cart")
        // console.log($("textarea[name='comment']").val())
        $.ajax({
            method:"POST",
            dataType: "html",
            data: {
                cart: cart,
                price: data.price,
                comment: $("textarea[name='comment']").val(),
                addressTo: $("input[name='address-to']").val()
            },
            success: (data) => {
                localStorage.clear()
                alert(JSON.parse(data).message)
                window.location.replace("/")
            }
        })
    })
})