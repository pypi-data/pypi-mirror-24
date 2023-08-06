## -*- coding: utf-8; -*-
<%inherit file="/master/view.mako" />

${parent.body()}

% if not instance.executed and request.has_perm('{}.execute'.format(permission_prefix)):
    <div class="buttons">
      % if instance.enabled and not instance.executing:
          ${h.form(url('{}.execute'.format(route_prefix), uuid=instance.uuid))}
          ${h.csrf_token(request)}
          ${h.submit('execute', "Execute this upgrade", class_='autodisable')}
          ${h.end_form()}
      % elif instance.enabled:
          <button type="button" disabled="disabled" title="This upgrade is currently executing">Execute this upgrade</button>
      % else:
          <button type="button" disabled="disabled" title="This upgrade is not enabled">Execute this upgrade</button>
      % endif
    </div>
% endif
