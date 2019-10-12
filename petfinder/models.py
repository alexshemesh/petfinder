from sqlalchemy import Column, Integer, String, DateTime
from petfinder.database import Base
from sqlalchemy.event import listen


class PetRecord(Base):
    __tablename__ = 'pet_record'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    phone = Column(String(32))
    color = Column(String(120))
    type = Column(String(32))
    tags = Column(String(1024))
    desc = Column(String(1024))


    def generate_tags(self):
        array_of_values = []
        for key in self.__dict__:
            value =  self.__dict__[key]
            array_of_values = array_of_values + str(value).split(' ')
        tags_to_set = ','.join( array_of_values)
        self.tags = tags_to_set

    def __init__(self, name=None, phone=None,color=None, type=None, desc=None):
        self.name = name
        self.phone = phone
        self.color = color
        self.type = type
        self.desc = desc


    def __repr__(self):
        return '<pet %r>' % (self.name)


def generate_tags(mapper, connect, target):
    target.generate_tags()

listen(PetRecord, 'before_insert', generate_tags)
