from clld.db.meta import DBSession
from clld.web.adapters.geojson import GeoJson, pacific_centered
from clld.web.maps import Layer, Map, ParameterMap

from fijian100wl import models


class LanguagesMap(Map):
    def get_options(self):
        return {
            "show_labels": False,
            "max_zoom": 14,
        }


class GeoJsonCommunalect(GeoJson):
    def feature_iterator(self, ctx, req):
        return DBSession.query(models.FijiVillage).filter(
            models.FijiVillage.communalect_pk == ctx.pk
        )


class CommunalectMap(LanguagesMap):
    def get_layers(self):
        """Generate the list of layers.

        :return: list or generator of :py:class:`clld.web.maps.Layer` instances.
        """
        yield Layer(
            getattr(self.ctx, "id", "id"),
            "%s" % self.ctx,
            GeoJsonCommunalect(self.ctx).render(self.ctx, self.req, dump=False),
        )


class GeoJsonCommunalectGroup(GeoJson):
    def feature_iterator(self, ctx, req):
        return DBSession.query(models.FijiVillage).filter(
            models.FijiVillage.communalectgroup_pk == ctx.pk
        )


class CommunalectGroupMap(LanguagesMap):
    def get_layers(self):
        """Generate the list of layers.

        :return: list or generator of :py:class:`clld.web.maps.Layer` instances.
        """
        yield Layer(
            getattr(self.ctx, "id", "id"),
            "%s" % self.ctx,
            GeoJsonCommunalectGroup(self.ctx).render(self.ctx, self.req, dump=False),
        )


class EntryMap(ParameterMap):
    def get_options(self):
        return {
            "show_labels": False,
            "max_zoom": 14,
        }


def includeme(config):
    # Fiji
    pacific_centered()

    config.register_map("languages", LanguagesMap)
    config.register_map("communalect", CommunalectMap)
    config.register_map("communalectgroup", CommunalectGroupMap)
    config.register_map("parameter", EntryMap)
