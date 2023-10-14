import functools

from clld import RESOURCES, Resource
from clld.interfaces import IDomainElement, ILanguage, IMapMarker, IValue, IValueSet
from clld.web.adapters import register_resource_adapters
from clld.web.app import menu_item
from clld.web.icon import PREFERED_COLORS, SECONDARY_COLORS, SHAPES, MapMarker
from clldutils.svg import data_url, icon
from pyramid.config import Configurator

# we must make sure custom models are known at database initialization!
from fijian100wl import interfaces, models

COLORS = PREFERED_COLORS + SECONDARY_COLORS


class FijiMapMarker(MapMarker):
    def __call__(self, ctx, req):
        idx = None

        if IValue.providedBy(ctx):
            # table value on parameter
            idx = ctx.domainelement.number
        elif IValueSet.providedBy(ctx):
            # languages on parameter map
            idx = ctx.values[0].domainelement.number
        elif IDomainElement.providedBy(ctx):
            # table legend on parameter
            idx = ctx.number
        elif ILanguage.providedBy(ctx):
            if ctx.communalectgroup_pk is None:
                idx = -1
            else:
                idx = ctx.communalectgroup_pk

        if idx is None:
            import logging

            logging.getLogger(__name__).info(ctx.__dict__)

        if idx is not None:
            if idx >= 0:
                # ORDERED_ICONS provided by clld is badly ordered
                s = SHAPES[idx % len(SHAPES)]
                c = COLORS[idx % len(COLORS)]
            else:
                s = SHAPES[-1]
                c = COLORS[-1]
            return data_url(icon(s + c))
        return super(FijiMapMarker, self).__call__(ctx, req)


def main(global_config, **settings):
    """This function returns a Pyramid WSGI application."""
    # import logging
    # logging.getLogger(__name__).info(settings)

    config = Configurator(settings=settings)
    config.include("clld.web.app")

    config.registry.registerUtility(FijiMapMarker(), IMapMarker)

    resources = [
        # Resource('language', models.FijiVillage, ILanguage),
        Resource("communalect", models.FijiCommunalect, interfaces.ICommunalect),
        Resource(
            "communalectgroup",
            models.FijiCommunalectGroup,
            interfaces.ICommunalectGroup,
        ),
    ]
    for rsc in resources:
        RESOURCES.append(rsc)
        config.register_resource_routes_and_views(rsc)
        register_resource_adapters(config, rsc)

    config.register_menu(
        ("dataset", functools.partial(menu_item, "dataset", label="Home")),
        ("languages", functools.partial(menu_item, "languages", label="Villages")),
        (
            "communalects",
            functools.partial(menu_item, "communalects", label="Communalects"),
        ),
        (
            "communalectgroups",
            functools.partial(
                menu_item, "communalectgroups", label="Communalect Groups"
            ),
        ),
        ("parameters", functools.partial(menu_item, "parameters", label="Concepts")),
    )

    return config.make_wsgi_app()
