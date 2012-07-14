function prepareDocument(){	
	//code to prepare page here.
	initTrees();
	bindDocument();
	highlight_navbar();
	
	jQuery("#submit_review").click(test); 
}

function bindDocument(){
	jQuery("#tree").bind("reselect.jstree", function () {
		jQuery("#tree").bind("select_node.jstree", function (e, data) {
						// no need to use `first` here, just use your original function,loop problem solved.
                        if(jQuery.data(data.rslt.obj[0], "href"))
                        {
                            window.location=jQuery.data(data.rslt.obj[0], "href");
                        }
                        else
                        {
                            alert("No href defined for this element");
                        }
		})
	});
}

function initTrees(){
/*
	jQuery("#tree").jstree({
		"json_data" : {
			"data": [
					{
						"data" : "Employee",
						"attr" : { "id" : "node.id1"},
                            
						"children" :[
						             {"data":"Add", "metadata":{"href":"/hr/employee_form/"}, "attr":{ "id" : "node.id11" }},
						             {"data":"View", "metadata":{"href":"/hr/employee_list/"}, "attr":{ "id" : "node.id12" }},
						             {"data":"Google", "children":[{"data":"Youtube", "metadata":{"href":"http://youtube.com"}, "attr":{ "id" : "li.node.id5" }},{"data":"Gmail", "metadata":{"href":"http://www.gmail.com"}, "attr":{ "id" : "li.node.id6" }},{"data":"Orkut","metadata":{"href":"http://www.orkut.com"}, "attr":{ "id" : "li.node.id7" }}], "metadata" : {"href":"http://youtube.com"}, "attr":{ "id" : "li.node.id8" }}
						             ]
					},                        
					{
						"data" : "Person",
						"attr" : { "id" : "node.id2"},
                        
						"children" :[
						             {"data":"Add", "metadata":{"href":"/hr/person_form/"}, "attr":{ "id" : "node.id21" }},
						             {"data":"View", "metadata":{"href":"/hr/person_list/"}, "attr":{ "id" : "node.id22" }},
						             ]
					}    
					]
		},
		"cookies" : {"cookie_options" : {path: '/'}},
		"plugins" : [ "themes", "json_data", "ui", "cookies"]
	});
*/
/*
	jQuery("#demo1").jstree({   
	    "json_data" : {  
	      "ajax" : {  
	         "url" : "/test/testoutf/"//,  
	         //"data" : function (n) {   
	         //    return { id : n.attr ? n.attr("id") : 0 };   
	         //},
	          //error: function(e){alert(e);}
	      }  
	  },  
	 "plugins" : [ "themes","json_data", "ui"]
	});
*/
}

function highlight_navbar(){
		//path.indexOf(str) returns -1 if string is not found in path
	    var path = jQuery(location).attr("href")//.split('?')[0];
	    if (path){
	    	jQuery("nav li a").each(function(){
	            if(path.indexOf(jQuery(this).attr("href"))>=0){
	            	jQuery(this).closest("li").addClass("active");
	                return;
	            }
	        });
	     }
}

function test(){
	// build an object of review data to submit
	var data = jQuery("#tree").jstree("get_json", -1);
	str = JSON.stringify(data);
	var review = 1;
	// make request, process response
	jQuery.post("/test/testin/", { data: str },
		function(response){
			//jQuery("#review_errors").empty();
			// evaluate the "success" parameter
			//if(response.success == "True"){
			// disable the submit button to prevent duplicates
			//}
			//else{
			// add the error text to the review_errors div
			//jQuery("#review_errors").append(response.html);
			//}
		}, "json");
}

jQuery(document).ready(prepareDocument);

//////////////////////////////////////////////////////extra code////////////////////////////////////////////////////////////////////////////

/*
jQuery('#.ym-hlist li').click(function(){
	jQuery('#.ym-hlist li').removeClass('active');
	jQuery(this).addClass('active');
});
*/
	
/*
jQuery(".ym-hlist a").click(function () {
	jQuery("div").each(function (i) {
      if (this.style.color != "blue") {
        this.style.color = "blue";
      } else {
        this.style.color = "";
      }
    });
  });
*/

/* 
            $.cookie("example", "foo", { expires: 1 });
            alert( $.cookie("example") );

*/

