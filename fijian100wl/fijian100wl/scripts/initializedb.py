from clld.cliutil import Data
from clld.db.meta import DBSession
from clld.db.models import common

import fijian100wl
from fijian100wl import models


def main(args):
    cldf = args.cldf

    Data()

    dataset = common.Dataset(
        id=fijian100wl.__name__,
        name="Fijian Language 100 Word List",
        description="Fijian Language 100 Word List",
        domain="tulip.kyoto-u.ac.jp/fijian100wl",
        publisher_name="Fijian Language GIS Project",
        publisher_place="Japan/Fiji/New Zealand",
        publisher_url="https://fijigis.github.io/",
        license="http://creativecommons.org/licenses/by/4.0/",
        jsondata={
            "license_icon": "cc-by.png",
            "license_name": "Creative Commons Attribution 4.0 International License",
        },
    )
    DBSession.add(dataset)

    communalectgroup2pk = {}
    for cldf_language in cldf["LanguageTable"]:
        if cldf_language["CommunalectGroup"]:
            if cldf_language["CommunalectGroup"] not in communalectgroup2pk:
                pk = len(communalectgroup2pk)
                DBSession.add(
                    models.FijiCommunalectGroup(
                        pk=pk,
                        id=pk,
                        name=cldf_language["CommunalectGroup"],
                    )
                )
                communalectgroup2pk[cldf_language["CommunalectGroup"]] = pk
    DBSession.flush()

    communalect2pk = {}
    for cldf_language in cldf["LanguageTable"]:
        if cldf_language["Communalect"]:
            if cldf_language["Communalect"] not in communalect2pk:
                pk = len(communalect2pk)
                DBSession.add(
                    models.FijiCommunalect(
                        pk=pk,
                        id=pk,
                        name=cldf_language["Communalect"],
                        communalectgroup_pk=communalectgroup2pk[
                            cldf_language["CommunalectGroup"]
                        ],
                    )
                )
                communalect2pk[cldf_language["Communalect"]] = pk
    DBSession.flush()

    languages = []
    for cldf_language in cldf["LanguageTable"]:
        language_id = cldf_language["ID"]
        communalect_pk = (
            communalect2pk[cldf_language["Communalect"]]
            if cldf_language["Communalect"]
            else None
        )
        communalectgroup_pk = (
            communalectgroup2pk[cldf_language["CommunalectGroup"]]
            if cldf_language["CommunalectGroup"]
            else None
        )
        languages.append(
            models.FijiVillage(
                pk=language_id,
                id=language_id,
                name=cldf_language["Name"],
                communalect_pk=communalect_pk,
                communalectgroup_pk=communalectgroup_pk,
                latitude=cldf_language["Latitude"],
                longitude=cldf_language["Longitude"],
            )
        )
    DBSession.add_all(languages)
    DBSession.flush()

    concepts = []
    for cldf_concept in cldf["ParameterTable"]:
        concept_id = cldf_concept["ID"]
        concepts.append(
            common.Parameter(
                pk=concept_id,
                id=concept_id,
                name=cldf_concept["Name"],
                description=cldf_concept["Description"],
            )
        )
    DBSession.add_all(concepts)
    DBSession.flush()

    concept_name2freq = {}
    for cldf_value in cldf["ValueTable"]:
        concept_id = cldf_value["Parameter_ID"]
        name = cldf_value["Value"]
        if concept_id not in concept_name2freq:
            concept_name2freq[concept_id] = {}
        if name in concept_name2freq[concept_id]:
            concept_name2freq[concept_id][name] += 1
        else:
            concept_name2freq[concept_id][name] = 1

    domainelements = []
    concept_name2pk = {}
    for cldf_concept in cldf["ParameterTable"]:
        concept_id = cldf_concept["ID"]
        concept_name2pk[concept_id] = {}
        name_list = concept_name2freq[concept_id]
        for idx, name in enumerate(
            sorted(name_list.keys(), key=lambda x: name_list[x], reverse=True)
        ):
            domainelement = common.DomainElement(
                pk=len(domainelements),
                id="{}:{}".format(concept_id, idx),
                name=name,
                number=idx,
                parameter_pk=concept_id,
            )
            domainelements.append(domainelement)
            concept_name2pk[concept_id][name] = domainelement.pk
    DBSession.add_all(domainelements)
    DBSession.flush()

    valueset2pk = {}
    values = []
    for cldf_value in cldf["ValueTable"]:
        language_id = cldf_value["Language_ID"]
        concept_id = cldf_value["Parameter_ID"]
        vs_id = "{}:{}".format(language_id, concept_id)
        if vs_id not in valueset2pk:
            pk = len(valueset2pk)
            # DBSession.add(models.DataPoint(
            DBSession.add(
                common.ValueSet(
                    pk=pk,
                    id=vs_id,
                    language_pk=language_id,
                    parameter_pk=concept_id,
                )
            )
            valueset2pk[vs_id] = pk
        values.append(
            common.Value(
                pk=cldf_value["ID"],
                id=cldf_value["ID"],
                domainelement_pk=concept_name2pk[concept_id][cldf_value["Value"]],
                # name=cldf_value["Value"],
                description=cldf_value["Comment"],
                valueset_pk=valueset2pk[vs_id],
            )
        )
    DBSession.add_all(values)
    DBSession.flush()

    # TODO: CLDF
    contributors = [
        common.Contributor(
            id=0,
            name="Fijian Language GIS Project",
            description="Interdisciplinary team comprising professionals from linguistics, geography, and computer science.",
        ),
    ]
    DBSession.add_all(contributors)
    DBSession.flush()
    DBSession.add_all(
        common.Editor(dataset_pk=dataset.pk, contributor_pk=contributor.pk, ord=ord)
        for ord, contributor in enumerate(contributors)
    )


def prime_cache(args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodically whenever data has been updated.
    """
