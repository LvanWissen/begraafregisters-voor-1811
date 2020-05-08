from rdflib import ConjunctiveGraph, Namespace, Literal, URIRef, BNode, XSD, RDFS

from rdfalchemy import rdfSubject, rdfSingle, rdfMultiple

ga = Namespace("https://data.goldenagents.org/datasets/SAA/ontology/")
pnv = Namespace('https://w3id.org/pnv#')

saa = Namespace("https://data.goldenagents.org/datasets/SAA/")
saaRecord = Namespace("https://data.goldenagents.org/datasets/SAA/Record/")
saaChurch = Namespace("https://data.goldenagents.org/datasets/SAA/Church/")
saaPersonName = Namespace(
    "https://data.goldenagents.org/datasets/SAA/PersonName/")


class Record(rdfSubject):
    rdf_type = ga.IndexOpBegraafregisters

    identifier = rdfSingle(saa.identifier)
    sourceReference = rdfSingle(saa.sourceReference)
    inventoryNumber = rdfSingle(saa.inventoryNumber)
    urlScan = rdfSingle(saa.urlScan)
    mentionsRegisteredName = rdfMultiple(saa.mentionsRegisteredName)
    mentionsBuriedName = rdfMultiple(saa.mentionsBuriedName)
    relationInformation = rdfSingle(saa.relationInformation)
    cemetery = rdfSingle(saa.cemetery)
    burialDate = rdfSingle(saa.burialDate)


class Church(rdfSubject):
    rdf_type = ga.Church

    label = rdfSingle(RDFS.label)


class PersonName(rdfSubject):
    rdf_type = pnv.PersonName

    # These map to A2A
    literalName = rdfSingle(pnv.literalName)
    givenName = rdfSingle(pnv.givenName)
    surnamePrefix = rdfSingle(pnv.surnamePrefix)
    baseSurname = rdfSingle(pnv.baseSurname)

    prefix = rdfSingle(pnv.prefix)
    disambiguatingDescription = rdfSingle(pnv.disambiguatingDescription)
    patronym = rdfSingle(pnv.patronym)
    surname = rdfSingle(pnv.surname)


def getRdf(model, format='turtle'):

    g = rdfSubject.db = ConjunctiveGraph()

    r = Record(saaRecord.term(model.id),
               identifier=model.id,
               sourceReference=model.source,
               inventoryNumber=model.inventory,
               cemetery=Church(saaChurch.term(str(model.church.id)),
                               label=model.church.name),
               burialDate=Literal(model.date, datatype=XSD.date))

    if model.relationinfo:
        r.relationInformation = model.relationinfo.name

    buriedNames = []
    for p in model.buried:
        for n in p.names:
            pn = PersonName(saaPersonName.term(str(n.id)),
                            literalName=n.literalname,
                            givenName=n.givenname,
                            surnamePrefix=n.surnameprefix,
                            baseSurname=n.basesurname)
            buriedNames.append(pn)

    r.mentionsRegisteredName = buriedNames

    registeredNames = []
    for p in model.registered:
        for n in p.names:
            pn = PersonName(saaPersonName.term(str(n.id)),
                            literalName=n.literalname,
                            givenName=n.givenname,
                            surnamePrefix=n.surnameprefix,
                            baseSurname=n.basesurname)
            registeredNames.append(pn)

    r.mentionsRegisteredName = registeredNames

    g.bind('pnv', pnv)
    g.bind('ga', ga)
    g.bind('saa', saa)

    return g.serialize(format=format).decode("utf-8")