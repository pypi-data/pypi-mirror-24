import xml.etree.ElementTree

import os
from glob import glob


class JUnitReportAttributes:
  def __init__(self,
               title='Unit Test Report',
               test_group_name='Test Group / Test Case',
               show_skipped=True):
    self.title = title
    self.test_group_name = test_group_name
    self.show_skipped = show_skipped


class JUnitReport:
  def __init__(self, dir, attrs):
    report_files = [y for x in os.walk(dir) for y in glob(os.path.join(x[0], '*.xml'))]
    self.attrs = attrs
    self.test_suits = []  # type: list[JUnitTestSuit]
    for r in report_files:
      root = xml.etree.ElementTree.parse(r).getroot()
      if root.tag == 'testsuite':
        suite = JUnitTestSuit(root, self)
        if suite.only_skipped and not self.attrs.show_skipped:
          continue
        self.test_suits.append(suite)

  @property
  def duration(self):
    return sum([float(x.time) for x in self.test_suits])

  @property
  def tests(self):
    if self.attrs.show_skipped:
      return sum([x.tests_count for x in self.test_suits])
    return self.errors + self.failed + self.passed

  @property
  def failed(self):
    return sum([x.failures_count for x in self.test_suits])

  @property
  def errors(self):
    return sum([x.errors_count for x in self.test_suits])

  @property
  def skipped(self):
    return sum([x.skipped_count for x in self.test_suits])

  @property
  def passed(self):
    return sum([x.passed_count for x in self.test_suits])

  def __getitem__(self, item):
    if item == 'tests':
      return self.tests
    if item == 'failed':
      return self.failed
    if item == 'errors':
      return self.errors
    if item == 'skipped':
      return self.skipped
    if item == 'passed':
      return self.passed
    return None


class JUnitTestSuit:
  def __init__(self, root, report):
    attrs = root.attrib
    self.report = report
    self.name = attrs['name']
    self.tests_count = int(attrs['tests'])
    self.failures_count = int(attrs['failures'])
    self.errors_count = int(attrs['errors'])
    self.skipped_count = int(attrs['skipped'])
    self.passed_count = self.tests_count - self.skipped_count - self.failures_count - self.errors_count
    self.time = attrs['time']
    self.test_cases = []  # type: list[JUnitTestCase]

    for child in root:
      testcase = JUnitTestCase(child, report)
      if testcase.is_skipped and not self.report.attrs.show_skipped:
        continue
      self.test_cases.append(testcase)

  @property
  def name_(self):
    return self.name.replace(' ', '_')

  @property
  def only_skipped(self):
    return self.skipped_count == self.tests_count

  @property
  def status(self):
    if self.errors_count > 0:
      return 'error'
    if self.failures_count > 0:
      return 'fail'
    if self.skipped_count == self.tests_count:
      return 'skipped'
    return 'pass'

  @property
  def status_level(self):
    levels = []
    if self.failures_count > 0:
      levels.append('failed')
    if self.errors_count > 0:
      levels.append('errors')
    if self.passed_count > 0:
      levels.append('passed')
    if self.skipped_count > 0:
      levels.append('skipped')
    return ' '.join(levels)

  def __getitem__(self, item):
    if item == 'tests':
      return self.tests_count
    if item == 'failed':
      return self.failures_count
    if item == 'errors':
      return self.errors_count
    if item == 'skipped':
      return self.skipped_count
    if item == 'passed':
      return self.passed_count
    return None


class JUnitTestCase:
  def __init__(self, root, report):
    self.report = report
    attrs = root.attrib
    self.test_suit_name = attrs['classname']
    self.status = attrs['status']
    self.time = attrs['time']
    self.name = attrs['name']
    sout = root.find('system-out')
    self.sout = ''
    if not sout is None:
      self.sout = sout.text
    skipped = root.find('skipped')
    self.skipped = None
    self.skipped_msg = None
    if not skipped is None:
      self.skipped = skipped.text
      self.skipped_msg = skipped.attrib['message']
    err = root.find('error')
    self.error = None if err is None else JUnitTestError(err)

  @property
  def test_suite_name_(self):
    return self.test_suit_name.replace(' ', '_')

  @property
  def name_(self):
    return self.name.replace(' ', '_')

  @property
  def is_failed(self):
    return self.status == 'failed' and self.error is None

  @property
  def is_error(self):
    return self.status == 'failed' and not self.error is None

  @property
  def is_skipped(self):
    return self.status == 'skipped'

  @property
  def is_passed(self):
    return self.status == 'passed'

  def __getitem__(self, item):
    if item == 'failed':
      return self.is_failed
    if item == 'errors':
      return self.is_error
    if item == 'skipped':
      return self.is_skipped
    if item == 'passed':
      return self.is_passed
    return None

  @property
  def output(self):
    if self.is_error:
      return '%s %s' % (self.sout, self.error.output)
    if self.is_skipped:
      return '%s\nskipped: %s %s' % (self.sout, self._or_empty(self.skipped_msg), self._or_empty(self.skipped))
    return self.sout

  def _or_empty(self, p):
    return p if not p is None else ''


class JUnitTestError():
  def __init__(self, root):
    attrs = root.attrib
    self.message = attrs['message']
    self.type = attrs['type']
    self.output = root.text
    pass
