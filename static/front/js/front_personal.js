$(function () {                         //基本资料和修改密码切换界面
    $('#my-passwd').on('click',function (event) {
        event.preventDefault();
        var self=$(this);
        self.children().addClass('cur2');
        $('#my-base').children().removeClass('cur2');
        $('.my-password').show();
        $('.my-message').hide()
    })
    $('#my-base').on('click',function (event) {
        event.preventDefault();
        var self=$(this);
        self.children().addClass('cur2');
        $('#my-passwd').children().removeClass('cur2');
        $('.my-message').show();
        $('.my-password').hide();
    })
});
$(function () {                         //回复和我的帖子切换
    $('#my-reply').on('click',function (event) {
        event.preventDefault();
        var self=$(this);
        self.children().addClass('cur2');
        $('#my-post').children().removeClass('cur2');
        $('.my-reply').show();
        $('.my-post').hide();
        $('#fenye').hide();
    });
    $('#my-post').on('click',function (event) {
        event.preventDefault();
        var self=$(this);
        $('#fenye').show();
        self.children().addClass('cur2');
        $('#my-reply').children().removeClass('cur2');
        $('.my-post').show();
        $('.my-reply').hide();
    })
});
$(function () {                                         //左侧tab切换
    $('.tag-list>li').on('click',function () {
        var index=$(this).index();
        var self =$(this);
        self.siblings().removeClass('cur3');
        self.addClass('cur3');
        var list=$('.personal-right').eq(index);
        list.show();
        list.siblings('.personal-right').hide();
    })
});

$(function () {
    $('#cancalfollow').on('click',function (event) {
        var self=$(this);
        var board_id=self.attr('board_id');
        var csrf_token=$('input[name=csrf_token]').val();
        console.log(csrf_token);
        console.log(board_id);
        $.ajax({
            type:'post',
            url:'/followBoard/',
            data:{
                board_id:board_id,
                csrf_token:csrf_token
            },
            success:function (data) {
                if(data['code']===201){
                    xtalert.alertSuccessToast(data['message']);
                    setTimeout(function () {
                        window.location.reload()
                    },1000)
                }else{
                    xtalert.alertNetworkError(data['message'])
                }
            },
            error:function (error) {
                xtalert.alertNetworkError()
            }
        })
    })
});



$(function () {                                 //单击修改获取修改里的参数（体验优化）
    $('#upperson').on('click',function () {
        var intr=$('#intr').text();
        console.log(intr);
        var username=$('#username').text();
        var avatar=$('#avatar').text();
        $('input[name=username]').val(username);
        $('textarea[name=intr]').val(intr);
        $('input[name=avatar]').val(avatar);
    })
});



$( function () {                       //七牛云上传图片设置
lqiniu.setUp({
    'domain':'http://lydwz.club/',
    'browse_btn': 'upload-btn',   //按钮名称
    'uptoken_url': '/common/uptoken/',
    'success': function (up,file,info) {

        $('#img-input').val(file.name)
    }
});
});

$(function () {                                                           //修改用户信息
    $('#upUser').on('click',function (event) {
        var username=$('input[name=username]').val();
        var intr=$('textarea[name=intr]').val();
        var avatar=$('input[name=avatar]').val();
        var csrf_token=$('input[name=csrf_token]').val();
        $.ajax({
            type: 'post',
            url:'/upUser/',
            data:{
                username:username,
                intr:intr,
                avatar,
                csrf_token:csrf_token
            },
            success:function (data) {
                if(data['code']===200){
                    xtalert.alertSuccessToast(data['message'])
                }else{
                    xtalert.alertErrorToast(data['message'])
                }
            },
            error:function (errors) {
                xtalert.alertNetworkError()
            }
        })
    })
});



$(function () {                                                         //c发送修改密码验证码
    //获取邮箱验证码  //
    $('#get_code').on('click',function (event) {    //
        event.preventDefault();  //阻止表单的默认事件
        var self=$(this);
        var count=60;
        var mobile=$("input[name=email]").val();      //获取邮箱账号
        // '''错误代码500；服务器异常  200 成功   错误代码400： 没有输入邮箱账号'''
        $.ajax({       //异步执行
            url:'/send_resetpasswd/',
            type:'get',
            data:{
                mobile:mobile
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

$(function () {                                              //修改密码
    $('#xiugai').on('click',function (event) {
        event.preventDefault()
        code=$('input[name=code]').val();
        password=$('input[name=password2]').val();
        password1=$('input[name=password3]').val();
        csrf_token=$('input[name=csrf_token]').val();
        $.ajax({
            url:'/resetpassword/',
            type:'post',
            data:{
                code:code,
                password:password,
                password1:password1,
                csrf_token:csrf_token
            },
            success:function (data) {
                if(data['code']===200){
                    xtalert.alertSuccessToast(data['message']);
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

