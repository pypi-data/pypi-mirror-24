$(document).ready(function(){
    // for loading symbol
    var code_loading_sym = '<img src="/static/new/images/default.gif" style="width:20px;">'
    $('.chosen-select').chosen({
	width:"100%"
    })
    
    //~ GLOBAL VARIABLES
    var g_data = {}
    var project_domain = "/django_assistant"
    var active_input;
    var g_api_id;

    //~ functions
    function getParams(parentElement){
	var value,key;
	var data = {}
	$.each(parentElement.children(),function(index,item){
	    value = $(this).children('.value').val()
	    key = $(this).children('.key').val() 
	    if(key != "" && key != undefined){
		data[key] = value
	    }
	})
	return data
    }
    
    function fillEditModal(){
	$('.edit_api_url').val($('.api_details_top .api_url').val())
	$('.edit_api_http_type').val($('.api_details_top .http_type').val())
	$('.edit_api_descr').val($('.api_descr').html())
    }
    
    //~ adding/editing API input params 
    $('body').on('click','.edit_params,.add_params',function(){
	$(this).html(code_loading_sym)
	var parent_element = $('#'+$(this).attr('parent_element')) 
	var data = {}
	
	data["edit_mode"] = $(this).attr("edit_mode")
	data["api_id"] = $(this).attr("api_id")
	data["apiparam_id"] = $(this).attr("apiparam_id")
	data["params"] = JSON.stringify(getParams(parent_element))
	$.ajax({
	    url		:  project_domain + '/a_edit_params/',
	    type	:  'POST',
	    content_type:  "application/x-www-form-urlencoded",
	    data	:  data,
	    success	:  function(json){
			    $.notify({
				// options
				message	: 'Input added successfully !!',
			    }, {
				// settings
				type	: 'info',
				placement	: {
						from: "bottom",
						align: "left"
				},
				delay	: 400,
			    });
			    load_right_side($('.add_params').attr("api_id"))
	    }
	})
    })

    //~ searching URL collection
    $('body').on('keyup','#search_api_collection',function(){
	query_string = $(this).val()
	$('.api_list').children().hide().filter(function(){
	    var value = $(this).attr('url_value');
	    if(value.toLowerCase().indexOf(query_string) >= 0 ){
		return $(this).show()
	    }
	})
    })
    

    //~ populating the LHS with APIs
    var api_collection = [];
    api_list()
    function api_list(){
	$('.api_list').html('')
	$.ajax({
	    url 	: project_domain + '/a_get_apis/',
	    type 	: "GET",
	    success 	: function(json){
			    var uc=l=r=u=0;
			    $.each(json["response"],function(index,api){
			    api_collection.push(api['url'])
			    var url_val = ''
			    if(api["url"].length >32 ){
				url_val = api["url"].substring(0,31) + '...'
			    }else{
				url_val = api["url"]
			    }
		    
			    if(api["api_status"] == "1"){ uc = uc+1 }
			    if(api["api_status"] == "2"){ l = l+1 }
			    if(api["api_status"] == "3"){ r = r+1 }
			    if(api["api_status"] == "4"){ u = u+1 }
		    
		    
			var url_item_code = '<div class="api_item" url_value="'+api["url"]+'">\
						<div class="row">\
						    <div class="col-lg-1 col-md-1 col-sm-1 col-xs-1 paddingLeftZero" >\
							<p class="api_status api_status_'+api["api_status"]+'"></p>\
						    </div>\
						    <div class="col-lg-10 col-md-10 col-sm-10 col-xs-10 paddingLeftZero">\
							<span style="color:grey;font-size:13px;margin-right:20px;">'+api["http_type"]+' </span>\
							<span class="fetch_api_details api_url_value" api_id="'+api["api_id"]+'" data-toggle="tooltip" data-placement="bottom" title="'+api["url"]+'"> '+url_val+'</span>\
						    </div>\
						    <div class="col-lg-1 col-md-1 col-sm-1 col-xs-1 paddingLeftZero">\
							<button class="delete_api" api_id="'+api["api_id"]+'">x</button>\
						    </div>\
						</div>\
					    </div>'
		    
					    $('.api_list').append(url_item_code)
		    
			$('.left_tab_data .api_stat ul li:has(.api_status_1)').html('<p class="api_status_1"></p>'+uc)
			$('.left_tab_data .api_stat ul li:has(.api_status_2)').html('<p class="api_status_2"></p>'+l)
			$('.left_tab_data .api_stat ul li:has(.api_status_3)').html('<p class="api_status_3"></p>'+r)
			$('.left_tab_data .api_stat ul li:has(.api_status_4)').html('<p class="api_status_4"></p>'+u)
			
		    
		})
		    
		    
	    }
	})
    }
    
    //~ hitting an API with data
    $('body').on('click','.hit_api',function(){
	g_data = {}
	url = $('.api_url').val()
	http_type = $('.api_details_top .http_type').val() == "get" ? "GET" : "POST"
	$.each($('#'+active_input).children(),function(index,item){
	    value = $(this).children('.value').val()
	    key = $(this).children('.key').val() 
	    g_data[key] = value
	})
	$.ajax({
	    url 	: url,
	    type 	: http_type,
	    data 	: g_data,
	    success	:function(json){
			    var jsonStr = json;
			    var jsonPretty = JSON.stringify(json, null, '\t');
			    $(".api_result").text(jsonPretty);
			    $(".api_result").show()
	    }
	})
    })

    //~ fetching data for an API
    $('body').on('click','.fetch_api_details',function(){
	api_id = $(this).attr("api_id") 
	load_right_side(api_id)
    })
    
    function load_right_side(api_id){
	$.ajax({
	    url 	: project_domain + '/a_fetch_api_details/',
	    type 	: 'POST',
	    data	: {api_id:api_id},
	    success 	: function(json){
		
			    api = json["api"]
			    url = api["url"]
			    params = api["params"]
			    console.log(json)
			    $('.api_url').val(url)
			    $('.tab_belt_data #id_inputs #input_tab_data_container .existing_input').remove()
			    $('#id_inputs .list-inline .existing_input_header').remove()

			    var selected_tag_ids={}
			    
			    $.each(params,function(index,item){
				var keyValue_code = '';
				$('#id_inputs .list-inline').prepend('<li class="existing_input_header existing_input_'+index+'" tab="level2" target="existing_input_'+index+'">Input '+index+'<p class="delete_input pull-right"  input_index="'+index+'" input_id="'+item["inputset_id"]+'" api_id="'+api_id+'">X</p></li>')
		    
				var edit_key_value_code = '';
				$('#edit_api #inputs .list-inline').prepend('<li class="existing_input_header existing_input_'+index+'" tab="level2" target="edit_input_'+index+'">Input '+index+'<p class="delete_input pull-right"  input_index="'+index+'" input_id="'+item["inputset_id"]+'" api_id="'+api_id+'">X</p></li>')
				
				var tags_code = ''
				selected_tag_ids["input"+index]=[]
				$.each(item["inputset_tags"],function(index2,v){
				    selected_tag_ids["input"+index].push(1)
				    tags_code = tags_code + v["name"]
				})
			    
				$.each(item["inputset_params"],function(k,v){
				    var keyValue_code_temp =	'<div class="key_value_pair_each">\
								    <input type="text" class="key" value="'+k+'" placeholder="key">\
								    <input type="text" class="value"  value="'+v+'" placeholder="value">\
								</div>'
							
				    var keyValue_code_temp2 =	'<div class="edit_key_value_pair_each">\
								    <input type="text" class="key" value="'+k+'" placeholder="key">\
								    <input type="text" class="value"  value="'+v+'" placeholder="value">\
								</div>\
								'
							
				    keyValue_code += keyValue_code_temp
				    edit_key_value_code += keyValue_code_temp2
						
				})
				
		    
				var params_tab_code = '<div id="existing_input_'+index+'" class="existing_input" style="display:none;">' + keyValue_code + '</div>'
				var params_tab_code2 = '<div id="edit_input_'+index+'" class="existing_input">' + edit_key_value_code + '\
							<select type="text"  id="edit_tags_'+index+'"  \
							    data-placeholder="Add tags" class="chosen-select" multiple>\
							</select>\
							<button api_id="" apiparam_id="'+item["inputset_id"]+'" tags_container="edit_tags_'+index+'" parent_element="edit_input_'+index+'" \
							    edit_mode="edit" class="btn edit_params">Save changes to input'+index+'</button>\
						    </div>'
		    
		    
		   
				$('.tab_belt_data #id_inputs #input_tab_data_container').append(params_tab_code)
				$('#edit_api #inputs #edit_inputs_container').append(params_tab_code2)
				$('.add_params').attr('api_id',api_id)

				
					
		})
		    
    
		
			    //~ filling description
			    $('#description_container p').html(api["descr"])
			    
			    //~ filling the http_type
			    $('.api_details_top .http_type').val(api["http_type"])
			    
			    //storing api_id in addNewParams button
			    $('#create_container .add_params').attr('api_id',api["id"])
			    $('.tab_belt_data').show()
			    $('.tab_belt ul').show()
			    $('.api_result').hide()
			    g_api_id = api["id"]
			    $('#id_inputs .list-inline li').removeClass('active')
			    $('#id_inputs .list-inline li:first-child').addClass('active')
			    var curr_input_set = $('.api_details_outer #id_inputs .list-inline li:first-child').attr('target')
			    $('.add_new_input').hide()
			    $('.existing_input').hide()
			    $('#'+curr_input_set).show()
			    $('#param_container input').val('')
			    $('.add_params').html('Add Input')
			    active_input = curr_input_set
			    fillEditModal()
	    }
	    
	})
	
    }	

    //~ creating an API
    $('body').on('click','.create_api_btn',function(){
	var temp = $(this).html()
	$(this).html(code_loading_sym)
	var that                = $(this)
	var data 		= {}
	var url 		= $('#id_create_api .api_url1').val()
	var http_type 		= $('#id_create_api .httptype_value').val()
	var descr 		= $('#id_create_api .descr_value').val()
    
	data["url"] 		= url
	data["http_type"] 	= http_type
	data["descr"] 		= descr
	data["edit_mode"] 	= "add"
	console.log(data)
	$.ajax({
	    url 	: project_domain + '/a_create_api/',
	    type	:"POST",
	    data	:data,
	    success	:function(json){
			    console.log(json)
			    $('.httptype_value option').removeAttr("selected");
			    $('.api_url1').val("");
			    $('.descr_value').val("");
			    api_list()
			    $.notify({
				// options
				message	: 'API created successfully !!',
			    }, {
				// settings
				type	: 'info',
				placement	: {
						from: "bottom",
						align: "left"
				},
				delay	: 400,
			    });
			    that.html(temp)
			    
			    //~ alert("success")
	    }
	})
    })

    //~ deleting API
    //~ deleteAPI
    $('body').on('click','.delete_api',function(){
	var api_id   = $(this).attr("api_id")
	var api_val  = $('.fetch_api_details[api_id="'+api_id+'"]').text()
	$('#deleteAPI .delete_API_confirm').attr('api_id',api_id)
	$('#deleteAPI .api_name').text(api_val)
	$('#deleteAPI').modal('show')
	
    });
   
    $('body').on('click','.delete_API_confirm',function(){
	var temp = $(this).html()
	$(this).html(code_loading_sym)
	var that  = $(this)
	var api_id = $(this).attr("api_id")
	$.ajax({
	    url 	: project_domain+'/a_delete_api/',
	    type 	: "POST",
	    data 	: { api_id : api_id },
	    success 	: function(json){
			    that.html(temp)
			    $('#deleteAPI').modal('hide')
			    api_list()
			    load_right_side(api_id)
	    }
	    
	    
	})
    })

    //~ click api detail tabs
    $('body').on('click','#id_inputs ul li,.tab_belt li',function(){
	//~ alert()
	var tab_val = $(this).attr('tab')
	if(tab_val == 'level1'){
	    $('.tab_belt li').removeClass('active')
	    $(this).addClass('active')
	}else{
	    $('#id_inputs ul li').removeClass('active')
	    $(this).addClass('active')
	}
	target_id = $(this).attr('target')
    
	$('#'+target_id).show()
	$('#'+target_id).siblings().hide()
	
	//~ storing the active input
	if($('#'+target_id).hasClass('existing_input')){
	    active_input = target_id
	}else{
	    active_input = ''
	}
	
	
    })
    
    //~ api status choose popover on hover
    $("[data-toggle='popover']").popover({ trigger: "manual" , html: true, animation:false})
    .on("click", function () {
	var _this = this;
	$(this).popover("show");
	$(".popover").on("mouseleave", function () {
	    $(_this).popover('hide');
	});
    }).on("mouseleave", function () {
	var _this = this;
	setTimeout(function () {
	    if (!$(".popover:hover").length) {
		$(_this).popover("hide");
	    }
	}, 300);
    }).parent().on('click', '[data-select]', function() {
	console.log('get');

	var $selectValue = $(this).attr("data-select");

       $("#quotetype").find('option').attr("selected", false);
      
       $('#quotetype').val($selectValue).trigger('change');
    });
    
    
    //~ update api status
    $('#api_status').on('shown.bs.popover', function() {
	$('#api_status_form input').on('click', function() {
	    //~ alert($('input[name=api_status]:checked').val());
	    var api_status = $('input[name=api_status]:checked').val()
	    //~ console.log(api_id+" "+api_status)
	    $.ajax({
		url 	: project_domain + "/a_edit_api_status/",
		type	:"POST",
		data	:{
				api_id : g_api_id,
				api_status : api_status
		},
		success	:function(json){
				alert("success")
		}
	    })
	});
    });

    //~ navigation in edit API modal
    $('body').on('click','#edit_api .nav_options ul li',function(){
	$('#edit_api .nav_options li').removeClass('active')
	$(this).addClass('active')
	var target = $(this).attr('target')
	$('#'+target).siblings().hide()
	$('#'+target).show()
    })
    
    //~ editing API
    $('body').on('click','.save_api',function(){
	var edit_element = $(this).attr('edit_element')
	if(edit_element == "basic_info"){
	    data = {}
	    data["api_id"] 	 =  api_id
	    data["edit_element"] =  "basic_info"
	    data["url"] 	 =  $('.edit_api_url').val()
	    data["http_type"] 	 = $('.edit_api_http_type').val()
	}
	if(edit_element == "info"){
	    data 		 = {}
	    data["api_id"] 	 =  api_id
	    data["edit_element"] =  "info"
	    data["description"]  =  $('.edit_api_descr').val()
	    
	}
	$.ajax({
	    url 	: project_domain + '/a_edit_api/',
	    type 	: "POST",
	    data	: data,
	    success	: function(json){
			    //~ alert("success")
			    api_list()
			    $('#edit_api').modal('hide')
			    load_right_side(api_id)
	    }
	})	
    })
    
    //~ show confirm MODAL for deleting an input
    $('body').on('click','.delete_input',function(){
	
	var index = $(this).attr('input_index')
	var input_id = $(this).attr('input_id')
	var api_id = $(this).attr('api_id')
	$('.input_name').html("input"+index)
	$('#delete_inputset').modal('show')
	$('.delete_inputset_confirm').attr('input_id',input_id)
	$('.delete_inputset_confirm').attr('api_id',api_id)
	
    })
    
    //~ deleting an input
    $('body').on('click','.delete_inputset_confirm',function(){
	var that  = $(this)
	var temp  = $(this).text()
	$(this).html(code_loading_sym)
	var input_id = $(this).attr('input_id')
	var api_id = $(this).attr('api_id')
	
	$.ajax({
	    
	    url		: project_domain + "/a_delete_api_input/",
	    type	:"POST",
	    data	:{input_id:input_id},
	    success	:function(){
			    //~ alert("success")
			    load_right_side(api_id)
			    that.html(temp)
			    $('#delete_inputset').modal('hide')
			    $.notify({
				// options
				message	: 'Input deleted successfully !!',
			    }, {
				// settings
				type	: 'info',
				placement	: {
						from: "bottom",
						align: "left"
				},
				delay	: 400,
			    });
	    }
	})
	
	
    })
    
    //get tags
    //~ var tags_list=[];
    //~ $.ajax({
	//~ url	: project_domain + "/a_get_tags/",
	//~ type	:"GET",
	//~ success	:function(json){
		    //~ var keys = [];
		    //~ var x;
		    //~ tags_list = json["tags"]
		    //~ $.each(tags_list,function(key,value){
			//~ var item_id, item_value;
			//~ item_value = value["name"]
			//~ item_id = value["id"]
			//~ x = x + '<option value="'+item_id+'" tag_id="' + item_id + '" >' + item_value + '</option>'
		    //~ })
		    //~ $('#id_tags').append(x)
		    //~ $('#id_tags').trigger('chosen:updated');
	//~ }
    //~ })
    
    // tab changing left
    
    $('body').on('click','.left_tabs ul li',function(){
	$('.left_tabs ul li').removeClass('active')
	$(this).addClass('active')
	var id_val = $(this).attr('id')
	$('.left_tab_data').hide()
	$('#id_'+id_val).show()
    });
})
