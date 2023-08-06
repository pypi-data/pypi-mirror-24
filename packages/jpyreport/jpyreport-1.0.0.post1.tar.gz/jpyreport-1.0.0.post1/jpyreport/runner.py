from optparse import OptionParser
import os, sys

from report_items import *
from junit_parser import JUnitReport, JUnitReportAttributes

__SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))

usage = "usage: %prog xml_reports_directory [-d file | -c cssfile]"
oparser = OptionParser(usage=usage, prog="jpyreport")
oparser.add_option("-d", "--dest", dest="result_path", default='.', help="write report to file", metavar="file")
oparser.add_option("-c", "--css", dest="css_path", action="store", default="%s/style.css" % __SCRIPT_PATH,
                   help="css file to link", metavar="css")
oparser.add_option("-t", "--title", dest="report_title", default='Unit Test Report',
                   help="title for report, default: 'Unit Test Report'",
                   metavar="title")
oparser.add_option("-g", "--group_title", dest="group_title", default='Test Group / Test Case',
                   help="title for test group column, default: 'Test Group / Test Case'",
                   metavar="group_title")
oparser.add_option("-s", "--show_skipped", dest="show_skipped", action="store_true", default=False,
                   help="whether or not to show skipped tests",
                   metavar="skipped")


def run():
  (options, args) = oparser.parse_args(sys.argv[1:])
  if len(args) < 1:
    oparser.print_usage()
    sys.exit(1)

  source_path = args[0]
  if not os.path.isdir(source_path):
    print 'Error: source path must be directory.'
    sys.exit(1)

  result_path = update_result_path(options.result_path)
  attrs = JUnitReportAttributes(title=options.report_title,
                                test_group_name=options.group_title,
                                show_skipped=options.show_skipped)
  generate_report(source_path, result_path, options.css_path, attrs)


def update_result_path(result_path):
  if not os.path.exists(result_path):
    os.makedirs(result_path)
  if not os.path.isfile(result_path):
    result_path = '%s/junit-report.html' % (result_path)
  if not '.html' in result_path:
    result_path = result_path + '.html'
  return result_path


def generate_report(source_path, result_path, css_path, attrs):
  report = JUnitReport(source_path, attrs)

  with open('%s/report.js' % __SCRIPT_PATH, 'r') as f:
    js = f.read()

  with open(css_path, 'r') as f:
    css = f.read()

  html = HtmlReportPage(report, js, css).html()
  f = open(result_path, "w+")
  f.write(html)
  f.close()


if __name__ == "__main__":
  run()
