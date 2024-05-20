$(document).ready(() => {
    $(".delete").click((e)=> {
        let id = e.target.id
        $(`li[data-ingr-id='${id}']`).hide(20)
        $.ajax({
            method: "POST",
            url: `/ingridient/delete/${id}`,
            dataType: "html"
        })
    })
})