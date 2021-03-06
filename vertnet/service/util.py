#!/usr/bin/env python

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

__author__ = "John Wieczorek"
__contributors__ = "Aaron Steele, John Wieczorek"
__copyright__ = "Copyright 2016 vertnet.org"
__version__ = "util.py 2016-08-15T15:54+02:00"

import json
import logging

UTIL_VERSION=__version__

ADD_TO_DOWNLOAD_RESULTS = ['url', 'citation', 'gbifdatasetid', 'gbifpublisherid', 'email', 
    'contact', 'pubdate', 'lastindexed', 'migrator', 'hasmedia', 'hastissue',
    'wascaptive', 'isfossil', 'vntype', 'haslength']

OMIT_FROM_DOWNLOADS = ['location', 'record', 'verbatim_record', 'count', 'icode',
    'title', 'orgname', 'emlrights', 'networks', 'hashid', 'rank', 'haslicense', 
    'mappable', 'source_url', 'hastypestatus', 'language', 'iptrecordid',
    'ownerinstitutioncode', 'organismquantity', 'organismquantitytype', 'parenteventid', 
    'samplesizevalue', 'samplesizeunit', 'pointradiusspatialfit', 'footprintspatialfit', 
    'taxonid', 'acceptednameusageid', 'parentnameusageid', 'originalnameusageid', 
    'nameaccordingtoid', 'taxonconceptid', 'parentnameusage', 'nameaccordingto', 
    'nomenclaturalstatus']

TRANSLATE_HEADER = {'pubdate':'dataset_pubdate', 'url':'dataset_url', 
    'title':'dataset_title', 'contact':'dataset_contact', 'email':'dataset_contact_email',
    'citation':'dataset_citation', 'dctype':'type', 'migrator':'migrator_version'}

DWC_RECLEVEL = ['DCType', 'Modified', 'Language', 'License', 'RightsHolder', 
    'AccessRights', 'BibliographicCitation', 'References', 'InstitutionID', 
    'CollectionID', 'DatasetID', 'InstitutionCode', 'CollectionCode', 'DatasetName', 
    'OwnerInstitutionCode', 'BasisOfRecord', 'InformationWithheld', 
    'DataGeneralizations', 'DynamicProperties']

DWC_OCC = ['OccurrenceID', 'CatalogNumber', 'RecordNumber', 'RecordedBy', 
    'IndividualCount', 'OrganismQuantity', 'OrganismQuantityType', 'Sex', 'LifeStage', 
    'ReproductiveCondition', 'Behavior', 'EstablishmentMeans', 'OccurrenceStatus', 
    'Preparations', 'Disposition', 'AssociatedMedia', 'AssociatedReferences', 
    'AssociatedSequences', 'AssociatedTaxa', 'OtherCatalogNumbers', 'OccurrenceRemarks']

DWC_ORGANISM = ['OrganismID', 'OrganismName', 'OrganismScope', 'AssociatedOccurrences',
    'AssociatedOrganisms', 'PreviousIdentifications', 'OrganismRemarks']

DWC_SAMPLE = ['MaterialSampleID']

DWC_EVENT = ['EventID', 'parentEventID', 'FieldNumber', 'EventDate', 'EventTime', 
    'StartDayOfYear', 'EndDayOfYear', 'Year', 'Month', 'Day', 'VerbatimEventDate', 
    'Habitat', 'SamplingProtocol', 'SampleSizeValue', 'SampleSizeUnit', 'SamplingEffort', 
    'FieldNotes', 'EventRemarks']

DWC_LOCATION = ['LocationID', 'HigherGeographyID', 'HigherGeography', 'Continent', 
    'WaterBody', 'IslandGroup', 'Island', 'Country', 'CountryCode', 'StateProvince', 
    'County', 'Municipality', 'Locality', 'VerbatimLocality', 'MinimumElevationInMeters', 
    'MaximumElevationInMeters', 'VerbatimElevation', 'MinimumDepthInMeters', 
    'MaximumDepthInMeters', 'VerbatimDepth', 'MinimumDistanceAboveSurfaceInMeters', 
    'MaximumDistanceAboveSurfaceInMeters', 'LocationAccordingTo', 'LocationRemarks', 
    'DecimalLatitude', 'DecimalLongitude', 'GeodeticDatum', 
    'CoordinateUncertaintyInMeters', 'CoordinatePrecision', 'PointRadiusSpatialFit',
    'VerbatimCoordinates', 'VerbatimLatitude', 'VerbatimLongitude', 
    'VerbatimCoordinateSystem', 'VerbatimSRS', 'FootprintWKT', 'FootprintSRS', 
    'FootprintSpatialFit', 'GeoreferencedBy', 'GeoreferencedDate', 
    'GeoreferenceProtocol', 'GeoreferenceSources', 'GeoreferenceVerificationStatus', 
    'GeoreferenceRemarks']

