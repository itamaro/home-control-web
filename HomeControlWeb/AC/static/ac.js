 $(function() {
	
	init();
	
	function updateImage(){
		$("#btnLoadImage").button('loading');
		$('#webcamArea').html('<img src="/static/img/loading.gif" />');
		$.get("/AC/webcam", function(content){
			$('#webcamArea').html(content);
			$("#btnLoadImage").button('reset');
		});
	}
	
	function updateImage__ProxyMethod(){
		$('#webcamArea').html('<img src="/AC/webcam.png" />');
	}
	
	function init(){
		// bind click to update image button
		$("#btnLoadImage").click(function(){
			updateImage();
		});
		// bind click to send A/C command button
		$("#btnSendAcCommand").click(function(){
			$("#btnSendAcCommand").button('loading');
			$.get("/AC/command", function(content){
				$('#acCommandArea').html(content);
				$("#btnSendAcCommand").button('reset');
			});
		});
		
		updateImage();
	}
	
});
