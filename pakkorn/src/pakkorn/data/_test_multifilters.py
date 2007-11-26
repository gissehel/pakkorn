import unittest
from pakkorn.data import MultiFilters

class TestMultiFilters(unittest.TestCase) :
    def setUp(self) :
        pass

    def test_creation(self) :
        multifilters = MultiFilters()
        self.assertNotEqual(multifilters,None)

    def test_doc_1(self) :
        multifilters = MultiFilters()
        multifilters.add_filter(constraint1=8)
        multifilters.add_filter(constraint2=5)
        multifilters.define_new_set()
        multifilters.add_filter(constraint1=7)
        multifilters.add_filter(constraint3=23)
        constaints = {
            'constraint1' : lambda object,value : object[0]==value,
            'constraint2' : lambda object,value : object[1]==value,
            'constraint3' : lambda object,value : object[2]==value,
            }
        test1 = (8,5,12)
        test2 = (7,12,23)
        test3 = (8,12,12)
        self.assertEqual(multifilters.check_filters(test1,constaints),True)
        self.assertEqual(multifilters.check_filters(test2,constaints),True)
        self.assertEqual(multifilters.check_filters(test3,constaints),False)

    def test_doc_2(self) :
        multifilters = MultiFilters()
        multifilters.add_filter(constraint1=8,constraint2=5)
        multifilters.define_new_set()
        multifilters.add_filter(constraint1=7,constraint3=23)
        constaints = {
            'constraint1' : lambda object,value : object[0]==value,
            'constraint2' : lambda object,value : object[1]==value,
            'constraint3' : lambda object,value : object[2]==value,
            }
        test1 = (8,5,12)
        test2 = (7,12,23)
        test3 = (8,12,12)
        self.assertEqual(multifilters.check_filters(test1,constaints),True)
        self.assertEqual(multifilters.check_filters(test2,constaints),True)
        self.assertEqual(multifilters.check_filters(test3,constaints),False)


    def test_doc_3(self) :
        multifilters = MultiFilters(constraint1=8,constraint2=5)
        multifilters.define_new_set(constraint1=7,constraint3=23)
        constaints = {
            'constraint1' : lambda object,value : object[0]==value,
            'constraint2' : lambda object,value : object[1]==value,
            'constraint3' : lambda object,value : object[2]==value,
            }
        test1 = (8,5,12)
        test2 = (7,12,23)
        test3 = (8,12,12)
        self.assertEqual(multifilters.check_filters(test1,constaints),True)
        self.assertEqual(multifilters.check_filters(test2,constaints),True)
        self.assertEqual(multifilters.check_filters(test3,constaints),False)
