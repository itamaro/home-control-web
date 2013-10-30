function silly_url(url){
	purl = $.url(url);
	qs = purl.param();
	qs["key"] = $.url().param("key");
	return purl.attr("path") + "?" + $.param(qs);
}
