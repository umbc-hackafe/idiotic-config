function do_command(item, command, val) {
    var data = {};

    if (val != undefined) {
	data["val"] = val;
    }
    $.get("/api/item/" + item + "/command/" + command, data);
}

function do_scene(scene, action) {
    $.get("/api/scene/" + scene + "/command/" + (action?action:""));
}

$(function() {
    $(".command").each(function() {
	var elm = $(this);
	elm.on(elm.data("event"), function() {
	    if (elm.data("use-val")) {
		do_command(elm.data("item"), elm.data("command"), elm.val());
	    } else {
		do_command(elm.data("item"), elm.data("command"));
	    }
	});
    });

    $(".scene-control").each(function() {
	var elm = $(this);
	elm.click(function(evt) {
	    do_scene(elm.data("scene"), elm.data("action"));
	});
    });

    $("form").submit(function(){return false;});
});
