$(function () {                                         //拉黑前台用户
    $('.blockuser').on('click',function (event) {
        event.preventDefault();         //阻止表单默认行为
        var self=$(this);
        var tr=self.parent().parent();
        var id=tr.attr('data-user-id');          //获取绑定在tr标签上的前台用户id
        var csrf_token=$('input[name=csrf_token]').val();
        console.log(csrf_token);
        $.ajax({                        //异步请求拉黑用户
            type:'post',
            url:'/cms/blockuser/',
            data:{
                id:id,
                csrf_token:csrf_token
            },
            success:function (data) {                   //成功返回
                if(data['code']===200){
                    window.location.reload()            //重新刷新页面
                }else{
                    xtalert.alertError(data['message'])
                }
            },error:function (errors) {                 //失败返回
                xtalert.alertNetworkError();
            }
        })
    })
});


$(function () {                                         //拉黑前台用户
    $('.calcelblock').on('click',function (event) {
        event.preventDefault();         //阻止表单默认行为
        var self=$(this);
        var tr=self.parent().parent();
        var id=tr.attr('data-user-id');          //获取绑定在tr标签上的前台用户id
        var csrf_token=$('input[name=csrf_token]').val();
        console.log(csrf_token);
        $.ajax({                        //异步请求拉黑用户
            type:'post',
            url:'/cms/calcelblock/',
            data:{
                id:id,
                csrf_token:csrf_token
            },
            success:function (data) {                   //成功返回
                if(data['code']===200){
                    window.location.reload()            //重新刷新页面
                }else{
                    xtalert.alertError(data['message'])
                }
            },error:function (errors) {                 //失败返回
                xtalert.alertNetworkError();
            }
        })
    })
});