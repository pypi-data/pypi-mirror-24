# -*- coding: utf-8 -*-

"""Utilities for serializing to BEL namespace and BEL annotation files"""

from __future__ import print_function

import getpass
import logging
import sys
import time

import os

from pybel.constants import NAMESPACE_DOMAIN_TYPES, belns_encodings, METADATA_AUTHORS, METADATA_CONTACT, METADATA_NAME
from pybel.utils import get_bel_resource
from .summary.error_summary import get_incorrect_names_by_namespace, get_undefined_namespace_names
from .summary.node_summary import get_names_by_namespace
from .utils import get_iso_8601_date as get_date

__all__ = [
    'make_namespace_header',
    'make_annotation_header',
    'make_author_header',
    'make_citation_header',
    'make_properties_header',
    'write_namespace',
    'write_annotation',
    'export_namespace',
    'export_namespaces',
    'get_merged_namespace_names',
    'merge_namespaces',
    'check_cacheable',
]

log = logging.getLogger(__name__)

DATETIME_FMT = '%Y-%m-%dT%H:%M:%S'
DATE_FMT = '%Y-%m-%d'
DATE_VERSION_FMT = '%Y%m%d'
DEFAULT_NS_DESCRIPTION = 'This namespace was serialized by PyBEL Tools'


def make_namespace_header(name, keyword, domain, query_url=None, description=None, species=None, version=None,
                          created=None):
    """Makes the ``[Namespace]`` section of a BELNS file

    :param str name: The namespace name
    :param str keyword: Preferred BEL Keyword, maximum length of 8
    :param str domain: One of: :data:`pybel.constants.NAMESPACE_DOMAIN_BIOPROCESS`, 
                    :data:`pybel.constants.NAMESPACE_DOMAIN_CHEMICAL`,
                    :data:`pybel.constants.NAMESPACE_DOMAIN_GENE`, or
                    :data:`pybel.constants.NAMESPACE_DOMAIN_OTHER`
    :param str query_url: HTTP URL to query for details on namespace values (must be valid URL)
    :param str description: Namespace description
    :param str species: Comma-separated list of species taxonomy id's
    :param str version: Namespace version. Defaults to current date in ``YYYYMMDD`` format.
    :param str created: Namespace public timestamp, ISO 8601 datetime
    :return: An iterator over the lines of the ``[Namespace]`` section of a BELNS file
    :rtype: iter[str]
    """
    if domain not in NAMESPACE_DOMAIN_TYPES:
        raise ValueError('Invalid domain: {}. Should be one of: {}'.format(domain, NAMESPACE_DOMAIN_TYPES))

    yield '[Namespace]'
    yield 'Keyword={}'.format(keyword)
    yield 'NameString={}'.format(name)
    yield 'DomainString={}'.format(domain)
    yield 'VersionString={}'.format(version if version else get_date())
    yield 'CreatedDateTime={}'.format(created if created else time.strftime(DATETIME_FMT))
    yield 'DescriptionString={}'.format(
        DEFAULT_NS_DESCRIPTION if description is None else description.strip().replace('\n', ''))

    if species is not None:
        yield 'SpeciesString={}'.format(species)

    if query_url is not None:
        yield 'QueryValueURL={}'.format(query_url)


def make_author_header(name=None, contact=None, copyright_str=None):
    """Makes the ``[Author]`` section of a BELNS file

    :param str name: Namespace's authors
    :param str contact: Namespace author's contact info/email address
    :param str copyright_str: Namespace's copyright/license information. Defaults to ``Other/Proprietary``
    :return: An iterable over the ``[Author]`` section of a BELNS file
    :rtype: iter[str]
    """
    yield '[Author]'
    yield 'NameString={}'.format(name if name is not None else getpass.getuser())
    yield 'CopyrightString={}'.format('Other/Proprietary' if copyright_str is None else copyright_str)

    if contact is not None:
        yield 'ContactInfoString={}'.format(contact)


