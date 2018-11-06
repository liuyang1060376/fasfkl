$(function () {
    var ue = UE.getEditor('editor',{
        'serverUrl': '/ueditor/upload/',        //初始化eidtor
        toolbars: [
                [
                'undo', //撤销
                'redo', //重做
                'bold', //加粗
                'italic', //斜体
                'source', //源代码
                'blockquote', //引用
                'selectall', //全选
                'insertcode', //代码语言
                'fontfamily', //字体
                'fontsize', //字号
                'simpleupload', //单图上传
                'emotion' //表情
                ]
        ]
    });
    $('#J_reply').on('click',function (event) {              //回复功能
        event.preventDefault();                             //阻止表单的默认行为
        var content=ue.getContent();                                     //获取ueditor的内容
        var self=$(this);
        var post_id=self.attr('post-id');                    //获取评论的帖子的id
        var csrf_token=$('input[name=csrf_token]').val();
        $.ajax({
            type:'post',
            url:'/acommen/',
            data:{
                content:content,
                post_id:post_id,
                csrf_token:csrf_token
            },
            success:function (data) {               //成功后返回
                if(data['code']===200){
                    xtalert.alertSuccessToast(data['message']);
                    timer=setInterval(function () {
                        window.location.reload();   //1.5秒后刷新页面
                        clearInterval(timer)
                    },1000)
                }else if(data['code']===403){
                    xtalert.alertError(data['message'])
                }else{
                    window.location='/login/'
                }
            },
            error:function (errors) {
                xtalert.alertNetworkError()
            }
        })
    });
});


$(function () {                                     //上方评论
   $('#fb').on('click',function (event) {
       event.preventDefault();
       var self=$(this);
       var content=$('#content1').val();
       var post_id=self.attr('post-id');
       var csrf_token=$('input[name=csrf_token]').val();
        $.ajax({
            type:'post',
            url:'/acommen/',
            data:{
                content:content,
                post_id:post_id,
                csrf_token:csrf_token
            },
            success:function (data) {               //成功后返回
                if(data['code']===200){
                    xtalert.alertSuccessToast(data['message']);
                    timer=setInterval(function () {
                        window.location.reload();   //1.5秒后刷新页面
                        clearInterval(timer)
                    },1000)
                }else if(data['code']===403){
                    xtalert.alertError(data['message'])
                }else{
                    window.location='/login/'
                }
            },
            error:function (errors) {
                xtalert.alertNetworkError()
            }
        })
   })
});

$(function () {
    $('.recent_article>a').on('click',function (event) {
        var self=$(this);
        var href=self.attr('href');
        var post_id=self.attr('post-id');
        console.log(post_id);
        var newhref=href+'?id='+post_id;
        self.attr('href',newhref)
    })
});


$(function () {                                 //点赞功能
    $('.like').on('click',function (event) {
        event.preventDefault();
        var self=$(this);
        var commen_id=self.attr('data-commen-id');           //获取评论的id
        var csrf_token=$('input[name=csrf_token]').val();
        console.log(commen_id);
        $.ajax({
            type:'post',
            url:'/commenLike/',
            data:{
                csrf_token:csrf_token,
                commen_id:commen_id,
            },
            success:function (data) {
                if(data['code']===200){
                    window.location.reload()   //刷新页面
                }else if(data['code']===400){
                    xtalert.alertError(data['message'])
                }else if(data['code']===300){
                    xtalert.alertError(data['message'])
                }
                else{
                    window.location='/login/'
                }
            },
            error:function (errors) {
                xtalert.alertNetworkError()
            }
        })
    })
});
$(function () {
   $('#plike').on('click',function (event) {
       event.preventDefault();
       var self=$(this);
       post_id=self.attr('post-id');
       var csrf_token=$('input[name=csrf_token]').val();
       $.ajax({
           type:'post',
           url:'/postLike/',
           data:{
               csrf_token:csrf_token,
               post_id:post_id
           },
           success:function (data) {
               if(data['code']===200){
                   xtalert.alertSuccessToast(data['message']);
                   setTimeout(function () {
                       window.location.reload()
                   },1000)
               }
               else if(data['code']===404){
                   xtalert.alertErrorToast(data['message'])
               }
               else{
                   window.location='/login/'
               }
           },
           error:function (data) {
               xtalert.alertNetworkError(data['message']);
           }
       })
   })
});

