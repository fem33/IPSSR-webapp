import configparser
from flask import Flask, render_template, redirect, url_for, request

# Read configuration from file.
config = configparser.ConfigParser()
config.read('config.ini')
app = Flask(__name__, template_folder='templates')

cyto = ""
blast = ""
hemo = ""
plate = ""
anc = ""


@app.route('/main', methods=['GET', 'POST'])
def main():
    global cyto
    global blast
    global hemo
    global plate
    global anc

    score = calculate_ipssr(cyto, int(blast), int(hemo), int(plate), int(anc))
    category = calculate_cat(score)
    values = {"score": score,
              "category": category}
    return render_template('home.html', elements = values)


@app.route('/', methods=['GET', 'POST'])
def start():
    if "marrow" and "hemoglobin" and "platelets" and "anc" and "cyto" in request.form:
        global cyto
        global blast
        global hemo
        global plate
        global anc

        cyto = request.form['cyto']
        blast = request.form['marrow']
        hemo = request.form['hemoglobin']
        plate = request.form['platelets']
        anc = request.form['anc']

        return redirect(url_for('main'))
    else:
        return render_template('start.html')


# Variables:
#    cc:    Cytogenic Category ("verygood","good","intermediate","poor","verypoor")
#    h:     Hemoglobin (g/dL)
#    p:     Platlets (x10^9L):
#    anc:   Absolute Neutrophil Count (x10^9/L)
#    bmb:   Bome Marrow Blasts (percent)

def calculate_ipssr(cc, bmb, h, p, anc):
    return cc_score(cc) + bmb_score(bmb) + h_score(h) + p_score(p) + anc_score(anc)


def calculate_cat(score):
    if score <= 1.5:
        return "Very Low"
    elif score > 1.5 and score <= 3:
        return "Low"
    elif score > 3 and score <= 4.5:
        return "Intermediate"
    elif score > 4.5 and score <= 6:
        return "High"
    elif score > 6:
        return "Very High"
    else:
        return "Could not calculate score"


def cc_score(cc):
    if cc == "verygood":
        return 0
    elif cc == "good":
        return 1
    elif cc == "intermediate":
        return 2
    elif cc == "poor":
        return 3
    elif cc == "verypoor":
        return 4
    else:
        return False


def bmb_score(bmb):
    if bmb <= 2:
        return 0
    elif bmb < 5:
        return 1
    elif bmb < 10:
        return 2
    elif bmb <= 30:
        return 3
    else:
        return False


def h_score(h):
    if h >= 10:
        return 0
    elif h > 8:
        return 1
    elif h >= 0:
        return 1.5
    else:
        return False


def p_score(p):
    if p >= 100:
        return 0
    elif p >= 50:
        return 0.5
    elif p >= 0:
        return 1
    else:
        return False


def anc_score(anc):
    if anc >= 0.8:
        return 0
    elif anc >= 0:
        return 0.5
    else:
        return False