from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:example@localhost:8123/begraafregisters'
db = SQLAlchemy(app)


class Person(db.Model):
    __tablename__ = "person"
    id = db.Column('id', db.Integer, primary_key=True)
    gender = db.Column('gender', db.Enum('male', 'female', name='genders'))

    names = db.relationship('Personname', secondary='person2personname')


class Record(db.Model):
    __tablename__ = "record"
    id = db.Column('id', db.Unicode, primary_key=True)
    inventory = db.Column('inventory', db.Unicode)
    date = db.Column('date', db.Date)
    church_id = db.Column('church_id', db.Integer, db.ForeignKey('church.id'))
    source = db.Column('source', db.Unicode)
    scan_id = db.Column('scan_id', db.Integer, db.ForeignKey('scan.id'))
    relationinfo_id = db.Column('relationinfo_id', db.Integer,
                                db.ForeignKey('relationinfo.id'))

    church = db.relationship('Church', foreign_keys=church_id)
    scan = db.relationship('Scan', foreign_keys=scan_id)
    relationinfo = db.relationship('Relationinfo',
                                   foreign_keys=relationinfo_id)

    registered = db.relationship(
        "Record2person",
        primaryjoin=
        "and_(Record.id==Record2person.record_id, Record2person.buried==False)"
    )
    buried = db.relationship(
        "Record2person",
        primaryjoin=
        "and_(Record.id==Record2person.record_id, Record2person.buried==True)")

    def __repr__(self):
        return self.id


class Record2person(db.Model):
    __tablename__ = "record2person"
    id = db.Column('id', db.Integer, primary_key=True)
    record_id = db.Column('record_id', db.Unicode, db.ForeignKey('record.id'))
    person_id = db.Column('person_id', db.Integer, db.ForeignKey('person.id'))
    buried = db.Column('buried', db.Boolean, default=False)

    person = db.relationship('Person', foreign_keys=person_id)
    record = db.relationship('Record', foreign_keys=record_id)

    def __repr__(self):
        return self.person.names[0].literalname


class Personname(db.Model):
    __tablename__ = "personname"
    id = db.Column('id', db.Integer, primary_key=True)
    givenname = db.Column('givenName', db.Unicode)
    patronym = db.Column('patronym', db.Unicode)
    surnameprefix = db.Column('surnamePrefix', db.Unicode)
    basesurname = db.Column('baseSurname', db.Unicode)
    literalname = db.Column('literalName', db.Unicode)

    def __repr__(self):
        return self.literalname


class Person2person(db.Model):
    __tablename__ = "person2person"
    id = db.Column('id', db.Integer, primary_key=True)
    p1_id = db.Column('p1_id', db.Integer, db.ForeignKey('person.id'))
    p2_id = db.Column('p2_id', db.Integer, db.ForeignKey('person.id'))
    relationinfo_id = db.Column('relationinfo_id', db.Integer,
                                db.ForeignKey('relationinfo.id'))

    relationinfo = db.relationship('Relationinfo',
                                   foreign_keys=relationinfo_id)
    person1 = db.relationship('Person', foreign_keys=p1_id)
    person2 = db.relationship('Person', foreign_keys=p2_id)


class Relationinfo(db.Model):
    __tablename__ = "relationinfo"
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.deferred(db.Column('name', db.Text))
    parent_category_id = db.Column('parent_category_id', db.Integer,
                                   db.ForeignKey('relationinfo.id'))

    parent_category = db.relationship('Relationinfo',
                                      foreign_keys=parent_category_id)

    def __repr__(self):
        return self.name


class Church(db.Model):
    __tablename__ = "church"
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.Unicode)

    def __repr__(self):
        return self.name


class Scan(db.Model):
    __tablename__ = "scan"
    id = db.Column('id', db.Integer, primary_key=True)
    url = db.Column('url', db.Unicode)

    def __repr__(self):
        _, url = self.url.rsplit('#', 1)
        return url


class Person2personname(db.Model):
    __tablename__ = "person2personname"
    id = db.Column('id', db.Integer, primary_key=True)
    person_id = db.Column('person_id', db.Integer, db.ForeignKey('person.id'))
    personname_id = db.Column('personname_id', db.Integer,
                              db.ForeignKey('personname.id'))

    person = db.relationship('Person', foreign_keys=person_id)
    personname = db.relationship('Personname', foreign_keys=personname_id)


if __name__ == '__main__':

    app.config['FLASK_ADMIN_SWATCH'] = 'flatly'
    admin = Admin(app, name='Begraafregisters', template_mode='bootstrap3')

    class FullViewRecord(ModelView):
        column_display_pk = True
        column_display_all_relations = True

        form_ajax_refs = {
            'church': {
                'fields': ['name'],
                'page_size': 10
            },
            'scan': {
                'fields': ['url'],
                'page_size': 10
            },
            'registered': {
                'fields': ['person'],
                'page_size': 10
            },
            'buried': {
                'fields': ['person'],
                'page_size': 10
            }
        }

    class FullViewPerson(ModelView):
        column_display_pk = True
        column_display_all_relations = True

        form_ajax_refs = {
            'names': {
                'fields':
                ['givenname', 'basesurname', 'surnameprefix', 'literalname'],
                'page_size':
                10
            }
        }

    admin.add_view(FullViewRecord(Record, db.session))
    admin.add_view(FullViewPerson(Person, db.session))
    #admin.add_view(FullView(Personname, db.session))
    #admin.add_view(FullView(Relationinfo, db.session))
    #admin.add_view(FullView(Scan, db.session))

    db.create_all()
    app.run('0.0.0.0', 8000)
