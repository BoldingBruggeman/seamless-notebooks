import argparse
import yaml

parser = argparse.ArgumentParser()
parser.add_argument('fabm_yaml')
parser.add_argument('--scale', type=float, default=0.3)
args = parser.parse_args()

with open(args.fabm_yaml) as f:
    y = yaml.safe_load(f)

for name, info in y['instances'].items():
    parameters = info.get('parameters', {})
    if not parameters:
        continue
    for parameter, value in parameters.items():
        path = 'instances/%s/parameters/%s' % (name, parameter)
        if isinstance(value, (float, int)) and not isinstance(value, bool):
            l, r = (1 - args.scale) * value, (1 + args.scale) * value
            if r < l:
                l, r = r, l
            xml = '<parameter file="fabm.yaml" variable="%s" minimum="%s" maximum="%s" />' % (path, l, r)
            if isinstance(value, int):
                xml = '<!-- %s -->' % xml
            print(xml)