import configparser
from flask import Flask, render_template, redirect, url_for, request

# Read configuration from file.
config = configparser.ConfigParser()
config.read('config.ini')
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'


# Variables:
#    CC:    Cytogenic Category ("verygood","good","intermediate","poor","verypoor")
#    H:     Hemoglobin (g/dL)
#    P:     Platlets (x10^9L):
#    ANC:   Absolute Neutrophil Count (x10^9/L)
#    BMB:   Bome Marrow Blasts (percent)

def CalculateIPSSR(CC, BMB, H, P, ANC):
    return CC_Score(CC) + BMB_Score(BMB) + H_Score(H) + P_Score(P) + ANC_Score(ANC)


def CC_Score(CC):
    if CC == "verygood":
        return 0
    elif CC == "good":
        return 1
    elif CC == "intermediate":
        return 2
    elif CC == "poor":
        return 3
    elif CC == "verypoor":
        return 4
    else:
        return False


def BMB_Score(BMB):
    if BMB <= 2:
        return 0
    elif BMB < 5:
        return 1
    elif BMB < 10:
        return 2
    elif BMB <= 30:
        return 3
    else:
        return False


def H_Score(H):
    if H >= 10:
        return 0
    elif H > 8:
        return 1
    elif H >= 0:
        return 1.5
    else:
        return False


def P_Score(P):
    if P >= 100:
        return 0
    elif P >= 50:
        return 0.5
    elif P >= 0:
        return 1
    else:
        return False


def ANC_Score(ANC):
    if ANC >= 0.8:
        return 0
    elif ANC >= 0:
        return 0.5
    else:
        return False