# -*- encoding: utf-8 -*-
# begin

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy import Column, Integer, BigInteger, String, ForeignKey, Unicode, Binary, LargeBinary, Time, DateTime, Date, Text, Boolean, Float, JSON, Enum
from sqlalchemy.orm import relationship, backref, deferred
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Person(Base):
    __tablename__ = "person"
    id = Column('id', Integer, primary_key=True)
    # name = Column('name', Unicode)
    name = association_proxy('names', 'literalname')
    gender = Column('gender', Enum('male', 'female', name='genders'))

    names = relationship('Personname', secondary='person2personname')


class Record(Base):
    __tablename__ = "record"
    id = Column('id', Unicode, primary_key=True)
    inventory = Column('inventory', Unicode)
    date = Column('date', Date)
    church_id = Column('church_id', Integer, ForeignKey('church.id'))
    source = Column('source', Unicode)
    scan_id = Column('scan_id', Integer, ForeignKey('scan.id'))
    relationinfo_id = Column('relationinfo_id', Integer,
                             ForeignKey('relationinfo.id'))

    church = relationship('Church', foreign_keys=church_id)
    scan = relationship('Scan', foreign_keys=scan_id)
    relationinfo = relationship('Relationinfo', foreign_keys=relationinfo_id)

    registered = relationship(
        "Record2person",
        primaryjoin=
        "and_(Record.id==Record2person.record_id, Record2person.buried==False)"
    )
    buried = relationship(
        "Record2person",
        primaryjoin=
        "and_(Record.id==Record2person.record_id, Record2person.buried==True)")


class Record2person(Base):
    __tablename__ = "record2person"
    id = Column('id', Integer, primary_key=True)
    record_id = Column('record_id', Unicode, ForeignKey('record.id'))
    person_id = Column('person_id', Integer, ForeignKey('person.id'))
    buried = Column('buried', Boolean, default=False)

    person = relationship('Person', foreign_keys=person_id)
    record = relationship('Record', foreign_keys=record_id)


class Personname(Base):
    __tablename__ = "personname"
    id = Column('id', Integer, primary_key=True)
    givenname = Column('givenName', Unicode)
    patronym = Column('patronym', Unicode)
    surnameprefix = Column('surnamePrefix', Unicode)
    basesurname = Column('baseSurname', Unicode)
    literalname = Column('literalName', Unicode)


class Person2person(Base):
    __tablename__ = "person2person"
    id = Column('id', Integer, primary_key=True)
    p1_id = Column('p1_id', Integer, ForeignKey('person.id'))
    p2_id = Column('p2_id', Integer, ForeignKey('person.id'))
    relationinfo_id = Column('relationinfo_id', Integer,
                             ForeignKey('relationinfo.id'))

    relationinfo = relationship('Relationinfo', foreign_keys=relationinfo_id)

    person1 = relationship('Person', foreign_keys=p1_id, backref='related_to')
    person2 = relationship('Person',
                           foreign_keys=p2_id,
                           backref='related_from')


class Relationinfo(Base):
    __tablename__ = "relationinfo"
    id = Column('id', Integer, primary_key=True)
    name = deferred(Column('name', Text))
    parent_category_id = Column('parent_category_id', Integer,
                                ForeignKey('relationinfo.id'))

    parent_category = relationship('Relationinfo',
                                   foreign_keys=parent_category_id)


class Church(Base):
    __tablename__ = "church"
    id = Column('id', Integer, primary_key=True)
    name = Column('name', Unicode)


class Scan(Base):
    __tablename__ = "scan"
    id = Column('id', Integer, primary_key=True)
    name = Column('name', Unicode)
    uuid = Column('uuid', Unicode)
    url = Column('url', Unicode)


class Person2personname(Base):
    __tablename__ = "person2personname"
    id = Column('id', Integer, primary_key=True)
    person_id = Column('person_id', Integer, ForeignKey('person.id'))
    personname_id = Column('personname_id', Integer,
                           ForeignKey('personname.id'))

    person = relationship('Person', foreign_keys=person_id)
    personname = relationship('Personname', foreign_keys=personname_id)


# end
