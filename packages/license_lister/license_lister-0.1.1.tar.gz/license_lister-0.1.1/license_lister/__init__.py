#!/usr/bin/env python

import gevent.monkey as monkey
monkey.patch_all()

import argparse
import json
import os
import re
import subprocess
import sys

from gevent.pool import Pool


REQUIREMENT_FILE_NAME_PATTERN = r'requirement.*\.txt'


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p',
                        action='append',
                        help='Path to search for requirement files, repeat '
                             'flag to add more paths',
                        default=[])
    parser.add_argument('--resolve-versions',
                        action='store_true',
                        default=False,
                        help='If more than one version of a package is used, '
                             'show the license info for each version '
                             'individually')
    parser.add_argument('--pool-size',
                        type=int,
                        default=5,
                        help='Number of concurrent connections to PyPi when '
                             'fetching package license data')
    parser.add_argument('--format',
                        type=str,
                        choices=['text', 'json'],
                        default='text',
                        help='Format for license list output')

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    return parser.parse_args()


def find_requirement_files(repo_path):
    for root, dirs, files in os.walk(repo_path):
        path = root.split(os.sep)
        for file in files:
            if re.search(REQUIREMENT_FILE_NAME_PATTERN, file):
                path_to_file = os.path.sep.join(path) + os.path.sep + file
                yield path_to_file


def get_packages(file_path, resolve_versions):
    for line in open(file_path):
        if resolve_versions:
            package_name = line.strip()
        else:
            package_name = line.strip().split('==')[0]
        if package_name:
            yield package_name


def get_license(package_name):
    print('Fetching license for {}'.format(package_name))
    args = ['yolk', '-M', package_name, '-f', 'license']
    process = subprocess.Popen(args, stdout=subprocess.PIPE)
    out, err = process.communicate()
    if err:
        print('Error getting license for {}: {}'.format(package_name, err))
        return 'UNKNOWN'
    return out.decode('utf8').strip() or 'UNKNOWN'


def get_all_licenses(packages, pool_size):
    print('Fetching license info from PyPi...')

    pool = Pool(pool_size)

    licenses = pool.map(get_license, packages)

    return packages, licenses


def render_license_list(packages, licenses, format='text'):

    if format == 'json':
        data = []
        for package, license in zip(packages, licenses):
            data.append({'name': package, 'license': license})
        print(json.dumps(data, indent=2))
    elif format == 'text':
        output = zip(packages, licenses)
        for package, license in output:
            print('{:<40s} {}'.format(package, license))
    else:
        raise Exception('Unknown format: {}'.format(format))


def run():
    args = parse_args()

    packages = set()

    for base_path in args.p:
        for requirement_file in find_requirement_files(base_path):
            print('Processing file: {}'.format(requirement_file))
            packages.update(get_packages(requirement_file,
                                         args.resolve_versions))

    packages = sorted(list(packages), key=lambda x: x.lower())

    print('Found {} packages:'.format(len(packages)))

    packages, licenses = get_all_licenses(packages, pool_size=args.pool_size)

    render_license_list(packages, licenses, args.format)
