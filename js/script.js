$(function() {
	$("#sortable").sortable({evert: true, 
		update: function(event, ui) {
        var i = 1
        $(this).children().each(function(idx, val){
			$(this).find(">:first-child").html(i);
            	i++; 
            	});	
			}
		});
	$("#sortable").disableSelection();
});

$(document).ready(function()
{	
	var i = 1		
	$("#add-item").click(function(){
		var item_text = $("#item-text").val()
		if(item_text != '') {
			var item_html = "<span class='item-rank'>" + (i++) + "</span> <span class='item-name'>" + item_text + "</span>";
			$("<div class='ranking-item'>" + item_html + "</div>").appendTo("#sortable");
			$("#item-text").val("")
		}
	});

	$("#submit-ranking").click(function()
	{	
		var ranking = {
			title: $("#ranking-title-input").val(),
			item_ids: [],
			item_names: [],
			item_contents: []
		};
		$("#new-ranking").submit(function(event) {
			$("#sortable").children().each(function(idx, val){
				ranking.item_ids.push($(this).find("#item-id").val());
				ranking.item_names.push($(this).find(".item-name").text());
				ranking.item_contents.push($(this).find(".item-name").text());
            });	
			$("input[name='ranking']").val(JSON.stringify(ranking));
		});
	});
});