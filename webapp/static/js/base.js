const baseUrl = document.location.protocol + "//" + document.location.hostname + ":" + document.location.port
const dropdownHeight = 220;

// Hamburger button
$('.navbar-button').on('click', function () {

    $('.animated-icon').toggleClass('open');
    $("body").toggleClass("noscroll")

    if ($(".animated-icon").hasClass("open")) {
        // Show overlay menu
        $(".nav-overlay-menu").css("display", "block")
    }
    else {
        // hide overlay menu
        $(".nav-overlay-menu").css("display", "none")
    }
});

// Normal Navigation
$(".nav-list-item-link-dropdown").on("mouseover", showDropdown);
$(".nav-dropdown-background-reset").bind("mouseenter", hideDropdown);
$(".nav-list-item-link:not(.nav-list-item-link-dropdown)").on("mouseover", hideDropdown)

function hideDropdown() {
    $(".nav-dropdown-background-reset").css("pointer-events", "none"); // Ignore all events and pass them through

    $(".nav-dropdown-background").stop();
    $(".nav-dropdown-content").stop();

    $(".nav-dropdown-content").css("display", "none");
    $(".nav-dropdown-background").animate({"height": 0});
}

function showDropdown() {
    $(".nav-dropdown-content").css("display", "none");

    let dropdownContent = $(this).next();

    $(".nav-dropdown-background-reset").css("pointer-events", "auto"); // Is now able to revive events
    $(".nav-dropdown-background").animate({"height": dropdownHeight});

    dropdownContent.delay(175)
        .queue(function (next) { 
            $(this).fadeIn();
            next(); 
        });
}

// Overlay navigation

$(".nav-list-overlay-item-link-dropdown").on("click", function() {
    let dropdownContent = $(this).next();
    console.log(dropdownContent);
    dropdownContent.toggle("open");
});