<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "communalects" %>
<%block name="title">${_('Communalect')}: ${ctx.name}</%block>

<h2>${_('Communalect')}: ${ctx.name}</h2>

<h3>${_('Part of Communalect Group')} ${h.link(request, ctx.communalectgroup)}</h3>

% if map_ or request.map:
${(map_ or request.map).render()}
% endif

${request.get_datatable('languages', h.models.Language, fijicommunalect=ctx).render()}
