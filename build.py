#!/usr/bin/env python3

import os
import shutil
import argparse
import subprocess

def postprocess_html(root):
    to_process = []
    for root, _dirs, files in os.walk(root):
        for file in files:
            if file.endswith('.html'):
                to_process.append(os.path.join(root, file))
    subprocess.run(['yarn', 'mjrender', *to_process]).check_returncode()

    print('Fixing up alabaster.css')
    with open('build/html/_static/alabaster.css', 'r+') as cssfile:
        lines = cssfile.readlines()
        for i, line in enumerate(lines):
            if line.startswith('@import url("basic.css");'):
                lines[i] = '@import "./basic.css";\n'
                break
        cssfile.seek(0, 0)
        cssfile.writelines(lines)

def clean_command(args):
    shutil.rmtree('build', ignore_errors=True)
    shutil.rmtree('dist', ignore_errors=True)
    shutil.rmtree('.cache', ignore_errors=True)

def build_command(args):
    subprocess.run(['sphinx-build', '-M', 'html', 'source', 'build']).check_returncode()
    postprocess_html('build/html')
    # if args.production:
    #     shutil.rmtree('dist', ignore_errors=True)

    #     # FIXME: this currently has a problem: Parcel doesn't work well with jQuery and underscore
    #     # Check the developer console and you'll see two errors
    #     subprocess.run(['yarn', 'build'], shell=True).check_returncode()

def deploy_command(args):
    # FIXME: need to change the source to 'dist/' once the jQuery issue is fixed
    subprocess.run([
        'rsync', '-zavP', '--exclude', '.buildinfo',
        '--delete-excluded', '--delete', 'build/html/', args.dest
    ]).check_returncode()

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(required=True, help='sub-command help')

    clean_parser = subparsers.add_parser('clean', help='clean help')
    clean_parser.set_defaults(func=clean_command)

    build_parser = subparsers.add_parser('build', help='build help')
    build_parser.add_argument('-p, --production', dest='production', action='store_true', help='build for production')
    build_parser.set_defaults(func=build_command)

    deploy_parser = subparsers.add_parser('deploy', help='deploy help')
    deploy_parser.add_argument('dest', help='destination')
    deploy_parser.set_defaults(func=deploy_command)

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
