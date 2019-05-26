$.get('api/leak', (data) => {
    $("#secret_ciphertext").text(data)
})

$( document ).ready(() => {
    $("#btn_encrypt").click(() => {
        $.ajax('api/encrypt', {
            data: JSON.stringify({'data': $("#encrypt_input").val()}),
            contentType: "application/json",
            type: "POST",
            success: (data) => {
                $("#encrypt_box").text(data)
            }
        })
    })

    $("#btn_verify").click(() => {
        $.ajax('api/verify', {
            data: JSON.stringify({'data': $("#flag_input").val()}),
            contentType: "application/json",
            type: "POST",
            success: (data) => {
                $("#verify_box").text(data)
            }
        })
    })
})
