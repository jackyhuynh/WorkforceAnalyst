from flask import Flask, render_template, redirect, url_for, flash, abort, request
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from datetime import date
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from source.forms import LoginForm, RegisterForm, CreatePostForm, CommentForm
from flask_gravatar import Gravatar
from werkzeug.utils import secure_filename
import pandas as pd
import os
import re
import nltk
from nltk import pos_tag
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize


nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
ckeditor = CKEditor(app)
Bootstrap(app)
gravatar = Gravatar(app, size=100, rating='g', default='retro', force_default=False, force_lower=False, use_ssl=False,
                    base_url=None)


# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///blog.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


# UPLOAD FILE
UPLOAD_FOLDER = './data'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_PATH'] = 16 * 1000 * 1000


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# CONFIGURE TABLE
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    posts = relationship("BlogPost", back_populates="author")
    comments = relationship("Comment", back_populates="comment_author")


class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    author = relationship("User", back_populates="posts")
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    comments = relationship("Comment", back_populates="parent_post")


class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("blog_posts.id"))
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    parent_post = relationship("BlogPost", back_populates="comments")
    comment_author = relationship("User", back_populates="comments")
    text = db.Column(db.Text, nullable=False)


db.create_all()


def read_data_file(path):
    # Read in the data file
    dfjob = pd.read_csv(path)

    dfjob.drop(
        ['#', 'jobid', 'country', 'apply_link', 'company_link', 'date_posted_parsed', 'current_url', 'date_posted',
         'domain', 'region'], axis=1, inplace=True)
    # Drop the row where the company name or link is blank:
    dfjob.dropna(axis=0, how='all', subset=['company_name', 'job_type'], thresh=2, inplace=True)
    # Assume all the missing value in salary_formated is negotiable (50% of the dataset)
    dfjob['salary_formatted'] = dfjob['salary_formatted'].fillna('Negotiable')
    # Fill in the rating with 0
    dfjob['company_rating'] = dfjob['company_rating'].fillna(0.0)
    dfjob['company_reviews_count'] = dfjob['company_reviews_count'].fillna(0.0)

    return dfjob


def create_token(keyword_dict, dfjob):
    pos_tag(keyword_dict)
    ps = PorterStemmer()

    # process the job description.
    def prepare_job_desc(desc):
        # tokenize description.
        tokens = word_tokenize(desc)

        # Parts of speech (POS) tag tokens.
        token_tag = pos_tag(tokens)

        # Only include some POS tags.
        include_tags = ['VBN', 'VBD', 'JJ', 'JJS', 'JJR', 'CD', 'NN', 'NNS', 'NNP', 'NNPS']
        filtered_tokens = [tok for tok, tag in token_tag if tag in include_tags]

        # stem words.
        stemmed_tokens = [ps.stem(tok).lower() for tok in filtered_tokens]
        return set(stemmed_tokens)

    dfjob['job_description_word_set'] = dfjob['description_text'].map(prepare_job_desc)

    # process the keywords
    tool_keywords_set = set(
        [ps.stem(tok) for tok in keyword_dict])  # stem the keywords (since the job description is also stemmed.)
    tool_keywords_dict = {ps.stem(tok): tok for tok in
                          keyword_dict}  # use this dictionary to revert the stemmed words back to the original.
    return tool_keywords_set, tool_keywords_dict


def freq_skill_list(dfjob, tool_keywords_set, country_code=''):
    tool_list = []

    msk = dfjob['country_code'] != country_code  # just in case you want to filter the data.
    num_postings = len(dfjob[msk].index)
    for i in range(num_postings):
        job_desc = dfjob[msk].iloc[i]['description_text'].lower()
        job_desc_set = dfjob[msk].iloc[i]['job_description_word_set']
        # check if the keywords are in the job description. Look for exact match by token.
        tool_words = tool_keywords_set.intersection(job_desc_set)
        # label the job descriptions without any tool keywords.
        if len(tool_words) == 0:
            tool_list.append('nothing specified')

        tool_list += list(tool_words)

    return tool_list


#
def top_tool_list(tool_list, tool_keywords_dict, index):
    # create the list of tools.
    df_tool = pd.DataFrame(data={'cnt': tool_list})
    df_tool = df_tool.replace(tool_keywords_dict)
    df_tool_top = df_tool['cnt'].value_counts().reset_index().rename(columns={'index': 'tool'}).iloc[:index]
    df_tool_top['stats_percent'] = round((df_tool_top['cnt']/len(df_tool_top))*100)

    return df_tool_top


# Read the resume in
def read_resume():
    # Open text file resume
    file1 = open('../data_analyst/data/resume.txt', 'r')
    resume_data = []

    while True:
        # Get next line from file
        line = file1.readline()
        resume_data.append(line)
        # if line is empty or end of file is reached
        if not line:
            break
    file1.close()
    return resume_data


