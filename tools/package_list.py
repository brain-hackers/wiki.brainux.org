import requests


res = requests.get('https://raw.githubusercontent.com/brain-hackers/buildbrain/master/os-brainux/setup_brainux.sh')
lines = res.text.split('\n')

found_packages = []
backslashed = False

for (i,line) in enumerate(lines):       
    if line.strip().startswith('apt install') or backslashed:
        if backslashed:
            packages = line.strip().split(' ')
        else:
            packages = line.strip().split(' ')[2:]
        packages = [p for p in packages if not p.startswith('-')]
        packages = [p for p in packages if not p == '\\']
        packages = [p.rstrip('\\') for p in packages]
        found_packages.extend(packages)
        backslashed = line.endswith('\\')

print('|パッケージ名|')
print('|:-|')
print('\n'.join(f'|{p}|' for p in found_packages))