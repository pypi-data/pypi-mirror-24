#!/usr/bin/env python
# -*- coding: utf-8 -*-

from marshmallow import fields, post_load

from sibus_lib.lib import GenericData, GenericSchema


class ServiceMonitorSchema(GenericSchema):
    cpu_percent = fields.Float()

    ram_total = fields.Integer()
    ram_free = fields.Integer()
    ram_used = fields.Integer()

    swap_total = fields.Integer()
    swap_free = fields.Integer()
    swap_used = fields.Integer()

    fs_total = fields.Integer()
    fs_free = fields.Integer()
    fs_used = fields.Integer()

    usb_total = fields.Integer()
    usb_free = fields.Integer()
    usb_used = fields.Integer()

    @post_load
    def make_object(self, data):
        return ServiceMonitorData(**data)

class ServiceMonitorData(GenericData):
    def __init__(self, cpu_percent = -1, ram_total=-1, ram_free=-1, ram_used=-1,
                 swap_total = -1, swap_free=-1, swap_used=-1,
                 fs_total=-1, fs_free=-1, fs_used=-1,
                 usb_total=-1, usb_free=-1, usb_used=-1
                        ):
        self.cpu_percent = cpu_percent

        self.ram_total = ram_total
        self.ram_free = ram_free
        self.ram_used = ram_used

        self.swap_total = swap_total
        self.swap_free = swap_free
        self.swap_used = swap_used

        self.fs_total = fs_total
        self.fs_free = fs_free
        self.fs_used = fs_used

        self.usb_total = usb_total
        self.usb_free = usb_free
        self.usb_used = usb_used

    def toJson(self):
        schema = SysmonSchema()
        json_result = schema.dumps(self)
        return json_result.data
