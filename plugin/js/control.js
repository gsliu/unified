
var query;

chrome.runtime.onMessage.addListener(function(request, sender) {
    if (request.action == "getSource") {
        query = request.source;
    }
});

function onWindowLoad() {

    var message = document.querySelector('#message');

    chrome.tabs.executeScript(null, {
        file: "js/getpage.js"
    }, function() {
        // If you try and inject into an extensions page or the webstore/NTP you'll get an error
        if (chrome.runtime.lastError) {
            query = 'There was an error injecting script : \n' + chrome.runtime.lastError.message;
        }
    });

}

window.onload = onWindowLoad;





$("#btn_analyze").click( function() {
    query = query.replace(/[ \t\n\r]+[\n\r]/g, "");
    query = query.replace(/<head.*head>/g, "");
    query = query.replace(/<[^>]*>/g, "");
    query = query.replace(/[ \t\n\r]+[\n\r]/g, "");

    query = encodeURIComponent(query);

    makesearch();
});

var dosearch = false;

function makesearch() {
    //query = html2text(pageContent);
    console.log(query);
    
    if(dosearch == true) {
        return;
    }

    dosearch = true;


    $('#div_search_result').show();
    textsearch(query);

    dosearch = false;
}


function textsearch(query) {
    //query = ' 2016-06-08T22:55:23.785Z| vcpu-0| I120: SnapshotVMXConsolidateOnlineCB: Done with consolidate'
    console.log("textMatch::" + query);
    $('#btn_analyze').empty();
    $('#btn_analyze').append('<span class="glyphicon glyphicon-refresh glyphicon-refresh-animate"></span> Processing...');
    var t1 = new Date();
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

                    ss = result["url"].split('/');
                    kbnumber = ss[ss.length - 1];
                    console.log(kbnumber);


                    var title = safe_tags_replace(result["title"]);
                    //var text = safe_tags_replace(result["text"])
                    var text = (result["text"]);

                    kbhtml = '<div><h4><a href="' + result["url"] + '">' + title + '</a></h4><p>' + text + '</p> ' +
                        '<p><a href="' + result["url"] + '" >' + result["url"] + '</a></p>' +
                        '<p><b>Similarity:</b>'
                    var j = 0
                    for( ; j < result['rank']; j ++) {
                        kbhtml = kbhtml + '<a href="#"> <span style="color:#FFD700" class="glyphicon glyphicon-star"></span> </a>'
                    }

                    for(; j < 5; j ++) {
                        kbhtml = kbhtml + '<a href="#"><span style="color:#FFD700" class="glyphicon glyphicon-star-empty"></span> </a>'
                    }
                    kbhtml = kbhtml + '<a style="float:right" href="http://unified.eng.vmware.com/symptom.html?id=' + kbnumber +'"><b>Symptom Details</b></a>'

                    //kbhtml = kbhtml + '</p> <p><a class="btn btn-primary" href="#">Comments <span class="glyphicon glyphicon-chevron-right"></span></a></p><hr></div>'
                    kbhtml = kbhtml + '</p> <hr></div>'


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

            $('#btn_analyze').empty();
            $('#btn_analyze').append('Analyze!');
            dosearch = false;

        }
    })
}


