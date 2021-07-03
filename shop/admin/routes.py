from flask import render_template,session, request,redirect,url_for,flash
from shop import app,db,bcrypt
from .forms import RegistrationForm,LoginForm
from .models import Register
from shop.products.models import Addproduct,Category,Brand
import os, datetime



@app.route('/admin')
def admin():
    if 'email' not in session:
        flash(f'please login first','warning')
        return redirect(url_for('login'))
    products = Addproduct.query.all()
    return render_template('admin/index.html', title='Admin page',products=products)

@app.route('/brands')
def brands():
    brands = Brand.query.order_by(Brand.id.desc()).all()
    return render_template('admin/brand.html', title='brands',brands=brands)


@app.route('/categories')
def categories():
  categories = Category.query.order_by(Category.id.desc()).all()
  return render_template('admin/brand.html', title='categories',categories=categories)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    today = datetime.datetime.now()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        user = Register(name=form.name.data,username=form.username.data, email=form.email.data,
                    password=hash_password, date_created = today)
        db.session.add(user)
        flash(f'welcome {form.name.data} Thanks for registering','success')
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('admin/register.html',title='Register user', form=form)


@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm(request.form)
    if request.method == "POST"and form.validate():
        user = Register.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['email'] = form.email.data
            flash(f'welcome {form.email.data}, you are now logged in...','success')
            return redirect(request.args.get('next') or url_for('admin'))
        else:
            flash(f'Wrong email or password', 'warning')
            return redirect(url_for('login'))
    return render_template('admin/login.html',title='Login page',form=form)