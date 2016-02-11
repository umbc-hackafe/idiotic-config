function do_api(url, data) {
    console.log('API REQUEST ' + url);
    $.get(url, data);
}

function do_command(item, command, val) {
    var data = {};

    if (val != undefined) {
	  data["val"] = val;
    }
    do_api("/api/item/" + item + "/command/" + command, data);
}

function do_scene(scene, action) {
    do_api("/api/scene/" + scene + "/command/" + (action?action:""));
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
