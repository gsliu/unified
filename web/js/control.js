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
var dosearch = false;

function makesearch() {
    if(dosearch == true) {
        return;
    }

    dosearch = true;

    $('#div_top_hit').hide();

    $('#div_search_result').show();
    console.log($('#input_file_upload').get(0).files)
    if($('#input_file_upload').get(0).files.length ==0) {
        textsearch();
        dosearch = false;
    } else {

        filesearch();

    }

}


function textsearch() {
    //query = query.toLowerCase()
    var query = $('#text_search_input').val();
    console.log("textMatch::" + query);

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
                    var title = safe_tags_replace(result["title"]);
                    //var text = safe_tags_replace(result["text"])
                    var text = (result["text"]);

                    kbhtml = '<div><h4><a href="' + result["url"] + '">' + title + '</a></h4><p>' + text + '</p> <p><b></b>Similarity:</b>'
                    var j = 0
                    for( ; j < result['rank']; j ++) {
                        kbhtml = kbhtml + '<a href="#"> <span class="glyphicon glyphicon-star"></span> </a>'
                    }

                    for(; j < 5; j ++) {
                        kbhtml = kbhtml + '<a href="#"><span class="glyphicon glyphicon-star-empty"></span> </a>'
                    }

                    //kbhtml = kbhtml + '</p> <p><a class="btn btn-primary" href="#">Comments <span class="glyphicon glyphicon-chevron-right"></span></a></p><hr></div>'
                    //kbhtml = kbhtml + '</p> <hr></div>'


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
    listtophits()
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

function filesearch() {

    $('#btn_analyze').empty();
    $('#btn_analyze').append('<span class="glyphicon glyphicon-refresh glyphicon-refresh-animate"></span> Processing...');

    console.log("handleFileUpload called");
    var query = $('#text_search_input').val();

    var url = "http://unified.eng.vmware.com:8000/file";
    for(var i = 0; i < $('#input_file_upload').get(0).files.length; i ++) {
        var file = $('#input_file_upload').get(0).files[i];
        var formData = new FormData();
        formData.append('file', file);
    }

    formData.append('text', query);
    var t1 = new Date();
    $.ajax({
        url: url,
        type: "post",
        data: formData,
        processData: false,
        contentType: false,
        success: function(res){



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
                    var title = safe_tags_replace(result["title"]);
                    //var text = safe_tags_replace(result["text"])
                    var text = (result["text"]);

                    kbhtml = '<div><h4><a href="' + result["url"] + '">' + title + '</a></h4><p>' + text + '</p> <p><b></b>Similarity:</b>'
                    var j = 0
                    for( ; j < result['rank']; j ++) {
                        kbhtml = kbhtml + '<a href="#"> <span class="glyphicon glyphicon-star"></span> </a>'
                    }

                    for(; j < 5; j ++) {
                        kbhtml = kbhtml + '<a href="#"><span class="glyphicon glyphicon-star-empty"></span> </a>'
                    }

                    //kbhtml = kbhtml + '</p> <p><a class="btn btn-primary" href="#">Comments <span class="glyphicon glyphicon-chevron-right"></span></a></p><hr></div>'
                    //kbhtml = kbhtml + '</p> <hr></div>'


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




            console.log("upload successfully")
            $('#btn_analyze').empty();
            $('#btn_analyze').append('Analyze!');
            dosearch = false;
        },
        error:function(){
            //$("#file_upload_result").html('there was an error while submitting');
            console.log("upload failed")
            $('#btn_analyze').empty();
            $('#btn_analyze').append('Analyze!');
            dosearch = false;
        }

    });



}