function sendDropMessage() {
    let message = $("#dropMessageTextarea").val();
    let monster_code = $("input[name=monster_code]").val();

    $.ajax({
        type: "PUT",
        url: baseUrl + "/database/add_drop_message",
        data: JSON.stringify({"monster_code": monster_code, "message": message}),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function() {
            $('#dropMessageDialog').modal('hide');
        },
        error: function(data) {
            $("#dropMessageError").html(data.responseJSON.message);
        }
    });
}
$("#sendDropMessageButton").on("click", sendDropMessage);
