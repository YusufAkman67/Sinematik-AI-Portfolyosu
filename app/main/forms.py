from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Optional

class PromptEntryForm(FlaskForm):
    title = StringField('Başlık', validators=[
        DataRequired(message='Başlık zorunludur.'),
        Length(1, 128, message='Başlık en fazla 128 karakter olabilir.')
    ])
    original_prompt = TextAreaField('Prompt (Girdi)', validators=[
        DataRequired(message='Prompt içeriği zorunludur.'),
        Length(1, 500, message='Prompt en fazla 500 karakter olabilir.')
    ])
    negative_prompt = TextAreaField('Negatif Prompt (İsteğe Bağlı)', validators=[
        Optional(),
        Length(0, 500, message='Negatif Prompt en fazla 500 karakter olabilir.')
    ])
    tags = StringField('Etiketler (Virgülle ayırarak girin)', validators=[
        Optional(),
        Length(0, 200, message='Etiket metni en fazla 200 karakter olabilir.')
    ])
    submit = SubmitField('Promptu Kaydet')

class AIDiaryEntryForm(FlaskForm):
    title = StringField('Günlük Başlığı', validators=[
        DataRequired(message='Günlük başlığı zorunludur.'),
        Length(1, 128, message='Başlık en fazla 128 karakter olabilir.')
    ])
    content = TextAreaField('Günlük İçeriği', validators=[
        DataRequired(message='Günlük içeriği zorunludur.'),
        Length(1, 2000, message='İçerik en fazla 2000 karakter olabilir.')
    ])
    prompt_entry_id = SelectField('İlişkili Prompt (İsteğe Bağlı)', coerce=int)
    submit = SubmitField('Günlüğü Kaydet')
