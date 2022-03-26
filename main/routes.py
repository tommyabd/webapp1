
import email
from fileinput import filename
import os
from main import app
from main import db
from flask import render_template,request,redirect, session,url_for,send_file,flash
from main.forms import GesCalc1,GesCalc2,MevzuatForm
from main.models import Mevzuatlar,OnGrid,Projects,Bilgilendirme,Musteriler,OnGridText,iletisim,User
from openpyxl import load_workbook
from flask_login import login_required,login_user,logout_user
import smtplib


@app.route('/')
def index():
    projects = Projects.query.all()
    return render_template('index.html', projects=projects)

@app.route('/projects')
def projects():
    title = "Projeler"
    projects = Projects.query.all()
    return render_template('Projects/projects.html', projects=projects,title=title)

@app.route('/pr-info/<int:id>')
def pr_info(id):
    title = "Projeler"
    models = Projects.query.all()
    content = Projects.query.get(id)
    return render_template('Projects/project_info.html', content=content, models=models, id=id, title=title)

@app.route('/ongrid', methods=['GET', 'POST'])
def ongrid():
    if request.method == "POST":
        file  = load_workbook('main static excel BaseXlsx Ongrid_Hesap_Program.xlsx')
        
        sheet = file.active

        GecenYilkiEnerjiTuketimi = request.form.get('gyetuketimi')
        GesYeriYillikGuneslenmeSaati = request.form.get('gsaat')
        SozlesmeGucu = request.form.get('sgucu')
        EnerjiAlimVeSatimBedeli = request.form.get('easbedeli')
        name = request.form.get('isim')
        lastname = request.form.get('soyisim')
        alan = request.form.get('area')

        sheet['F4'] = int(GecenYilkiEnerjiTuketimi)
        sheet['F5'] = int(GesYeriYillikGuneslenmeSaati)
        sheet['F6'] = int(SozlesmeGucu)
        sheet['F9'] = int(EnerjiAlimVeSatimBedeli)
        sheet['H23'] = int(alan)
        file.save(os.path.join('main\static\excel', '{}.xlsx'.format(name+lastname)))
        filename = '{}.xlsx'.format(name+lastname)

        content_to_create = Musteriler(isim = request.form.get('isim'),
                                   soyisim = request.form.get('soyisim'),
                                    email = request.form.get('email'),
                                    numara = request.form.get('phone'),
                                    proje_tipi = "OnGrid",
                                    file = "{}.xlsx".format(name+lastname))
        db.session.add(content_to_create)
        model_to_create = OnGrid(isim = name,
                                 soyisim = lastname,
                                 email = request.form.get('email'),
                                 numara = request.form.get('phone'),
                                 gyetuketimi = GecenYilkiEnerjiTuketimi,
                                 gesygsaati = GesYeriYillikGuneslenmeSaati,
                                 sozlemegucu = SozlesmeGucu,
                                 alisvesatisbedeli = EnerjiAlimVeSatimBedeli,
                                 alan = alan)
        db.session.add(model_to_create)
        db.session.commit()   
        return redirect(url_for('ongrid_info', name=name, id=SozlesmeGucu, filename=filename ))
    return render_template('OnGrid_1.html', title='Projelendirme')

@app.route('/ongrid/<string:name>/<int:id>/<filename>', methods=['GET', 'POST'])
def ongrid_info(name,id,filename):
    model = OnGrid.query.filter_by(isim=name, sozlemegucu=id).first()
    content = OnGridText.query.all()

    data1 = model.gyetuketimi/365/model.gesygsaati
    data2 = model.sozlemegucu

    # mesage = "{}".format(filename)
    # server = smtplib.SMTP('smtp.gmail.com')
    # server.starttls()
    # server.login("qurdalamag@gmail.com", "Parol555")
    # server.sendmail("qurdalamag@gmail.com","tamerlan.abdullayev23@gmail.com", mesage)
    return render_template('OnGrid_Info.html', data1=data1, data2=data2, content=content, filename=filename, title="Projelendirme")

@app.route('/offgrid', methods=['GET','POST'])
def offgrid():
    content = OnGridText.query.all()
    if request.method == "POST":
        file = load_workbook(url_for('static',filename='excel/BaseXlsx/Ongrid_Hesap_Program.xlsx'))
        sheet = file.active

        name = request.form.get('isim')
        lastname = request.form.get('soyisim')
        gepa = request.form.get('gepa')
        number = request.form.get('phone')
        email = request.form.get('email')
        filename = '{}offgrid.xlsx'.format(name+lastname)

        content_to_create=Musteriler(isim=name,soyisim=lastname,email=email,numara=number,proje_tipi='OffGrid',file=filename)
        db.session.add(content_to_create)
        db.session.commit()

        mesage = "{}".format(filename)
        

        for i in range(4,15):
            datab = []
            datab += [request.form.get('{}adet'.format(i))]
            datab += [request.form.get('{}1stw'.format(i))]
            datab += [request.form.get('{}gks'.format(i))]
            datab += [request.form.get('{}aks'.format(i))]

        for x in range(0,11):
            sheet['B{}'.format(4+x)] = datab[0]
            sheet['C{}'.format(4+x)] = datab[1]
            sheet['E{}'.format(4+x)] = datab[2]
            sheet['H{}'.format(4+x)] = datab[3]
            sheet['D{}'.format(4+x)] = int(datab[2])+int(datab[3])

        file.save(os.path.join('main\static\excel', '{}offgrid.xlsx'.format(name+lastname)))

        return redirect(url_for('offgrid_info', filename='{}offgrid.xlsx'.format(name+lastname)))
    return render_template('OffGrid.html')

