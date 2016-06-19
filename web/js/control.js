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


function makefirstsearch() {
    $('#div_search_input').hide();

    $('#div_search_bar').show();
    $('#div_search_result').show();

    var query = $('#search_input').val();
    $('#search_bar_input').val(query)
    console.log(query);
    makesearch(query);
}

function makelatersearch() {
    var query = $('#search_bar_input').val();
    console.log(query);
    makesearch(query);

}


function makesearch(query) {
    query = query.toLowerCase()
    query = query.replace(/\r?\n|\r/g, " ");
    console.log("searching ...." + query);
    $.ajax({
        type: "get",
        url: "http://unified.eng.vmware.com:8080/SearchDispatcher/rest/search?q=" + query,
        //data: 'q=' + query,
        cache: false, //......
        success: function (res) {


            $("#searchResultsContent").empty();
            res = JSON.parse(res);
            console.log(res['hits']);

            if (res['hits']['total'] != 0) {
                for (var i = 0; i < res['hits']['hits'].length; i++) {


                    var result = res['hits']['hits'][i];
                    if (result['_index'] === "bugzilla") {
                        console.log("bug = " + result['_id']);
                        $("#div_search_result").append('<div class="user" style="width: 1200.720;"><li class="b-bd-t1-gray" style="padding-bottom: 15px;">' +
                            '<div class="a-row b-row pd-t10 pd-b20">' +
                            '<h5><a class="l-para-head no-bd-t" href=' + result['_source']['url'] + 'target="_blank">' + result['_source']['summary'] + '</a></h5>' +
                            '<p class="c-body pd-t5" style="margin-bottom: 4px;">' + result['_source']['text'] + '</p>' +
                            '<a class="c-body" href="' + result['_source']['url']  +
                            '" target="_blank">' +  result['_source']['url'] + '</a></div>' +
                            '</li>');

                    } else if (result['_index'] === "ikb") {
                        console.log("ikb = " + result['_id']);
                        $("#div_search_result").append('<li class="b-bd-t1-gray" style="padding-bottom: 15px;">' +
                            '<div class="a-row b-row pd-t10 pd-b20">' +
                            '<h5><a class="l-para-head no-bd-t" href=' + result['_source']['url'] + 'target="_blank">' + result['_source']['summary'] + '</a></h5>' +
                            '<p class="c-body pd-t5" style="margin-bottom: 4px;">' + result['_source']['syptom'] + '</p>' +
                            '<a class="c-body" href="' + result['_source']['url']  +
                            '" target="_blank">' +  result['_source']['url'] + '</a></div>' +
                            '</li></div>');
                    }


                    /*
                     $("#div_search_result").append('<li class="b-bd-t1-gray" style="padding-bottom: 15px;">' +
                     '<div class="a-row b-row pd-t10 pd-b20">' +
                     '<h3><a class="l-para-head no-bd-t" href=' + kb['U'] + 'target="_blank">' + kb['T'] + '</a></h3>' +
                     '<p class="c-body pd-t5" style="margin-bottom: 4px;">' + kb['S'] + '</p>' +
                     '<a class="c-body" href="' + kb['UE']  +
                     '" target="_blank">' +  kb['UE'] + '</a></div>' +
                     '</li>');
                     */


                }
            }

        }
    })
}
