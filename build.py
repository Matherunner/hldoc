#!/usr/bin/env python3

import os
import glob
import shutil
import argparse
import subprocess

def postprocess_html(root):
    print('Rendering MathJax')
    to_process = []
    for root, _, files in os.walk(root):
        for file in files:
            if file.endswith('.html'):
                to_process.append(os.path.join(root, file))
    subprocess.run(['npm', 'run', 'mjrender', *to_process]).check_returncode()

    print('Delete unused files')
    for file in glob.glob('build/html/_static/underscore-*.js'):
        os.remove(file)
    for file in glob.glob('build/html/_static/jquery-*.js'):
        os.remove(file)
    os.remove('build/html/objects.inv')

def clean_command(args):
    shutil.rmtree('build', ignore_errors=True)
    shutil.rmtree('dist', ignore_errors=True)
    shutil.rmtree('.cache', ignore_errors=True)

def build_command(args):
    subprocess.run(['sphinx-build', '-M', 'html', 'source', 'build']).check_returncode()
    postprocess_html('build/html')

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(required=True, help='sub-command help')

    clean_parser = subparsers.add_parser('clean', help='clean help')
    clean_parser.set_defaults(func=clean_command)

    build_parser = subparsers.add_parser('build', help='build help')
    build_parser.add_argument('-p, --production', dest='production', action='store_true', help='build for production')
    build_parser.set_defaults(func=build_command)

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
