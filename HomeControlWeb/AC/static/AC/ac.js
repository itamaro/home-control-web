 $(function() {
	
	init();
	
	function init(){
		// bind click to send A/C power toggle button
		$("#btnAcPower").click(function(){
			send_ac_command("#btnAcPower", "0");
		});
		// bind click to send A/C settings update button
		$("#btnAcUpdate").click(function(){
			send_ac_command("#btnAcUpdate", "1");
		});
	}
	
});
	
function send_ac_command(btn, pwr){
	$(btn).button("loading");
	$.get(silly_url(Urls["AC-command"](active_id()) + "?" + $.param({
				"mode": $("#acMode").val(),
				"fan": $("#acFan").val(),
				"temp": $("#acTemp").val(),
				"power": pwr})), function(content){
		$("#acDebugArea").html(
			$("<div />").addClass("alert alert-info alert-dismissable").html(
			$("<button />").addClass("close").attr({"type": "button",
			"data-dismiss": "alert", "aria-hidden": "true"}).html("&times"))
			.append('Arduino Response: "' + content + '"'));
		$("#acDebugArea").show();
		if ("Beep Timeout" == content){
			alert_class = "alert-warning";
			msg = "Could not verify command. You should probably try again.";
		}else if ("Unsupported Command" == content){
			alert_class = "alert-warning";
			msg = "Sorry, but the requested state is not supported yet.";
		}else if ("Success" == content){
			alert_class = "alert-success";
			msg = "Command executed successfully";
		}else{
			alert_class = "alert-danger";
			msg = "Something went terribly wrong... :-(";
		}
		$("#feedbackArea").html(
			$("<div />").addClass("alert alert-dismissable").addClass(alert_class).html(
			$("<button />").addClass("close").attr({"type": "button",
			"data-dismiss": "alert", "aria-hidden": "true"}).html("&times"))
			.append(msg));
		$("#feedbackArea").show();
		$(btn).button('reset');
	});
}
