from flask_admin._compat import as_unicode, string_types, text_type
from flask_admin.contrib.sqla.ajax import QueryAjaxModelLoader
from flask_admin.contrib.sqla import ModelView

from begraafregisters import admin, db
from begraafregisters.models import Record, Person2person, Personname, Person, Relationinfo, Scan, Church

from jinja2 import Markup

from begraafregisters.utils import getRdf


class DefaultView(ModelView):
    can_create = False
    can_edit = False
    can_delete = False


class DefaultEditView(ModelView):
    can_create = True
    can_edit = True
    can_delete = True


class FullViewRecord(DefaultEditView):

    # inline_models = (Church, Scan, Record2person, Relationinfo)

    def _display_scan(view, context, model, name):
        if not model.scan:
            return ''

        return Markup(
            f'<a href="https://images.memorix.nl/ams/download/fullsize/{model.scan.uuid}.jpg" target="_blank" >{model.scan.name}</a>'
        )

    def _display_turtle(view, context, model, name):

        turtle = getRdf(model, format='turtle')

        return Markup(f'<code>{Markup.escape(turtle)}</code>')

    column_formatters_detail = {'scan': _display_scan, 'rdf': _display_turtle}

    column_display_pk = True
    column_display_all_relations = True
    column_list = [
        'id', 'inventory', 'church', 'date', 'buried', 'registered',
        'relationinfo', 'source', 'scan'
    ]
    can_view_details = True
    column_details_list = column_list + ['rdf']

    form_columns = [
        'id', 'inventory', 'date', 'church', 'scan', 'source', 'buried',
        'registered', 'relationinfo'
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


class FullViewPerson(DefaultEditView):

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


class FullViewPerson2Person(DefaultEditView):
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


class FullViewPersonName(DefaultEditView):
    column_display_pk = True
    column_display_all_relations = True
    column_list = ('id', 'givenname', 'surnameprefix', 'basesurname',
                   'literalname', 'persons')

    form_ajax_refs = {'persons': {'fields': ['name'], 'page_size': 10}}


class FullViewRelationinfo(DefaultEditView):
    column_display_pk = True
    column_display_all_relations = True
    column_list = ('id', 'name', 'parent_category')


class FullViewScan(DefaultEditView):
    column_display_pk = True
    column_display_all_relations = True
    column_list = ('id', 'name', 'url', 'uuid')

    form_columns = ['id', 'name', 'url', 'uuid']
    form_widget_args = {'id': {'readonly': True}}

    form_ajax_refs = {'records': {'fields': ['id'], 'page_size': 10}}


class FullViewChurch(DefaultEditView):
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
