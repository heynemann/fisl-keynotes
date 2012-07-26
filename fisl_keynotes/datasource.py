#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import HTMLParser
from urllib2 import urlopen
import urllib
import hashlib
from xml.etree import ElementTree as etree


FISL_TALKS_URL = 'http://fisl.org.br/13/papers_ng/public/fast_grid?event_id=3'
FISL_TALKS_FILE = 'fisl_keynotes/fisl_talks.xml'

def unescape(text):
    h = HTMLParser.HTMLParser()
    return h.unescape(text)

class FislConference(object):

    def fetch_data(self):
        with open(FISL_TALKS_FILE) as response:
            self.xml = etree.fromstring(response.read())
        self.persons = map(Person, self.xml.findall('authorship/person'))
        self.talks = map(Talk, self.xml.findall('slots/slot'))
        self.rooms = map(Room, self.xml.findall('rooms/room'))

    def find_person_by_name(self, name, email):
        for person in self.persons:
            if name.lower() in person.name.lower():
                person.email = email
                yield person

    def find_talks_by_person(self, person):
        for talk in self.talks:
            if talk.candidate == person.candidate:
                talk.room = self.find_room_from_talk(talk)
                yield talk

    def find_room_from_talk(self, talk):
        for room in self.rooms:
            if talk.room_id == room.id:
                return room


class Person(object):
    def __init__(self, xml_element=None, email=None, name=None):
        if xml_element is not None:
            self.name = unescape(xml_element.get('name'))
            self.candidate = unescape(xml_element.get('candidate'))
        else:
            self.email = email
            self.name = name

    @property
    def gravatar(self):
        size = 115
        default = 'http://fisl-keynotes.herokuapp.com/static/img/troll.png'
        gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(self.email.lower()).hexdigest() + "?"
        gravatar_url += urllib.urlencode({'d':default, 's':str(size)})
        return gravatar_url


class Talk(object):
    def __init__(self, xml_element=None, person=None, room=None, date=None, title=None):
        if xml_element is not None:
            self.candidate = unescape(xml_element.get('candidate'))
            self.title = unescape(xml_element.get('title'))
            self.abstract = unescape(xml_element.get('abstract'))
            self.date = datetime.datetime.strptime('%s%s%s' % (
                                                      xml_element.get('date'),
                                                      xml_element.get('hour'),
                                                      xml_element.get('minute')),
                                          '%Y-%m-%d%H%M')
            self.room_id = xml_element.get('room')

        else:
            self.author = person
            self.room = room
            self.title = title
            self.date = date 

class Room(object):
    def __init__(self, xml_element=None, name=None):
        if xml_element is not None:
            self.id = xml_element.get('id')
            self.capacity = xml_element.find('capacity').text
            self.name = unescape(xml_element.find('name').text)
        else:
            self.name = name

class GlobaisTalks(object):

    def all_talks(self):
        fisl = FislConference()

        fisl.fetch_data()

        globais = [(u'carício', 'rafael@caricio.com'),
                ('heynemann', 'heynemann@gmail.com'),
                ('Zimerer', 'alexanmtz@gmail.com'), 
                ('Francisco Souza', 'f@souza.cc'), 
                ('Al-Chueyr', 'tatiana.martins@corp.globo.com'),
                ('Demetrius', 'demetrius.nunes@corp.globo.com'),
                ('Juarez', 'juarez.bochi@corp.globo.com'),
                ('motta', 'tiago.motta@corp.globo.com')]

        estande = Room(name='Estande Globo.com')
        lightning_talks = [
                Talk(person=Person(name=u'Diego Manhães',
                    email="diego@dmpinheiro.net"),
                    room=estande,
                    title=u"Otimização de aplicativos em Python",
                    date=datetime.datetime(2012,7,27,12,00,00)),
                Talk(person=Person(name=u'Leonardo Mello',
                    email="leonardo.rodrigues@corp.globo.com"),
                    room=estande,
                    title=u"Automatização de setup e gerenciamento de servidores",
                    date=datetime.datetime(2012,7,27,16,00,00)),
                Talk(person=Person(name='Colin Saliceti',
                    email="colin@corp.globo.com"),
                    room=estande,
                    title=u"Hot Deploy - Serviço contínuo",
                    date=datetime.datetime(2012,7,27,17,00,00)),
                ]
        global_talks = []

        for glb in globais:
            for person in fisl.find_person_by_name(*glb):
                for t in fisl.find_talks_by_person(person):
                    t.author = person
                    global_talks.append(t)

        global_talks.extend(lightning_talks)
        global_talks = sorted(global_talks, key=lambda item: item.date)
        return global_talks

if __name__ == '__main__':
    fisl = FislConference()

    fisl.fetch_data()

    globais = [(u'carício', 'rafael@caricio.com'),
            ('heynemann', 'heynemann@gmail.com'),
            ('Zimerer', 'alexanmtz@gmail.com'), 
            ('Francisco Souza', 'f@souza.cc'), 
            ('Al-Chueyr', 'tatiana.martins@corp.globo.com'),
            ('Demetrius', 'demetrius.nunes@corp.globo.com'),
            ('Juarez', 'juarez.bochi@corp.globo.com'),
            ('motta', 'tiago.motta@corp.globo.com')]


    global_talks = []

    for glb in globais:
        for person in fisl.find_person_by_name(*glb):
            for t in fisl.find_talks_by_person(person):
                t.author = person
                global_talks.append(t)

    global_talks = sorted(global_talks, key=lambda item: item.date)

    for t in global_talks:
        print t.title
        print t.abstract
        print t.date
        print t.room.name
        print '-' * 20



