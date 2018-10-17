$(function () {                         //搜索内容
    $('#search_go').on('click',function () {
        var content=$('input[name=content]').val();
        console.log(content);
        var self=$(this);
        var href=self.attr('href');
        var newhref=href+'?content='+content;
        self.attr('href',newhref)
    })
});

$(function () {                         //进入帖子详情页面
    $('.open_post').on('click',function (event) {
        var self=$(this);
        var id=self.attr('post-id');
        var href=self.attr('href');
        var newhref=href+'?id='+id;
        self.attr('href',newhref)
    })
});