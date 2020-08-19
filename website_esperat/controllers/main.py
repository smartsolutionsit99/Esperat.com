# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request
from odoo.addons.website_form.controllers.main import WebsiteForm
import logging
_logger = logging.getLogger(__name__)

class WebsiteForm(WebsiteForm):

    # Check and insert values from the form on the model <model>
    @http.route('/website_form/<string:model_name>', type='http', auth="public", methods=['POST'], website=True)
    def website_form(self, model_name, **kwargs):
        if model_name == 'spare.order':
            _logger.warning("************************************")
        return super(WebsiteForm, self).website_form(model_name, **kwargs)

    def insert_record(self, request, model, values, custom, meta=None):
        if model.model == 'spare.order':
            _logger.warning("************************************")
            _logger.warning(values)
        return super(WebsiteForm, self).insert_record(request, model, values, custom, meta=meta)