/*
            $(document).ready(function(){
                $("#tree").jstree({
                    "json_data" : {
                        "data":[
                            {
                                "data" : "Employees",
                                "attr" : { "id" : "li.node.id1" },
                                "children" :[
                                             {"data":"Add employee", "metadata":{"href":"/mgmt/employee_form/"}, "attr":{ "id" : "li.node.id2" }},
                                             {"data":"Add communication", "metadata":{"href":"/mgmt/communication_form/"}, "attr":{ "id" : "li.node.id3" }},
                                             {"data":"View employees", "metadata":{"href":"/mgmt/employee_list/"}, "attr":{ "id" : "li.node.id4" }},
                                             {"data":"Google", "children":[{"data":"Youtube", "metadata":{"href":"http://youtube.com"}, "attr":{ "id" : "li.node.id5" }},{"data":"Gmail", "metadata":{"href":"http://www.gmail.com"}, "attr":{ "id" : "li.node.id6" }},{"data":"Orkut","metadata":{"href":"http://www.orkut.com"}, "attr":{ "id" : "li.node.id7" }}], "metadata" : {"href":"http://youtube.com"}, "attr":{ "id" : "li.node.id8" }}
                                            ]
                            },
                            {
                                "data" : "Networking sites",
                                "attr":{ "id" : "li.node.id9" },
                                "children" :[
                                    {"data":"Facebook", "metadata":{"href":"http://www.fb.com"}, "attr":{ "id" : "li.node.id10" }},
                                    {"data":"Twitter", "metadata":{"href":"http://twitter.com"}, "attr":{ "id" : "li.node.id11" }}
                                ]
                            }
                        ],
                        "attr":{ "id" : "li.node.id0" }
                    },
                    "plugins" : [ "themes", "json_data", "ui", "cookies" ]
                }).bind("select_node.jstree", function(e, data)
                    {
                        if(jQuery.data(data.rslt.obj[0], "href"))
                        {
                            window.location=jQuery.data(data.rslt.obj[0], "href");
                        }
                        else
                        {
                            alert("No href defined for this element");
                        }
                    })
            });
*/

/*
jQuery("#treetest").jstree({
		"json_data" : {
			"data":

[{"data":"Blues","attr":{"id":"2"},"state":"open","children":[{"data":"Hard Rock","attr":{"id":"3"},"state":"open","children":[]},{"data":"Pop Rock","attr":{"id":"4"},"state":"open","children":[]},]},{"data":"Rock","attr":{"id":"1"},"state":"open","children":[]},]
//[{"data":"Blues","attr":{"id":"2"},"state":"open","children":[{"data":"Hard Rock","attr":{"id":"3"},"state":"open","children":[]},{"data":"Pop Rock","attr":{"id":"4"},"state":"open","children":[]},]},{"data":"Rock","attr":{"id":"1"},"state":"open","children":[]},]
//[{"data":"Employeestest","attr":{"id":"node1","class":""},"state":"open","metadata":{},"children":[{"data":"Add employee","attr":{"id":"li.node.id2"},"metadata":{"href":"/mgmt/employee_form/"}},{"data":"Add communication","attr":{"id":"li.node.id3"},"metadata":{"href":"/mgmt/communication_form/"}},{"data":"View employees","attr":{"id":"li.node.id4"},"metadata":{"href":"/mgmt/employee_list/"}},{"data":"Google","attr":{"id":"li.node.id8","class":""},"state":"open","metadata":{"href":"http://youtube.com"},"children":[{"data":"Youtube","attr":{"id":"li.node.id5"},"metadata":{"href":"http://youtube.com"}},{"data":"Gmail","attr":{"id":"li.node.id6"},"metadata":{"href":"http://www.gmail.com"}},{"data":"Orkut","attr":{"id":"li.node.id7","class":""},"metadata":{"href":"http://www.orkut.com"}}]}]}]
				

//				 [
//				 {
//					 "data": "Blues", "attr":{ "id": "2" }, "state":"open", 
//					 "children": 
// 				 			[
// 				 			 {"data": "Hartd Rock", "attr":{ "id": "3" }, "state":"open", "children": [ ]},
//				 			 {"data": "Pop Rock", "attr":{ "id": "4" }, "state":"open", "children": [ ]},
// 				 			]
//				 },
//				 { 
//					 "data": "Rock", "attr":{ "id": "1" }, "state":"open", 
//					 "children": [ ]
//				 },      
//				 ]

		},
		"plugins" : [ "themes", "json_data", "ui"]
});
*/


