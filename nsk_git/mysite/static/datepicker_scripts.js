function prepareDocument(){	
	//code to prepare page here.
	tabs = initDateWidget();
}

function initDateWidget(){
	jQuery( "#datepicker" ).datepicker({
		//showOptions: {direction: 'up' }
		//showOn: "button",
		//buttonImage: "/static/css/add-ons/ui-lightness/images/calendar.gif",
		//buttonImageOnly: true,
    	beforeShow: function(input, inst)
    	{
    		inst.dpDiv.css({marginTop: -input.offsetHeight + 'px', marginLeft: input.offsetWidth + 'px'});
    	}
	});	
}
jQuery(document).ready(prepareDocument);
