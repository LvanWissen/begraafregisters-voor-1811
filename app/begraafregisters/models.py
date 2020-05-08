from sqlalchemy.ext.associationproxy import association_proxy
from flask_admin._compat import as_unicode, string_types, text_type

from begraafregisters import db


class Person(db.Model):
    __tablename__ = "person"
    id = db.Column('id', db.Integer, primary_key=True)
    gender = db.Column('gender', db.Unicode)

    name = association_proxy('names', 'literalname')

    # related_to = db.relationship(
    #     'Person',
    #     secondary='person2person',
    #     primaryjoin="Person.id==Person2person.p1_id",
    #     secondaryjoin="Person.id==Person2person.p2_id",
    #     backref="related_from")

    def __repr__(self):
        # return self.name
        return ', '.join(text_type(v) for v in self.name)
        # return self.id

    def __str__(self):
        # return self.name
        return ', '.join(text_type(v) for v in self.name)
        # return "Test"
        # return self.name


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

    church = db.relationship('Church',
                             foreign_keys=church_id,
                             backref='records')
    scan = db.relationship('Scan', foreign_keys=scan_id, backref='records')
    relationinfo = db.relationship('Relationinfo',
                                   foreign_keys=relationinfo_id,
                                   backref='records')

    registered = db.relationship(
        "Person",
        secondary='record2person',
        primaryjoin=
        "and_(Record.id==Record2person.record_id, Record2person.buried==False)"
    )
    buried = db.relationship(
        "Person",
        secondary='record2person',
        primaryjoin=
        "and_(Record.id==Record2person.record_id, Record2person.buried==True)")

    # registered = association_proxy('registered_p', 'name')
    # buried = association_proxy('buried_p', 'name')

    def __repr__(self):
        return self.id


class Record2person(db.Model):
    __tablename__ = "record2person"
    id = db.Column('id', db.Integer, primary_key=True)
    record_id = db.Column('record_id', db.Unicode, db.ForeignKey('record.id'))
    person_id = db.Column('person_id', db.Integer, db.ForeignKey('person.id'))
    buried = db.Column('buried', db.Boolean, default=False)

    person = db.relationship('Person',
                             foreign_keys=person_id,
                             backref='record')
    record = db.relationship('Record', foreign_keys=record_id)

    def __repr__(self):
        return self.record.id


class Personname(db.Model):
    __tablename__ = "personname"
    id = db.Column('id', db.Integer, primary_key=True)
    givenname = db.Column('givenName', db.Unicode)
    patronym = db.Column('patronym', db.Unicode)
    surnameprefix = db.Column('surnamePrefix', db.Unicode)
    basesurname = db.Column('baseSurname', db.Unicode)
    literalname = db.Column('literalName', db.Unicode)

    persons = db.relationship('Person',
                              secondary='person2personname',
                              backref='names')

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

    person1 = db.relationship('Person',
                              foreign_keys=p1_id,
                              backref='related_to')
    person2 = db.relationship('Person', foreign_keys=p2_id)

    def __repr__(self):

        return f"{self.person2} ({self.relationinfo})"


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
    id = db.Column('id', db.Unicode, primary_key=True)
    name = db.Column('name', db.Unicode)
    uuid = db.Column('uuid', db.Unicode)
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
