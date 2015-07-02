from mock import patch, Mock
import unittest
import logging

import loggly.handlers as handlers

class TestLogglyHandler(unittest.TestCase):
    def setUp(self):
        handlers.session = self.session = Mock()

        self.handler = handlers.HTTPSHandler('url', localname='localname')

        self.record = Mock()
        self.record.levelno = logging.DEBUG
        self.record.exc_info = ['one', 'two']
        self.record.message = 'message'
        self.record.created = 'created'
        self.record.name = 'record'

        self.record.getMessage.return_value = self.record.message

        # expected loggly message
        self.expected = {
            'host': 'localname',
            'message': 'message',
            'full_message': 'test',
            'timestamp': 'created',
            'level': 'DEBUG',
            'facility': 'record'
        }

    def test_bg_cb(self):
        """ the background callback should do nothing """
        handlers.bg_cb(None, None)

    def test_handler_init(self):
        """ it should create a configured handler """
        h = handlers.HTTPSHandler(
            'url', fqdn='fq', localname='bob', facility='auth')

        self.assertEqual(h.url, 'url')
        self.assertEqual(h.fqdn, 'fq')
        self.assertEqual(h.localname, 'bob')
        self.assertEqual(h.facility, 'auth')

    def test_get_full_message_msg(self):
        """ it should log the message """
        self.record.exc_info = None
        result = self.handler.get_full_message(self.record)

        self.record.getMessage.assert_called_once_with()

        self.assertEqual('message', result)

    @patch('traceback.format_exception')
    def test_get_full_message_exc(self, trace):
        """ it should log the traceback """
        trace.return_value = ['trace', 'two']

        result = self.handler.get_full_message(self.record)

        trace.assert_called_once_with('one', 'two')
        self.assertEqual('trace\ntwo', result)

    def test_emit(self):
        """ it should emit the record """
        handler = self.handler

        handler.format = Mock()
        handler.format.return_value = 'msg'

        handler.emit(self.record)

        handler.format.assert_called_once_with(self.record)

        self.session.post.assert_called_once_with(
            'url', data='msg', background_callback=handlers.bg_cb)

    def test_emit_interrupt(self):
        """ it should raise the interrupt """
        handler = self.handler
        handler.format = Mock()

        self.session.post.side_effect = KeyboardInterrupt('Boom!')

        self.assertRaises(KeyboardInterrupt, handler.emit, self.record)

    def test_emit_exit(self):
        """ it should raise the exit """
        handler = self.handler
        handler.format = Mock()

        self.session.post.side_effect = SystemExit('Boom!')

        self.assertRaises(SystemExit, handler.emit, self.record)

    def test_emit_except(self):
        """ it should raise the exit """
        handler = self.handler
        handler.format = Mock()
        handler.handleError = Mock()

        self.session.post.side_effect = Exception('Boom!')

        handler.emit(self.record)

        handler.handleError.assert_called_once_with(self.record)
