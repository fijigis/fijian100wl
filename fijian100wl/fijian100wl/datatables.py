from clld.web.datatables.base import Col, DataTable, IntegerIdCol, LinkCol, LinkToMapCol
from clld.web.util.helpers import map_marker_img
from clld.web.util.htmllib import HTML
from sqlalchemy.orm import joinedload

from fijian100wl import models


class VillageCol(LinkCol):
    def format(self, item):
        return HTML.span(
            map_marker_img(self.dt.req, self.get_obj(item)), LinkCol.format(self, item)
        )

    def search(self, qs):
        return super(VillageCol, self).search(qs)


class CommunalectCol(LinkCol):
    def format(self, item):
        return LinkCol.format(self, item.communalect)


class CommunalectGroupCol(LinkCol):
    def format(self, item):
        return LinkCol.format(self, item.communalectgroup)


class FijiVillages(DataTable):
    __constraints__ = [models.FijiCommunalect, models.FijiCommunalectGroup]

    def base_query(self, query):
        # LEFT OUTER JOIN is used because communalect can be null
        query = query.outerjoin(models.FijiCommunalect).outerjoin(
            models.FijiCommunalectGroup
        )
        if self.fijicommunalect:
            return query.filter(
                models.FijiVillage.communalect == self.fijicommunalect
            ).options(joinedload(models.FijiVillage.communalect))
        if self.fijicommunalectgroup:
            return query.filter(
                models.FijiVillage.communalectgroup == self.fijicommunalectgroup
            ).options(joinedload(models.FijiVillage.communalectgroup))
        return query

    def col_defs(self):
        # TODO: sort/search functionalities for communalect and communalectgroup
        # import logging
        # import logging
        # logging.getLogger(__name__).info(self.model)
        # logging.getLogger(__name__).info(models.FijiCommunalect.name.property.columns)
        # , model_col=models.FijiCommunalect.name
        return [
            IntegerIdCol(self, "id"),
            VillageCol(self, "name"),
            CommunalectCol(
                self,
                "communalect",
                model_col=models.FijiCommunalect.name,
                sDescription="Communalect",
            ),
            CommunalectGroupCol(
                self,
                "communalectgroup",
                model_col=models.FijiCommunalectGroup.name,
                sTitle="Communalect Group",
                sDescription="Communalect group",
            ),
            LinkToMapCol(self, "m"),
            Col(self, "latitude", sDescription="The geographic latitude"),
            Col(self, "longitude", sDescription="The geographic longitude"),
        ]


class FijiCommunalects(DataTable):
    def col_defs(self):
        return [
            IntegerIdCol(self, "id"),
            LinkCol(self, "name"),
            CommunalectGroupCol(self, "communalectgroup", sTitle="Communalect Group"),
        ]


class FijiCommunalectGroups(DataTable):
    def col_defs(self):
        return [
            IntegerIdCol(self, "id"),
            LinkCol(self, "name"),
        ]


def includeme(config):
    """register custom datatables"""
    config.register_datatable("languages", FijiVillages)
    config.register_datatable("communalects", FijiCommunalects)
    config.register_datatable("communalectgroups", FijiCommunalectGroups)
