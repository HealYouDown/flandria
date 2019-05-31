function addBuild() {
    let title = $("input[name=build_title]").val();
    let description = $("textarea[name=build_description]").val();
    let public = $("input[name=public_checkbox]").is(":checked");
    let hash = location.hash.replace("#", "");
    let class_ = $('#classSelect option').eq(0).val(); // base class
    if (class_ == "base ship") {
        class_ = "ship";
    }
    let selectedClass = $("#classSelect").val();
    let selectedLevel = $("#levelSelect").val();

    $.ajax({
        type: "PUT",
        url: baseUrl + "/planner/add_build",
        data: JSON.stringify({
            "title": title, 
            "description": description, 
            "public": public,
            "class": class_, 
            "hash": hash,
            "selected_class": selectedClass,
            "selected_level": selectedLevel,
        }),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(response) {
            $('#saveBuildModal').modal('hide');
        },
        error: function(response) {
            console.log(repsonse);
            alert("Error when trying to add this build - see console")
        },
    });
}

function deleteBuild(event) {
    event.preventDefault();

    let hiddenInput = $(this).parent().parent().parent().find("input[name=build_id]")[0];
    let buildId = $(hiddenInput).val()

    $.ajax({
        type: "DELETE",
        url: baseUrl + "/planner/delete_build",
        data: JSON.stringify({"build_id": buildId}),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(response) {
            if (response["success"]) {
                let buildId = response["build_id"];
                $(`input[value=${buildId}]`).parent().parent().hide();
            }
        },
        error: function(response) {
            alert(response.responseJSON["error"])
        }
    });
}

/* Build list */

function setStarValue(buildId, increment) {
    let star = $(`input[value=${buildId}]`).siblings().find(".build-star");
    
    star.toggleClass("voted");

    let levelSpan = $(star.children()[0]);
    let currentCount = parseInt($(levelSpan).html());

    $(levelSpan).html(currentCount + increment)
}

function onBuildStarClick(event) {
    if (!$(this).hasClass("logged-in"))
        return

    event.preventDefault();

    let hiddenInput = $(this).parent().parent().parent().find("input[name=build_id]")[0];
    let buildId = $(hiddenInput).val()

    if ($(this).hasClass("voted")) {
        // Remove star
        $.ajax({
            type: "DELETE",
            url: baseUrl + "/planner/delete_star",
            data: JSON.stringify({"build_id": buildId}),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(response) {
                if (response["success"]) {
                    setStarValue(response["build_id"], -1)
                }
            }
        });
    }
    else {
        // Add star
        $.ajax({
            type: "PUT",
            url: baseUrl + "/planner/add_star",
            data: JSON.stringify({"build_id": buildId}),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(response) {
                if (response["success"]) {
                    setStarValue(response["build_id"], 1)
                }
            }
        });
    }
}
