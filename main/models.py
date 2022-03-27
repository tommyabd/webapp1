from sqlalchemy import Integer,String
from main import db, loginmanager
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user,current_user
from main import bcrypt

@loginmanager.user_loader  
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(), nullable=False, unique=False)
    email = db.Column(db.String())
    password_hash = db.Column(db.String(), nullable=False)

    @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')   

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password) 
            

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

class Kur(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    kur = db.Column(db.Integer())

