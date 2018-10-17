$(function () {                                          //点击帖子进入帖子详情页面
   $('.return_pdetial').on('click',function (event) {
       var self=$(this);
       var id=self.attr('post-id');
       var href=self.attr('href');
       var newhref=href+'?id='+id;
       self.attr('href',newhref)
   })
});