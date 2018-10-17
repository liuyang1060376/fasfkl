$(function () {             //登录功能
   $('#sub-btn').on('click',function (event) {
       event.preventDefault(); //取消按钮的默认提交事件
       var mobile=$('input[name=mobile]');     //获取用户名
       var passwd=$('input[name=passwd]');     //获取密码
       var csrf_token=$('input[name=csrf_token]');
       $.ajax({             //ajax发送用户名和密码登录
           type:'post',
           url: '/login/',
           data:{
               mobile:mobile.val(),
               passwd:passwd.val(),
               csrf_token:csrf_token.val()
           },
           success:function (data) {            //如果成功后调整到来的网页，如果直接使用登录则跳转到首页
               if(data['code']===200){
                   xtalert.alertSuccessToast(data['message']);
                   var return_to=$('#return_to_span').text();
                   if (return_to){
                       window.location=return_to;
                   }else{
                       window.location='/';
                   }

               }else{
                   xtalert.alertErrorToast(data['message'])
               }
           },
           error:function () {
               xtalert.alertNetworkError()
           }
       })

   })
});