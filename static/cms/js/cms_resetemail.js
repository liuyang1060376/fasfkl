$(function () {
     //验证邮箱和验证码是否匹配
     $("#xiugai").click(function (event) {
         event.preventDefault();//关闭按钮的默认事件
         var email=$('input[name=email]').val();   //获取邮箱的值
       var email_code=$('input[name=code]').val();//获取验证码
       var csrf_token=$('input[name=csrf_token]').val();//获取csrf_token的值
         $.ajax({          //异步执行
            type:'post',  //请求方式为post请求
            url: '/cms/resetemail/',   //url地址为
            data:{
                email:email,        //传送3个参数
                email_code:email_code,
                csrf_token:csrf_token
            },
            success:function (data) {   //200成功，400用户名或者密码错误
                if(data['code']===200){
                    xtalert.alertSuccessToast(data['message']);
                    email.val('');              //清空邮箱和验证码
                    email_code('');
                }else{
                    xtalert.alertError(data['message'])
                }
            },
            error:function (errors) {
                xtalert.alertNetworkError()    //请求失败，提示网路错误
            }
        })
   })
});
$(function () {
    //获取邮箱验证码  //
    $('#get_code').on('click',function (event) {    // //cms更改邮箱发送验证码
        event.preventDefault();  //阻止表单的默认事件
        var self=$(this);
        var count=60;
        var email=$("input[name=email]").val();      //获取邮箱账号
        var csrf_token=$('input[name=csrf_token]').val(); //获取csrf_token()
        // '''错误代码500；服务器异常  200 成功   错误代码400： 没有输入邮箱账号'''
        $.ajax({       //异步执行
            url:'/common/send_email_code',
            type:'get',
            data:{
                csrf_token:csrf_token,
                email:email
            },
            success:function (data) {
                if(data['code']===200){
                    xtalert.alertSuccessToast('验证码发送成功');
                    self.attr('disabled','disabled');
                    var counttime=60;
                    var timer=setInterval(function () {
                        count=count-1;
                        self.attr('disabled',true);
                        console.log(count);
                        self.val(count);
                        console.log('执行到text');
                        if(count<=0){
                            clearInterval(timer);
                            self.val('获取验证码');
                            }
                    },1000)
                }else if(data['code']===500){
                    xtalert.alertNetworkError()
                }else{
                    xtalert.alertErrorToast(data['message'])
                }
            },
            error:function (errors) {
                xtalert.alertNetworkError() //如果失败返回 网络错误
            }

        })

    })
});


    //
    // var count=60;
    // function timers(val) {      //倒计时时间
    //     if(val.innerHTML==0){
    //         val.innerHTML='重新获取验证';
    //         val.removeAttribute('disabled');
    //         count=60;
    //     }else{
    //         val.setAttribute('disabled',true);
    //         val.removeAttribute('href');
    //         val.innerHTML=count;
    //         count-=1
    //     }
    //     setTimeout(function () {
    //         timers(val);
    //     },1000)
    // }
    //
