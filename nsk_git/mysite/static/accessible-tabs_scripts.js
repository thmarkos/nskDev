function prepareDocument(){	
	//code to prepare page here.
	tabs = initTabs();
}
function initTabs(){
	//jQuery(".example2").accessibleTabs({fx:"show",fxspeed: '', syncheights: true, tabbody:'.tab-content'});
	var tabs = jQuery('.jquery_tabs').accessibleTabs({ fx:"show", fxspeed: '', syncheights: true, tabbody:'.tab-content' });
	
	jQuery("a[href=#tab2]").click(function(e){ // make a link that points to #dummy-text open a tab
        e.preventDefault(); // avoid the jumping of the page when clicking the anchor
        tabs.showAccessibleTabSelector('#tab2'); //pass selector (id is easiest) of the tab to show
    });

    var path = jQuery(location).attr("href")//.split('?')[0];
    if (path){
        	if(path.indexOf("tab1")>=0){
        		tabs.showAccessibleTabSelector('#tab1'); //pass selector (id is easiest) of the tab to show
        	}
            if(path.indexOf("tab2")>=0){
                tabs.showAccessibleTabSelector('#tab2');
            }
            if(path.indexOf("tab3")>=0){
                tabs.showAccessibleTabSelector('#tab3');
            }
            if(path.indexOf("tab4")>=0){
                tabs.showAccessibleTabSelector('#tab4');
            }
            if(path.indexOf("tab5")>=0){
                tabs.showAccessibleTabSelector('#tab5');
            }
            if(path.indexOf("tab6")>=0){
                tabs.showAccessibleTabSelector('#tab6');
            }
            if(path.indexOf("tab7")>=0){
                tabs.showAccessibleTabSelector('#tab7');
            }
            if(path.indexOf("tab8")>=0){
                tabs.showAccessibleTabSelector('#tab8');
            }
     }
}

jQuery(document).ready(prepareDocument);
