$(function () {                                        //加精
   $('.setgood').on('click',function (event) {
       event.preventDefault();
       var self=$(this);                                //把js对象转换成jquery对象
       var tr=self.parent().parent();                   //获取tr标签
       var id=tr.attr('data-post-id');                   //拿到绑定在tr标签的当前帖子的id
       var csrf_token=$('input[name=csrf_token]').val(); //获取csrf_token
       $.ajax({
           url:'/cms/agoodpost/',
           type:'post',
           data:{
               id:id,
               csrf_token:csrf_token
           },
           success:function (data) {                   //根据code返回不同结果
               if(data['code']===200){
                   window.location.reload()            //刷新页面
               }else{
                   xtalert.alertError(data['message'])      //返回错误信息
               }
           },
           error:function (errors) {
               xtalert.alertNetworkError()                  //提示网络错误
           }
       })
   })
});
$(function () {                                        //删除帖子
   $('.delpost').on('click',function (event) {
       event.preventDefault();
       var self=$(this);                                //把js对象转换成jquery对象
       var tr=self.parent().parent();                   //获取tr标签
       var id=tr.attr('data-post-id');                   //拿到绑定在tr标签的当前帖子的id
       var csrf_token=$('input[name=csrf_token]').val(); //获取csrf_token
       $.ajax({
           url:'/cms/delpost/',
           type:'post',
           data:{
               id:id,
               csrf_token:csrf_token
           },
           success:function (data) {                   //根据code返回不同结果
               if(data['code']===200){
                   window.location.reload()            //刷新页面
               }else{
                   xtalert.alertError(data['message'])      //返回错误信息
               }
           },
           error:function (errors) {
               xtalert.alertNetworkError()                  //提示网络错误
           }
       })
   })
});

$(function () {                                        //取消加精
   $('.notgood').on('click',function (event) {
       event.preventDefault();
       var self=$(this);                                //把js对象转换成jquery对象
       var tr=self.parent().parent();                   //获取tr标签
       var id=tr.attr('data-post-id');                   //拿到绑定在tr标签的当前帖子的id
       var csrf_token=$('input[name=csrf_token]').val(); //获取csrf_token
       $.ajax({
           url:'/cms/delgoodpost/',
           type:'post',
           data:{
               id:id,
               csrf_token:csrf_token
           },
           success:function (data) {                   //根据code返回不同结果
               if(data['code']===200){
                   window.location.reload()            //刷新页面
               }else{
                   xtalert.alertError(data['message'])      //返回错误信息
               }
           },
           error:function (errors) {
               xtalert.alertNetworkError()                  //提示网络错误
           }
       })
   })
});