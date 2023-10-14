<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "communalects" %>
<%block name="title">${_('Communalects')}</%block>

<h2>${_('Communalects')}</h2>

${ctx.render()}
