$(document).ready(() => {
    $("button#make-field").click((i, el) => {
        $('.forms').append(`<form method="POST">
                <div class="form-component">
                    <label for="title">Название ингридиента</label>
                    <input id="title" name="title" value=""
                           placeholder="Лосось">
                </div>
            </form>`)

    })
    $("button#send").click((e) => {
        e.preventDefault()
        $("form").each((i, el) => {
            let title = $(el).find("input").val()
            $.ajax({
                method: "POST", dataType: "html", data: {
                    title: title,
                }, success: (data) => {
                    let json_data = JSON.parse(data)
                    alert(json_data.message)
                    window.location.replace(`/goods/update/${json_data.goods_id}`)
                }
            })
        })
    })
})