__author__ = 'alexei'
from pony.orm import *
from model.group import Group
from model.contact import Contact
from datetime import datetime
from pymysql.converters import decoders


class ORMFixture:

    db = Database()

    class ORMGroup(db.Entity):
        _table_ = 'group_list'
        id = PrimaryKey(int, column='group_id')
        name = Optional(str, column='group_name')
        header = Optional(str, column='group_header')
        footer = Optional(str, column='group_footer')

    class ORMContact(db.Entity):
        _table_ = 'addressbook'
        id = PrimaryKey(int, column='id')
        firstname = Optional(str, column='firstname')
        lastname = Optional(str, column='lastname')
        deprecated = Optional(datetime, column='deprecated')

    def __init__(self, host, name, user, password):
        self.db.bind('mysql', host=host, database=name, user=user, password=password, conv=decoders)
        self.db.generate_mapping()
        sql_debug(True)

    @db_session
    def get_group_list(self):
        def convert_to_model(group):
            return Group(id=str(group.id), name=group.name, header=group.header, footer=group.footer)
        return list(map(convert_to_model, select(g for g in ORMFixture.ORMGroup)[:]))

    @db_session
    def get_contact_list(self):
        def convert_to_model(contact):
            return Contact(id=str(contact.id), firstname=contact.firstname, lastname=contact.lastname)
        return list(map(convert_to_model, select(c for c in ORMFixture.ORMContact if c.deprecated is None)))