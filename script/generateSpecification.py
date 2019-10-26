import yaml
import json
import sys
import csv
import copy

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--inputfile', help="the path to the input csv-file", required=True)
args = parser.parse_args()

print("Reading organizations from: %s"%args.inputfile)

def transformString(inputString):
    s = inputString.lower().replace("æ", "e")
    s = s.lower().replace("ø", "o")
    s = s.lower().replace("å", "a")
    return s

def generateSpec(template, org):
    # Need to do a deepcopy to actually copy the template into a new object.
    specification = copy.deepcopy(template)

    domain = transformString(org[1]).replace(" ", "").lower() + ".no"

    # Then put the org-specific values into the specification:
    specification['info']['title'] = template['info']['title'] + ' ' + org[1]
    specification['info']['contact']['name'] = org[1]
    specification['info']['contact']['url'] = 'https://www.' + domain
    specification['info']['contact']['email'] = 'info@' + domain

    # We must recreate the Server object
    specification['servers'] = []
    # Prod url
    server = {}
    server['url'] = "https://api." + domain
    server['description'] = 'Production server'
    specification['servers'].append(server)
    # Test url
    server = {}
    server['url'] = "https://api.test." + domain
    server['description'] = 'Test server'
    specification['servers'].append(server)

    return specification

templateFilePath = './script/'
templateFileName = 'regnskapsregister.yaml'
with open(templateFilePath + templateFileName) as t:
    template = yaml.safe_load(t)
    with open(args.inputfile, encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=",")
        # extracting field names through first row
        next(reader, None)
        for org in reader:
            orgNummer = org[0]
            # Transform special-chars:
            orgName = transformString(org[1]).replace(" ", "-").lower()
            templateFileName = templateFileName.replace(' ', '_')
            specificationPath = "./specs/"
            specificationFileName = specificationPath + orgName + "_openAPI"+ '.json'
            print('writing specifcation to file', specificationFileName)
            # Validate Prod url:
            with open(specificationFileName, 'w', encoding="utf-8") as outfile:
                json.dump(generateSpec(template, org), outfile, ensure_ascii=False, indent=2)
