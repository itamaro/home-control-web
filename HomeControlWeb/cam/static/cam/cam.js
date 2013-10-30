 $(function() {
	
	init();
	
	function init(){
		// bind click to update image button
		$("#btnLoadImage").click(function(){
			updateImage();
		});
	}
	
});
	
function updateImage(){
	$("#btnLoadImage").button('loading');
	$('#webcamArea').html('<img src="/static/img/loading.gif" />');
	$.get(silly_url(Urls["cam-snapshot"](active_id())),
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
