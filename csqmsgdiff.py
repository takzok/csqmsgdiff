# -*- coding= utf-8 -*-

__version__ = '1.0.0'

import argparse
import creatediff
import getsource
import csqhtmlscraper

def main():
  try:
    # create parser and subparsers instance.
    parser = argparse.ArgumentParser(
      description='Scraping MQ for z/OS system message list from Knowledge Center and get diff of messages between MQ versions.')

    subparsers = parser.add_subparsers(help='sub-command help', title='subcommands')
    parser.add_argument('--version', default=False, action='version', version='%(prog)s ' + __version__)

    # subcommand diff instance
    parser_diff = subparsers.add_parser(
      'diff',
      help='Output message differences between versions in html file format.(side-by-side style)')
    parser_diff.add_argument(
      'referenced_csv_path',
      type=str,
      help='Location of the reference csv file(s).')
    parser_diff.add_argument(
      'compared_csv_path',
      type=str,
      help='Location of the csv file(s) to be compared')
    parser_diff.add_argument(
      'output_path',
      type=str,
      help='output path')
    parser_diff.add_argument(
      '-c',
      default=False,
      action='store_true',
      required=False,
      help='Export CSV file instead of html')
    parser_diff.set_defaults(func=call_diff_command)

    # subcommand scrape instance
    parser_scrape = subparsers.add_parser(
      'scrape', 
      help='Get messageID and message list as CSV files.')
    parser_scrape.add_argument(
      'mq_version',
      type=str,
      help='Target MQ version',
      choices=['800', '900', '910'])
    parser_scrape.add_argument(
      'input_path',
      type=str,
      help='Location of the source html file path to scrape.')
    parser_scrape.add_argument(
      'output_path',
      default='./',
      type=str,
      help='Location of the directory to output CSV file. (default: current directory)')
    parser_scrape.set_defaults(func=call_scrape_command)

    # subcommand source
    # get html source from given uri list
    parser_source = subparsers.add_parser(
      'source',
      help='Get source html files.')
    parser_source.add_argument(
      'url_list',
      help='Text file name that contains url list.')
    parser_source.add_argument(
      'output_path',
      default='./',
      type=str,
      help='Location of the directory to output html file(s). (default: current directory)')
    parser_source.set_defaults(func=call_source_command)

    # execute given subcommand
    args = parser.parse_args()
    args.func(args)

  except AttributeError as err:
    print(err)
    print('The subcommand is invalid')
  return

def call_diff_command(args):
  creatediff.create_diff(args)

def call_source_command(args):
  getsource.store_html_from_source(args)

def call_scrape_command(args):
  csqhtmlscraper.scrape_html(args)

if __name__ == '__main__':
  main()