def make_citation_header(name, description=None, url=None, version=None, date=None):
    """Makes the ``[Citation]`` section of a BEL config file.

    :param str name: Citation name
    :param str description: Citation description
    :param str url: URL to more citation information
    :param str version: Citation version
    :param str date: Citation publish timestamp, ISO 8601 Date
    :return: An iterable over the lines of the ``[Citation]`` section of a BEL config file
    :rtype: iter[str]
    """
    yield '[Citation]'
    yield 'NameString={}'.format(name)

    if date is not None:
        yield 'PublishedDate={}'.format(date)

    if version is not None:
        yield 'PublishedVersionString={}'.format(version)

    if description is not None:
        yield 'DescriptionString={}'.format(description)

    if url is not None:
        yield 'ReferenceURL={}'.format(url)


def make_properties_header(case_sensitive=True, delimiter='|', cacheable=True):
    """Makes the ``[Processing]`` section of a BEL config file.
    
    :param bool case_sensitive: Should this config file be interpreted as case-sensitive?
    :param str delimiter: The delimiter between names and labels in this config file
    :param bool cacheable: Should this config file be cached?
    :return: An iterable over the lines in the ``[Processing]`` section of a BEL config file
    :rtype: iter[str]
    """
    yield '[Processing]'
    yield 'CaseSensitiveFlag={}'.format('yes' if case_sensitive else 'no')
    yield 'DelimiterString={}'.format(delimiter)
    yield 'CacheableFlag={}'.format('yes' if cacheable else 'no')


def write_namespace(namespace_name, namespace_keyword, namespace_domain, author_name, citation_name, values,
                    namespace_description=None, namespace_species=None, namespace_version=None,
                    namespace_query_url=None, namespace_created=None, author_contact=None, author_copyright=None,
                    citation_description=None, citation_url=None, citation_version=None, citation_date=None,
                    case_sensitive=True, delimiter='|', cacheable=True, functions=None, file=None, value_prefix='',
                    sort_key=None):
    """Writes a BEL namespace (BELNS) to a file

    :param str namespace_name: The namespace name
    :param str namespace_keyword: Preferred BEL Keyword, maximum length of 8
    :param str namespace_domain: One of: :data:`pybel.constants.NAMESPACE_DOMAIN_BIOPROCESS`, 
                            :data:`pybel.constants.NAMESPACE_DOMAIN_CHEMICAL`,
                            :data:`pybel.constants.NAMESPACE_DOMAIN_GENE`, or
                            :data:`pybel.constants.NAMESPACE_DOMAIN_OTHER`
    :param str author_name: The namespace's authors
    :param str citation_name: The name of the citation
    :param iter[str] values: An iterable of values (strings)
    :param str namespace_query_url: HTTP URL to query for details on namespace values (must be valid URL)
    :param str namespace_description: Namespace description
    :param str namespace_species: Comma-separated list of species taxonomy id's
    :param str namespace_version: Namespace version
    :param str namespace_created: Namespace public timestamp, ISO 8601 datetime
    :param str author_contact: Namespace author's contact info/email address
    :param str author_copyright: Namespace's copyright/license information
    :param str citation_description: Citation description
    :param str citation_url: URL to more citation information
    :param str citation_version: Citation version
    :param str citation_date: Citation publish timestamp, ISO 8601 Date
    :param bool case_sensitive: Should this config file be interpreted as case-sensitive?
    :param str delimiter: The delimiter between names and labels in this config file
    :param bool cacheable: Should this config file be cached?
    :param functions: The encoding for the elements in this namespace
    :type functions: iterable of characters
    :param file file: A writable file or file-like
    :param str value_prefix: a prefix for each name
    :param sort_key: A function to sort the values with :func:`sorted`. Give ``False`` to not sort
    """
    file = sys.stdout if file is None else file

    for line in make_namespace_header(namespace_name, namespace_keyword, namespace_domain,
                                      query_url=namespace_query_url, description=namespace_description,
                                      species=namespace_species, version=namespace_version, created=namespace_created):
        print(line, file=file)
    print(file=file)

    for line in make_author_header(author_name, contact=author_contact, copyright_str=author_copyright):
        print(line, file=file)
    print(file=file)

    for line in make_citation_header(citation_name, description=citation_description, url=citation_url,
                                     version=citation_version, date=citation_date):
        print(line, file=file)
    print(file=file)

    for line in make_properties_header(case_sensitive=case_sensitive, delimiter=delimiter, cacheable=cacheable):
        print(line, file=file)
    print(file=file)

    function_values = ''.join(sorted(functions if functions is not None else belns_encodings.keys()))

    print('[Values]', file=file)

    if sort_key is None:
        values = sorted(set(values))
    elif sort_key:
        values = sorted(set(values), key=sort_key)

    for value in map(str, values):
        if not value.strip():
            continue
        print('{}{}|{}'.format(value_prefix, value.strip(), function_values), file=file)


