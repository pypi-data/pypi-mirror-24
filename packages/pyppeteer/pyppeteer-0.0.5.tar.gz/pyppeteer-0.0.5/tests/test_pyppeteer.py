#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_pyppeteer
----------------------------------

Tests for `pyppeteer` module.
"""

import asyncio
import logging
import unittest

from syncer import sync
from tornado import web

from pyppeteer.launcher import launch
from pyppeteer.util import install_asyncio, get_free_port


def setUpModule() -> None:
    logging.getLogger('tornado').setLevel(logging.ERROR)
    # logging.getLogger('pyppeteer').setLevel(logging.ERROR)
    install_asyncio()


BASE_HTML = '''
<html>
<head><title>main</title></head>
<body>
<h1 id="hello">Hello</h1>
<a id="link1" href="./1">link1</a>
<a id="link2" href="./2">link2</a>
</body>
</html>
'''


class MainHandler(web.RequestHandler):
    def get(self) -> None:
        self.write(BASE_HTML)


class LinkHandler1(web.RequestHandler):
    def get(self) -> None:
        self.write('''
<head><title>link1</title></head>
<h1 id="link1">Link1</h1>
<a id="back1" href="./">back1</a>
        ''')


class TestPyppeteer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.port = get_free_port()
        cls.app = web.Application([
            ('/', MainHandler),
            ('/1', LinkHandler1),
        ], logging='error')
        cls.server = cls.app.listen(cls.port)
        cls.browser = launch()
        cls.page = sync(cls.browser.newPage())

    @classmethod
    def tearDownModule(cls):
        cls.browser.close()
        cls.server.stop()

    def setUp(self):
        sync(self.page.goto('http://localhost:' + str(self.port)))

    @sync
    async def test_get(self):
        self.assertEqual(await self.page.title(), 'main')
        self.elm = await self.page.querySelector('h1#hello')
        self.assertTrue(self.elm)

    @sync
    async def test_plain_text(self):
        text = await self.page.plainText()
        self.assertEqual(text.split(), ['Hello', 'link1', 'link2'])

    @sync
    async def test_content(self):
        html = await self.page.content()
        self.assertEqual(html.replace('\n', ''), BASE_HTML.replace('\n', ''))

    @sync
    async def test_element(self):
        elm = await self.page.querySelector('h1')
        text = await elm.evaluate('(element) => element.textContent')
        self.assertEqual('Hello', text)

    @sync
    async def test_elements(self):
        elms = await self.page.querySelectorAll('a')
        self.assertEqual(len(elms), 2)
        elm1 = elms[0]
        elm2 = elms[1]
        self.assertEqual(await elm1.attribute('id'), 'link1')
        self.assertEqual(await elm2.attribute('id'), 'link2')

    @sync
    async def test_element_inner_html(self):
        elm = await self.page.querySelector('h1')
        text = await elm.evaluate('(element) => element.innerHTML')
        self.assertEqual('Hello', text)

    @sync
    async def test_element_outer_html(self):
        elm = await self.page.querySelector('h1')
        text = await elm.evaluate('(element) => element.outerHTML')
        self.assertEqual('<h1 id="hello">Hello</h1>', text)

    @sync
    async def test_element_attr(self):
        elm = await self.page.querySelector('h1')
        _id = await elm.attribute('id')
        self.assertEqual('hello', _id)

    @sync
    async def test_click(self):
        await self.page.click('#link1')
        await self.page.waitForSelector('h1#link1')
        self.assertEqual(await self.page.title(), 'link1')
        elm = await self.page.querySelector('h1#link1')
        self.assertTrue(elm)

    @sync
    async def test_wait_for_timeout(self):
        await self.page.click('#link1')
        await self.page.waitFor(0.1)
        self.assertEqual(await self.page.title(), 'link1')

    @sync
    async def test_elm_click(self):
        btn1 = await self.page.querySelector('#link1')
        self.assertTrue(btn1)
        await btn1.click()
        await self.page.waitForSelector('h1#link1')
        self.assertEqual(await self.page.title(), 'link1')

    @sync
    async def test_back_forward(self):
        await self.page.click('#link1')
        await self.page.waitForSelector('h1#link1')
        self.assertEqual(await self.page.title(), 'link1')
        await self.page.goBack()
        await self.page.waitForSelector('h1#hello')
        self.assertEqual(await self.page.title(), 'main')
        elm = await self.page.querySelector('h1#hello')
        self.assertTrue(elm)
        await self.page.goForward()
        await self.page.waitForSelector('h1#link1')
        self.assertEqual(await self.page.title(), 'link1')
        btn2 = await self.page.querySelector('#link1')
        self.assertTrue(btn2)

    @sync
    async def test_cookies(self) -> None:
        cookies = await self.page.cookies()
        self.assertEqual(cookies, [])
        await self.page.evaluate(
            '() => {document.cookie = "username=John Doe"}'
        )
        cookies = await self.page.cookies()
        self.assertEqual(cookies, [{
            'name': 'username',
            'value': 'John Doe',
            'domain': 'localhost',
            'path': '/',
            'expires': 0,
            'size': 16,
            'httpOnly': False,
            'secure': False,
            'session': True,
        }])
        await self.page.setCookie({'name': 'password', 'value': '123456'})
        cookies = await self.page.evaluate(
            '() => document.cookie'
        )
        self.assertEqual(cookies, 'username=John Doe; password=123456')
        cookies = await self.page.cookies()
        self.assertEqual(cookies, [{
            'name': 'password',
            'value': '123456',
            'domain': 'localhost',
            'path': '/',
            'expires': 0,
            'size': 14,
            'httpOnly': False,
            'secure': False,
            'session': True,
        }, {
            'name': 'username',
            'value': 'John Doe',
            'domain': 'localhost',
            'path': '/',
            'expires': 0,
            'size': 16,
            'httpOnly': False,
            'secure': False,
            'session': True,
        }])
        await self.page.deleteCookie({'name': 'username'})
        cookies = await self.page.evaluate(
            '() => document.cookie'
        )
        self.assertEqual(cookies, 'password=123456')
        cookies = await self.page.cookies()
        self.assertEqual(cookies, [{
            'name': 'password',
            'value': '123456',
            'domain': 'localhost',
            'path': '/',
            'expires': 0,
            'size': 14,
            'httpOnly': False,
            'secure': False,
            'session': True,
        }])
