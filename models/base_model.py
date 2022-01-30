#!/usr/bin/python3
"""
contains BaseModel definitions.
"""

import uuid
from datetime import datetime
from models import storage


class BaseModel:
    """
    defines all common attributes/methods for other classes
    """

    def __init__(self, *args, **kwargs):
        """initializes object using dictionary if given otherwise
        it gives default value
        """
        if kwargs:
            for key, value in kwargs.items():
                if key != '__class__':
                    setattr(self, key, value)
            self.created_at = datetime.strptime(kwargs['created_at'],
                                                '%Y-%m-%dT%H:%M:%S.%f')
            self.updated_at = datetime.strptime(kwargs['updated_at'],
                                                '%Y-%m-%dT%H:%M:%S.%f')
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)

    def __str__(self):
        """string repr of obj"""
        return f'[{self.__class__.__name__}] ({self.id}) {self.__dict__}'

    def save(self):
        """updates the public instance attribute"""
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """returns a dictionary containing all key/value of __dict__
        of the instance"""
        dic = vars(self)
        dic['__class__'] = self.__class__.__name__
        dic['updated_at'] = self.updated_at.isoformat()
        dic['created_at'] = self.created_at.isoformat()
        return vars(self)
