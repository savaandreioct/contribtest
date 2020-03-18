# generate site from static pages, loosely inspired by Jekyll
# run like this:
#   ./generate.py test/source output
# the generated `output` should be the same as `test/expected_output`

import os
import logging
# import needed packages
import json
import sys
from jinja2 import FileSystemLoader, Environment

log = logging.getLogger(__name__)


def list_files(folder_path):
    # check if folder_path is empty, return paths for .rst files to be used
    if (len(os.listdir(folder_path)) != 0):
        try:
            for name in os.listdir(folder_path):
                base, ext = os.path.splitext(name)
                if ext != '.rst':
                    continue
                yield os.path.join(folder_path, name), base
        except:
            print("Empty folder")


def read_file(file_path):
    # reads a .rst file from file_parh and returns the metadata and content
    with open(file_path, 'r') as f:
        raw_metadata = ""
        for line in f:
            # metadata ends with ---, content starts next line
            if line.strip() == '---':
                if raw_metadata:
                    try:
                        metadata = json.loads(raw_metadata)
                    except:
                        metadata = json.loads(None)
                        print("No metadata")
                break
            raw_metadata += line
        content = ""
        # strip blank lines from .rst files of file_path
        for line in f:
            content += line.strip('\n')

        if content:
            try:
                content = content.strip()
            except:
                print("Something wrong")

        # if metadata processed return a metadata json, else return blank json

    return metadata, content.strip('\n')


def write_output(name, html, output_path):
    # if output folder does not exist try to create
    if not os.path.exists(output_path):
        try:
            os.makedirs(output_path)
        except:
            print('Error cannot create folder')
            sys.exit()
    with open(os.path.join(output_path, name + '.html'), 'w') as f:
        f.write(html)


def generate_site(folder_path, output_path):
    log.info("Generating site from %r", folder_path)
    # creates an env from the html to load layouts from the system file
    jinja_env = Environment(loader=FileSystemLoader(folder_path + 'layout'), trim_blocks=True)
    for file_path, name in list_files(folder_path):
        # return metadata and content separately
        metadata, content = read_file(file_path)
        # gets and create in template the template from layout and
        template = jinja_env.get_template(metadata['layout'])
        # randering
        data = dict(metadata, content=content)
        html = template.render(**data).replace('\n\n', '\n')
        # writes the result in a html file and save
        write_output(name, html, output_path)
        log.info("Writing %r with template %r", name, metadata['layout'])


def main():
    generate_site(sys.argv[1], sys.argv[2])


if __name__ == '__main__':
    logging.basicConfig()
    main()
