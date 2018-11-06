$(function () {                                          //点击帖子进入帖子详情页面
   $('.return_pdetial').on('click',function (event) {
       var self=$(this);
       var id=self.attr('post-id');
       var href=self.attr('href');
       var newhref=href+'?id='+id;
       self.attr('href',newhref)
   })
});


$(function () {                                                 //关注板块
   $('.follow').on('click',function (event) {
       var self=$(this);
       console.log($('.follow'));
       var board_id=self.attr('board-id');
       var csrf_token=$('input[name=csrf_token]').val();
       $.ajax({
           type:'post',
           url:'/followBoard/',
           data:{
               board_id:board_id,
               csrf_token:csrf_token
           },
           success:function (data){
               if(data['code']){
                   xtalert.alertSuccessToast(data['message']);
                   setTimeout(function () {
                       window.location.reload()
                   },500)
               }else if(data['code']===201){
                   xtalert.alertSuccessToast(data['message']);
                   window.location.reload()
               }
               else{
                   window.location='http://127.0.0.1:5000/login/'
               }
           },
           error:function (errors) {
                xtalert.alertErrorToast()
           }
       })
   })
});


var url=window.location.href;                       //排行切换效果
$(function () {
    if(url.indexOf('st=2')>=0){
        $('.title_select_inner').removeClass('title_select_xanzhong');
        $('.jh').addClass('title_select_xanzhong')
}
    if(url.indexOf('st=1')>=0){
        $('.title_select_inner').removeClass('title_select_xanzhong');
        $('.zx').addClass('title_select_xanzhong')
}
    if(url.indexOf('st=3')>=0){
        $('.title_select_inner').removeClass('title_select_xanzhong');
        $('.rm').addClass('title_select_xanzhong')
}
});



$(function () {                                           //鼠标进入取消效果
    $('#nofollow').mouseenter(function () {
        var self=$(this);
        self.html('取消关注');
        self.css('fontsize','17px')
    });
    $('#nofollow').mouseout(function () {
        var self=$(this);
        self.html('已关注');
        self.css('fontsize','15px')
    })
})