import gzip
from lxml import etree
from datetime import datetime
import dateutil.parser
from collections import defaultdict

from sqlalchemy import create_engine
engine = create_engine(
    'postgresql://postgres:example@localhost:8123/begraafregisters',
    echo=False)

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from model import Base
Base.metadata.create_all(engine)

from model import Record, Person, Record2person, Personname, Relationinfo, Church, Scan
"""
DELETE FROM "church" ;
DELETE FROM "person" ;
DELETE FROM "person2person" ;
DELETE FROM "person2personname" ;
DELETE FROM "personname" ;
DELETE FROM "record" ;
DELETE FROM "record2person" ;
DELETE FROM "relationinfo" ;
DELETE FROM "scan" ;
DELETE FROM "source" ;
"""


def get_one_or_create(session,
                      model,
                      create_method='',
                      create_method_kwargs=None,
                      cachedict=None,
                      **kwargs):
    """
    Source: https://stackoverflow.com/a/21146492
    """

    if cachedict is None:
        cachedict = defaultdict(dict)

    items = frozenset(kwargs.items())

    try:
        # try to retrieve from cachedict
        obj = cachedict[model].get(
            items,
            session.query(model).filter_by(**kwargs).one())

        return obj, cachedict

    except NoResultFound:
        kwargs.update(create_method_kwargs or {})
        created = getattr(model, create_method, model)(**kwargs)
        try:
            session.add(created)
            session.flush()
            cachedict[model][items] = created  # update cache

            return created, cachedict
        except IntegrityError:
            session.rollback()
            return session.query(model).filter_by(**kwargs).one(), cachedict


def addRecords(
        filename='/home/leon/Documents/Golden_Agents/begraafregisters-voor-1811/data/SAA_Index_op_begraafregisters_voor_1811_20190207.xml.gz'
):

    cachedict = None

    # load file
    if filename.endswith('.gz'):
        with gzip.open(filename) as gzipfile:
            tree = etree.parse(gzipfile)

    elif filename.endswith('.xml'):
        tree = etree.parse(filename)

    ### Add records
    records = tree.findall("//indexRecord")
    n_total = len(records)

    for n, record in enumerate(records, 1):

        if n % 1000 == 0:
            print(f"{n}/{n_total} records", end='\r')
            session.commit()
            break

        if record.find('datumBegrafenis') is not None:
            try:
                date = datetime.fromisoformat(
                    record.find('datumBegrafenis').text)
            except:
                date = None
        else:
            date = None

        r = Record(id=record.attrib['id'],
                   inventory=record.find('inventarisnummer').text,
                   date=date)

        if record.find('begraafplaats') is not None:
            church, cachedict = get_one_or_create(
                session,
                Church,
                cachedict=cachedict,
                name=record.find('begraafplaats').text)
        else:
            church = None

        if record.find('bronverwijzing') is not None:
            source = record.find('bronverwijzing').text
            r.source = source

        scan, cachedict = get_one_or_create(session,
                                            Scan,
                                            cachedict=cachedict,
                                            url=record.find('urlScan').text)

        if record.find('relatieinformatie') is not None:
            relationinfo, cachedict = get_one_or_create(
                session,
                Relationinfo,
                cachedict=cachedict,
                name=record.find('relatieinformatie').text)
        else:
            relationinfo = None

        r.church = church
        r.source = source
        r.scan = scan
        r.relationinfo = relationinfo

        for ingeschrevene in record.findall('ingeschrevene'):
            givenNames = ingeschrevene.find('voornaam')
            if givenNames is not None:
                givenName = givenNames.text
            else:
                givenName = None

            surnamePrefixes = ingeschrevene.find('tussenvoegsel')
            if surnamePrefixes is not None:
                surnamePrefix = surnamePrefixes.text
            else:
                surnamePrefix = None

            baseSurnames = ingeschrevene.find('achternaam')
            if baseSurnames is not None:
                baseSurname = baseSurnames.text
            else:
                baseSurname = None

            literalName = " ".join([
                i for i in [givenName, surnamePrefix, baseSurname]
                if i is not None
            ])

            pn, cachedict = get_one_or_create(session,
                                              Personname,
                                              cachedict=cachedict,
                                              givenname=givenName,
                                              surnameprefix=surnamePrefix,
                                              basesurname=baseSurname,
                                              literalname=literalName)

            # p = Person(name=literalName)
            p = Person()
            p.names.append(pn)

            r2p = Record2person(buried=False)
            r2p.person = p

            r.registered.append(r2p)

            session.add(r)


if __name__ == "__main__":
    session = Session()

    addRecords()

    for p in session.query(Person).all():
        print(p.name)

    session.close()
