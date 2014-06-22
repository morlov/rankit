$(document).ready(function()
{	

	$(function() {
		$(".ranking-content").sortable({revert: 200, 
			update: function(event, ui) {
	        	var i = 1
	        	$(this).children().each(function(idx, val){
					$(this).find(".item-rank").html(i++);
	            });	
			}
			});
		$(".ranking-content").sortable("disable");
		$(".ranking-content").disableSelection();
	});

	var cached_ranking_content = $(".ranking-content").html();

	$("#sort-ranking").click(function(){
		if($(this).val() === "Cancel") {
		  	$(".ranking-content").sortable("disable");
		  	$(this).val("Sort");
    		$(".ranking-content").html(cached_ranking_content).sortable("refresh");
		}
		else {
		 	$(".ranking-content").sortable("enable");
		  	$(this).val("Cancel");
		};
		$("#submit-ranking").toggle("slow", function(){});
	});

	var i = 1;
	$("#add-item").on('click', function(){
		$(".ranking-content").sortable("enable");
		var item_name = $("#item-text").val();
		var item_content = "";
		if(item_name != '') {
		 	var new_item =
		 		'<div class="item">' +
		 			'<div class="ranking-item" data-item-id=""> ' + 
		 				'<span class="item-rank">' + (i++) +'</span>' +
						'<span class="item-name">' + item_name + '</span> ' +
		 				'<button class="ranking-button open">show</button>' +
		 			'</div>' +
		 			'<div class="item-content">' +
		 				'<span class="item-body">' + item_content + '</span> ' +
		 			'</div> ' +
		 		'</div> ';
			$(new_item).appendTo($(".ranking-content"));
			$("#item-text").val("");
		}      
	});
	
	$("#post-ranking").submit(function(event) {
		var ranking = {
		title: $("#ranking-title-input").val(),
		item_ids: [],
		item_names: [],
		item_contents: []
		};
		$(".ranking-content").children().each(function(idx, val){
			ranking.item_ids.push($(this).data("item-id"));
			ranking.item_names.push($(this).find(".item-name").text());
			ranking.item_contents.push($(this).find(".item-content").text());
        });	
		$("input[name='ranking']").val(JSON.stringify(ranking));
		$("#submit-ranking").attr("disabled","disabled");
	});


	$(".ranking-content").on('click', ".ranking-button.open", 
		function() {
			$(this).closest(".item").find(".item-content").slideToggle();
			if($(this).html()==="show") {
				$(this).html("hide");
			}
		else {
			$(this).html("show");
		}
	});

	$(".ranking-content").on('mouseenter', ".ranking-item",
		function() {
		$(this).css('background-color','#edf3f8');
		$(this).find(".ranking-button.open").show();
	});

	$(".ranking-content").on('mouseleave', ".ranking-item",
	 	function() { 
	 	$(this).css('background-color','#fff');
	 	$(this).find(".ranking-button.open").hide();
	});

});