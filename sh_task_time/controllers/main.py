# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
import json
from odoo import http
from odoo.http import request
from odoo.tools.misc import file_open
from datetime import datetime


from odoo.addons.bus.controllers.main import BusController

class PosOrderController(BusController):

    def _poll(self, dbname, channels, last, options): 
        """Add the relevant channels to the BusController polling."""        
        if options.get('sh.timer.render'):
            channels = list(channels)
            lock_channel = (
                request.db,
                'sh.timer.render',
                options.get('sh.timer.render')
            )
            channels.append(lock_channel)
            
        return super(PosOrderController, self)._poll(dbname, channels, last, options)