def make_annotation_header(keyword, description=None, usage=None, version=None, created=None):
    """Makes the ``[AnnotationDefinition]`` section of a BELANNO file

    :param str keyword: Preferred BEL Keyword, maximum length of 8
    :param str description: A description of this annotation
    :param str usage: How to use this annotation
    :param str version: Namespace version. Defaults to date in ``YYYYMMDD`` format.
    :param str created: Namespace public timestamp, ISO 8601 datetime
    :return: A iterator over the lines for the ``[AnnotationDefinition]`` section
    :rtype: iter[str]
    """

    yield '[AnnotationDefinition]'
    yield 'Keyword={}'.format(keyword)
    yield 'TypeString={}'.format('list')
    yield 'VersionString={}'.format(version if version else get_date())
    yield 'CreatedDateTime={}'.format(created if created else time.strftime(DATETIME_FMT))

    if description is not None:
        yield 'DescriptionString={}'.format(description.strip().replace('\n', ''))

    if usage is not None:
        yield 'UsageString={}'.format(usage.strip().replace('\n', ''))


def write_annotation(keyword, values, citation_name, description=None, usage=None, version=None, created=None,
                     author_name=None, author_copyright=None, author_contact=None, case_sensitive=True, delimiter='|',
                     cacheable=True, file=None, value_prefix=''):
    """Writes a BEL annotation (BELANNO) to a file

    :param str keyword: The annotation keyword
    :param dict[str, str] values: A dictionary of {name: label}
    :param str citation_name: The citation name
    :param str description: A description of this annotation
    :param str usage: How to use this annotation
    :param str version: The version of this annotation. Defaults to date in ``YYYYMMDD`` format.
    :param str created: The annotation's public timestamp, ISO 8601 datetime
    :param str author_name: The author's name
    :param str author_copyright: The copyright information for this annotation. Defaults to ``Other/Proprietary``
    :param str author_contact: The contact information for the author of this annotation.
    :param bool case_sensitive: Should this config file be interpreted as case-sensitive?
    :param str delimiter: The delimiter between names and labels in this config file
    :param bool cacheable: Should this config file be cached?
    :param file file: A writable file or file-like
    :param str value_prefix: An optional prefix for all values
    """
    file = sys.stdout if file is None else file

    for line in make_annotation_header(keyword, description=description, usage=usage, version=version, created=created):
        print(line, file=file)
    print(file=file)

    for line in make_author_header(name=author_name, contact=author_contact, copyright_str=author_copyright):
        print(line, file=file)
    print(file=file)

    print('[Citation]', file=file)
    print('NameString={}'.format(citation_name), file=file)
    print(file=file)

    for line in make_properties_header(case_sensitive=case_sensitive, delimiter=delimiter, cacheable=cacheable):
        print(line, file=file)
    print(file=file)

    print('[Values]', file=file)
    for key, value in sorted(values.items()):
        if not key.strip():
            continue
        print('{}{}|{}'.format(value_prefix, key.strip(), value.strip().replace('\n', '')), file=file)


