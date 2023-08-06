## -*- coding: utf-8; -*-
<%inherit file="tailbone:templates/master/view.mako" />

<%def name="content_title()">
  <h1>${instance_title}</h1>
</%def>

${parent.body()}
