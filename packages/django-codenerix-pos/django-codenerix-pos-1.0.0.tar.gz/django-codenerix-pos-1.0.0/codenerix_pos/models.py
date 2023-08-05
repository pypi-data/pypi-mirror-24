# -*- coding: utf-8 -*-
#
# django-codenerix-pos
#
# Copyright 2017 Centrologic Computational Logistic Center S.L.
#
# Project URL : http://www.codenerix.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import uuid
import hashlib
from channels import Channel

from django.db import models
from django.utils.encoding import smart_text
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q

from jsonfield import JSONField

from codenerix_payments.models import PaymentRequest

from codenerix.models import CodenerixModel
from codenerix_extensions.corporate.models import CorporateImage
from codenerix_products.models import ProductFinal
from codenerix_invoicing.models import BillingSeries
from codenerix_extensions.lib.cryptography import AESCipher

"""
Plant
    Zones
    CorporateImage
    BillingSeries

Zones
    POS (pantalla fisica)
        Hardware Los que tengo (muchos)
        Hardware Los que puedo usar (muchos)
        token --- pos client (software instalado, minimo el id)
        Salable products (POSProduct)

    Slot (mesas)


Hardware (ticket, dni, caja, dispositivo de firma, dispositivo de consulta)
    nombre
    configuracion
    tipo (ticket, dni, caja, firma, consulta)
    token
"""

# Changing this KEYS will affect to any client beacuse it is used for communication as a standard
KIND_POSHARDWARE = (
    ("TICKET", _("Ticket printer")),
    ("DNIE", _("DNIe card reader")),
    ("CASH", _("Cash drawer")),
    ("WEIGHT", _("Weight")),
    ("SIGN", _("Signature pad")),
    ("QUERY", _("Query service (Ex: Barcode)")),  # Barcode reader, Point of Information for clients, etc...
)


class POSPlant(CodenerixModel):
    """
    Plant
    """
    corporate_image = models.ForeignKey(CorporateImage, related_name='posplants', verbose_name=_("Corporate image"), blank=False, null=False)
    billing_series = models.ForeignKey(BillingSeries, related_name='posplants', verbose_name='Billing series', blank=False, null=False)
    name = models.CharField(_("Name"), max_length=250, blank=False, null=False, unique=True)

    def __unicode__(self):
        return self.__str__()

    def __str__(self):
        return u"{}".format(smart_text(self.name))

    def __fields__(self, info):
        fields = []
        fields.append(('name', _("Name")))
        return fields


class POSZone(CodenerixModel):
    """
    Zone
    """
    plant = models.ForeignKey(POSPlant, related_name='zones', verbose_name=_("Plant"), blank=False, null=False)
    name = models.CharField(_("Name"), max_length=250, blank=False, null=False, unique=True)

    def __unicode__(self):
        return self.__str__()

    def __str__(self):
        return u"{}".format(smart_text(self.name))

    def __fields__(self, info):
        fields = []
        fields.append(('plant', _("Plant")))
        fields.append(('name', _("Name")))
        return fields


