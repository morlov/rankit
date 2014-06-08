
var i = 1;

function addItem() { 
	var elem = document.getElementById('sortable');
    var item = document.createElement('div');
    item.className = "ranking-item";
    var itemText= document.getElementById("item-text");
    if (itemText.value != '') {
		var itemHtml = '<span class="item-rank">'+i+'</span> <span class="item-name">'+itemText.value+'</span>';
		i++;
		itemText.value = '';
		item.innerHTML=itemHtml;
		elem.appendChild(item)
    }
}

$(function() {
	$( "#sortable" ).sortable({ 
							    revert: true, 
		                        update: function(event, ui) {
                                i = 1
                                $(this).children().each(function(idx, val){
								    $(this).find(">:first-child").html(i);
                                    i++; 
                                	})	
								}
		});
		$( "#sortable" ).disableSelection();
	});