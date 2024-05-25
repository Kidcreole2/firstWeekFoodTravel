$(document).ready(() => {
    $('.order-upworked button').click((e) => {
        let id = e.target.id
        $.ajax({
            method: "POST",
            dataType: "html",
            url: `/order/update/${id}`,
            data: {
                status: "waiting kitchen"
            },
            success: () => {
                alert("Успешно отправлено на кухню")
                $(`#order_${id}`).hide(50)
            }
        })
    })

    $('input.on-kitchen').click((e) => {
        let id = e.target.id
        $.ajax({
            method: "POST",
            dataType: "html",
            url: `/order/update/${id}`,
            data: {
                status: "on kitchen"
            },
            success: () => {
                let order = $(`#order_${id}`)
                $(`order_${id}`).remove()
                $('.in-progress ul').append(order)
            }
        })
    })

    $('input.wait-courier').click((e) => {
        let id = e.target.id
        $.ajax({
            method: "POST",
            dataType: "html",
            url: `/order/update/${id}`,
            data: {
                status: "wait courier"
            },
            success: () => {
                let order = $(`#order_${id}`)
                $(`order_${id}`).hide(20).remove()
                $('div.wait-courier ul.orders-list').append(order)
            }
        })
    })

    $('input.in-deliver').click((e) => {
        let id = e.target.id
        $.ajax({
            method: "POST",
            dataType: "html",
            url: `/order/update/${id}`,
            data: {
                status: "in deliver"
            },
            success: () => {
                $(`order_${id}`).hide(20).remove()
            }
        })
    })

    $('.in-deliver button').click((e) => {
        let id = e.target.id
        $.ajax({
            method: "POST",
            dataType: "html",
            url: `/order/update/courier/${id}`,
            data: {
                status: "in deliver"
            },
            success: () => {
                $(`order_${id}`).hide(20).remove()
            }
        })
    })
    $('.delivered button').click((e) => {
        let id = e.target.id
        $.ajax({
            method: "POST",
            dataType: "html",
            url: `/order/update/${id}`,
            data: {
                status: "delivered"
            },
            success: () => {
                $(`order_${id}`).hide(20).remove()
            }
        })
    })
})