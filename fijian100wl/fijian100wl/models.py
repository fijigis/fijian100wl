from clld import interfaces
from clld.db.meta import Base, CustomModelMixin
from clld.db.models import IdNameDescriptionMixin, common
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship
from zope.interface import implementer

from fijian100wl.interfaces import ICommunalect, ICommunalectGroup

# -----------------------------------------------------------------------------
# specialized common mapper classes
# -----------------------------------------------------------------------------


@implementer(interfaces.ILanguage)
class FijiVillage(CustomModelMixin, common.Language):
    """
    New table 'fijilanguage' has one-to-one relationship with the existing table 'language'
    """

    pk = Column(Integer, ForeignKey("language.pk"), primary_key=True)
    communalect_pk = Column(Integer, ForeignKey("fijicommunalect.pk"), nullable=True)
    communalectgroup_pk = Column(
        Integer, ForeignKey("fijicommunalectgroup.pk"), nullable=True
    )

    @declared_attr
    def communalect(cls):
        return relationship(
            "FijiCommunalect", innerjoin=True
        )  # , backref=backref('fijivillage', order_by=cls.communalect_pk))

    @declared_attr
    def communalectgroup(cls):
        return relationship(
            "FijiCommunalectGroup", innerjoin=True
        )  # , backref=backref('fijivillage', order_by=cls.communalectgroup_pk))


@implementer(ICommunalect)
class FijiCommunalect(Base, CustomModelMixin, IdNameDescriptionMixin):
    pk = Column(Integer, primary_key=True)
    communalectgroup_pk = Column(
        Integer, ForeignKey("fijicommunalectgroup.pk"), nullable=False
    )

    @declared_attr
    def communalectgroup(cls):
        return relationship(
            "FijiCommunalectGroup",
            innerjoin=True,
            back_populates="communalect",
            order_by=cls.communalectgroup_pk,
        )  # backref=backref('fijicommunalect', order_by=cls.communalectgroup_pk))


@implementer(ICommunalectGroup)
class FijiCommunalectGroup(Base, CustomModelMixin, IdNameDescriptionMixin):
    pk = Column(Integer, primary_key=True)
    communalect = relationship(
        "FijiCommunalect", back_populates="communalectgroup"
    )  # backref="fijicommunalectgroups")
