$(function () {                         //基本资料和修改密码切换界面
    $('#my-passwd').on('click',function (event) {
        event.preventDefault();
        var self=$(this);
        self.children().addClass('cur2');
        $('#my-base').children().removeClass('cur2');
        $('.my-password').show();
        $('.my-message').hide()
    })
    $('#my-base').on('click',function (event) {
        event.preventDefault();
        var self=$(this);
        self.children().addClass('cur2');
        $('#my-passwd').children().removeClass('cur2');
        $('.my-message').show();
        $('.my-password').hide();
    })
});
$(function () {                         //回复和我的帖子切换
    $('#my-reply').on('click',function (event) {
        event.preventDefault();
        var self=$(this);
        self.children().addClass('cur2');
        $('#my-post').children().removeClass('cur2');
        $('.my-reply').show();
        $('.my-post').hide()
    })
    $('#my-post').on('click',function (event) {
        event.preventDefault();
        var self=$(this);
        self.children().addClass('cur2');
        $('#my-reply').children().removeClass('cur2');
        $('.my-post').show();
        $('.my-reply').hide();
    })
});
$(function () {                                         //左侧tab切换
    $('.tag-list>li').on('click',function () {
        var index=$(this).index();
        var self =$(this);
        self.siblings().removeClass('cur3');
        self.addClass('cur3');
        var list=$('.personal-right').eq(index);
        list.show();
        list.siblings('.personal-right').hide();
    })
})