@app.route('/offgrid_info/<string:filename>', methods=['GET', 'POST'])
def offgrid_info(filename):
    model = Musteriler.query.filter_by(file='{}offgird.xlsx'.format(filename))
    content = OnGridText.query.all()
    
    # server = smtplib.SMTP('smtp.gmail.com')
    # server.starttls()
    # server.login("qurdalamag@gmail.com", "Parol555")
    # server.sendmail("qurdalamag@gmail.com","tamerlan.abdullayev23@gmail.com", filename)

    filename2 = '{}offgird.xlsx'.format(filename)
    return render_template('OffGrid_Info.html', filename=filename, content=content)

@app.route('/projelendirme')
def projelendirme():
    return render_template('projelendirme.html',title='Projelendirme')

@app.route('/mevzuatlar', methods=['GET','POST'])
def mevzuatlar():
    models = Mevzuatlar.query.all()
    return render_template('mevzuatlar.html', title='Mevzuatlar', models = models)

@app.route('/bilgilendirme/<int:id>', methods=['GET'])
def bilgilendirme(id):
    title = "Bilgilendirmeler"
    models = Bilgilendirme.query.all()
    content = Bilgilendirme.query.get(id)
    return render_template('bilgilendirme.html', content=content, models=models,title=title)

@app.route('/bize_ulash' ,methods=['GET','POST'])
def contactus():
    return render_template('bizeulas.html')

@app.route('/file_download/<filename>')
def fd(filename):
    return send_file('static\excel\{}'.format(filename),as_attachment=True)

# --------- Admin Panel Routes --------------------

@app.route('/admin')
@login_required
def admin():
    return render_template('admin/index.html')

# ---------  Admin Login --------------------------
@app.route('/login', methods=['GET','POST'])
def admin_login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        attempted_user = User.query.filter_by(username=username).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=request.form.get('password')):
            login_user(attempted_user)
            return redirect(url_for('admin'))
        else:
            flash('Kullanıcı İsminizi Veya Şifrenizi Yalnış Girdiniz!')

    return render_template('admin/login.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('login')

# --------- Iletisim ------------------------------
@app.route('/admin/iletisim', methods=['GET','POST'])
def admin_iletisim():
    content = iletisim.query.get(1)
    if request.method == 'POST':
        content.email = request.form.get('email')
        content.number = request.form.get('numara')
        content.adress = request.form.get('adress')
        db.session.commit()
    return render_template('admin/iletisim.html', content=content)

# --------- Mevzuatlar------------------------
@app.route('/admin/mevzuatlar', methods=['GET','POST'])
def admin_mevzuatlar():
    model = Mevzuatlar.query.all()
    return render_template('admin/mevzuats.html', model=model) 

@app.route('/admin/mv-add', methods=['GET','POST'])
def mevzuat_add():
    if request.method == "POST":
        content_to_create = Mevzuatlar(title = request.form.get('title'),
                                    text = request.form.get('ckeditor'))
        db.session.add(content_to_create)
        db.session.commit()
        return redirect(url_for("admin_mevzuatlar"))
    return render_template('admin/Mevzuatlar/mevzuat_add.html')

@app.route('/admin/mv-delete/<int:id>')
def mv_delete(id):
    mdelete=Mevzuatlar.query.get_or_404(id)
    db.session.delete(mdelete)
    db.session.commit()
    return redirect(url_for("admin_mevzuatlar"))

@app.route('/admin/mv-update/<int:i>', methods=['GET', 'POST'])
def mv_update(i):
    model = Mevzuatlar()
    content = model.query.get(i)

    if request.method == "POST":
       content.title = request.form.get('title')
       content.text = request.form.get('ckeditor')
       db.session.commit()
       return redirect(url_for("admin_mevzuatlar"))
    return render_template('admin/Mevzuatlar/mevzuat_update.html', content=content)

@app.route('/admin/mevzuat/<int:id>', methods=['GET','POST'])
def mv_info(id):
    model = Mevzuatlar()
    content = model.query.get(id)
    return render_template('admin/Mevzuatlar/mevzuat_info.html', content=content)


# --------- Projeler-------------------------
@app.route('/admin/projeler')
def admin_projeler():
    model = Projects.query.all()
    return render_template('admin/Projeler/projects.html', model=model)

@app.route('/admin/pj-creat/', methods=['GET', 'POST'])
def pj_create():
    model = Projects()
    if request.method == "POST":
        f = request.files['photo']
        fname = f.filename
        if fname:     
            f.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(fname)))
        content_to_create = Projects(name = request.form.get('name'),
                                    location = request.form.get('location'),
                                    area = request.form.get('area'),
                                    explanation = request.form.get('exp'),
                                    products = request.form.get('product'),
                                    gExplanation = request.form.get('grafic'),
                                    rtMoney = request.form.get('rtm'),
                                    pPower = request.form.get('ppower'),
                                    profit = request.form.get('profit'),
                                    img = fname)
        db.session.add(content_to_create)                            
        db.session.commit()
        return redirect(url_for('admin_projeler'))
    return render_template('admin/Projeler/proje_add.html')

