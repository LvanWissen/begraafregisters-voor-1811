-- Created by Vertabelo (http://vertabelo.com)
-- Last modification date: 2020-01-08 20:43:22.851

-- tables
-- Table: church
CREATE TABLE church (
    id serial  NOT NULL,
    name varchar(255)  NOT NULL,
    CONSTRAINT name UNIQUE (name) NOT DEFERRABLE  INITIALLY IMMEDIATE,
    CONSTRAINT church_pk PRIMARY KEY (id)
);

-- Table: person
CREATE TABLE person (
    id serial  NOT NULL,
    gender varchar(20)  NULL,
    CONSTRAINT person_pk PRIMARY KEY (id)
);

-- Table: person2person
CREATE TABLE person2person (
    id serial  NOT NULL,
    p1_id int  NOT NULL,
    p2_id int  NOT NULL,
    relationinfo_id int  NOT NULL,
    CONSTRAINT person2person_pk PRIMARY KEY (id)
);

-- Table: person2personname
CREATE TABLE person2personname (
    id serial  NOT NULL,
    person_id int  NOT NULL,
    personname_id int  NOT NULL,
    CONSTRAINT person2personname_pk PRIMARY KEY (id)
);

-- Table: personname
CREATE TABLE personname (
    id serial  NOT NULL,
    givenName varchar(255)  NULL,
    patronym varchar(255)  NULL,
    surnamePrefix varchar(255)  NULL,
    baseSurname varchar(255)  NULL,
    literalName varchar(255)  NOT NULL DEFAULT 'Unknown',
    CONSTRAINT personname_pk PRIMARY KEY (id)
);

-- Table: record
CREATE TABLE record (
    id varchar(50)  NOT NULL,
    inventory varchar(20)  NOT NULL,
    date date  NOT NULL,
    church_id int  NOT NULL,
    source_id int  NOT NULL,
    scan_id int  NOT NULL,
    relationinfo_id int  NULL,
    CONSTRAINT record_pk PRIMARY KEY (id)
);

-- Table: record2person
CREATE TABLE record2person (
    id serial  NOT NULL,
    record_id varchar(50)  NOT NULL,
    person_id int  NOT NULL,
    burried boolean  NOT NULL,
    CONSTRAINT record2person_pk PRIMARY KEY (id)
);

-- Table: relationinfo
CREATE TABLE relationinfo (
    id serial  NOT NULL,
    name text  NOT NULL,
    parent_category_id int  NULL,
    CONSTRAINT relationinfoname UNIQUE (name) NOT DEFERRABLE  INITIALLY IMMEDIATE,
    CONSTRAINT relationinfo_pk PRIMARY KEY (id)
);

-- Table: scan
CREATE TABLE scan (
    id serial  NOT NULL,
    url varchar(255)  NOT NULL,
    CONSTRAINT url UNIQUE (url) NOT DEFERRABLE  INITIALLY IMMEDIATE,
    CONSTRAINT scan_pk PRIMARY KEY (id)
);

-- Table: source
CREATE TABLE source (
    id serial  NOT NULL,
    reference text  NOT NULL,
    CONSTRAINT reference UNIQUE (reference) NOT DEFERRABLE  INITIALLY IMMEDIATE,
    CONSTRAINT source_pk PRIMARY KEY (id)
);

-- foreign keys
-- Reference: person2person_person (table: person2person)
ALTER TABLE person2person ADD CONSTRAINT person2person_person
    FOREIGN KEY (p2_id)
    REFERENCES person (id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: person2personname_person (table: person2personname)
ALTER TABLE person2personname ADD CONSTRAINT person2personname_person
    FOREIGN KEY (person_id)
    REFERENCES person (id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: person2personname_personname (table: person2personname)
ALTER TABLE person2personname ADD CONSTRAINT person2personname_personname
    FOREIGN KEY (personname_id)
    REFERENCES personname (id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: person_person2person (table: person2person)
ALTER TABLE person2person ADD CONSTRAINT person_person2person
    FOREIGN KEY (p1_id)
    REFERENCES person (id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: product_purchase_item (table: record2person)
ALTER TABLE record2person ADD CONSTRAINT product_purchase_item
    FOREIGN KEY (record_id)
    REFERENCES record (id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: purchase_purchase_item (table: record2person)
ALTER TABLE record2person ADD CONSTRAINT purchase_purchase_item
    FOREIGN KEY (person_id)
    REFERENCES person (id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: record_church (table: record)
ALTER TABLE record ADD CONSTRAINT record_church
    FOREIGN KEY (church_id)
    REFERENCES church (id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: record_relationinfo (table: record)
ALTER TABLE record ADD CONSTRAINT record_relationinfo
    FOREIGN KEY (relationinfo_id)
    REFERENCES relationinfo (id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: record_scan (table: record)
ALTER TABLE record ADD CONSTRAINT record_scan
    FOREIGN KEY (scan_id)
    REFERENCES scan (id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: record_source (table: record)
ALTER TABLE record ADD CONSTRAINT record_source
    FOREIGN KEY (source_id)
    REFERENCES source (id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: relationinfo_relation (table: person2person)
ALTER TABLE person2person ADD CONSTRAINT relationinfo_relation
    FOREIGN KEY (relationinfo_id)
    REFERENCES relationinfo (id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: relationinfo_relationinfo (table: relationinfo)
ALTER TABLE relationinfo ADD CONSTRAINT relationinfo_relationinfo
    FOREIGN KEY (parent_category_id)
    REFERENCES relationinfo (id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- End of file.

