$(function () {                                     //添加CMS_USER
    $('#addcms').on('click',function (event) {
        event.preventDefault();
        var username=$('#username').val();
        var password=$('#password').val();
        var password1=$('#password1').val();
        var email=$('#email').val();
        var csrf_token=$('input[name=csrf_token]').val();
        $.ajax({
            url:'/cms/aCmsUser/',
            type:'post',
            data:{
                username:username,
                password:password,
                password1:password1,
                email:email,
                csrf_token:csrf_token
            },
            success:function (data) {
                if(data['code']===200){
                    xtalert.alertSuccessToast(data['message'])
                    setTimeout(function () {
                        window.location.reload()
                    },1000)
                }else{
                    xtalert.alertErrorToast(data['message'])
                }
            },
            error:function (error) {
                xtalert.alertNetworkError()
            }
        })
    })
});
console.log('abc');
$(function () {
    console.log(123);
    $('.setcms').on('click',function (event) {
        var self=$(this);
        console.log('hah');
        var cms_id=self.parent().parent().attr('cms_id');
        var href=self.attr('href');
        var newhref=href+'?cms_id='+cms_id
        self.attr('href',newhref)
    })
});

