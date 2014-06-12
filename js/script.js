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
		var content = {
			title: $("#ranking-title-input").val(),
			items: []  
		};
		$("#new-ranking").submit(function(event) {
			$("#sortable").children().each(function(idx, val){
				content.items.push($(this).find(".item-name").text());
            });	
			$("input[name='content']").val(JSON.stringify(content));
		});
	});
});