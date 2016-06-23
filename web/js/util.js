/**
 * Created by gliu on 6/20/16.
 */

var tagsToReplace = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;'
};

function replaceTag(tag) {
    return tagsToReplace[tag] || tag;
}

function safe_tags_replace(str) {
    return str.replace(/[&<>]/g, replaceTag);
}


function uploadOnChange() {

    var filename = $('#input_file_upload').val();
    console.log(filename);
    var lastIndex = filename.lastIndexOf("\\");
    if (lastIndex >= 0) {
        filename = filename.substring(lastIndex + 1);
    }
    document.getElementById('input_file_upload_text').value = filename;
}

function reset() {
    $('#input_file_upload').val("");
    $('#text_search_input').val("");


}