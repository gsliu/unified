/**
 * Created by gliu on 2/25/16.
 */

/*

 var timer, delay = 300;
 $("#issueDescription").bind('keydown blur change', function(e) {
 var _this = $(this);
 clearTimeout(timer);
 timer = setTimeout(function() {
 console.log("ahaha");
 searchKB();
 }, delay );
 });

 */


// A $( document ).ready() block.
$( document ).ready(function() {
    console.log( "ready!" );
    listtophits();
});

function makesearch() {

    $('#div_top_hit').hide();

    $('#div_search_result').show();


    var query = $('#text_search_input').val();
    //var query = document.getElementById('text_search_input').val()
    console.log(query);
    search(query);
}


function search(query) {
    //query = query.toLowerCase()
    //
    var t1 = new Date();
   query = query.replace(/\r?\n|\r/g, " ");
    console.log("searching ...." + query);
    $.ajax({
        type: "post",
        url: "http://unified.eng.vmware.com:8000/text",
        data: "text=" + query,
        cache: false, //......
        success: function (res) {

            var t2 = new Date();
            var dif = t1.getTime() - t2.getTime();

            var Seconds_from_T1_to_T2 = dif / 1000;
            var td = Math.abs(Seconds_from_T1_to_T2);
            //display the result
            $("#div_search_result").empty();
            res = JSON.parse(res);
            console.log(res);
            if(res.length > 0) {
                //show the total result number
                $("#div_search_result").append('<h3 class="page-header"> About ' + res.length + ' results  <small>' + td + 'seconds</small> </h3>');

                //show in div div_search_result
                for (var i = 0; i < res.length; i++) {
                    var result = res[i];

                    kbhtml = '<div><h4><a href="' + result["url"] + '">' + result["title"] + '</a></h4><p>' + result["text"] + '</p> <p>Similarity:' +
                        '<a href="#"> <span class="glyphicon glyphicon-star"></span> </a>' +
                        '<a href="#"><span class="glyphicon glyphicon-star"></span> </a>' +
                        '<a href="#"><span class="glyphicon glyphicon-star"></span></a>' +
                        '<a href="#"><span class="glyphicon glyphicon-star"></span></a>' +
                        '<a href="#"><span class="glyphicon glyphicon-star"></span> </a>' +
                        '</p> <p><a class="btn btn-primary" href="#">Comments <span class="glyphicon glyphicon-chevron-right"></span></a></p><hr></div>'


                    $("#div_search_result").append(kbhtml);
                }


            } else {
                //no result found...
                console.log('no found')
                dot = '';
                if(query.length > 50) {
	            dot = '...' 
                } 
                kbhtml = '<p> Your search - <b>' + query.substring(0, 50) + dot + '</b> - did not match any documents.</p>' +
                    '<p>Suggestions:</p>' +
                    '<ul><li>Input more logs or upload support bundles.</li><li>Describe your problem with more details.</li><li>Try more keywords.</li></ul>'
    
                $("#div_search_result").append(kbhtml);

            }



        }
    })
}


function displayhits() {
    $('#div_top_hit').show()
    $('#div_search_result').hide();
}




function listtophits() {

    $.ajax({
        type: "get",
        url: "http://unified.eng.vmware.com:8000/tophit",
        //data: "text=" + query,
        cache: false, //......
        success: function (res) {

            //display the result
            $("#div_top_hit").empty();
            $("#div_top_hit").append('<h3 class="page-header">Top Hit Knowledgebases</h3>')

            res = JSON.parse(res);
            console.log(res);
            if(res.length > 0) {
                //show the total result number


                //show in div div_search_result
                for (var i = 0; i < res.length; i++) {
                    var result = res[i];

                    kbhtml = '<div><h4><a href="' + result["url"] + '">' + result["title"] + '</a></h4><p>' + result["text"] +
                        '</p> <b>' + res[i]['hits']+ '</b> this week </p> ' +
                    ' <hr></div>'

                    $("#div_top_hit").append(kbhtml);
                }


            } else {
                //no result found...

            }



        }
    })
}

