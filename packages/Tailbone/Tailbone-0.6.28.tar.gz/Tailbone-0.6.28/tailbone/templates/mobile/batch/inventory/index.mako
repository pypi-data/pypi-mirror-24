## -*- coding: utf-8; -*-
<%inherit file="/mobile/master/index.mako" />

<%def name="title()">Inventory</%def>

% if request.has_perm('batch.inventory.create'):
    ${h.link_to("New Inventory Batch", url('mobile.batch.inventory.create'), class_='ui-btn ui-corner-all')}
% endif

${parent.body()}
