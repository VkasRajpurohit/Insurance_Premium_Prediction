# Required libraries
import logging as lg
import pickle

from flask import Flask, render_template, request
from flask_cors import cross_origin


app = Flask(__name__)  # app as object created
model = pickle.load(open("Stack_Reg_model.pkl", "rb"))  # trained model

# Create and configure logger
lg.basicConfig(filename="logfile.log", filemode='w', level=lg.INFO,
               format='%(asctime)s %(levelname)s: %(message)s',
               datefmt='%Y-%m-%d %H:%M:%S')

lg.info('app start- working fine')


@app.route('/')  # To render Home_Page
@cross_origin()
def home_page():
    """landing to home_page"""
    # render_template-- https://getbootstrap.com/
    lg.info('landing on home page- working fine')
    return render_template('index.html')


@app.route('/about')  # To render about page
@cross_origin()
def about():
    """about page-- app information"""
    lg.info('about page- working fine')
    return render_template('about.html')


@app.route('/contact')  # To render contact page
@cross_origin()
def contact():
    """contact information"""
    lg.info('contact page- working fine')
    return render_template('contact.html')


@app.route('/premium', methods=['POST'])   # To render result page-- premium
@cross_origin()
def predict_premium():
    """It will return predicted premium"""
    if request.method == 'POST':

        try:
            age = int(request.form['age'])

            sex = request.form['sex']
            if sex == 'male':
                sex_male = 1
            else:
                sex_male = 0

            bmi = float(request.form['bmi'])

            children = int(request.form['children'])

            smoker = request.form['smoker']
            if smoker == 'yes':
                smoker_yes = 1
            else:
                smoker_yes = 0

            region = request.form['region']
            if region == 'southeast':
                region_southeast = 1
                region_southwest = 0
                region_northwest = 0

            elif region == 'southwest':
                region_southeast = 0
                region_southwest = 1
                region_northwest = 0

            elif region == 'northwest':
                region_southeast = 0
                region_southwest = 0
                region_northwest = 1

            else:
                region_southeast = 0
                region_southwest = 0
                region_northwest = 0

            lg.info('input data: {}, {}, {}, {}, {}, {}'.format(age, sex, bmi, children, smoker, region))

            # Feature Transformation: Replacing feature Age with Exponential Transformation
            age = age**(1/1.2)

            prediction = model.predict([[age, bmi, children, sex_male, smoker_yes,
                                         region_northwest, region_southeast, region_southwest]])

            final_premium = round(prediction[0], 2)
            lg.info('Premium : {}'.format(final_premium))

        except Exception as e:
            lg.warning('unable to complete request: {}'.format(e))

    return render_template('premium.html', result=final_premium)


if __name__ == '__main__':
    app.run(debug=True)
