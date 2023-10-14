<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "communalectgroups" %>
<%block name="title">${_('Communalect Groups')}</%block>

<h2>${_('Communalect Groups')}</h2>

${ctx.render()}
