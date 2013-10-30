 $(function() {
	
	init();
	
	function init(){
		$("#instSelector").change(load_details);
		$(".selectpicker").selectpicker();
		load_details();
	}
	
});

function active_id(){
	return $("#instSelector").val();
}

function load_details(){
	inst_id = active_id();
	cur_url = $.url();
	details_url = Urls[details_view_name](inst_id);
	if (cur_url.attr("path") != details_url){
		// Need to redirect
		window.location.href = silly_url(details_url);
	}
}
