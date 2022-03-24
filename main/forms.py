from flask_wtf import FlaskForm
from sqlalchemy import String
from wtforms import StringField,EmailField,PasswordField,SubmitField,IntegerField,FileField,TextAreaField
from wtforms.validators import Length,EqualTo,Email,DataRequired
from main.models import Mevzuatlar


class GesCalc1(FlaskForm):
    aGuc = IntegerField(label='Anlaşma Gücü',validators=[DataRequired()])
    bFiyat = IntegerField(label='Birim Fiyat',validators=[DataRequired()])
    sycTuketim = IntegerField(label='Bir Sonraki Yıl Cari Fiyat',validators=[DataRequired()])
    submit =  SubmitField(label='submit')

class GesCalc2(FlaskForm):
    isim = StringField(label='Isim', validators=[DataRequired()])
    soyisim = StringField(label='Soyisim', validators=[DataRequired()])
    email = EmailField(label='Email', validators=[DataRequired()])
    numara = StringField(label='Numara', validators=[DataRequired()])
    submit = SubmitField(label='submit')

class ProjectsForm(FlaskForm):
    Name = StringField(label='Proje Adı', validators=[Length(max=30),DataRequired()])  
    location = StringField(label='Şehir', validators=[Length(max=30),DataRequired()])
    area = IntegerField(lable='Arazi km2', validators=[DataRequired()])
    explanation = StringField(label='Acıklama', validators=[DataRequired()])
    explanation2 =StringField(label='Açıklama2')
    rtmoney = StringField(label='Paranin Geri Dönüşümü')
    ppower = StringField(label='Uretilen Guc')
    profit = StringField(label='kazanc')
    file = FileField
    submit = SubmitField()

class MevzuatForm(FlaskForm):
    title = StringField(label='Title',validators=[DataRequired()])
    text = TextAreaField(label='Text',validators=[DataRequired()])
    submit = SubmitField()