def export_namespace(graph, namespace, directory=None, cacheable=False):
    """Exports all names and missing names from the given namespace to its own BEL Namespace files in the given
    directory.

    Could be useful during quick and dirty curation, where planned namespace building is not a priority.

    :param pybel.BELGraph graph: A BEL graph
    :param str namespace: The namespace to process
    :param str directory: The path to the directory where to output the namespace. Defaults to the current working
                      directory returned by :func:`os.getcwd`
    :param bool cacheable: Should the namespace be cacheable? Defaults to ``False`` because, in general, this operation 
                        will probably be used for evil, and users won't want to reload their entire cache after each
                        iteration of curation.
    """
    directory = os.getcwd() if directory is None else directory
    path = os.path.join(directory, '{}.belns'.format(namespace))

    with open(path, 'w') as file:
        log.info('Outputting to %s', path)
        right_names = get_names_by_namespace(graph, namespace)
        log.info('Graph has %d correct names in %s', len(right_names), namespace)
        wrong_names = get_incorrect_names_by_namespace(graph, namespace)
        log.info('Graph has %d incorrect names in %s', len(right_names), namespace)
        undefined_ns_names = get_undefined_namespace_names(graph, namespace)
        log.info('Graph has %d names in missing namespace %s', len(right_names), namespace)

        names = (right_names | wrong_names | undefined_ns_names)

        if 0 == len(names):
            log.warning('%s is empty', namespace)

        write_namespace(
            namespace_name=namespace,
            namespace_keyword=namespace,
            namespace_domain='Other',
            author_name=graph.document.get(METADATA_AUTHORS),
            author_contact=graph.document.get(METADATA_CONTACT),
            citation_name=graph.document.get(METADATA_NAME),
            values=names,
            cacheable=cacheable,
            file=file
        )


def export_namespaces(graph, namespaces, directory=None, cacheable=False):
    """Thinly wraps :func:`export_namespace` for an iterable of namespaces.
    
    :param pybel.BELGraph graph: A BEL graph
    :param iter[str] namespaces: An iterable of strings for the namespaces to process
    :param str directory: The path to the directory where to output the namespaces. Defaults to the current working
                      directory returned by :func:`os.getcwd`
    :param bool cacheable: Should the namespaces be cacheable? Defaults to ``False`` because, in general, this operation 
                        will probably be used for evil, and users won't want to reload their entire cache after each 
                        iteration of curation.
    """
    directory = os.getcwd() if directory is None else directory  # avoid making multiple calls to os.getcwd later
    for namespace in namespaces:
        export_namespace(graph, namespace, directory=directory, cacheable=cacheable)


def get_merged_namespace_names(locations, check_keywords=True):
    """Loads many namespaces and combines their names.
    
    :param iter[str] locations: An iterable of URLs or file paths pointing to BEL namespaces.
    :param bool check_keywords: Should all the keywords be the same? Defaults to ``True``
    :return: A dictionary of {names: labels}
    :rtype: dict[str, str]
    
    Example Usage
    
    >>> graph = ...
    >>> original_ns_url = ...
    >>> export_namespace(graph, 'MBS') # Outputs in current directory to MBS.belns
    >>> value_dict = get_merged_namespace_names([original_ns_url, 'MBS.belns'])
    >>> with open('merged_namespace.belns', 'w') as f:
    >>> ...  write_namespace('MyBrokenNamespace', 'MBS', 'Other', 'Charles Hoyt', 'PyBEL Citation', value_dict, file=f)
    """
    resources = {location: get_bel_resource(location) for location in locations}

    if check_keywords:
        resource_keywords = set(config['Namespace']['Keyword'] for config in resources.values())
        if 1 != len(resource_keywords):
            raise ValueError('Tried merging namespaces with different keywords: {}'.format(resource_keywords))

    result = {}
    for resource in resources:
        result.update(resource['Values'])
    return result


