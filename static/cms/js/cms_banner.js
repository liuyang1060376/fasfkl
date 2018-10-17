$(function () {         //添加banner,用于添加一个新的banner
   $('#submit-btn').on('click',function (event) {   //当你单击添加banner这个按钮时候
       event.preventDefault()                       //阻止表单的默认提交事件
       var name=$('input[name=name]').val();        //获取需要的信息
       var img_url=$('input[name=img_url]').val();
       var link_url=$('input[name=link_url]').val();
       var priority=$('input[name=priority]').val();
       var csrf_token=$('input[name=csrf_token]').val();
       var id=$('input[name=name]').attr('data-id');
       var types=$('input[name=name]').attr('data-type');
       if(!name || !img_url ||!link_url ||!priority){      //前端验证，要求所有信息都的输入
            xtalert.alertErrorToast('请输入完整信息')
       }else{
           //根据types这个值判断用户需要的是那种请求【(添加banner)||（修改banner）】
           if(types==='update'){    //如果types=update则表示是修改banner
               url="/cms/updatebanner/" //让他的url为updatebanner
           }else{
               url='/cms/addbanner/' //否则让他跳转到添加banner视图函数
           }
          $.ajax({     //异步的去处理
              url:url,
              type:'post',      //请求方式为post请求
              data:{           //配置发送信息
                    id:id,
                    csrf_token:csrf_token,
                    name:name,
                    img_url:img_url,
                    link_url:link_url,
                    priority:priority
              },
              success:function (data) {
                  if(data['code']===200){     //如果成功，返回的code为200，则让他重新加载页面
                     window.location.reload() //重新加载页面
                  }else{
                     xtalert.alertErrorToast(data['message'])  //否则则弹出错误信息
                  }
              },
              error:function () {
                    xtalert.alertNetworkError()              //失败弹出网络错误
              }
          })
       }
   })
});


$(function () {             //编辑banner，修改banner的设置
   $('.edit_banner_btn').on('click',function (event) {
       event.preventDefault();//取消按钮的默认事件
       var self=$(this);
       var tr=self.parent().parent();//得到按钮的父标签的父标签，最终得到存放数值的tr
       var dataname=tr.attr('data-name');//获取tr的属性
       var dataimg=tr.attr('data-img');
       var datalink=tr.attr('data-link');
       var datapriority=tr.attr('data-priority');
                                            // 把得到的值赋值给input标签
       $('input[name=name]').val(dataname);
       $('input[name=img_url]').val(dataimg);
       $('input[name=link_url]').val(datalink);
       $('input[name=priority]').val(datapriority);
       $('input[name=name]').attr('data-type','update');//用于判断单击保存按钮时候是修改还是添加
       $('input[name=name]').attr('data-id',tr.attr('data-id'));//用与在数据库中查找用户需要哪一个修改哪一个banner
   })
});


$(function () {                         //删除banner图
   $('.del-banner').on('click',function (event) {
       event.preventDefault();      //阻止按钮的默认事件
       var self=$(this);            //把当前对象转换成jquery对象
       var id=self.parent().parent().attr('data-id');   //获取要删除的banner_id
       var csrf_token=$('input[name=csrf_token]').val(); //获取csrf_token
       xtalert.alertConfirm({           //警告框
           'msg':'你确定删除这个轮播图吗?',
           'confirmCallback':function () {
                $.ajax({    //异步请求
                    url: '/cms/dbanner/',    //请求的url
                    type: 'post',            //请求方式
                    data: {                  //传输的值
                        id:id,
                        csrf_token:csrf_token
                    },
                success:function (data) {        //成功返回
                    if(data['code']===200){
                         window.location.reload();  //重新加载这个这个url
                    }else{
                        xtalert.alertError(data['message'])
                    }
                },
                error:function () {              //失败返回
                     xtalert.alertNetworkError()
                }
            })
           }}
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
