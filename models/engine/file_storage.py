#!/usr/bin/python3
'''File Storage'''
import json
import models
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    '''serializes and deserialzes json files'''

    __file_path = 'file.json'
    __objects = {}
    class_dict = {"BaseModel": BaseModel, "User": User, "Place": Place,
                  "Amenity": Amenity, "City": City, "Review": Review,
                  "State": State}

    def all(self, cls=None):
        '''Return dictionary of <class>.<id> : object instance'''
        obj = {}
        if cls is None:
            return (self.__objects)
        else:
            if type(cls) is str:
                cls = models.classes[cls]
            for key, val in self.__objects.items():
                if cls.__name__ == val.__class__.__name__:
                    obj[key] = val
            return (obj)

    def new(self, obj):
        '''Add new obj to existing dictionary of instances'''
        if obj:
            key = '{}.{}'.format(obj.__class__.__name__, obj.id)
            self.__objects[key] = obj

    def save(self):
        '''Save obj dictionaries to json file'''
        my_dict = {}

        for key, obj in self.__objects.items():
            '''if type(obj) is dict:
            my_dict[key] = obj
            else:'''
            my_dict[key] = obj.to_dict()
        with open(self.__file_path, 'w') as f:
            json.dump(my_dict, f)

    def reload(self):
        '''If json file exists, convert obj dicts back to instances'''
        try:
            with open(self.__file_path, 'r') as f:
                new_obj = json.load(f)
            for key, val in new_obj.items():
                obj = self.class_dict[val['__class__']](**val)
                self.__objects[key] = obj
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        '''Delete obj from __objects if present'''
        if not obj:
            return
        key = '{}.{}'.format(type(obj).__name__, obj.id)
        if key in self.__objects:
            del self.__objects[key]
            self.save()
