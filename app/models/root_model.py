#!/usr/bin/python3
"""

"""

import uuid
from datetime import datetime


class RootModel:
    """
    
    """
    

    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def save(self):
        """

        """
        self.updated_at = datetime.now()
    
    def to_dict(self):
        """
        Object instance to dict.
        """
        instance_dict = self.__dict__.copy()
        instance_dict["__class__"] = self.__class__.__name__
        instance_dict["created_at"] = self.created_at.isoformat()
        instance_dict["updated_at"] = self.updated_at.isoformat()

        return instance_dict
    
    def __str__(self):
        """
        
        """
        class_name = self.__class__.__name__
        return "[{}] ({}) {}".format(class_name, self.id, self.__dict__)



if __name__ == '__main__':
    my_model = RootModel()
    my_model.name = "My Root Model"
    my_model.number = 35
    print(my_model, "\n")

    my_model.save()
    print(my_model, "\n")

    my_model_json = my_model.to_dict()
    print(my_model_json, "\n")
    print("JSON of my_model")
    for key in my_model_json.keys():
        print("\t{}: ({}) - {}".format(key, type(my_model_json[key]), my_model_json[key]))
