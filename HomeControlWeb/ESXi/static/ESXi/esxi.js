 $(function() {
	init();
	
	function init(){
		$("#esxiHost").change(get_host_data_from_cache);
		
		$('.selectpicker').selectpicker();
		
		get_host_data_from_cache();
	}
});

function load_view_to_details(view_name){
	host_id = $("#esxiHost").val();
	$.get(Urls[view_name](host_id) + "?" + $.param({"key": $.url().param("key")}),
	function(content){
		$("#hostDetailsArea").html(content);
		$("#loadingModal").modal('hide');
	});
}

function get_host_data_from_cache(){
	load_view_to_details("rhost-get-cache-data");
}

function update_remote_host_data(){
	$("#loadingModal").modal({keyboard: false});
	load_view_to_details("rhost-update-remote-data");
}

function get_vm_data_from_cache(vm_id){
	$.get(Urls["rhost-get-cache-vm-data"](vm_id) + "?" + $.param({"key": $.url().param("key")}),
	function(content){
		power = content["power"].toLowerCase();
		$("#vmIcon-" + vm_id).attr("src", "/static/img/vm-icon-" + power + ".png");
		$("#vmLoadbar-" + vm_id).hide();
		$("#vm" + (("off" == power) ? "Shutdown" : "TurnOn") + "-" + vm_id).hide();
		$("#vm" + (("off" == power) ? "TurnOn" : "Shutdown") + "-" + vm_id).show();
	});
}

function change_vm_power_state(vm_id, target_view){
	$("#vmLoadbar-" + vm_id).show();
	$("#vmShutdown-" + vm_id).hide();
	$("#vmTurnOn-" + vm_id).hide();
	$.get(Urls[target_view](vm_id) + "?" + $.param({"key": $.url().param("key")}),
	function(content){
		get_vm_data_from_cache(vm_id);
	});
}

function turn_on_vm(vm_id){
	change_vm_power_state(vm_id, "rhost-turn-on-vm");
}

function shutdown_vm(vm_id, name){
	if (confirm("Are you sure you want to shutdown VM " + name + "?")){
		change_vm_power_state(vm_id, "rhost-shutdown-vm");
	}
}

function change_host_power_state(host_id, target_view){
	$("#hostLoadbar").show();
	$("#hostShutdown").hide();
	$("#hostTurnOn").hide();
	$.get(Urls[target_view](host_id) + "?" + $.param({"key": $.url().param("key")}),
	function(content){
		get_host_data_from_cache();
	});
}

function turn_on_host(host_id){
	change_host_power_state(host_id, "rhost-turn-on-host");
}

function shutdown_host(host_id){
	if (confirm("Are you sure?")){
		change_host_power_state(host_id, "rhost-shutdown-host");
	}
}
