function showUpgrade(num) {
    $(".upgrade").hide();
    let selector = ".upgrade#" + num;
    $(selector).show();
}

function onSliderChange() {
    var val = $("#levelSlider").val()
    $("#sliderValue").html(val.toString());
    $("#sliderValue").attr("class", val);
    showUpgrade(val);
}

$(".upgrade").hide();
$(".slider").bind("input", onSliderChange)

onSliderChange();