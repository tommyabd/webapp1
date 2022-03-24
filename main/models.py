from sqlalchemy import Integer,String
from main import db 

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(), nullable=False, unique=False)
    email = db.Column(db.String(), nullable=True, unique=False)
    password_hash = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f'User {self.username}'

class HomePage(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    

class OnGrid(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    isim = db.Column(db.String(),nullable=False)
    soyisim = db.Column(db.String(), nullable=False)
    email = db.Column(db.String())
    numara = db.Column(db.String())
    gyetuketimi = db.Column(db.Integer())
    gesygsaati = db.Column(db.Integer())
    sozlemegucu = db.Column(db.Integer())
    ototumiktari = db.Column(db.Integer())
    alisvesatisbedeli = db.Column(db.Integer())
    alan = db.Column(db.Integer())

class Projects(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    location = db.Column(db.String(length=30))
    area = db.Column(db.Integer())
    eTitle = db.Column(db.String(length=100))
    explanation =db.Column(db.String())
    pTitle = db.Column(db.String(length=100))
    products = db.Column(db.String(length=100))
    gExplanation = db.Column(db.String(length=300))
    img = db.Column(db.String())
    rtMoney = db.Column(db.Integer())
    pPower = db.Column(db.Integer())
    profit = db.Column(db.Integer())

class Bilgilendirme(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    title = db.Column(db.String())
    text = db.Column(db.String())
    img = db.Column(db.String())

class Mevzuatlar(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String())
    text = db.Column(db.String())

    def __repr__(self):
        return f'MV {self.title}'
    
class Musteriler(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    isim = db.Column(db.String())
    soyisim = db.Column(db.String())
    email = db.Column(db.String())
    numara = db.Column(db.String())
    proje_tipi = db.Column(db.String())
    file = db.Column(db.String())

class OnGridText(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String())
    text = db.Column(db.String()) 

class iletisim(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String())
    number = db.Column(db.String())
    adress = db.Column(db.String())

class rltest1(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String())
    text = db.Column(db.String())
    tsts  = db.Column(db.Integer, db.ForeignKey('usrtest1.id'))

class usrtest1(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())
    lastname = db.Column(db.String())
    rlrl = db.relationship('rltest1', backref='backd')


# class OffGridEsya(db.Model):
#     id = db.Column(db.Integer(), primary_key=True)
#     esya = db.Column(db.String())
#     adet = db.Column(db.Integer())
#     birstw = db.Column(db.Integer())
#     GundeKullanimSuresi = db.Column(db.Integer())
#     GunduzKullanimSuresi = db.Column(db.Integer())
#     AksamKullanimSuresi = db.Column(db.Integer())
#     Gepa = db.Column(db.Integer())
#     OffGridId = db.Column(db.Integer())


