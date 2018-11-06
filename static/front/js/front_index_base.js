window.onload=function () {                                 //搜索框样式
    var search=document.getElementById("search");
    search.onblur=function () {
        $('#search').animate({
            "margin-left":"272px"
            },1000);
    };
};
$(function () {                                                   //搜索功能
   $('#search_btn').on('click',function (event) {
       var searchs=$('#search').css('margin-left');
       if (searchs==='0px'){
           content=$('#search').val();
           var self=$(this);
           var href=self.attr('href');
           var newhref=href+'?content='+content;
           self.attr('href',newhref)
       }else{
           event.preventDefault();
           $('#search').animate({
            "margin-left":"0"
            },1000);
           console.log('hah');
       }

   });
});

$(function () {                                             //注销登录
   $('#front_off').on('click',function (event) {
      event.preventDefault();
      var csrf_token=$('input[name=csrf_token]').val();     //获取csrf_token
        $.ajax({            //异步请求
            type:'post',    //请求方式
            url:'/front_off/',          //请求url
            data:{
                csrf_token:csrf_token
            },
            success:function (data) {                        //成功返回
                xtalert.alertSuccess(data['message']);
                timer=setInterval(function () {
                   window.location.reload();                 //刷新页面
                   clearInterval(timer)
                },1000)
            },
            error:function (errors) {
                xtalert.alertNetworkError()
            }
        })
   })
});

$(function () {                                                 //侧边tag
    $('#close').on('click',function (event) {
        $('.f-left-nav').animate({
            "width":0
        },1000);
        $('.left-tag').animate({
            "width":0
        },1000)
    });
    $('#board').on('click',function (event) {
        event.preventDefault();
        $('.f-left-nav').animate({
            'width':258
        },1000);
        $('.left-tag').animate({
            'width':258
        },1000);
    })
});

$(function () {                                                 //侧边单击进入板块
    $('.board-list-tag>li>a').on('click',function (event) {
        var self=$(this);
        var id=self.attr('board-id');
        var href=self.attr('href');
        var newself=href+'?id='+id;
        self.attr('href',newself)
    })
});



$(function () {                                                    //鼠标进入头像显示设置列表显示
    $('#personal-go').on('click',function (event) {
        event.preventDefault();
        $('.dropdown-user').slideToggle(300)
    })
});