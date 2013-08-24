 $(function() {
	
	init();
	
	function get_key_url(){
		var key = $.url().param('key');
		return (key ? '?key=' + key : '');
	}
	
	function updateImage(){
		$("#btnLoadImage").button('loading');
		$('#webcamArea').html('<img src="/static/img/loading.gif" />');
		$.get("/AC/webcam" + get_key_url(), function(content){
			$('#webcamArea').html(content);
			$("#btnLoadImage").button('reset');
		});
	}
	
	function updateImage__ProxyMethod(){
		$('#webcamArea').html('<img src="/AC/webcam.png' + get_key_url() + '" />');
	}
	
	function init(){
		// bind click to update image button
		$("#btnLoadImage").click(function(){
			updateImage();
		});
		// bind click to send A/C command button
		$("#btnSendAcCommand").click(function(){
			$("#btnSendAcCommand").button('loading');
			$.get("/AC/command" + get_key_url(), function(content){
				$('#acCommandArea').html(content);
				$("#btnSendAcCommand").button('reset');
			});
		});
		
		updateImage();
	}
	
});
