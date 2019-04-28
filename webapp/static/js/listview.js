const observer = lozad(); // lazy loads elements with default selector as '.lozad'
observer.observe();

var order;

$("#orderSelect").bind("change", function() {
    order = this.value;
    applySort();
});
$("#orderSelect").trigger("change");

$("#filterSelect").bind("change", applyFilter);
$("#filterSelect").trigger("change");

$("#sortSelect").bind("change", applySort);
$("#sortSelect").trigger("change");

$(".search-input").on("keyup", applySearch)

$("#viewSelect").on("change", function() {
    let val = $("#viewSelect").val();
    if (val == "unfiltered") {
        let newUrl = baseUrl + "?filtered=False"
        console.log(newUrl);
        $(location).attr('href', newUrl);
    }
    else {
        $(location).attr('href', baseUrl);
    }
});

// Prevents Dropdown Menu from being closed when clicked on
// Can only be closed with an outside click.
$(document).on('click', '.dropdown-menu', function (e) {
    e.stopPropagation();
});

function applySearch() {
    let searchString = $(".search-input").val().toLowerCase();
    
    if (searchString.length == 0) {
        applyFilter();
        applySort();
        return
    }

    if (searchString.length < 3) {
        return
    }

    var list = $("span.name");
    
    var matchingItems = [];

    $.each(list, function(index, item) {
        let name = item.innerText.toLowerCase();
        
        if (name.indexOf(searchString) != -1) {
            matchingItems.push($(item).parent().parent().parent())
        }
    });

    $(".flex-item").hide();
    $.each(matchingItems, function(_, item) {
        $(item).show();
    });

    // Updates Dropdown Offets because body height may have changed and a scrollbar
    // is now hidden/shown 
    updateDropdownContentOffsets();

}

function applyFilter() {
    let filter = $("#filterSelect").val()

    if (filter == undefined) {
        // No filter dropdown
        // Functions gets called after search input is cleared -> show all
        $(".flex-item").show();
    }
    
    let v = filter.split(":");

    let filter_name = v[0];
    let filter_value = v[1]

    if (filter_name == "all") {
        $(".flex-item").show();
    }

    else if (filter_name == "location") {
        let counter_filter_value = v[1] == 0 ? 1 : 0;
        // Show
        $(`input[name=${filter_name}][value=${filter_value}]`).parent().parent().show();
        // Hide
        $(`input[name=${filter_name}][value=${counter_filter_value}]`).parent().parent().hide();
    }

    else if (filter_name == "rating_type") {
        $(".flex-item").hide()
        $(`input[name=${filter_name}][value=${filter_value}]`).parent().parent().show();
    }

    else if (filter_name == "class_land" || filter_name == "class_sea") {
        var list = $(`input[name=${filter_name}`);

        $.each(list, function(index, item) {
            if ($(item).val().toLowerCase().indexOf(filter_value) != -1) {
                $(item).parent().parent().show()
            }
            else {
                $(item).parent().parent().hide();
            }
        });
    }
}

function sortByName(a, b) {
    let aName = $(a).val();
    let bName = $(b).val();
    if (order == "asc") {
        return ((aName < bName) ? -1 : ((aName > bName) ? 1 : 0));
    }
    else {
        return ((aName < bName) ? 1 : ((aName > bName) ? -1 : 0));
    }
}

function sortByNumber(a, b) {
    let aNumber = parseInt($(a).val());
    let bNumber = parseInt($(b).val());
    if (order == "asc") {
        return aNumber - bNumber;
    }
    else {
        return bNumber - aNumber;
    }
}

function applySort() {
    let sortBy = $("#sortSelect").val();

    if (sortBy == "added") {
        if (order == "asc") {
            $(".flex-item").css("order", "");
        }
        else {
            $($(".flex-item").get().reverse()).each(function(index, item) {
                $(item).css("order", index);
            });
        }
        return
    }

    var list = $(`input[name=${sortBy}]`)

    // String
    if (sortBy == "name")
        var sortedList = list.sort(sortByName);
    // Anything else sort by number
    else
        var sortedList = list.sort(sortByNumber);

    $.each(sortedList, function(index, item) {
        $(item).parent().parent().css("order", index);
    });
}