@app.route('/admin/pj-delete/<int:id>')
def pf_delete(id):
    model = Projects.query.get_or_404(id)
    db.session.delete(model)
    db.session.commit()
    return redirect(url_for("admin_projeler"))

@app.route('/admin/pj-update/<int:id>', methods=['GET','POST'])
def pj_update(id):
    model = Projects.query.get(id)
    if request.method == 'POST':
        f = request.files['photo']
        fname = f.filename
        if fname:     
            f.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(fname)))

        model.name = request.form.get('name')
        model.location = request.form.get('location')
        model.area = request.form.get('area')
        model.explanation = request.form.get('exp')
        model.products = request.form.get('product')
        model.gExplanation = request.form.get('grafic')
        model.rtMoney = request.form.get('rtm')
        model.pPower = request.form.get('ppower')
        model.profit = request.form.get('profit')
        model.img = fname

        db.session.commit()
        return redirect(url_for('admin_projeler'))
    return render_template('admin/Projeler/proje_update.html', model=model)

@app.route('/admin/pj-info/<int:id>')
def  pj_info(id):
    content = Projects.query.get(id)
    return render_template('admin/Projeler/proje_info.html', content=content)



#----- Bilgilendirme ------------
@app.route('/admin/bilgilendirme')
def admin_bilgilendirme():
    content = Bilgilendirme.query.all()
    return render_template('admin/Bilgilendirme/bilgilendirme.html', model=content)

@app.route('/admin/bg_create', methods=['GET','POST'])
def bg_create():
    if request.method == "POST":
        f = request.files['photo']
        fname = f.filename
        if fname:
            f.save(os.path.join(app.config['UPLOAD_FOLDER'],'Bilgilendirme',secure_filename(fname)))
        content_to_create = Bilgilendirme(title = request.form.get('title'),
                                          text = request.form.get('ckeditor'),
                                          img = fname)
        db.session.add(content_to_create)
        db.session.commit()
        return redirect(url_for('admin_bilgilendirme'))
    return render_template('admin/Bilgilendirme/bilgilendirme_create.html')

@app.route('/admin/bg_update/<int:id>', methods=['GET','POST'])
def bg_update(id):
    content = Bilgilendirme.query.get(id)
    if request.method == "POST":
        f = request.files['photo']
        fname = f.filename
        if fname:
            f.save(os.path.join(app.config['UPLOAD_FOLDER'],'Bilgilendirme',secure_filename(fname)))   
        else:
            fname = content.img
            
        content.title = request.form.get('title')
        content.text = request.form.get('ckeditor')
        content.img = fname
        db.session.commit()
        return redirect(url_for('admin_bilgilendirme'))
    return render_template('admin/Bilgilendirme/bilgilendirme_update.html', content=content)

@app.route('/admin/bg_delete/<int:id>', methods=['GET','POST'])
def bg_delete(id):
    content = Bilgilendirme.query.get_or_404(id)
    db.session.delete(content)
    db.session.commit()
    return redirect(url_for('admin_bilgilendirme'))

@app.route('/admin/ongrid_text', methods=['GET', 'POST'])
def admin_ongrid_text():
    content = OnGridText.query.all()
    return render_template('admin/OnGrid/ongrid_text.html', content=content)

@app.route('/admin/ongrid_text/create', methods=['GET', 'POST'])
def og_create():
    if request.method == "POST":
        content_to_create = OnGridText(title = request.form.get('title'),
                                        text = request.form.get('ckeditor'))
        db.session.add(content_to_create)
        db.session.commit()
        return redirect(url_for('admin_ongrid_text'))
    return render_template('admin/OnGrid/ongrid_create.html')

@app.route('/admin/bg_update/<int:id>', methods=['GET','POST'])
def og_update(id):
    content = OnGridText.query.get(id)
    if request.method == "POST":
        content.title = request.form.get('title')
        content.text = request.form.get('ckeditor')
        db.session.commit()
        return redirect(url_for('admin_ongrid_text'))
    return render_template('admin/OnGrid/ongrid_text_update.html', content=content)

@app.route('/admin/bg_delete/<int:id>', methods=['GET','POST'])
def og_delete(id):
    content = OnGridText.query.get_or_404(id)
    db.session.delete(content)
    db.session.commit()
    return redirect(url_for('admin_ongrid_text'))
