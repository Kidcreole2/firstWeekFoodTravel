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
                window.location.reload()
            }
        })
    })

    $('.order-deprecated').click(function () {
        let id = this.id
        $.ajax({
            method: "POST",
            dataType: "html",
            url: `/order/update/${id}`,
            data: {
                status: "deprecated"
            },
            success: () => {
                alert("Заказ отменен")
                $(`#order_${id}`).hide(50)
                window.location.reload()
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
                window.location.reload()
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
                window.location.reload()
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
                window.location.reload()
            }
        })
    })

    $('.in-delivery button').click((e) => {
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
                window.location.reload()
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
                alert("Заказ доставлен")
                window.location.reload()
            }
        })
    })
})
