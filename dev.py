import argparse
import re
import os
import sys

def update_package_version(version):
    with open('./pymaps/__version__.py', 'w') as f:
        f.write('__version__ = "{}"'.format(str(version)))


if __name__ == '__main__':
    PYTHON = 'python'

    parser = argparse.ArgumentParser()
    parser.add_argument("--version", help="number of the new package version")
    parser.add_argument("--gitpush", help="message for commit and push to Github")
    args = parser.parse_args()
    print(args)

    if args.version:
        msg = '-' * 80 + '\nUPDATING PACKAGE VERSION TO {}\n' + '-' * 80
        print(msg.format(args.version))
        version_pattern = '[0-9]{1,2}\.[0-9]{1,2}\.[0-9]{1,2}'
        version_is_valid = re.match(version_pattern, args.version) is not None
        if version_is_valid:
            update_package_version(args.version)
            print('Sucess!')
        else:
            raise ValueError('Invalid Version {}'.format(args.version))

    THIS_DIR = os.getcwd()
    tests = 'setup.py test'
    docs = 'docs.py'
    install = 'setup.py install'

    print('-' * 80 + '\nRUNNING TESTS\n' + '-' * 80)
    r = os.system(' '.join([PYTHON, tests]))
    if r != 0:
        raise SystemError('Error while testing.')


    print('-' * 80 + '\nBUILDING DOCS\n' + '-' * 80)
    os.chdir('./docs')
    r= os.system(' '.join([PYTHON, docs]))
    if r != 0:
        raise SystemError('Error while building docs.')
    os.chdir(THIS_DIR)


    print('-' * 80 + '\nINSTALLING PACKAGE\n' + '-' * 80)
    r= os.system(' '.join([PYTHON, install]))
    if r != 0:
        raise SystemError('Error while installing the package.')

    if args.gitpush:
        print('-' * 80 + '\nPUSHING TO REPOSITORY\n' + '-' * 80)
        print('Git add')
        os.system('git add .')
        print('Git commit')
        os.system('git commit -m "{}"'.format(args.gitpush))
        print('Git push')
        os.system('git push')
