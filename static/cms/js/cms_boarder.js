$(function () {                                     //添加/修改板块
    $('#submit-btn').on('click',function (event) {
        event.preventDefault();                     //阻止按钮默认事件
        var name=$('input[name=name]').val();       //获取用户输入的数据（4-6）
        var img_url=$('input[name=img_url]').val();
        var intr=$('textarea[name=intr]').val();
        var notice=$('textarea[name=notice]').val();
        var csrf_token=$('input[name=csrf_token]').val();
        var id=$('input[name=name]').attr('data-id');
        var data_request=$('input[name=name]').attr('data-request');     //判断是否是修改操作
        if(!name || !img_url ||!intr||!notice){                                  //前端简单验证
            xtalert.alertError('请输入完整信息')
        }else{
            if(data_request==='update'){                          //判断请求是编辑还是添加，根据访问的方式不同选择不同的url
                url='/cms/updateboard/'
            }else{
                url='/cms/addboard/'
            }
            $.ajax({               //异步请求
                url:url,   //访问的url
                type:'post',            //使用post请求方式
                data:{                  //传递的数据
                    csrf_token:csrf_token,
                    name:name,
                    id:id,
                    img_url:img_url,
                    intr:intr,
                    notice:notice
                },
                success:function (data) {           //成功返回
                    if(data['code']===200){
                        window.location.reload()        //重新加载页面
                    }else{
                        xtalert.alertError(data['message'])     //返回后台的错误信息
                    }
                },
                error:function (errors) {                   //失败提示网络错误
                    xtalert.alertNetworkError()
                }
            })
        }
    })
});

$(function () {
   $('.edit_board_btn').on('click',function (event) {  //编辑板块
       event.preventDefault();
       var self=$(this);     //把js对象转换成jquery对象
       var tr=self.parent().parent();//通过self获取tr标签
       var name=tr.attr('data-name');
       var img_url=tr.attr('data-img-url');
       var intr=tr.attr('data-intr');
       var id=tr.attr('data-id');
       var notice=tr.attr('data-notice');
       $('input[name=name]').val(name);       //获取用户输入的数据（4-6）
       $('input[name=img_url]').val(img_url);
       $('textarea[name=intr]').val(intr);
       $('textarea[name=notice]').val(notice);
       $('input[name=name]').attr('data-id',id); //把这个标签绑定一个属性data-id方便执行修改或者删除的时候传参
       $('input[name=name]').attr('data-request','update') //方便执行保存操作时候判别是添加还是修改
   })
});


$(function () {             //删除板块
    $('.del-board').on('click',function (event) {
        event.preventDefault();  //阻止按钮的默认事件
        var self=$(this);       //把js对象转换成jquery对象
        xtalert.alertConfirm({
            'msg':'你确定删除这个板块吗？',
            'confirmCallback':function () {
                var tr=self.parent().parent();  //获取当前对象的父对象的父对象（tr）
                var csrf_token=$('input[name=csrf_token]').val();
                var id=tr.attr('data-id');
                console.log(id);
                console.log(csrf_token);
                $.ajax({      //异步请求
                        url:'/cms/delboard/',    //请求url
                        type:'post',        //post请求
                        data:{
                            id:id,
                            csrf_token:csrf_token
                        },
                        success:function (data) {
                            if(data['code']===200){         //如果成功了，且状态码为200
                                window.location.reload()    //重新加载页面
                            }else{
                                xtalert.alertError(data['message'])     //提示出错信息
                            }
                        },
                        error:function (errors) {
                            xtalert.alertNetworkError()        //请求失败，返回网络错误
                        }
                    })
            }
            }
        );
    })
});


$(function () {                                 //上传文件到七牛网
    lqiniu.setUp({
        'domain':'http://pfc2azd93.bkt.clouddn.com/',
        'browse_btn': 'select_img',             //绑定的按钮
        'uptoken_url': '/common/uptoken/',
        'success': function (up,file,info) {    //上传成功后执行的操作
            $('input[name=img_url]').val(file.name)
        }
    });
});
