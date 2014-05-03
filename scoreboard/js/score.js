var n = 1;
/*<![CDATA[*/
jQuery(function($) {
(function($){
	
	setInterval(flip, 100);

})(jQuery);
});
/*]]>*/

function flip(){
	var size;
	var n = $('#up-down').val();
	
	$('.glyphicon-remove').each(function(){
		size = $(this).css('font-size').substring(0,2);	
		$(this).css('font-size', parseInt(size) + parseInt(n) + "px");	
		
	});
	if(parseInt(size) > 12) 
			$('#up-down').val(-1);
	if(parseInt(size) < 10) 
			$('#up-down').val(1);

}

function obnovit_stranicu() {
location.reload();
}

setInterval("obnovit_stranicu()", 5000);