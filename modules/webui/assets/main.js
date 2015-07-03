function do_command(item, command, val) {
    var data = {};
    data[item] = command;

    if (val != undefined) {
	data["value"] = val;
    }
    $.get("/CMD", data);
}

$(function() {
    $(".command").each(function() {
	var elm = $(this);
	elm.on(elm.data("event"), function() {
	    if (elm.data("use-val") == "true") {
		do_command(elm.data("item"), elm.data("command"), elm.val());
	    } else {
		do_command(elm.data("item"), elm.data("command"));
	    }
	});
    });
});
