$(document).ready(function () {
    $("#view").change(function () {
        $("#view_form").submit();
    });

    var queryString = window.location.search;
    var params = new URLSearchParams(queryString);

    var view = params.get("view");
    if (view === "" || view === null || view === undefined || (view !== "10" && view !== "20" && view !== "30")) {
        view = 10;
    }
    $("#view").val(view);

    var sort = params.get("sort");
    if (sort === "" || sort === null || sort === undefined) {
        sort = "new-to-old";
    }
    $("#sort").val(sort);

    var status = params.get("status");
    if (status === "" || status === null || status === undefined) {
        status = "all";
    }
    $("#status").val(status);

    var type = params.get("type");
    if (type === "" || type === null || type === undefined) {
        type = "all";
    }
    $("#type").val(type);

    var room = params.getAll("room_count");
    $('input[type="checkbox"]').prop("checked", false);
    room.forEach(function (value) {
        $('input[type="checkbox"][value="' + value + '"]').prop("checked", true);
    });

    var min_price = params.get("min_price");
    var max_price = params.get("max_price");
    $("#min_price").val(min_price);
    $("#max_price").val(max_price);

    var min_metre = params.get("min_metre");
    var max_metre = params.get("max_metre");
    $("#min_metre").val(min_metre);
    $("#max_metre").val(max_metre);

    var min_location_floor = params.get("min_location_floor");
    var max_location_floor = params.get("max_location_floor");
    $("#min_location_floor").val(min_location_floor);
    $("#max_location_floor").val(max_location_floor);

    var min_building_years = params.get("min_building_years");
    var max_building_years = params.get("max_building_years");
    $("#min_building_years").val(min_building_years);
    $("#max_building_years").val(max_building_years);


    $("#filter-form").submit(function (event) {
        event.preventDefault();
    
        var queryParams = [];
        var selectedRoomCounts = [];
    
        $("form#filter-form :input").each(function () {
            var element = $(this);
            var name = element.attr("name");
            var value = element.val();
    
            if (element.is(':checkbox')) {
                if (element.is(":checked")) {
                    selectedRoomCounts.push(element.val());
                }
            } else {
                if (value.trim() !== "") {
                    queryParams.push(name + "=" + encodeURIComponent(value));
                }
            }
        });
    
        if (selectedRoomCounts.length > 0) {
            queryParams.push("room_count=" + selectedRoomCounts.join(","));
        }
    
        var queryString = queryParams.join("&");
        var currentUrl = window.location.href.split("?")[0];
        var newUrl = currentUrl + (queryParams.length > 0 ? "?" + queryString : "");
    
        window.location.href = newUrl;
    });
});