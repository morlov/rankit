$(document).ready(function()
{	

	$(function() {
		$(".ranking-content").sortable({revert: 200, 
			update: function(event, ui) {
	        	var i = 1
	        	$(this).children().each(function(idx, val){
					$(this).find(">:first-child").html(i++);
	            });	
			}
			});
		$(".ranking-content").sortable("disable");
		$(".ranking-content").disableSelection();
	});

	var cached_ranking_content = $(".ranking-content").html();

	$("#sort-ranking").click(function(){
		if($("#sort-ranking").val() === "Cancel") {
		  	$(".ranking-content").sortable("disable");
		  	$("#sort-ranking").val("Sort");
    		$(".ranking-content").html(cached_ranking_content).sortable("refresh");
		}
		else {
		 	$(".ranking-content").sortable("enable");
		  	$("#sort-ranking").val("Cancel");
		};
		$("#submit-ranking").toggle("slow", function(){});
	});

	var i = 1;
	$("#add-item").click(function(){
		$(".ranking-content").sortable("enable");
		var item_text = $("#item-text").val()
		if(item_text != '') {
			var item_html = "<span class='item-rank'>" + (i++) + "</span> <span class='item-name'>" + item_text + "</span>";
			$("<div class='ranking-item' data-item-id=''>" + item_html + "</div>").appendTo($(".ranking-content"));
			$("#item-text").val("")
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
			ranking.item_contents.push($(this).find(".item-name").text());
        });	
		$("input[name='ranking']").val(JSON.stringify(ranking));
		$("#submit-ranking").attr("disabled","disabled");
	});
});