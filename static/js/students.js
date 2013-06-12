var oTable;
var asInitVals = new Array();

function pad(s){
	var s = String(s)
	if (s.length<2){
		return "0"+s;
	} else {
		return s;
	}
	  
}

$(function() {
	$("input[id$=date]").datepicker({ 
		dateFormat: "dd.mm.yy",
		changeYear: true,
		changeMonth: true,
		yearRange:"1930:2020"
	 });
	
	oTable = $(".searchresult").dataTable({
		"oLanguage": {
			"sUrl": "/js/dataTables.russian.txt"
		},
		"sDom":"lrtip",
		"bStateSave":true,
		"iCookieDuration": 60*60*24,
		"aoColumnDefs": [
      		{
      			"bSearchable": false,
      			"bSortable": false,
      		    "aTargets": [ 0 ] 
      		}
    	],
		"iDisplayLength": 25,
		"bProcessing": true,
        "bServerSide": true,
        "sAjaxSource": "ajax_search/",
        "fnStateSave": function (oSettings, oData) {
            localStorage.setItem( 'DataTables', JSON.stringify(oData) );
        },
        "fnStateLoad": function (oSettings) {
            return JSON.parse( localStorage.getItem('DataTables') );
        },
        "fnServerData": function ( sSource, aoData, fnCallback, oSettings ) {
		      	oSettings.jqXHR = $.ajax( {
			        "dataType": 'json',
			        "type": "POST",
			        "url": sSource+window.location.search,
			        "data": aoData,
			        "success": fnCallback
	      		} );
	      	}
        });
	
	var oSettings = oTable.fnSettings();
	if(oTable.length){
		var cols = oTable.fnSettings().aoColumns
		for(i in cols){
			var cb =  $('input[id=check'+i+']')
			cb.attr('checked', cols[i].bVisible? true : false);
			cb.on('click', function(){
				var ind = i;
				fnShowHide(parseInt($(this).attr('value')), $(this).prop('checked')? true: false)
			});
			// also reset filters on columns
			$('input.col_filter[num='+i+']').attr('value',	oSettings.aoPreSearchCols[ i ].sSearch);
			}
		//oTable.fnDraw();
	}		
	
	$('input[id=allcheck]').click(function(){
		var inputs = $('input[id^=check]')
		var ch = $(this).prop('checked')
		inputs.prop('checked', ch);
		var cols = oTable.fnSettings().aoColumns;
			for (i in cols){
				if (i > 0) {
					//fnShowHide(i, ch);
					oTable.fnSetColumnVis( i, ch, false );
				}
			}
			oTable.fnDraw();
		}
	)
	
	var $filter_inputs = $("input.col_filter")
	
	$filter_inputs.keyup( function () {
		/* Filter on the column (the index) of this element */
		oTable.fnFilter( this.value, $(this).attr('num') );
	} );
	
	$('table.form').each(function(){
		if (localStorage.getItem(this.id+'_visibility') == 'false'){
			$(this).hide()
		}
	})
	
	//FIXME url
	$('input#id_citizenship').autocomplete({
		source:"../countries/",
		minLength: 0
		})
	
	$('form').submit(function(){
		window.onbeforeunload = null;
	})
	

	function date_increase(from, to, days){
		$(from).on('change',
			function(){
				var parts = this.value.match(/(\d+)/g);
				d = new Date(parts[2], parts[1]-1,parts[0])
				d.setDate(d.getDate()+days);
				var day = pad(d.getDate());
				month = pad(d.getMonth()+1)
				new_date = day+'.'+month+'.'+d.getFullYear()
				$(to).val(new_date)
				
			}
		);
	}
	
	date_increase('#id_invitation_sent_date','#id_invitation_received_date', 45)
	date_increase('#id_invitation_duration_from_date','#id_invitation_duration_till_date', 90)
	
	$('.delete_button').click(
		function(){
			return confirm("Удалить?");
		}
	)
	
});

function toggle_form(form){
	var $table = $(form).parent().next()
	$table.toggle()
	localStorage.setItem($table.attr('id')+'_visibility',$($table).is(":visible"));
}

function fnShowHide( iCol, vsbl )
{
    /* Get the DataTables object again - this is not a recreation, just a get of the object */
    oTable = $('.searchresult').dataTable();
    oTable.fnSetColumnVis( iCol, vsbl );
}

