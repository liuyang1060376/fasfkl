$(function () {
    $('#delcommen').on('click',function (event) {
        var self=$(this);
        var id=self.attr('cm-id');
        var csrf_token=$('input[name=csrf_token]').val()
        $.ajax({
            type:'post',
            url:'/cms/delcommen/',
            data:{
                id:id,
                csrf_token:csrf_token
            },
            success:function (data) {
                if(data['code']===200){
                   window.location.reload()
                }else{
                    xtalert.alertErrorToast(data['code'])
                }
            },
            error:function (errors) {
                xtalert.alertNetworkError()
            }
        })
    })
});