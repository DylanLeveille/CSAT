# -*- coding: utf-8 -*-
from enum import Enum
from flask import Flask, render_template, request, flash, redirect, url_for
from markupsafe import Markup
from flask_wtf import FlaskForm, CSRFProtect
from wtforms.validators import DataRequired, Length, Regexp
# from wtforms.fields import *
from flask import send_file
from flask_bootstrap import Bootstrap5, SwitchField
from flask_sqlalchemy import SQLAlchemy

from components.uploadForm import UploadForm
from components.goalForm import GoalForm
from logic.logic import getResults

import itertools
import json
from copy import deepcopy
import random
import pandas
import re
from natsort import natsorted
import math
from functools import reduce
import sys

app = Flask(__name__)
app.secret_key = 'dev'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

# set default button sytle and size, will be overwritten by macro parameters
app.config['BOOTSTRAP_BTN_STYLE'] = 'primary'
app.config['BOOTSTRAP_BTN_SIZE'] = 'sm'

# set default icon title of table actions
app.config['BOOTSTRAP_TABLE_VIEW_TITLE'] = 'Read'
app.config['BOOTSTRAP_TABLE_EDIT_TITLE'] = 'Update'
app.config['BOOTSTRAP_TABLE_DELETE_TITLE'] = 'Remove'
app.config['BOOTSTRAP_TABLE_NEW_TITLE'] = 'Create'

bootstrap = Bootstrap5(app)
db = SQLAlchemy(app)
csrf = CSRFProtect(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    upload_form = UploadForm()
    if request.method == "POST":
        if 'getTemplate' in request.form:
            return send_file(
                'exampleControlSheets/template.xlsx',
                download_name='template.xlsx',
                as_attachment=True
            )

        elif 'getExample' in request.form:
            return send_file(
                'exampleControlSheets/templateFilledExampleCases.xlsx',
                download_name='templateExample.xlsx',
                as_attachment=True
            )

        elif 'uploadControl' in request.form:
            if upload_form.validate_on_submit():
                file = request.files['excel_file']
                global data
                global assets

                assets = dict()
                data = pandas.read_excel(file, keep_default_na=False) #get excel as pandas file

                i = 4
                while (i < len(data.columns)):
                    assets[data.columns[i]] = i
                    i += 3

                return render_template(
                    "attackerProfile.html",
                    asset_names = list(assets.keys()), 
                    asset_names_len = len(assets.keys()),
                    goal_form = GoalForm()
                )
        else: #we are on the objectives/budget page
            print(request)
            print(request.form)

            global objectivePriorities
            global budget

            objectivePriorities = ""

            "objectiveC-{{asset_names[i]}}-subgoal1"

            #check if at least one objective selected per subgoal
            subgoalNum = 1
            currAsset = ""
            symbol = "&"

            # oneObjectivePerSubgoal = False
            for input in request.form:
                if input.startswith("objective") and request.form[input] != '0': #means it is a checkbox objective and was checked
                    objectivesSplit = input.split("-")
                    assetSplit = objectivesSplit[1]
                    if input[-1] != str(subgoalNum): #means at different subgoal
                        symbol = ">"
                        currAsset = ""
                        subgoalNum += 1

                    if (assetSplit != currAsset):
                        currAsset = assetSplit

                        if input[-1] == str(subgoalNum): #means at same subgoal
                            objectivePriorities += "}"
                            objectivePriorities += symbol
                            objectivePriorities += (currAsset + "{")
                            symbol = "&"
                    
                    if objectivePriorities[-1] != "{":
                        objectivePriorities += ","
                    
                    objectivePriorities += objectivesSplit[0][-1]
                
                elif input.startswith("budget"):
                    budget = request.form[input]

            objectivePriorities += "}"
            objectivePriorities = objectivePriorities[2:]

            print(objectivePriorities)
            
            return render_template(
                    "loading.html",
                )
            
    return render_template(
        "index.html",
        form=upload_form,
    )

@app.route('/results', methods=['GET', 'POST'])
def results():
    resultByCases, optionalControls, mandatoryControls = getResults(data, assets, objectivePriorities, budget)
 
    return render_template(
                "report.html",
                resultByCases = resultByCases,
                optionalControls = optionalControls,
                mandatoryControls = mandatoryControls,
                data = data
            )

def natsortList(value, attribute=None):
    return natsorted(value)

if __name__ == '__main__':
    app.add_template_filter(natsortList)
    app.run(debug=True)
