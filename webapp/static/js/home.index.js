function onSearchListClick() {
    let item = $("#searchInput").getSelectedItemData();
    window.location = baseUrl + `/database/${item["table"]}/${item["code"]}`
}

var searchOptions = {
    url: function(string) {
        return baseUrl + "/database/search?s=" + string 
    },
    getValue: "name",
    minCharNumber: 1,
    list: {
        maxNumberOfElements: 30,
        showAnimation: {
            type: "slide", //normal|slide|fade
            time: 500,
            callback: function() {}
        },

        hideAnimation: {
            type: "slide", //normal|slide|fade
            time: 400,
            callback: function() {}
        },
        onClickEvent: onSearchListClick,
    },
    requestDelay: 150,
    template: {
        type: "custom",
        method: function(name, item) {
            return `
            <a href="/database/${item.table}/${item.code}" class="d-flex align-items-center">
                <img src="${baseUrl}/static/img/item_icons/${item.icon}">
                <span class="ml-1">${name}</span>
            </a>
            `
        }
    },
}

$("#searchInput").easyAutocomplete(searchOptions);
// Triggers events once because animation isn't shown first time.. bug
$("#eac-container-searchInput").trigger("show.eac");
$("#eac-container-searchInput").trigger("hide.eac")