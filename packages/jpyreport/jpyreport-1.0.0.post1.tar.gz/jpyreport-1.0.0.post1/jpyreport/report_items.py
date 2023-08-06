from abc import abstractmethod
import time

from yattag import Doc
from pyhtml import *


def __used_pyhtml():
  return html()


class HtmlReportElement(object):
  def __init__(self, doc, report):
    self.doc = doc  # type: Doc
    self.report = report
    self._status_levels = ['passed', 'failed', 'errors']
    self._columns = ['tests', 'passed', 'failed', 'errors']
    self._column_headers = ['Count', 'Pass', 'Fail', 'Error']
    if self.report.attrs.show_skipped:
      self._status_levels.append('skipped')
      self._columns.append('skipped')
      self._column_headers.append('Skipped')

  @abstractmethod
  def html(self): pass

  def _js_show_level(self, level):
    return 'javascript:showLevel("%s")' % level

  def _js_show_status_level(self, level):
    return 'javascript:showStatusLevel("%s")' % level


class HtmlReportPage(HtmlReportElement):
  def __init__(self, report, js, css):
    super(self.__class__, self).__init__(Doc(), report)
    self.js = js
    self.css = css

  def html(self):
    doc, tag, text, line = self.doc.ttl()
    doc.asis('<!DOCTYPE html>')
    with tag('html'):
      with tag('head'):
        with tag('title'):
          text(self.report.attrs.title)
      with tag('style'):
        doc.asis(self.css)
      with tag('body'):
        with tag('script', language='javascript', type='text/javascript'):
          doc.asis(self.js)
        HtmlReportSummary(doc, self.report).html()
        HtmlShowDetailLine(doc, self.report).html()
        HtmlReportTable(doc, self.report).html()
    return doc.getvalue()


class HtmlReportSummary(HtmlReportElement):
  def html(self):
    doc, tag, text, line = self.doc.ttl()
    with tag('div', klass='summary'):
      with tag('h1'):
        text(self.report.attrs.title)
      with tag('p', klass='attribute'):
        with tag('strong'):
          text('Duration ')
        text(self.__duration())
      with tag('p', klass='attribute'):
        with tag('strong'):
          text('Status ')
        line('a', '%d tests' % self.report.tests, href=self._js_show_level('all'),
             klass='status_link summary default all')
        text(', ')
        non_zero_levels = [x for x in self._status_levels if self.report[x] > 0]
        for level in non_zero_levels:
          line('a', '%s %s' % (self.report[level], level), href=self._js_show_status_level(level),
               klass='status_link summary %s' % level)
          if non_zero_levels.index(level) < len(non_zero_levels) - 1:
            text(', ')

  def __duration(self):
    return time.strftime('%H:%M:%S', time.gmtime(self.report.duration))


class HtmlShowDetailLine(HtmlReportElement):
  def html(self):
    doc, tag, text = self.doc.tagtext()
    with tag('p', klass='show-details-line'):
      text('Show ')
      items = ['Summary', 'Failed', 'All']
      for item in items:
        with tag('a', href=self._js_show_level(item.lower())):
          text(item)
        text(' ')


class HtmlReportTable(HtmlReportElement):
  def html(self):
    doc, tag, text = self.doc.tagtext()
    with tag('table'):
      HeaderRow(self.doc, self.report).html()
      for test_suit in self.report.test_suits:
        TestSuitRow(self.doc, test_suit).html()
        for test_case in test_suit.test_cases:
          TestCaseRow(self.doc, test_case).html()


class HeaderRow(HtmlReportElement):
  def html(self):
    doc, tag, text, line = self.doc.ttl()
    with tag('tr', klass='header'):
      line('td', self.report.attrs.test_group_name, klass='col-test-group')
      for h in self._column_headers:
        line('td', h)


class TestSuitRow(HtmlReportElement):
  def __init__(self, doc, testsuit):
    super(self.__class__, self).__init__(doc, testsuit.report)
    self.testsuit = testsuit  # type: JUnitTestSuit

  def html(self):
    doc, tag, text, line = self.doc.ttl()
    with tag('tr', klass=self.__class(), status_level='all %s' % self.testsuit.status_level,
             onclick='toggleLevel("' + self.testsuit.name_ + '")'):
      line('td', self.testsuit.name)
      for col in self._columns:
        line('td', self.testsuit[col])

  def __class(self):
    return 'suitcase testsuit %s' % self.testsuit.status


class TestCaseRow(HtmlReportElement):
  def __init__(self, doc, testcase):
    super(self.__class__, self).__init__(doc, testcase.report)
    self.test_case = testcase  # type: JUnitTestCase

  def html(self):
    doc, tag, text, line = self.doc.ttl()
    with tag('tr', klass='hidden %s' % self.__class(), level=self.__level(), status_level=self.__status_level()):
      with tag('td', klass=self.__class()):
        line('div', self.test_case.name, klass='testcase_name')
      with tag('td', colspan=len(self._columns) + 1, align='center'):
        line('a', self.test_case.status, klass='popup_link', href='javascript:0', onclick='togglePopup(this)')
        with tag('div', klass='popup_window hidden'):
          line('pre', self.test_case.output)

  def __class(self):
    if self.test_case.is_error:
      return 'testcase error'
    if self.test_case.is_failed:
      return 'testcase failed'
    if self.test_case.is_skipped:
      return 'testcase skipped'
    return 'testcase default'

  def __level(self):
    levels = []
    levels.append('all')
    levels.append(self.test_case.test_suite_name_)
    levels.append(self.test_case.name_)
    if self.test_case.is_error or self.test_case.is_failed:
      levels.append('failed')
    return ' '.join(levels)

  def __status_level(self):
    levels = [x for x in self._status_levels if self.test_case[x]]
    return ' '.join(levels)


class TotalRow(HtmlReportElement):
  def html(self):
    doc, tag, text, line = self.doc.ttl()
    with tag('tr', klass='total'):
      line('td', 'Total')
      for col in self._columns:
        line('td', self.report[col])