def merge_namespaces(input_locations, output_path, namespace_name, namespace_keyword, namespace_domain, author_name,
                     citation_name, namespace_description=None, namespace_species=None, namespace_version=None,
                     namespace_query_url=None, namespace_created=None, author_contact=None, author_copyright=None,
                     citation_description=None, citation_url=None, citation_version=None, citation_date=None,
                     case_sensitive=True, delimiter='|', cacheable=True, functions=None, value_prefix='',
                     sort_key=None, check_keywords=True):
    """Merges namespaces from multiple locations to one.
    
    :param iter input_locations: An iterable of URLs or file paths pointing to BEL namespaces.
    :param str output_path: The path to the file to write the merged namespace
    :param str namespace_name: The namespace name
    :param str namespace_keyword: Preferred BEL Keyword, maximum length of 8
    :param str namespace_domain: One of: :data:`pybel.constants.NAMESPACE_DOMAIN_BIOPROCESS`, 
                            :data:`pybel.constants.NAMESPACE_DOMAIN_CHEMICAL`,
                            :data:`pybel.constants.NAMESPACE_DOMAIN_GENE`, or
                            :data:`pybel.constants.NAMESPACE_DOMAIN_OTHER`
    :param str author_name: The namespace's authors
    :param str citation_name: The name of the citation
    :param str namespace_query_url: HTTP URL to query for details on namespace values (must be valid URL)
    :param str namespace_description: Namespace description
    :param str namespace_species: Comma-separated list of species taxonomy id's
    :param str namespace_version: Namespace version
    :param str namespace_created: Namespace public timestamp, ISO 8601 datetime
    :param str author_contact: Namespace author's contact info/email address
    :param str author_copyright: Namespace's copyright/license information
    :param str citation_description: Citation description
    :param str citation_url: URL to more citation information
    :param str citation_version: Citation version
    :param str citation_date: Citation publish timestamp, ISO 8601 Date
    :param bool case_sensitive: Should this config file be interpreted as case-sensitive?
    :param str delimiter: The delimiter between names and labels in this config file
    :param bool cacheable: Should this config file be cached?
    :param functions: The encoding for the elements in this namespace
    :type functions: iterable of characters
    :param str value_prefix: a prefix for each name
    :param sort_key: A function to sort the values with :func:`sorted`
    :param bool check_keywords: Should all the keywords be the same? Defaults to ``True``
    """
    results = get_merged_namespace_names(input_locations, check_keywords=check_keywords)

    with open(output_path, 'w') as file:
        write_namespace(
            namespace_name=namespace_name,
            namespace_keyword=namespace_keyword,
            namespace_domain=namespace_domain,
            author_name=author_name,
            citation_name=citation_name,
            values=results,
            namespace_species=namespace_species,
            namespace_description=namespace_description,
            namespace_query_url=namespace_query_url,
            namespace_version=namespace_version,
            namespace_created=namespace_created,
            author_contact=author_contact,
            author_copyright=author_copyright,
            citation_description=citation_description,
            citation_url=citation_url,
            citation_version=citation_version,
            citation_date=citation_date,
            case_sensitive=case_sensitive,
            delimiter=delimiter,
            cacheable=cacheable,
            functions=functions,
            value_prefix=value_prefix,
            sort_key=sort_key,
            file=file
        )


def check_cacheable(config):
    """Checks the config returned by :func:`pybel.utils.get_bel_resource` to determine if the resource should be cached.

    If cannot be determined, returns ``False``

    :param dict config: A configuration dictionary representing a BEL resource
    :return: Should this resource be cached
    :rtype: bool
    """

    if 'Processing' in config and 'CacheableFlag' in config['Processing']:
        flag = config['Processing']['CacheableFlag']

        if 'yes' == flag:
            return True
        elif 'no' == flag:
            return False
        else:
            return ValueError('Invalid value for CacheableFlag: {}'.format(flag))

    return False