DWC_GEO = ['GeologicalContextID', 'EarliestEonOrLowestEonothem', 
    'LatestEonOrHighestEonothem', 'EarliestEraOrLowestErathem', 
    'LatestEraOrHighestErathem', 'EarliestPeriodOrLowestSystem', 
    'LatestPeriodOrHighestSystem', 'EarliestEpochOrLowestSeries', 
    'LatestEpochOrHighestSeries', 'EarliestAgeOrLowestStage', 
    'LatestAgeOrHighestStage', 'LowestBiostratigraphicZone', 
    'HighestBiostratigraphicZone', 'LithostratigraphicTerms', 'Group', 'Formation', 
    'Member', 'Bed']

DWC_ID = ['IdentificationID', 'IdentificationQualifier', 'TypeStatus', 'IdentifiedBy', 
    'DateIdentified', 'IdentificationReferences', 'IdentificationVerificationStatus', 
    'IdentificationRemarks']

DWC_TAXON = ['TaxonID', 'ScientificNameID', 'AcceptedNameUsageID', 'ParentNameUsageID', 
    'OriginalNameUsageID', 'NameAccordingToID', 'NamePublishedInID', 'TaxonConceptID', 
    'ScientificName', 'AcceptedNameUsage', 'ParentNameUsage', 'OriginalNameUsage', 
    'NameAccordingTo', 'NamePublishedIn', 'NamePublishedInYear', 'HigherClassification', 
    'Kingdom', 'Phylum', 'Class', 'Order', 'Family', 'Genus', 'Subgenus', 
    'SpecificEpithet', 'InfraspecificEpithet', 'TaxonRank', 'VerbatimTaxonRank', 
    'ScientificNameAuthorship', 'VernacularName', 'NomenclaturalCode', 'TaxonomicStatus', 
    'NomenclaturalStatus', 'TaxonRemarks']

VN_TRAIT = ['LengthInMM', 'LengthType', 'LengthUnitsInferred', 'MassInG', 'MassUnitsInferred',
    'UnderivedLifeStage', 'UnderivedSex']

DWC_ALL = DWC_RECLEVEL + DWC_OCC + DWC_ORGANISM + DWC_SAMPLE + DWC_EVENT + DWC_LOCATION \
    + DWC_GEO + DWC_ID + DWC_TAXON + VN_TRAIT

DWC_ALL_LOWER = [x.lower() for x in DWC_ALL]
DWC_HEADER_LIST = DWC_ALL_LOWER + ADD_TO_DOWNLOAD_RESULTS
DWC_HEADER = '\t'.join(DWC_HEADER_LIST)

def format_json(json):
    return json.replace('""{','{').replace('}""','}').replace('""','"')

def download_field_list():
    """Create a list of the fields in a download. These are the original field names."""
    field_list = []
    for f in DWC_HEADER_LIST:
        field_list.append(f)
    for f in OMIT_FROM_DOWNLOADS:
        try:
            field_list.remove(f)
        except:
            pass
#    logging.debug('%s: FIELD_LIST: %s' % (__version__, field_list))
    return field_list

def download_header():
    """Create a list of the fields in a download. These are the original field names."""
    fieldlist=download_field_list()
    translated = []
    for f in fieldlist:
        if f in TRANSLATE_HEADER:
            translated.append(TRANSLATE_HEADER[f])
        else:
            translated.append(f)
    return '\t'.join(translated)

def classify(record):
    result = dict(meta=record, reclevel={}, occ={}, organism={}, sample={}, event={}, 
        loc={}, geo={}, id={}, taxon={})

    for term in DWC_RECLEVEL:
        if record.has_key(term.lower()):
            result['reclevel'][term] = record[term.lower()]

    for term in DWC_OCC:
        if record.has_key(term.lower()):
            result['occ'][term] = record[term.lower()]

    for term in DWC_ORGANISM:
        if record.has_key(term.lower()):
            result['organism'][term] = record[term.lower()]

    for term in DWC_SAMPLE:
        if record.has_key(term.lower()):
            result['sample'][term] = record[term.lower()]

    for term in DWC_EVENT:
        if record.has_key(term.lower()):
            result['event'][term] = record[term.lower()]

    for term in DWC_LOCATION:
        if record.has_key(term.lower()):
            result['loc'][term] = record[term.lower()]

    for term in DWC_GEO:
        if record.has_key(term.lower()):
            result['geo'][term] = record[term.lower()]

    for term in DWC_ID:
        if record.has_key(term.lower()):
            result['id'][term] = record[term.lower()]

    for term in DWC_TAXON:
        if record.has_key(term.lower()):
            result['taxon'][term] = record[term.lower()]

    return result

def search_resource_counts(recs, old_res_counts=None):
    # Build dictionary of resources with their record counts
    res_counts = {}
    gbifdatasetid = None
    for rec in recs:
        if 'gbifdatasetid' in rec:
            gbifdatasetid=rec['gbifdatasetid']
        else:
            gbifdatasetid=rec[TRANSLATE_HEADER['gbifdatasetid']]
        if gbifdatasetid not in res_counts:
            res_counts[gbifdatasetid] = 1
        else:
            res_counts[gbifdatasetid] += 1
    return res_counts
