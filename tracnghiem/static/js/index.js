$('#stat-choose-school').material_select();

statistics = JSON.parse(statistics);

function change_stats(val){
    account_count = statistics[val].account_count;
    exam_count = statistics[val].exam_count;

    $("#stats-account-count").text(account_count);
    $("#stats-exam-count").text(exam_count);
}

$('#stat-choose-school').change(function(){
    val = $('#stat-choose-school').val();
    change_stats(val);
})

change_stats($('#stat-choose-school').val());