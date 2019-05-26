$( document ).ready(() => {
    $("#btn_encrypt").click(() => {
        $.ajax('api/encrypt', {
            data: JSON.stringify({'data': btoa($("#message_input").val())}),
            contentType: "application/json",
            type: "POST",
            success: (data) => {
                $("#encrypted_box").text(data)
            }
        })
    })

    $("#btn_verify").click(() => {
        $.ajax('api/verify', {
            data: JSON.stringify({'flag': $("#flag_input").val()}),
            contentType: "application/json",
            type: "POST",
            success: (data) => {
                $("#verify_box").text(data)
            }
        })
    })
})
