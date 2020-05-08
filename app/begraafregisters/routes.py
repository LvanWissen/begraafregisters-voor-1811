from flask import render_template
from flask import render_template, redirect

from begraafregisters import app, db
from begraafregisters.models import Record
from begraafregisters.utils import getRdf


def get_value(model, c):
    return getattr(model, c)


@app.route('/login', methods=['GET', 'POST'])
def login():

    return "test"


@app.route('/record/<id>', methods=['GET'])
def getRecordView(id):

    model = db.session.query(Record).filter_by(id=id).one()

    return render_template('record.html',
                           model=model,
                           details_columns=[
                               'id', 'inventory', 'church', 'date', 'buried',
                               'registered', 'relationinfo', 'source', 'scan'
                           ],
                           get_value=get_value,
                           jsonld=getRdf(model, format='json-ld'),
                           turtle=getRdf(model, format='turtle'))

    return getRdf(model, format='turtle')