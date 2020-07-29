import os
import re
import sys
import json

#***************** Config *****************

config_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.json')
config = {
    "rules_file": "sample_rules.txt",
    "target_path": "sample_content",
    "include_extensions": [ 'aspx', 'desc', 'md', 'htm', 'js', 'html' ],
    "exclude_file_names": [ ],
    "test_target_dir": "replaced_content",
    "comment_indicator": "=",
    "empty_string_indicator": "''",
    "test_mode": True,
    "regex": True
}

if os.path.isfile(config_file):
    config = json.load(open(config_file, 'r', encoding='utf-8'))
    for key in ("rules_file", "target_path", "test_target_dir"):
        config[key] = config[key].replace('\\', os.sep).replace('/', os.sep)
else:
    json.dump(config, open(config_file, 'w', encoding='utf-8'), indent=4)
    print(f'{config_file} file not found and was created. Please adapt it to your needs.')
    exit(2)

if config['test_mode'] and not os.path.isdir(config['test_target_dir']):
    os.makedirs(config['test_target_dir'])

#************** Reading rules **************

source_rules = []
target_rules = []

with open(config['rules_file'], "r", encoding='utf-8') as f: lines = f.readlines()
lines = list(filter(lambda line: not (config['comment_indicator'] and line.startswith(config['comment_indicator'])) and not re.match(r'^\s*$', line), lines))
for i, line in enumerate(lines):
    line = line.strip('\r').strip('\n')
    if config['regex']:
        line = line.replace('\\\\', '\\')
    if i % 2 == 0:
        source_rules.append(line)
    else:
        if line == config['empty_string_indicator']:
            target_rules.append('')
        else:
            target_rules.append(line)
        
rules_count = len(source_rules)
if rules_count != len(target_rules):
    print("[ERROR] Some rule lines have no pair.")
    exit(1)
print("Rules:")
for i in range(rules_count):
    target_rule = target_rules[i]
    if target_rules[i] == '':
        target_rule = '[empty string]'
    print(f'{source_rules[i]}\n{target_rule}\n')

#************** Counting files **************

print("[INFO] Counting files...", end="", flush=True)
total_files = 0
for root, dirs, files in os.walk(config['target_path']):
    for name in files:
        if name not in config['exclude_file_names']:
            path = os.path.join(root, name)
            type = name.split(".")[-1]
            if type in config['include_extensions']:
                total_files += 1
print("\r[OK] Total files:", total_files)

#************** Let's go replacing! **************

current_file = 0
changed_files = 0

for root, dirs, files in os.walk(config['target_path']):
    for name in files:
        if name not in config['exclude_file_names']:
            path = os.path.join(root, name)
            type = name.split(".")[-1]
            if type in config['include_extensions']:
                try:
                    with open(path, "r", encoding='utf-8') as f: source = f.read()
                    buffer = source
                    for i in range(rules_count):
                        if config['regex']:
                            buffer = re.sub(source_rules[i], target_rules[i], buffer)
                        else:
                            buffer = buffer.replace(source_rules[i], target_rules[i])
                    if buffer != source:
                        if config['test_mode']:
                            relative_path = path.replace(config['target_path'], '').strip(os.sep)
                            test_target_path = os.path.join(config['test_target_dir'], relative_path)
                            with open(test_target_path, "w", encoding='utf-8') as f: f.write(buffer)
                        else:
                            pass
                            with open(path, "w", encoding='utf-8') as f: f.write(buffer)  # !!! BEWARE ERRORS !!!!
                        changed_files += 1
                    current_file += 1
                    percentage = current_file / total_files * 100
                    progress_string = "\r[" + str(round(percentage)) + "%] " + \
                                     name.encode(sys.stdout.encoding, errors='replace').decode(sys.stdout.encoding)
                    print(progress_string.ljust(80 - len(progress_string)), end="", flush=True)
                except Exception as e:
                    print("\r[ERROR!!!] File:", path)
                    print(e)
                    print("-" * 79)
finishString = f"\r[FINISH] {changed_files} files processed. Happy checking =)"
print(finishString.ljust(80 - len(finishString)))
