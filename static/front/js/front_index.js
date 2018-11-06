$(function () {                 //跳转到选择的这个板块的主题
   $('.board_select').on('click',function (event) {
       var self=$(this);                  //把js对象转换成jquery对象
       var herf=self.attr('href');
       var id=self.attr('board-id');
       var newherf=herf+'?id='+id;
       self.attr('href',newherf)
   })
});

$(function () {                                     //点击帖子进入帖子详情
   $('.post_detial').on('click',function (event) {
       var self=$(this);                        //把js对象转换成jquery对象
       var herf=self.attr('href');
       var id=self.attr('data-post-id');
       var newherf=herf+'?id='+id;
       self.attr('href',newherf)
   })
});
$(function () {                                     //搜索
    $('#search_go').on('click',function (event) {
        content=$('#contentbt').val();
        var self=$(this);
        var href=self.attr('href');
        var newhref=href+'?content='+content;
        self.attr('href',newhref)
    })
});