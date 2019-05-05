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
    subprocess.run(['yarn', 'mjrender', *to_process], shell=True).check_returncode()

def clean_command(args):
    shutil.rmtree('_build', ignore_errors=True)

def test_command(args):
    subprocess.run(['sphinx-build', '-b', 'html', '.', '_build/html'], shell=True).check_returncode()
    postprocess_html('_build/html')

def deploy_command(args):
    subprocess.run([
        'rsync', '-zavP', '--exclude', '.buildinfo',
        '--delete-excluded', '--delete', '_build/html/', args.dest
    ]).check_returncode()

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(required=True, help='sub-command help')

    clean_parser = subparsers.add_parser('clean', help='clean help')
    clean_parser.set_defaults(func=clean_command)

    test_parser = subparsers.add_parser('test', help='test help')
    test_parser.set_defaults(func=test_command)

    deploy_parser = subparsers.add_parser('deploy', help='deploy help')
    deploy_parser.add_argument('dest', help='destination')
    deploy_parser.set_defaults(func=deploy_command)

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
