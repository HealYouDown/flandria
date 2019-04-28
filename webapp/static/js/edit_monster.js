function deleteDrop(event) {
    event.preventDefault();
    let parent = $(this).parent(); // div inside a 
    let item_code = parent.children("input[name=item_code]").val();
    let monster_code = $("input[name=monster_code]").val();

    $.ajax({
        type: "DELETE",
        url: baseUrl + "/database/delete_drop",
        data: JSON.stringify({"monster_code": monster_code, "item_code": item_code}),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(data) {
            if (data["success"]) {
                $(parent).parent().remove();
            }
        },
        error: function(data) {
            alert(data.status + " - " + data.responseJSON.message);
        }
    });
}

function addDrop() {
    let item_code = $("#addDropInput").val();
    let monster_code = $("input[name=monster_code]").val();

    $.ajax({
        type: "PUT",
        url: baseUrl + "/database/add_drop",
        data: JSON.stringify({"monster_code": monster_code, "item_code": item_code}),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(data) {
            location.reload();
        },
        error: function(data) {
            alert(data.status + " - " + data.responseJSON.message);
        }
    });
}


var searchOptions = {
    url: function(string) {
        return baseUrl + "/database/search?s=" + string 
    },
    getValue: "code",
    minCharNumber: 2,
    list: {
        maxNumberOfElements: 30,
        showAnimation: {
            type: "slide", //normal|slide|fade
            time: 400,
            callback: function() {},
        },

        hideAnimation: {
            type: "slide", //normal|slide|fade
            time: 200,
            callback: function() {},
        },
        onShowListEvent: function() {
            $("#addDropInputSpinner").hide();

        },
        onHideListEvent: function() {
            $("#addDropInputSpinner").hide();
        },
    },
    requestDelay: 150,
    template: {
        type: "custom",
        method: function(code, item) {
            return `
            <li class="d-flex align-items-center">
                <img src="${baseUrl}/static/img/item_icons/${item.icon}">
                <span class="ml-1">${item.name} (${code})</span>
            </li>
            `;
        }
    },
    preparePostData: function(data) {
        $("#addDropInputSpinner").show();
    },
}

$(".delete-icon").on("click", deleteDrop);
$("#addDropInput").easyAutocomplete(searchOptions);
$("#addDropButton").on("click", addDrop);