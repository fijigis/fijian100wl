<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "languages" %>
<%block name="title">${_('Village')}: ${ctx.name}</%block>

<h2>${_('Village')}: ${ctx.name}</h2>

% if ctx.communalect is not None:
<h3>Part of Communalect ${h.link(request, ctx.communalect)}</h3>
<h3>Part of Communalect Group ${h.link(request, ctx.communalectgroup)}</h3>
% endif

${request.get_datatable('values', h.models.Value, language=ctx).render()}

<%def name="sidebar()">
    <%util:well>
    ${request.map.render()}
    ${h.format_coordinates(ctx)}
    </%util:well>
</%def>
