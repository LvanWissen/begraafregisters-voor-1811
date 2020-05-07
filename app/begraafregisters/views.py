from flask_admin._compat import as_unicode, string_types, text_type
from flask_admin.contrib.sqla.ajax import QueryAjaxModelLoader
from flask_admin.contrib.sqla import ModelView

from begraafregisters import admin, db
from begraafregisters.models import Record, Person2person, Personname, Person, Relationinfo, Scan, Church


class FullViewRecord(ModelView):

    # inline_models = (Church, Scan, Record2person, Relationinfo)

    column_display_pk = True
    column_display_all_relations = True
    column_list = ('id', 'inventory', 'church', 'date', 'registered', 'buried',
                   'relationinfo', 'source', 'scan')

    form_columns = [
        'id', 'inventory', 'date', 'church', 'scan', 'source', 'registered',
        'buried', 'relationinfo'
    ]
    form_widget_args = {'id': {'readonly': True}}

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
            'fields': ['name'],
            'page_size': 10
        },
        'buried': {
            'fields': ['name'],
            'page_size': 10
        },
        'relationinfo': {
            'fields': ['name'],
            'page_size': 10
        }
    }


class FullViewPerson(ModelView):

    # inline_models = (Personname, )
    inline_models = ((Person2person, {
        'form_columns': ('id', 'person2', 'relationinfo'),
        'form_ajax_refs': {
            'person2': {
                'fields': ['name'],
                'page_size': 10
            },
            'relationinfo': {
                'fields': ['name'],
                'page_size': 10
            }
        }
    }), Personname)  # multiple relations?
    form_columns = ['names', 'related_to', 'gender', 'record']

    column_display_pk = True
    column_display_all_relations = True
    column_list = ('id', 'record', 'name', 'gender', 'related_to')

    form_ajax_refs = {
        'names': {
            'fields':
            ['givenname', 'basesurname', 'surnameprefix', 'literalname'],
            'page_size': 10
        },
        'record': {
            'fields': ['id'],
            'page_size': 10
        }
        # 'related_from': {
        #     'fields': ['name'],
        #     'page_size': 10
        # }
    }


class FullViewPerson2Person(ModelView):
    column_display_pk = True
    column_display_all_relations = True
    column_list = ('id', 'person1', 'person2', 'relationinfo')

    form_ajax_refs = {
        'person1': {
            'fields': ['name'],
            'page_size': 10
        },
        'person2': {
            'fields': ['name'],
            'page_size': 10
        },
        'relationinfo': {
            'fields': ['name'],
            'page_size': 10
        }
    }


class FullViewPersonName(ModelView):
    column_display_pk = True
    column_display_all_relations = True
    column_list = ('id', 'givenname', 'surnameprefix', 'basesurname',
                   'literalname', 'persons')

    form_ajax_refs = {'persons': {'fields': ['name'], 'page_size': 10}}


class FullViewRelationinfo(ModelView):
    column_display_pk = True
    column_display_all_relations = True
    column_list = ('id', 'name', 'parent_category')


class FullViewScan(ModelView):
    column_display_pk = True
    column_display_all_relations = True
    column_list = ('id', 'url')

    form_columns = ['id', 'url']
    form_widget_args = {'id': {'readonly': True}}

    form_ajax_refs = {'records': {'fields': ['id'], 'page_size': 10}}


class FullViewChurch(ModelView):
    column_display_pk = True
    column_display_all_relations = True
    column_list = ('id', 'name')

    form_ajax_refs = {'records': {'fields': ['id'], 'page_size': 10}}


# Load views for Flask-Admin
admin.add_view(FullViewRecord(Record, db.session))
admin.add_view(FullViewPerson(Person, db.session))
admin.add_view(FullViewPerson2Person(Person2person, db.session))
admin.add_view(FullViewPersonName(Personname, db.session))
admin.add_view(FullViewRelationinfo(Relationinfo, db.session))
admin.add_view(FullViewScan(Scan, db.session))
admin.add_view(FullViewChurch(Church, db.session))
