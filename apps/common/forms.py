from wtforms import StringField,IntegerField,Form
from wtforms.validators import Length,Email,Regexp,ValidationError
from apps.front.models import Front_user


class mobile_verify(Form):
    mobile=StringField(validators=[Regexp('^1(?:3\d|4[4-9]|5[0-35-9]|6[67]|7[013-8]|8\d|9\d)\d{8}$',message='请输入正确的手机号码')])

    def validate_mobile(self,field):
        mobile=field.data
        user=Front_user.query.filter_by(telephone=mobile).first()
        if user:
            raise ValidationError(message='您已经注册过了')



class resetpasswd_verify(Form):
    mobile = StringField(
        validators=[Regexp('^1(?:3\d|4[4-9]|5[0-35-9]|6[67]|7[013-8]|8\d|9\d)\d{8}$', message='请输入正确的手机号码')])