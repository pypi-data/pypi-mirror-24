# -*- coding: utf-8 -*-

# MIT License
# Copyright (c) 2017 David Betz
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import unittest
import pprint

try:
    from memorydb import MemoryDb
except:
    from .memorydb import MemoryDb

try:
    import idgen
except:
    from . import idgen

try:
    from hamlet import hamlet, piglet
except:
    from .hamlet import hamlet, piglet

try:
    import aggregate as aggregate
except:
    from . import aggregate as aggregate

pp = pprint.PrettyPrinter(depth=4)

class TestApp(unittest.TestCase):
    def setUp(self):
        self.provider = MemoryDb()

    def test_get_tokenized_data_no_indices_set(self):
        scope = idgen.generate(__name__)
        
        self.provider.insert(scope, 'item1', { 'title': 'n n z c c c d d d dddd' })
        self.provider.insert(scope, 'item2', { 'title': 'n n m c c d dddd doodle' })
        self.provider.insert(scope, 'item3', { 'title': 'n n z m m c d d d donkey' })

        analysis = self.provider.textAnalysis(scope)

        self.assertIsNone(analysis)

    def test_get_tokenized_data(self):
        scope = idgen.generate(__name__)
        
        self.provider.textIndex(scope, { 'title': True })
        self.provider.insert(scope, 'item1', { 'title': 'n n z c c c d d d dddd' })
        self.provider.insert(scope, 'item2', { 'title': 'n n m c c d dddd doodle' })
        self.provider.insert(scope, 'item3', { 'title': 'n n z m m c d d d donkey' })

        analysis = self.provider.textAnalysis(scope)
        dump = analysis.dump()

        sample_key = analysis.terms()[0]
        self.assertIsNotNone(sample_key)
        self.assertGreater(len(sample_key), 0)

        dump_single = analysis.dump()[sample_key]
        self.assertIsNotNone(dump_single)
        self.assertGreater(dump_single['sum'], 0)
        self.assertGreater(len(dump_single['spread'].keys()), 0)

        self.assertEquals(dump['c']['spread'][1]['value'], 'item3')
        self.assertEquals(dump['c']['spread'][2]['value'], 'item2')
        self.assertEquals(dump['c']['spread'][3]['value'], 'item1')

        self.assertEquals(dump['m']['spread'][1]['value'], 'item2')
        self.assertEquals(dump['m']['spread'][2]['value'], 'item3')

        self.assertEquals(dump['z']['spread'][1]['value'], 'item1')
        self.assertEquals(dump['z']['spread'][1]['next']['value'], 'item3')

        self.assertEquals(dump['d']['spread'][1]['value'], 'item2')
        self.assertEquals(dump['d']['spread'][3]['value'], 'item1')
        self.assertEquals(dump['d']['spread'][3]['next']['value'], 'item3')

        self.assertEquals(dump['n']['spread'][2]['value'], 'item1')
        self.assertEquals(dump['n']['spread'][2]['next']['value'], 'item2')
        self.assertEquals(dump['n']['spread'][2]['next']['next']['value'], 'item3')

    def test_get_tokenized_data_two_fields(self):
        scope = idgen.generate(__name__)

        self.provider.textIndex(scope, {
            'title': { 'weight': 2 },
            'text': { 'weight': 1 }
        })
        self.provider.insert(scope, 'item1', {
            'title': 'c d d',
            'text': 'n n z c c c d d d d d dddd'
        })
        self.provider.insert(scope, 'item2', {
            'title': 'm m z',
            'text': 'n n m c c d dddd doodle'
        })
        self.provider.insert(scope, 'item3', {
            'title': 'd d d',
            'text': 'n n z m m c d d d donkey'
        })

        analysis = self.provider.textAnalysis(scope)
        dump = analysis.dump()
        
        # print('[dump]')
        # pp.pprint(dump)
        # print('[/dump]')
        
        sample_key = analysis.terms()[0]
        self.assertIsNotNone(sample_key)
        self.assertGreater(len(sample_key), 0)

        dump_single = analysis.dump()[sample_key]
        self.assertIsNotNone(dump_single)
        self.assertGreater(dump_single['sum'], 0)
        self.assertGreater(len(dump_single['spread'].keys()), 0)

        self.assertEquals(dump['c']['spread'][1]['value'], 'item3')
        self.assertEquals(dump['c']['spread'][2]['value'], 'item2')
        self.assertEquals(dump['c']['spread'][5]['value'], 'item1')

        self.assertEquals(dump['m']['spread'][5]['value'], 'item2')
        self.assertEquals(dump['m']['spread'][2]['value'], 'item3')

        self.assertEquals(dump['z']['spread'][1]['value'], 'item1')
        self.assertEquals(dump['z']['spread'][2]['value'], 'item2')
        self.assertEquals(dump['z']['spread'][1]['next']['value'], 'item3')

        self.assertEquals(dump['d']['spread'][9]['value'], 'item1')
        self.assertEquals(dump['d']['spread'][1]['value'], 'item2')
        self.assertEquals(dump['d']['spread'][9]['next']['value'], 'item3')

        self.assertEquals(dump['n']['spread'][2]['value'], 'item1')
        self.assertEquals(dump['n']['spread'][2]['next']['value'], 'item2')
        self.assertEquals(dump['n']['spread'][2]['next']['next']['value'], 'item3')



    def test_get_tokenized_data_terms(self):
        scope = idgen.generate(__name__)
        
        self.provider.textIndex(scope, { 'title': True })
        self.provider.insert(scope, 'item1', { 'title': 'n n z c c c d d d dddd' })
        self.provider.insert(scope, 'item2', { 'title': 'n n m c c d dddd doodle' })
        self.provider.insert(scope, 'item3', { 'title': 'n n z m m c d d d donkey' })

        # print('[self.provider.dumpdb()]')
        # pp.pprint(self.provider.dumpdb())
        # print('[/]')
        # print('[self.provider.dumpindices(scope)]')
        # pp.pprint(self.provider.dumpindices(scope))
        # print('[/]')
        
        analysis = self.provider.textAnalysis(scope)

        terms = analysis.terms()

        self.assertIsNotNone(terms)
        self.assertGreater(len(terms[0]), 0)
        self.assertGreater(len(terms), 0)

    def test_get_tokenized_data_scores(self):
        scope = idgen.generate(__name__)

        self.provider.textIndex(scope, { 'title': True })
        self.provider.insert(scope, 'item1', { 'title': 'n n z c c c d d d dddd' })
        self.provider.insert(scope, 'item2', { 'title': 'n n m c c d dddd doodle' })
        self.provider.insert(scope, 'item3', { 'title': 'n n z m m c d d d donkey' })
          
        analysis = self.provider.textAnalysis(scope)
        
        sample_key = 'd'

        scores = analysis.scores(sample_key)

        self.assertEquals(scores[0], 3)
        self.assertEquals(scores[1], 1)

    def test_get_tokenized_data_top(self):
        scope = idgen.generate(__name__)

        self.provider.textIndex(scope, { 'title': True })
        self.provider.insert(scope, 'item1', { 'title': 'n n z c c c d d d dddd' })
        self.provider.insert(scope, 'item2', { 'title': 'n n m c c d dddd doodle' })
        self.provider.insert(scope, 'item3', { 'title': 'n n z m m c d d d donkey' })
          
        analysis = self.provider.textAnalysis(scope)
        
        sample_key = 'd'

        top = analysis.top(sample_key)

        self.assertEquals(top, 'item1')

    def test_get_tokenized_data_all(self):
        scope = idgen.generate(__name__)

        self.provider.textIndex(scope, { 'title': True })
        self.provider.insert(scope, 'item1', { 'title': 'n n z c c c d d d dddd' })
        self.provider.insert(scope, 'item2', { 'title': 'n n m c c d dddd doodle' })
        self.provider.insert(scope, 'item3', { 'title': 'n n z m m c d d d donkey' })
          
        analysis = self.provider.textAnalysis(scope)
        
        sample_key = 'm'

        all = analysis.all(sample_key)

        self.assertEquals(all[0], 'item2')
        self.assertEquals(all[1], 'item3')

    def test_get_tokenized_data_all_chained(self):
        scope = idgen.generate(__name__)

        self.provider.textIndex(scope, { 'title': True })
        self.provider.insert(scope, 'item1', { 'title': 'n n z c c c d d d dddd' })
        self.provider.insert(scope, 'item2', { 'title': 'n n m c c d dddd doodle' })
        self.provider.insert(scope, 'item3', { 'title': 'n n z m m c d d d donkey' })
          
        analysis = self.provider.textAnalysis(scope)
        
        sample_key = 'd'

        all = analysis.all(sample_key)

        self.assertEquals(all[0], 'item2')
        self.assertEquals(all[1], 'item1')
        self.assertEquals(all[2], 'item3')

    def test_get_tokenized_data_filter(self):
        scope = idgen.generate(__name__)

        self.provider.textIndex(scope, { 'title': True })
        self.provider.insert(scope, 'item1', { 'title': 'n n z c c c d d d dddd' })
        self.provider.insert(scope, 'item2', { 'title': 'n n m c c d dddd doodle' })
        self.provider.insert(scope, 'item3', { 'title': 'n n z m m c d d d donkey' })
          
        analysis = self.provider.textAnalysis(scope)

        sample_key = 'd'

        top = analysis.top(sample_key)

        filtered = analysis.filter(lambda p: p.startswith(sample_key))
        filtered_keys = filtered.keys()

        self.assertEquals(filtered['d']['sum'], 7)
        self.assertEquals(filtered['dddd']['sum'], 2)

    def test_get_tokenized_data_scores_top_filter_more_data(self):
        scope = idgen.generate(__name__)

        self.provider.textIndex(scope, { 'title': True })
        for n in range(20):
            self.provider.insert(scope, idgen.generate(__name__), { "title": piglet(400), "order": n })
          
        analysis = self.provider.textAnalysis(scope)
        terms = analysis.terms()
        sample_key = terms[0]
        scores = analysis.scores(sample_key)
        top = analysis.top(sample_key)
        filtered = analysis.filter(lambda p: p.startswith(sample_key[0]))
        filtered_keys = filtered.keys()
        for p in filtered_keys:
            self.assertEquals(p[0], sample_key[0])
            self.assertTrue(p in terms)

    def test_get_tokenize_data_highlight(self):
        scope = idgen.generate(__name__)

        self.provider.textIndex(scope, { 'title': True })
        self.provider.insert(scope, 'item1', { 'title': 'n n z c c c d d d dddd' })
        self.provider.insert(scope, 'item2', { 'title': 'n n m c c d dddd doodle' })
        self.provider.insert(scope, 'item3', { 'title': 'n n z m m c d d d donkey' })
          
        analysis = self.provider.textAnalysis(scope)

        sample_key = 'd'

        top = analysis.top(sample_key)

        p = self.provider.get(scope, top)

        highlighted = analysis.highlight(sample_key, p['title'], '<{{_}}>')
        
        self.assertEquals(highlighted, 'n n z c c c <d> <d> <d> dddd')

    def test_dumpindices_for_all(self):
        scope1 = idgen.generate(__name__)
        scope2 = idgen.generate(__name__)

        scope1_index = {
            "title": { "weight": 2 },
            "text": { "weight": 1 }
        }
        scope2_index = {
            "headings": { "weight": 2 }
        }
        self.provider.textIndex(scope1, scope1_index)
        self.provider.textIndex(scope2, scope2_index)

        all = self.provider.dumpindices()
        self.assertEquals(all[scope1], scope1_index)
        self.assertEquals(all[scope2], scope2_index)

    def test_dumpindices_for_single_scope(self):
        scope1 = idgen.generate(__name__)
        scope2 = idgen.generate(__name__)

        scope1_index = {
            "title": { "weight": 2 },
            "text": { "weight": 1 }
        }
        self.provider.textIndex(scope1, scope1_index)
        self.provider.textIndex(scope2, {
            "headings": { "weight": 2 }
        })

        self.assertEquals(self.provider.dumpindices(scope1), scope1_index)

    def test_dumpindices_for_wrong_scope(self):
        self.assertIsNone(self.provider.dumpindices('asdfasdf'))