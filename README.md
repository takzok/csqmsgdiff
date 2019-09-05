# csqmsgdiff

This application parses IBM MQ for z / OS system messages from the manual on the Knowledge Center and outputs the differences between versions.

## Prerequisties

python 3.5 or later(pre-req lxml)

## Usage

`python csqmsgdiff.py -h` to displya help.

### source command

Get html file that contains CSQ messages.

#### syntax

`python csqmsgdiff.py source [url_list] [output_path]`

| attribute   | description                                                                       |
|-------------|-----------------------------------------------------------------------------------|
| url_list    | Specify text file with URL of Knowledge center.                                   |
| output_path | Specify the location to save the acquired html file. (default: current directory) |

> Note: Sample URL list files are in sample/urlxxx.txt

### parse command

Generate CSQ message list in CSV format.

#### syntax

`python csqmsgdiff.py scrape [input_path] [output_path]`

| attribute   | description                                                                       |
|-------------|-----------------------------------------------------------------------------------|
| version     | Specify target MQ version (800, 900, 910).                                        |
| input_path  | Specify the location to read html file(s). (default: current directory)           |
| output_path | Specify the location to save the generated csv file. (default: current directory) |

### diff command

Generate a diff file of CSQ messages between MQ versions

#### syntax

`python csqmsgdiff.py source [referenced_csv_path] [comapred_csv_path] [output_path]`

| attribute           | description                                                              |
|---------------------|--------------------------------------------------------------------------|
| referenced_csv_path | Specify the location to read csv file(s). (left side pane in diff file)  |
| compated_csv_path   | Specify the location to read csv file(s). (right side pane in diff file) |
| output_path         | Specify the location to save the generated diff file.                    |

## Todo

- [ ] リファクタリング
