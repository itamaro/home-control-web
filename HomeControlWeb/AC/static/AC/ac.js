 $(function() {
	
	init();
	
	function send_ac_command(btn, pwr){
		$(btn).button('loading');
		$.get("command?" + $.param({"key": $.url().param('key'),
					"mode": $('#acMode').val(),
					"fan": $('#acFan').val(),
					"temp": $('#acTemp').val(),
					"power": pwr}), function(content){
			$("#acDebugArea").html(
				$("<div />").addClass("alert alert-info alert-dismissable").html(
				$("<button />").addClass("close").attr({"type": "button",
				"data-dismiss": "alert", "aria-hidden": "true"}).html("&times"))
				.append('Arduino Response: "' + content + '"'));
			$("#acDebugArea").show();
			if ("Beep Timeout" == content){
				alert_class = "alert-danger";
				msg = "Could not verify command. You should probably try again.";
			}else if ("Success" == content){
				alert_class = "alert-success";
				msg = "Command executed successfully";
			}
			$("#acFeedbackArea").html(
				$("<div />").addClass("alert alert-dismissable").addClass(alert_class).html(
				$("<button />").addClass("close").attr({"type": "button",
				"data-dismiss": "alert", "aria-hidden": "true"}).html("&times"))
				.append(msg));
			$("#acFeedbackArea").show();
			$(btn).button('reset');
		});
	}
	
	function init(){
		// bind click to send A/C power toggle button
		$("#btnAcPower").click(function(){
			send_ac_command("#btnAcPower", "toggle");
		});
		// bind click to send A/C settings update button
		$("#btnAcUpdate").click(function(){
			send_ac_command("#btnAcUpdate", "leave");
		});
		
		$('.selectpicker').selectpicker();
	}
	
});
