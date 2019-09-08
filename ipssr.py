import configparser
from flask import Flask, render_template, redirect, url_for, request

# Read configuration from file.
config = configparser.ConfigParser()
config.read('config.ini')
app = Flask(__name__)

@app.route('/main')
def main():
    cc = request.form['cyto']
    bmb = request.form['marrow']
    h = request.form['hemoglobin']
    p = request.form['platelets']
    anc = request.form['anc']

    score = calculate_ipssr(cc, bmb, h, p, anc)
    values = {"score":score}
    return render_template('home.html', elements = values)


# Variables:
#    cc:    Cytogenic Category ("verygood","good","intermediate","poor","verypoor")
#    h:     Hemoglobin (g/dL)
#    p:     Platlets (x10^9L):
#    anc:   Absolute Neutrophil Count (x10^9/L)
#    bmb:   Bome Marrow Blasts (percent)

def calculate_ipssr(cc, bmb, h, p, anc):
    return cc_score(cc) + bmb_score(bmb) + h_score(h) + p_score(p) + anc_score(anc)


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