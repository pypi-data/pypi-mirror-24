# Changelog for tmpld

## 0.2.5
### Aug 25, 2017
* Shell global uses delegator.py package, to print the stdout of a shell command, you will need to select the out attribute of the returned object.
* Cleaned up cli logic abit.


## 0.2.4
### Aug 22, 2017
* Added `strict` argument, when used it will raise an exception if an undefined variable is missing.


## 0.2.3
### Feb 17, 2016
* Added dirname to globals to help with constructing relative paths to `file` global function.
* Changed files argument to templates
* Switched to using argparse for loading files specified in arguments
* Added the --data argument for passing in data files in yaml or json
* New global called data holds deserialized result of each data file passed
* Passing in - or /dev/stdin as an input file now behaves correctly
* Added util module to cli package
* Added stderr output handler
* jpath global is now jsonpath
* util.get_dirs removes duplicate entries
* new contextmanager for opening files writes stdin to a StringIO buffer.
* Output handler now prints to stderr by default


## 0.2.2
### Feb 13, 2016
* Added dirname to globals to help with constructing relative paths to `file` global function.


## 0.2.1
### Feb 13, 2016
* Added embed template tag. Usage: `{% embed 'path/to/file' 'default', strip=True, strip_comments=False %}`
* Subclassed the `jinja2.Environment` in order to pass a filename context to templates created from strings, also passes filename as a global.
* Added the `FileSystemLoader` that adds the directories of the templates passed so that include's can be used in templates.
* Better handling of Kubernetes api client in instances where there is no Kubernetes server, or configuration cannot be determined.
* Fixed small bug when yaml frontmatter is specified but empty.
* Default logging level is now `WARNING`.
* Removed pycaps, lxml, and jsonpath-rw as hard requirements.
* Created the following extras for package: caps, xpath, jpath, all
* Added python wheel dist format support


## 0.2.0
### Jan 30, 2016
* Initial commit.
