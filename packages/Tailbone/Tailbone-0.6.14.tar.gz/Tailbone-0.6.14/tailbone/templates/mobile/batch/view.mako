## -*- coding: utf-8; -*-
<%inherit file="/mobile/master/view.mako" />

${parent.body()}

% if master.has_rows:
    <br />
    ${grid.render_complete()|n}
% endif
