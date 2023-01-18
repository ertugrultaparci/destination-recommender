from flask import Flask, render_template, flash, redirect, url_for, session, request
from wtforms import Form, BooleanField, StringField, validators
import destination_recommender
from destination_recommender import feature_encoder
import pandas as pd
from read_data import read_data

app = Flask(__name__)
app.debug=True
app.secret_key = "super secret key"

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/home')
def home():
    return render_template('home.html')



class RegisterForm(Form):
    name = StringField('', [validators.Length(min=1, max=500)], render_kw={"placeholder": "Please Enter Name here"})
    mail = StringField('', [validators.Length(min=1, max=500)], render_kw={"placeholder": "Please Enter E-mail here"})
    origin = StringField('', [validators.Length(min=1, max=500)], render_kw={"placeholder": "Please Enter Origin here"})



# User Register
@app.route('/code', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        mail = form.mail.data
        origin = form.origin.data
        print(name)
        print(mail)
        print(origin)


        dataframe = read_data('newdata.csv')

        # Encode the dataset:
        dataset = dataframe.values

        # categories and columns to be encoded
        name_to_encode = dataset[:,0]
        mail_to_encode = dataset[:,1]
        orig_to_encode = dataset[:,2]

        encoder_name = feature_encoder(name_to_encode)
        encoder_mail = feature_encoder(mail_to_encode)
        encoder_orig = feature_encoder(orig_to_encode)

        encoded_name = encoder_name.transform([name])
        encoded_mail = encoder_mail.transform([mail])
        encoded_orig = encoder_orig.transform([origin])

        new_test = pd.DataFrame()
        new_test['0'] = [int(encoded_name)]
        new_test['1'] = [int(encoded_mail)]
        new_test['2'] = [int(encoded_orig)]

        print(new_test)

        # Execute query
        out = destination_recommender.run(new_test)
        output=str(out)
        print(output)

        f = open("templates/outputs/Destination.html", "r")

        data = f.read()
        f.close()

        index_dest = data.index('<hh1>THE DESTINATION') + len('<hh1>THE DESTINATION')+ 3
        br_index = data.rindex('<br>')

        dest_old = data[index_dest: br_index].strip()

        x = data.replace(dest_old, output)

        f = open("templates/outputs/Destination.html", "w")
        f.write(x)
        f.close()

        return render_template("outputs/Destination.html")
    return render_template('code.html', form=form)


if __name__=='__main__':
    app.run()