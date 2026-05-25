from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError, Regexp
from app.models import User

class LoginForm(FlaskForm):
    username_or_email = StringField('Kullanıcı Adı veya E-posta', validators=[
        DataRequired(message='Bu alan zorunludur.'),
        Length(1, 120, message='Maksimum 120 karakter olmalıdır.')
    ])
    password = PasswordField('Şifre', validators=[
        DataRequired(message='Şifre zorunludur.')
    ])
    remember_me = BooleanField('Beni Hatırla')
    submit = SubmitField('Giriş Yap')

class RegisterForm(FlaskForm):
    username = StringField('Kullanıcı Adı', validators=[
        DataRequired(message='Kullanıcı adı zorunludur.'),
        Length(3, 64, message='Kullanıcı adı 3 ile 64 karakter arasında olmalıdır.'),
        Regexp(r'^[A-Za-z0-9_.]+$', message='Kullanıcı adı sadece harf, rakam, nokta ve alt çizgi içerebilir.')
    ])
    email = StringField('E-posta', validators=[
        DataRequired(message='E-posta zorunludur.'),
        Regexp(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', message='Geçersiz e-posta adresi.'),
        Length(1, 120, message='E-posta maksimum 120 karakter olmalıdır.')
    ])
    password = PasswordField('Şifre', validators=[
        DataRequired(message='Şifre zorunludur.'),
        Length(6, 128, message='Şifre en az 6 karakter olmalıdır.')
    ])
    confirm_password = PasswordField('Şifreyi Onayla', validators=[
        DataRequired(message='Lütfen şifrenizi tekrar girin.'),
        EqualTo('password', message='Şifreler eşleşmiyor.')
    ])
    submit = SubmitField('Kayıt Ol')

    def validate_username(self, field):
        user = User.query.filter_by(username=field.data).first()
        if user:
            raise ValidationError('Bu kullanıcı adı zaten alınmış.')

    def validate_email(self, field):
        user = User.query.filter_by(email=field.data).first()
        if user:
            raise ValidationError('Bu e-posta adresi zaten kayıtlı.')
