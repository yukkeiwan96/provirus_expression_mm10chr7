// this function executes our search via an AJAX call
function runSearch( term ) {
    // hide and clear the previous results, if any
    $('#results').hide();
    $('tbody').empty();
    
    // transforms all the form parameters into a string we can send to the server
    var frmStr = $('#gene_search').serialize();
    
    $.ajax({
        url: './search_gene.cgi',
        dataType: 'json',
        data: frmStr,
        success: function(data, textStatus, jqXHR) {
            processJSON(data);
        },
        error: function(jqXHR, textStatus, errorThrown){
            alert("No repeats found 5000 bp upstream nor downstream of the searched gene!");
        }
    });
}
// this processes a passed JSON structure representing gene matches and draws it
//  to the result table
function processJSON( data ) {
    
    // this will be used to keep track of row identifiers
    var next_row_num = 1;
    
    // iterate over each match and add a row to the result table for each
    $.each( data.matches, function(i, item) {
        var this_row_id = 'result_row_' + next_row_num++;
    
        // create a row and append it to the body of the table
        $('<tr/>', { "id" : this_row_id } ).appendTo('tbody');
        
        // add the virus column
        $('<td/>', { "text" : item.virus } ).appendTo('#' + this_row_id);
        
        // add the accession number column
        $('<td/>', { "text" : item.acnum } ).appendTo('#' + this_row_id);

        // add the alignment score column
        $('<td/>', { "text" : item.score } ).appendTo('#' + this_row_id);

        // add the repeat start column
        $('<td/>', { "text" : item.rstart } ).appendTo('#' + this_row_id);

        // add the repeat end column
        $('<td/>', { "text" : item.rend } ).appendTo('#' + this_row_id);
    });
    
    // now show the result section that was previously hidden
    $('#results').show();
}



// run our javascript once the page is ready
$(document).ready( function() {
    // define what should happen when a user clicks submit on our search form
    $('#submit').click( function() {
        runSearch();
        return false;  // prevents 'normal' form submission
    });
});
