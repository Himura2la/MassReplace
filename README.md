# How to use

1. Install [Python](https://www.python.org/downloads/)
2. Run `python replacer.py`
3. Edit the generated `config.json` file
4. Run `python replacer.py`
5. Check the result

# Config

Read the [replacer.py](replacer.py) file

# Notes

* Do not run this script with `test_mode == false` on directories outside the VCS.
* In `test_mode`, you can use the GNU diff tool to view changes between `target_path` and `test_target_dir`.
