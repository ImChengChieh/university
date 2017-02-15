/**
 * Created by Administrator on 2016/11/8.
 */
$(function(){
    // 编辑用户

    $(".addalumni_delete").on('click',function (){
        var id = $(this).parent().parent().children().eq(5).val();
        var node = $(this).parent().parent();
        alert(id);
        $.ajax({
            type:'post',
            url:'add_alumni',
            data:$('form').serialize(),
            success:function (response, status, xhr) {
                alert('')
            }
        })
    })
});