class POSHardware(CodenerixModel):
    """
    Hardware
    """
    pos = models.ForeignKey("POS", related_name='hardwares', verbose_name=_("Hardware"), blank=True, null=True)
    kind = models.CharField(_("Kind"), max_length=6, choices=KIND_POSHARDWARE, blank=False, null=False)
    name = models.CharField(_("Name"), max_length=250, blank=False, null=False, unique=True)
    enable = models.BooleanField(_('Enable'), default=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    config = JSONField(_("config"), blank=True, null=True)
    value = JSONField(_("config"), blank=True, null=True)

    def __unicode__(self):
        return self.__str__()

    def __str__(self):
        return u"{}".format(smart_text(self.name))

    def __fields__(self, info):
        fields = []
        fields.append(('pos', _("POS")))
        fields.append(('get_kind_display', _("Kind")))
        fields.append(('name', _("Name")))
        fields.append(('enable', _("Enable")))
        fields.append(('uuid', _("UUID")))
        fields.append(('config', _("Config")))
        fields.append(('value', _("Value")))
        return fields

    def save(self, *args, **kwargs):
        if 'doreset' in kwargs:
            doreset = kwargs.pop('doreset')
        else:
            doreset = True

        result = super(POSHardware, self).save(*args, **kwargs)
        if doreset:
            self.pos.reset_client()
        return result

    def recv(self, msg):
        self.value = msg
        self.save(doreset=False)

    def send(self, msg=None):
        '''
        Example of msg for each POSHARDWARE:
            TICKET: {'data': 'print this text, process thid dictionary or take my money'}
            CASH:   {'data': '...ANYTHING except None to open the Cash Drawer...' }
            DNIE:   {'data': '...ANYTHING except None to get again data from DNIe if connected...' }
            WEIGHT: {'data': '...ANYTHING except None to get the value of the last wegith' }
            SIGN:   --- NOT ALLOWED / NOT AVAILABLE ---
            QUERY:  --- NOT ALLOWED / NOT AVAILABLE ---
        '''
        if self.kind == 'TICKET':
            if msg is not None:
                data = msg
            else:
                raise IOError("Nothing to print???")
        elif self.kind in ['CASH', 'DNIE', 'WEIGHT']:
            data = 'DOIT'
        else:
            raise IOError("This Hardware can not send data anywhere")

        # Say it to send this message
        self.pos.send(data, self.uuid)


class POS(CodenerixModel):
    '''
    Point of Service
    '''
    name = models.CharField(_("Name"), max_length=250, blank=False, null=False, unique=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    key = models.CharField(_("Key"), max_length=32, blank=False, null=False, unique=True)
    zone = models.ForeignKey(POSZone, related_name='poss', verbose_name=_("Zone"))
    payments = models.ManyToManyField(PaymentRequest, related_name='poss', verbose_name=_("Payments"), blank=True, null=True)
    channel = models.CharField(_("Channel"), max_length=50, blank=True, null=True, unique=True, editable=False)
    # Hardware that can use
    hardware = models.ManyToManyField(POSHardware, related_name='poss', verbose_name=_("Hardware it can use"), blank=True, null=True)

    def __unicode__(self):
        return self.__str__()

    def __str__(self):
        return u"{}".format(smart_text(self.name))

    def __fields__(self, info):
        fields = []
        fields.append(('zone', _("Zone")))
        fields.append(('name', _("Name")))
        fields.append(('uuid', _("UUID")))
        fields.append(('key', _("Key")))
        fields.append(('channel', _("Channel")))
        fields.append(('hardware', _("Hardware")))
        return fields

    def save(self, *args, **kwargs):
        if 'doreset' in kwargs:
            doreset = kwargs.pop('doreset')
        else:
            doreset = True
        result = super(POS, self).save(*args, **kwargs)
        if doreset:
            self.reset_client()
        return result

    def reset_client(self):
        self.send({'action': 'reset'})

    def ping(self, uid=None):
        if uid is None:
            uidtxt = None
        else:
            uidtxt = uid.hex
        ref = hashlib.sha1(uuid.uuid4().hex.encode('utf-8')).hexdigest()
        self.send({'action': 'ping', 'ref': ref, 'uuid': uidtxt})
        return ref

    def send(self, data, uid=None):

        if uid:
            # Message for some client
            message = {
                'action': 'msg',
                'message': {
                    'data': data,
                },
                'uuid': uid.hex,
            }
        else:
            # Message for the server
            message = data

        # Send message
        crypto = AESCipher()
        msg = json.dumps(message)
        request = crypto.encrypt(msg, self.key).decode('utf-8')
        data = json.dumps({'message': request})
        Channel(self.channel).send({'text': data})


class POSSlot(CodenerixModel):
    '''
    Slots for Point of Service
    '''
    zone = models.ForeignKey(POSZone, related_name='slots', verbose_name=_("Zone"))
    name = models.CharField(_("Name"), max_length=250, blank=False, null=False, unique=True)
    # orders = models.ManyToManyField(SalesOrder, related_name='slots', editable=False, verbose_name=_("Orders"))
    pos_x = models.IntegerField(_('Pos X'), null=True, blank=True, default=None, editable=False)
    pos_y = models.IntegerField(_('Pos Y'), null=True, blank=True, default=None, editable=False)

    def __unicode__(self):
        return self.__str__()

    def __str__(self):
        return u"{}".format(smart_text(self.name))

    def __fields__(self, info):
        fields = []
        fields.append(('zone', _("Zone")))
        fields.append(('name', _("Name")))
        # fields.append(('orders', _("Orders")))
        return fields


class POSProduct(CodenerixModel):
    """
    Salable products in the POS
    """
    pos = models.ForeignKey(POS, related_name='posproducts', verbose_name=_("POS"))
    product = models.ForeignKey(ProductFinal, related_name='posproducts', verbose_name=_("Product"))
    enable = models.BooleanField(_('Enable'), default=True)

    class Meta(CodenerixModel.Meta):
        unique_together = (("pos", "product"))

    def __unicode__(self):
        return self.__str__()

    def __str__(self):
        return u"{} {}".format(smart_text(self.pos), smart_text(self.product))

    def __fields__(self, info):
        fields = []
        fields.append(('pos', _("POS")))
        fields.append(('product', _("Product")))
        fields.append(('enable', _("Enable")))
        return fields


class POSLog(CodenerixModel):
    """
    LOG for POS
    """
    pos = models.ForeignKey(POS, related_name='logs', verbose_name=_("POS"), editable=False, null=True)
    poshw = models.ForeignKey(POSHardware, related_name='logs', verbose_name=_("POS"), editable=False, null=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    log = JSONField(_("LOG"), blank=True, null=True)

    def __unicode__(self):
        return self.__str__()

    def __str__(self):
        return self.uuid.hex

    def __fields__(self, info):
        fields = []
        fields.append(('created', _("Created")))
        fields.append(('uuid', _("UUID")))
        fields.append(('pos', _("POS")))
        fields.append(('poshw', _("POSHardware")))
        fields.append(('log', _("Log")))
        return fields

    def __searchF__(self, info):

        # Build both lists
        poss = [(pos.pk, pos.name) for pos in POS.objects.all()]
        poshws = [(poshw.pk, poshw.name) for poshw in POSHardware.objects.all()]

        tf = {}
        tf['uuid'] = (_('UUID'), lambda x: Q(uuid__icontains=x), 'input')
        tf['pos'] = (_('POS'), lambda x: Q(pos__pk=x), poss)
        tf['poshw'] = (_('Hardware'), lambda x: Q(poshw__pk=x), poshws)
        return tf
