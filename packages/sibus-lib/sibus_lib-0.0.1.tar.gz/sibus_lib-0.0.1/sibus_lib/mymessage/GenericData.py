#!/usr/bin/env python
# -*- coding: utf-8 -*-

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from marshmallow import Schema, fields, post_load

class GenericSchema(Schema):
    def toObject(self, json_string):
        message = self.loads(json_string)
        return message.data

class GenericData():
    def __repr__(self):
        return "<%s> %s"%(self.__class__,self.toJson())