# Clean up the resume
def clean_resume_data(resume_data):
    # Clean up address, school, name, number, take only character in to the new string list
    for i in range(0, len(resume_data)):
        resume_data[i] = re.sub(r'\[.*?\]', '', resume_data[i])
        word1 = " ".join(re.findall("[a-zA-Z]+", resume_data[i]))
        resume_data[i] = word1

    # Using the keyword's dictionary to hold all the keyword
    keyword_dict = []

    for line in resume_data:
        li = list(line.split(" "))
        for string_ in li:
            keyword_dict.append(string_.lower())  # Convert the string to lower

    # Character that does not necessary to the search can be removed
    remove_characters = ['', 'a', 'truc', 'huynh', 'through', 'self', 'classroom', 'ide', 'concepts', 'founder',
                         'manager', 'online', 'first', 'second', 'are', 'was', 'unsatisfied',
                         'an', 'to', 'on', 'and', 'that', 'this', 'the', 'by', 'in', 'with', 's', 'of', 'non', 'co',
                         'my', 'your', 'his', 'her', 'they', 'their', 'he', 'she', 'it', 'under',
                         'may', 'guided', 'submit', 'vietnam', 'cis', 'any', 'unsatisfied', 'services', 'for',
                         'watercraft', 'specialist', 'us', 'recommendation', 'years', 'work', 'team',
                         'customer', 'ensure', 'supply', 'work', 'year', 'plans', 'customer', 'developing', 'records',
                         'technologies', 'computer', 'monitoring', 'building', 'market',
                         'ensures', 'supply', 'options', 'learn', 'master', 'recommendation', 'science', 'risk',
                         'strategize', 'experienced', 'create', 'tracking', 'stock', 'students',
                         'previous', 'concerns', 'structures', 'budget', 'next', 'methods', 'stakeholders', 'define',
                         'making', 'profits', 'achievement', 'address', 'routine', 'installed',
                         'visual', 'higher', 'coming', 'teaching', 'letters', 'chain', 'content', 'trading', 'cross',
                         'headquarters', 'audiences', 'increase', 'warehouse', 'loss', 'car',
                         'advice', 'highly', 'shows', 'toward', 'commander', 'compare', 'fiscal', 'directly',
                         'instructor', 'reduced', 'working', 'project', 'monitor', 'learning',
                         'ethical', 'teach', 'trade']

    soft_skill_remove = ["structure", "experience", "requirements", "worked", "years", "others", "skills",
                         "communication", "ability", "application", "program", "customers",
                         "company", "information", "plan", "knowledge", "benefit", "process", "training", "developed",
                         "assistant", "support", "schedules", "education",
                         "provided", "business", "operation", "systems", "oriented", "level", "base", "strong",
                         "procedures", "organization", "functional", "practices",
                         "reports", "office", "people", "certificate", "pay", "industries", "accountable", "staff",
                         "associate", "full", "equipment", "technology",
                         "maintaining", "design", "record", "clients", "bachelor", "projects", "issues", "using",
                         "relationship", "internal", "technical", "collaborative",
                         "meet", "implementation", "sales", "background", "detail", "preparing", "lead", "build",
                         "coordination", "monitored", "different", "software",
                         "marketing", "result", "weeks", "testing", "financial", "security", "proficient", "ensure",
                         "decision", "improve", "engineer", "efficiency",
                         "driving", "first", "futures", "instruction", "contracts", "strategies", "conducted",
                         "attention", "identified", "analytics", "evaluated"]
    for char in remove_characters:
        while char in keyword_dict:
            keyword_dict.remove(char)
    for char in soft_skill_remove:
        while char in keyword_dict:
            keyword_dict.remove(char)
    # remove the repeated word in the dictionary
    keyword_dict = list(dict.fromkeys(keyword_dict))

    return keyword_dict


def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.id != 1:
            return abort(403)
        return f(*args, **kwargs)

    return decorated_function


@app.route('/')
def get_all_posts():
    posts = BlogPost.query.all()

    return render_template("index.html", all_posts=posts, current_user=current_user)


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():

        if User.query.filter_by(email=form.email.data).first():
            print(User.query.filter_by(email=form.email.data).first())
            # User already exists
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))

        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            email=form.email.data,
            name=form.name.data,
            password=hash_and_salted_password,
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("get_all_posts"))

    return render_template("register.html", form=form, current_user=current_user)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()
        # Email doesn't exist or password incorrect.
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('get_all_posts'))
    return render_template("login.html", form=form, current_user=current_user)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))


@app.route("/post/<int:post_id>", methods=["GET", "POST"])
def show_post(post_id):
    form = CommentForm()
    requested_post = BlogPost.query.get(post_id)

    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("You need to login or register to comment.")
            return redirect(url_for("login"))

        new_comment = Comment(
            text=form.comment_text.data,
            comment_author=current_user,
            parent_post=requested_post
        )
        db.session.add(new_comment)
        db.session.commit()

    return render_template("post.html", post=requested_post, form=form, current_user=current_user)


@app.route("/about")
def about():
    return render_template("about.html", current_user=current_user)


@app.route("/new-post", methods=["GET", "POST"])
@admin_only
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user,
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))

    return render_template("make-post.html", form=form, current_user=current_user)


@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@admin_only
def edit_post(post_id):
    post = BlogPost.query.get(post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=current_user,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))

    return render_template("make-post.html", form=edit_form, is_edit=True, current_user=current_user)


@app.route("/delete/<int:post_id>")
@admin_only
def delete_post(post_id):
    post_to_delete = BlogPost.query.get(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    display = False
    if request.method == 'POST':

        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            display = True
            resume_dict = clean_resume_data(read_resume())
            data_file = read_data_file("../data_analyst/data/data.csv")
            tool_keywords_set, tool_keywords_dict = create_token(resume_dict, data_file)
            tool_list = freq_skill_list(data_file, tool_keywords_set)
            dftool_top_list = top_tool_list(tool_list, tool_keywords_dict, index=50)

            return render_template("upload.html", current_user=current_user, name=filename, display=display,
                                   resume_dict=resume_dict,
                                   column_names=dftool_top_list.columns.values, row_data=list(dftool_top_list.values.tolist()),
                                   link_column="Patient ID", zip=zip)

    return render_template("upload.html", current_user=current_user)


if __name__ == "__main__":
    app.run(debug=True)