$(function () {
    var ue=UE.getEditor('editor',{          //3-5初始化ueditor编辑器
       'serverUrl': '/ueditor/upload/'
    });
    $('#addpost').on('click',function (event) {         //发帖子
        event.preventDefault();   //阻止按钮的默认事件
        var title=$('input[name=title]').val();
        var content=ue.getContent();         //获取ueditor的所有内容，包括样式
        var id=$('select[name=select-board]').val();
        var csrf_token=$('input[name=csrf_token]').val();
        var img_code=$('input[name=img-code]').val();
        console.log(title);
        console.log(content);
        console.log(id);
        console.log(csrf_token);
        console.log(img_code);
        $.ajax({
            url:'/apost/',
            type:'post',
            data:{
                img_code:img_code,
                csrf_token:csrf_token,
                id:id,
                title:title,
                content:content
            },
            success:function (data) {
                if(data['code']===200){
                    xtalert.alertConfirm({
                        'msg':'恭喜你！帖子发表成功',
                        'title':'提示',
                        'confirmText':'回到首页',
                        'cancelText':'在发一篇',
                        'confirmCallback':function () {         //点击回到首页动作
                            window.location='/'
                        },
                        'cancelCallback':function () {
                            $('input[name=title]').val('');
                            ue.setContent('');
                            $('input[name=img-code]').val('');
                        }
                    })
                }else{
                    xtalert.alertError(data['message'])
                }
            },
            error:function (errors) {
                xtalert.alertNetworkError()
            }
        })
    })
});



$(function () {         //刷新图片验证码
   $('#search-img-code').on('click',function (event) {
       var self=$(this);
       var src=self.attr('src');
       var newsrc=src+'?wd=1';
       self.attr('src',newsrc)
   })
});