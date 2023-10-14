<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "communalectgroups" %>
<%block name="title">${_('Communalect Group')}: ${ctx.name}</%block>

<h2>${_('Communalect Group')}: ${ctx.name}</h2>

% if map_ or request.map:
${(map_ or request.map).render()}
% endif

${request.get_datatable('languages', h.models.Language, fijicommunalectgroup=ctx).render()}
