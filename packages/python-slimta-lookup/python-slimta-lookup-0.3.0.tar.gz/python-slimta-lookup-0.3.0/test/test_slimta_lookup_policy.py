
from mox3.mox import MoxTestBase, IsA

from slimta.envelope import Envelope
from slimta.lookup.policy import LookupPolicy
from slimta.lookup.drivers.dict import DictLookup


class TestDictLookup(MoxTestBase):

    def setUp(self):
        super(TestDictLookup, self).setUp()
        self.data = {}
        self.drv = DictLookup(self.data, '{address}')
        self.policy = LookupPolicy(self.drv, True, True)

    def test_verp(self):
        self.data['sender@example.com'] = {'verp': 'verp.com'}
        self.data['rcpt2@example.com'] = {'verp': 'verp.com'}
        env = Envelope('sender@example.com', ['rcpt1@example.com', 'rcpt2@example.com'])
        self.policy.apply(env)
        self.assertEquals('sender=example.com@verp.com', env.sender)
        self.assertEquals(['rcpt1@example.com', 'rcpt2=example.com@verp.com'], env.recipients)

    def test_alias(self):
        self.data['sender@example.com'] = {'alias': 'sender@other.com'}
        self.data['rcpt2@example.com'] = {'alias': 'other.com'}
        env = Envelope('sender@example.com', ['rcpt1@example.com', 'rcpt2@example.com'])
        self.policy.apply(env)
        self.assertEquals('sender@other.com', env.sender)
        self.assertEquals(['rcpt1@example.com', 'rcpt2@other.com'], env.recipients)

    def test_add_headers(self):
        self.data['sender@example.com'] = {'add_headers': '{"X-Test-A": "one"}'}
        self.data['rcpt2@example.com'] = {'add_headers': '{"X-Test-B": "two"}'}
        env = Envelope('sender@example.com', ['rcpt1@example.com', 'rcpt2@example.com'])
        env.parse(b"""\n\n""")
        self.policy.apply(env)
        self.assertEquals('one', env.headers['x-test-a'])
        self.assertEquals('two', env.headers['x-test-b'])

# vim:et:fdm=marker:sts=4:sw=4:ts=4:tw=0
