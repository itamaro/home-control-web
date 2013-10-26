 $(function() {
	
	init();
	
	function updateImage(){
		$("#btnLoadImage").button('loading');
		$('#webcamArea').html('<img src="/static/img/loading.gif" />');
		$.get(Urls["cam-snapshot"]() + "?" + $.param({
					"key": $.url().param("key")}),
		function(content){
			if("ERROR" == content["status"]){
				$('#webcamArea').html(content["msg"]);
			}else if("SUCCESS" == content["status"]){
				$('#webcamArea').html('<img src="' + content["image-src"] + '" />');
			}else{
				$('#webcamArea').html("Something went terribly wrong :-(");
			}
			$("#btnLoadImage").button('reset');
		});
	}
	
	function updateImage__ProxyMethod(){
		$('#webcamArea').html('<img src="webcam.png' + get_key_url() + '" />');
	}
	
	function init(){
		// bind click to update image button
		$("#btnLoadImage").click(function(){
			updateImage();
		});
	}
	
});
