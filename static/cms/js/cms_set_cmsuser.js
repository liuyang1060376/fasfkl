$(function () {                                     //设置用户权限
    $('.shezhi').on('click',function (event) {
        var self=$(this);
        var role_id=self.attr('role-id');
        var user_id=self.attr('user-id');
        var set=self.attr('set');
        var csrf_token=$('input[name=csrf_token]').val();
        $.ajax({
            type:'post',
            url:'/cms/setPermission/',
            data:{
                role_id:role_id,
                user_id:user_id,
                set:set,
                csrf_token:csrf_token
            },
            success:function (data) {
                if(data['code']===200){
                    xtalert.alertSuccessToast(data['message'])
                    setTimeout(function () {
                        window.location.reload()
                    },1000)
                }else{
                    xtalert.alertError(data['message'])
                }
            },
            error:function (error) {
                xtalert.alertNetworkError()
            }
        })
    })
});