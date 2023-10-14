<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "languages" %>
<%block name="title">${_('Village')}: ${ctx.language}, ${_('Concept')}: ${ctx.parameter}</%block>

<h2>
% if len(ctx.values) > 1:
    Words
% else:
    Word
% endif
    for Concept ${h.link(request, ctx.parameter)} in Village ${h.link(request, ctx.language)}
    ${h.contactmail(req, ctx, title="suggest changes")}
</h2>

<div style="clear: right;">
<ul>
% if len(ctx.values) > 1:
% for i, value in enumerate(ctx.values):
<li>${value.domainelement.name}: ${value.description}</li>
% endfor
% else:
<li>${ctx.values[0].domainelement.name}</li>
% endif
</ul>
</div>

<%def name="sidebar()">
    <%util:well>
    ${h.format_coordinates(ctx.language)}
    </%util:well>
</%def>
