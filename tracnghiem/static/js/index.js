statistics = JSON.parse(statistics);

function change_stats(val){
    var account_count, exam_count;
    if (val in statistics) {
        account_count = statistics[val].account_count;
        exam_count = statistics[val].exam_count;
    } else {
        account_count = 0;
        exam_count = 0;
    }

    $("#stats-account-count").text(account_count);
    $("#stats-exam-count").text(exam_count);
}

$('#stat-choose-school').change(function(){
    var val = $('#stat-choose-school').val();
    change_stats(val);
});

change_stats($('#stat-choose-school').val());