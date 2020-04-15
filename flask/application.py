from flask import Flask, render_template, Markup, request, redirect, url_for, flash, session
import os, errno
import glob
import datetime
import subprocess
# import torch
# import student


UPLOAD_FOLDER = './upload_dir/'

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/start')
def start():
    folder = 'static/img/styles/'
    # images = [f for f in listdir(folder) if not f.startswith('.')]
    images = [f for f in sorted(glob.glob(folder+"*.jpg"))]
    html = ''
    styleimage = ''
    title = ''
    first_img = True
    i = 1
    for image in images:
        filename_split = os.path.splitext(os.path.basename(image))
        filename_zero, fileext = filename_split
        html += '<div class="style-item"><a href="#" class="style-anchor" tabindex="'+str(i)+'"><div style="background: url('+image+') no-repeat;background-size: cover;" alt="" id="'+filename_zero+'" class="thumbnail"></div><span>'+filename_zero+'</span></a></div>'
        #<div class="hover-links"><a href="" class="site-btn sb-light">'+os.path.basename(filename_zero)+'</a></div>
        i += 1
        if first_img:
            styleimage = '<img src="'+image+'" alt="" id="'+os.path.basename(filename_zero)+'">'
            first_img = False
            title = os.path.basename(filename_zero)
    return render_template('start.html', content=Markup(html), style=Markup(styleimage), title=title)

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/single')
def single():
    return render_template('gallery-single.html')

def create_dir():
    try:
        os.makedirs(UPLOAD_FOLDER)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


@app.route('/apply_style', methods=['GET', 'POST'])
def apply_style():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'video' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['video']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename_split = os.path.splitext(os.path.basename(file.filename))
            filename_zero, fileext = filename_split
            filename = filename_zero+"_"+datetime.datetime.now().strftime("%d%m%y%H")+fileext
            create_dir()
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            # flash('Uploaded')
            return '{"result":"Uploaded"}'

@app.route('/progress')
def progress():
    # for i in range(500):
    #   print("%d" % i)
    return '{"progress":500}'

  # net_pretrained = student.AnimalBaselineNet()
  # weights_path = os.path.join('.', 'model', 'baseline.pth')
  # net_pretrained.load_state_dict(torch.load(weights_path, map_location="cpu"))

  # for layer in net_pretrained.children():
  #     print(layer)

    # return ''

if __name__ == '__main__':
    # app.secret_key = b'6hc/_gsh,./;2ZZx3c6_s,1//'
    # app.config['SESSION_TYPE'] = 'filesystem'

    # session.init_app(app)
    app.run(debug=True)