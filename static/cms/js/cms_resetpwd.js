$(function () {
    $('#submit').on('click',function (event) {      //cms修改用户密码
        event.preventDefault();  //阻止表单提交的默认行为
        var oldpasswd=$('input[name=oldpasswd]').val();//获取3个密码，以及CSRF_token的值
        var newpasswd=$('input[name=newpasswd]').val();
        var renewpasswd=$('input[name=renewpasswd]').val();
        var csrf_token=$('input[name=csrf_token]').val();
          $.ajax({
        url:'/cms/resetpwd/',
        type: 'post',
        data: {
            csrf_token:csrf_token,
            oldpasswd:oldpasswd,
            newpasswd:newpasswd,
            renewpasswd:renewpasswd
        },
   // code 200(输入正确，修改密码成功)
   // code 400(密码错误，修改密码失败)
   // code 403(表单验证失败，用户输入信息格式不正确)
        success:function (data) {        //成功之后返回的结果
            if (data['code']===200){
                xtalert.alertSuccessToast('密码修改成功') //密码修改成功后清空输入框里面对内容
                $('input[name=oldpasswd]').val('');
                $('input[name=newpasswd]').val('');
                $('input[name=renewpasswd]').val('');
            }else if(data['code']===400){
                xtalert.alertError(data['message'])
            }else{
                xtalert.alertInfo(data['message'])
            }
        },
        error:function (error) {
            xtalert.alertNetworkError()
        }
    })
    });

});