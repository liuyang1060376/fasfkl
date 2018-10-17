// 刷新验证码
$(function () {
   $('#img_verify_code').on('click',function (event) {
       var src=$('#img_verify_code').attr('src');
       newsrc=src+'?wd=1';
       $('#img_verify_code').attr('src',newsrc)
   }) 
});


//获取短信验证码
$(function () {
   $('#get_verfiy_code').on('click',function (event) {
       event.preventDefault();
       var self=$(this);
       var mobile=$('input[name=mobile]').val();
       var csrf_token=$('input[name=csrf_token]').val();
       $.ajax({
           type:'post',
           url:'/common/send_message/',
           data:{
               mobile:mobile,
               csrf_token:csrf_token
           },
           success:function (data) {
               if (data['code']===200){
                   xtalert.alertSuccessToast(data['message']);
                   var counttime=60;            //获取验证码后60秒倒计时
                   var timer=setInterval(function () {
                       self.attr('disabled',true);
                       counttime=counttime-1;
                       console.log(counttime);
                       self.val(counttime);
                       if (counttime<=0){
                           clearInterval(timer);
                           self.attr('disabled',false);
                           self.val('获取验证码')
                       }
                   },1000)
               }else if(data['code']===403){
                   xtalert.alertError(data['message'])
               }else{
                   xtalert.alertError(data['message'])
               }
           },
           error:function () {
               alert('shibai');
               xtalert.alertNetworkError()
           }
       })

   })
});

$(function () {
   $('#registnow').on('click',function (event) {
       event.preventDefault();           //取消按钮的默认提交事件
       var username=$('input[name=username]');
       var passwd=$('input[name=passwd]');
       var repasswd=$('input[name=repasswd]');
       var mobile=$('input[name=mobile]');
       var verifycode=$('input[name=verifycode]');
       var imgverifycode=$('input[name=imgverifycode]');
       var csrf_token=$('input[name=csrf_token]');
       $.ajax({
           type:'post',
           url:'/regist/',
           data:{
               username:username.val(),
               passwd:passwd.val(),
               repasswd:repasswd.val(),
               mobile:mobile.val(),
               verifycode:verifycode.val(),
               imgverifycode:imgverifycode.val(),
               csrf_token:csrf_token.val()
           },
           success:function (data) {
               if(data['code']===200){
                   xtalert.alertSuccessToast(data['message']);
                   var return_to=$('#return_to_span').text(); //查看是否是从其他url点击而来
                   if(return_to){
                       window.location=return_to; //如果是从其他网站跳转而来，则注册成功后调整到第三方页面
                   }else{                         //否则调整到首页
                       window.location='/'
                   }
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