 $(function() {
	
	init();
	
	function get_key_url(){
		var key = $.url().param('key');
		return (key ? '?key=' + key : '');
	}
	
	function updateImage(){
		$("#btnLoadImage").button('loading');
		$('#webcamArea').html('<img src="/static/img/loading.gif" />');
		$.get("webcam" + get_key_url(), function(content){
			$('#webcamArea').html(content);
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
