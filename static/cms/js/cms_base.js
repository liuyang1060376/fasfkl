$(function () {
    $('#search_post').on('click',function (event) {
        var self=$(this);
        content=$('#content_post').val();
        var href=self.attr('href');
        newhref=href+content;
        self.attr('href',newhref);
    })
});
$(function () {
    $('.nav-sidebar>li>a').click(function (event) {
        var that = $(this);
        if(that.children('a').attr('href') == '#'){
            event.preventDefault();
        }
        if(that.parent().hasClass('unfold')){
            that.parent().removeClass('unfold');
        }else{
            that.parent().addClass('unfold').siblings().removeClass('unfold');
        }
    });

    $('.nav-sidebar a').mouseleave(function () {
        $(this).css('text-decoration','none');
    });
});


$(function () {
    var url = window.location.href;
    if(url.indexOf('profile') >= 0){  //个人中心
        var profileLi = $('.profile-li');
        profileLi.addClass('unfold').siblings().removeClass('unfold');
        profileLi.children('.subnav').children().eq(0).addClass('active').siblings().removeClass('active');
    } else if(url.indexOf('resetpwd') >= 0){  //重置密码
        var profileLi = $('.profile-li');
        profileLi.addClass('unfold').siblings().removeClass('unfold');
        profileLi.children('.subnav').children().eq(1).addClass('active').siblings().removeClass('active');
    } else if(url.indexOf('resetemail') >= 0){ //重置邮箱
        var profileLi = $('.profile-li');
        profileLi.addClass('unfold').siblings().removeClass('unfold');
        profileLi.children('.subnav').children().eq(2).addClass('active').siblings().removeClass('active');
    } else if(url.indexOf('post') >= 0){  //帖子管理
        var postManageLi = $('.post-manage');
        postManageLi.addClass('unfold').siblings().removeClass('unfold');
    } else if(url.indexOf('commen') >= 0){  //评论管理
        var postManageLi = $('.comments-manage');
        postManageLi.addClass('unfold').siblings().removeClass('unfold');
    }else if(url.indexOf('boarder') >= 0) { //板块管理
        var boardManageLi = $('.board-manage');
        boardManageLi.addClass('unfold').siblings().removeClass('unfold');
    } else if(url.indexOf('cmsuser') >= 0){ //cms管理
        var cmsuserManageLi = $('.cmsuser-manage');
        cmsuserManageLi.addClass('unfold').siblings().removeClass('unfold');
    }else if(url.indexOf('setCms') >= 0){ //cms管理
        var cmsuserManageLi = $('.cmsuser-manage');
        cmsuserManageLi.addClass('unfold').siblings().removeClass('unfold');
    }else if(url.indexOf('front') >= 0){ //板块管理
        var userManageLi = $('.user-manage');
        userManageLi.addClass('unfold').siblings().removeClass('unfold');
    }else if(url.indexOf('banner') >= 0){ //轮播图
        var bannerManageLi = $('.banner-manage');
        bannerManageLi.addClass('unfold').siblings().removeClass('unfold');
    }
});


