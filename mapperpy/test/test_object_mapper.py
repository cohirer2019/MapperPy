import unittest
from assertpy import assert_that

from mapperpy.test.common_test_classes import *

from mapperpy import ObjectMapper, MapperOptions

__author__ = 'lgrech'

# validation whether implicit mapping works
# test exception messages


class ObjectMapperTest(unittest.TestCase):

    def test_map_empty_to_empty(self):
        assert_that(ObjectMapper(TestEmptyClass1, TestEmptyClass2).map(TestEmptyClass1())).\
            is_instance_of(TestEmptyClass2)
        assert_that(ObjectMapper(TestEmptyClass1, TestEmptyClass2).map(TestEmptyClass2())).\
            is_instance_of(TestEmptyClass1)

    def test_map_unknown_class_should_raise_exception(self):
        try:
            ObjectMapper(TestEmptyClass1, TestEmptyClass2).map(TestOtherClass())
            self.fail("Should raise ValueError")
        except ValueError as er:
            assert_that(er.message).contains(TestOtherClass.__name__)

    def test_map_one_explicit_property(self):
        # given
        mapper = ObjectMapper(TestClassSomeProperty1, TestClassMappedProperty).custom_mappings(
            {"some_property": "mapped_property"})

        # when
        mapped_object = mapper.map(TestClassSomeProperty1(some_property="some_value"))

        # then
        assert_that(mapped_object).is_instance_of(TestClassMappedProperty)
        assert_that(mapped_object.mapped_property).is_equal_to("some_value")

        # when
        mapped_object_rev = mapper.map(TestClassMappedProperty(mapped_property="other_value"))

        # then
        assert_that(mapped_object_rev).is_instance_of(TestClassSomeProperty1)
        assert_that(mapped_object_rev.some_property).is_equal_to("other_value")

    def test_map_unknown_property_should_raise_exception(self):
        # given
        mapper = ObjectMapper(TestClassSomeProperty1, TestClassMappedProperty).custom_mappings(
            {"some_property": "unknown"})

        # when
        try:
            mapper.map(TestClassSomeProperty1(some_property="some_value"))
            self.fail("Should raise AttributeError")
        except AttributeError as er:
            # then
            assert_that(er.message).contains("unknown")

        # given
        mapper = ObjectMapper(TestClassSomeProperty1, TestClassMappedProperty).custom_mappings(
            {"unknown": "mapped_property"})

        # when
        try:
            mapper.map(TestClassSomeProperty1(some_property="some_value"))
            self.fail("Should raise AttributeError")
        except AttributeError as er:
            # then
            assert_that(er.message).contains("unknown")

    def test_map_multiple_explicit_properties(self):
        # given
        mapper = ObjectMapper(TestClassSomeProperty1, TestClassMappedProperty).custom_mappings(
                            {"some_property": "mapped_property",
                             "some_property_02": "mapped_property_02",
                             "some_property_03": "mapped_property_03"})

        # when
        mapped_object = mapper.map(TestClassSomeProperty1(
            some_property="some_value",
            some_property_02="some_value_02",
            some_property_03="some_value_03",
            unmapped_property1="unmapped_value"))

        # then
        assert_that(mapped_object).is_instance_of(TestClassMappedProperty)
        assert_that(mapped_object.mapped_property).is_equal_to("some_value")
        assert_that(mapped_object.mapped_property_02).is_equal_to("some_value_02")
        assert_that(mapped_object.mapped_property_03).is_equal_to("some_value_03")
        assert_that(mapped_object.unmapped_property2).is_none()

        # when
        mapped_object_rev = mapper.map(TestClassMappedProperty(
            mapped_property="other_value",
            mapped_property_02="other_value_02",
            mapped_property_03="other_value_03",
            unmapped_property2="unmapped_value"))

        # then
        assert_that(mapped_object_rev).is_instance_of(TestClassSomeProperty1)
        assert_that(mapped_object_rev.some_property).is_equal_to("other_value")
        assert_that(mapped_object_rev.some_property_02).is_equal_to("other_value_02")
        assert_that(mapped_object_rev.some_property_03).is_equal_to("other_value_03")
        assert_that(mapped_object_rev.unmapped_property1).is_none()

    def test_map_multiple_properties_implicit(self):
        # given
        mapper = ObjectMapper.from_class(TestClassSomePropertyEmptyInit1, TestClassSomePropertyEmptyInit2)

        # when
        mapped_object = mapper.map(TestClassSomePropertyEmptyInit1(
            some_property="some_value",
            some_property_02="some_value_02",
            some_property_03="some_value_03",
            unmapped_property1="unmapped_value"))

        # then
        assert_that(mapped_object).is_instance_of(TestClassSomePropertyEmptyInit2)
        assert_that(mapped_object.some_property).is_equal_to("some_value")
        assert_that(mapped_object.some_property_02).is_equal_to("some_value_02")
        assert_that(mapped_object.some_property_03).is_equal_to("some_value_03")
        assert_that(mapped_object.unmapped_property2).is_none()

        # when
        mapped_object_rev = mapper.map(TestClassSomePropertyEmptyInit2(
            some_property="some_value",
            some_property_02="some_value_02",
            some_property_03="some_value_03",
            unmapped_property2="unmapped_value"))

        # then
        assert_that(mapped_object_rev).is_instance_of(TestClassSomePropertyEmptyInit1)
        assert_that(mapped_object_rev.some_property).is_equal_to("some_value")
        assert_that(mapped_object_rev.some_property_02).is_equal_to("some_value_02")
        assert_that(mapped_object_rev.some_property_03).is_equal_to("some_value_03")
        assert_that(mapped_object_rev.unmapped_property1).is_none()

    def test_map_implicit_with_prototype_obj(self):
        # given
        mapper = ObjectMapper(TestClassSomeProperty1, TestClassSomeProperty2,
                            left_prototype_obj=TestClassSomeProperty1(None),
                            right_prototype_obj=TestClassSomeProperty2(None))

        # when
        mapped_object = mapper.map(TestClassSomeProperty1(
            some_property="some_value",
            some_property_02="some_value_02",
            some_property_03="some_value_03",
            unmapped_property1="unmapped_value"))

        # then
        assert_that(mapped_object).is_instance_of(TestClassSomeProperty2)
        assert_that(mapped_object.some_property).is_equal_to("some_value")
        assert_that(mapped_object.some_property_02).is_equal_to("some_value_02")
        assert_that(mapped_object.some_property_03).is_equal_to("some_value_03")
        assert_that(mapped_object.unmapped_property2).is_none()

        # when
        mapped_object_rev = mapper.map(TestClassSomeProperty2(
            some_property="some_value",
            some_property_02="some_value_02",
            some_property_03="some_value_03",
            unmapped_property2="unmapped_value"))

        # then
        assert_that(mapped_object_rev).is_instance_of(TestClassSomeProperty1)
        assert_that(mapped_object_rev.some_property).is_equal_to("some_value")
        assert_that(mapped_object_rev.some_property_02).is_equal_to("some_value_02")
        assert_that(mapped_object_rev.some_property_03).is_equal_to("some_value_03")
        assert_that(mapped_object_rev.unmapped_property1).is_none()

    def test_map_override_implicit_mapping(self):
        # given
        mapper = ObjectMapper(TestClassSomePropertyEmptyInit1, TestClassSomePropertyEmptyInit2).custom_mappings(
                            {"some_property_02": "some_property_03",
                             "some_property_03": "some_property_02"})

        # when
        mapped_object = mapper.map(TestClassSomePropertyEmptyInit1(
            some_property="some_value",
            some_property_02="some_value_02",
            some_property_03="some_value_03",
            unmapped_property1="unmapped_value"))

        # then
        assert_that(mapped_object).is_instance_of(TestClassSomePropertyEmptyInit2)
        assert_that(mapped_object.some_property).is_equal_to("some_value")
        assert_that(mapped_object.some_property_02).is_equal_to("some_value_03")
        assert_that(mapped_object.some_property_03).is_equal_to("some_value_02")
        assert_that(mapped_object.unmapped_property2).is_none()

        # when
        mapped_object_rev = mapper.map(TestClassSomePropertyEmptyInit2(
            some_property="some_value",
            some_property_02="some_value_02",
            some_property_03="some_value_03",
            unmapped_property2="unmapped_value"))

        # then
        assert_that(mapped_object_rev).is_instance_of(TestClassSomePropertyEmptyInit1)
        assert_that(mapped_object_rev.some_property).is_equal_to("some_value")
        assert_that(mapped_object_rev.some_property_02).is_equal_to("some_value_03")
        assert_that(mapped_object_rev.some_property_03).is_equal_to("some_value_02")
        assert_that(mapped_object_rev.unmapped_property1).is_none()

    def test_map_with_nested_explicit_mapper(self):
        # given
        root_mapper = ObjectMapper(TestClassSomeProperty1, TestClassSomeProperty2,
                                 left_prototype_obj=TestClassSomeProperty1(None),
                                 right_prototype_obj=TestClassSomeProperty2(None))

        root_mapper.nested_mapper(ObjectMapper(TestClassSomePropertyEmptyInit1, TestClassSomePropertyEmptyInit2))

        # when
        mapped_object = root_mapper.map(TestClassSomeProperty1(
            some_property="some_value",
            some_property_02=TestClassSomePropertyEmptyInit1(
                some_property="nested_value",
                some_property_02="nested_value_02",
                some_property_03="nested_value_03",
                unmapped_property1="unmapped_nested_value"),
            some_property_03="some_value_03",
            unmapped_property1="unmapped_value"))

        # then
        assert_that(mapped_object).is_instance_of(TestClassSomeProperty2)
        assert_that(mapped_object.some_property).is_equal_to("some_value")
        assert_that(mapped_object.some_property_03).is_equal_to("some_value_03")
        assert_that(mapped_object.unmapped_property2).is_none()

        nested_mapped_obj = mapped_object.some_property_02
        assert_that(nested_mapped_obj).is_instance_of(TestClassSomePropertyEmptyInit2)
        assert_that(nested_mapped_obj.some_property).is_equal_to("nested_value")
        assert_that(nested_mapped_obj.some_property_02).is_equal_to("nested_value_02")
        assert_that(nested_mapped_obj.some_property_03).is_equal_to("nested_value_03")
        assert_that(nested_mapped_obj.unmapped_property2).is_none()

        # when
        mapped_object_rev = root_mapper.map(TestClassSomeProperty2(
            some_property="some_value",
            some_property_02=TestClassSomePropertyEmptyInit2(
                some_property="nested_value",
                some_property_02="nested_value_02",
                some_property_03="nested_value_03",
                unmapped_property2="unmapped_nested_value"),
            some_property_03="some_value_03",
            unmapped_property2="unmapped_value"))

        # then
        assert_that(mapped_object_rev).is_instance_of(TestClassSomeProperty1)
        assert_that(mapped_object_rev.some_property).is_equal_to("some_value")
        assert_that(mapped_object_rev.some_property_03).is_equal_to("some_value_03")
        assert_that(mapped_object_rev.unmapped_property1).is_none()

        nested_mapped_obj_rev = mapped_object_rev.some_property_02
        assert_that(nested_mapped_obj_rev).is_instance_of(TestClassSomePropertyEmptyInit1)
        assert_that(nested_mapped_obj_rev.some_property).is_equal_to("nested_value")
        assert_that(nested_mapped_obj_rev.some_property_02).is_equal_to("nested_value_02")
        assert_that(nested_mapped_obj_rev.some_property_03).is_equal_to("nested_value_03")
        assert_that(nested_mapped_obj_rev.unmapped_property1).is_none()

    def test_suppress_implicit_mapping(self):
        # given
        mapper = ObjectMapper(TestClassSomePropertyEmptyInit1, TestClassSomePropertyEmptyInit2).custom_mappings(
            {"some_property": None})

        # when
        mapped_object = mapper.map(TestClassSomePropertyEmptyInit1(
            some_property="some_value", some_property_02="some_value_02"))

        # then
        assert_that(mapped_object).is_instance_of(TestClassSomePropertyEmptyInit2)
        assert_that(mapped_object.some_property).is_none()
        assert_that(mapped_object.some_property_02).is_equal_to("some_value_02")

        # when
        mapped_object_rev = mapper.map(TestClassSomePropertyEmptyInit2(
            some_property="some_value",
            some_property_02="some_value_02"))

        # then
        assert_that(mapped_object_rev).is_instance_of(TestClassSomePropertyEmptyInit1)
        assert_that(mapped_object_rev.some_property).is_none()
        assert_that(mapped_object_rev.some_property_02).is_equal_to("some_value_02")

    def test_map_with_custom_left_initializers(self):
        # given
        mapper = ObjectMapper(TestClassSomePropertyEmptyInit1, TestClassMappedPropertyEmptyInit).left_initializers(
            {
                "some_property": lambda obj: obj.mapped_property + obj.mapped_property_02,
                "unmapped_property1": lambda obj: "prefix_{}".format(obj.unmapped_property2)})

        # when
        mapped_object = mapper.map(TestClassMappedPropertyEmptyInit(
            mapped_property="mapped_value", mapped_property_02="mapped_value_02", unmapped_property2="unmapped_value"))

        assert_that(mapped_object).is_instance_of(TestClassSomePropertyEmptyInit1)
        assert_that(mapped_object.some_property).is_equal_to("mapped_valuemapped_value_02")
        assert_that(mapped_object.unmapped_property1).is_equal_to("prefix_unmapped_value")

    def test_map_with_custom_right_initializers(self):
        # given
        mapper = ObjectMapper(TestClassSomePropertyEmptyInit1, TestClassMappedPropertyEmptyInit).right_initializers(
            {
                "mapped_property": lambda obj: obj.some_property + obj.some_property_02,
                "unmapped_property2": lambda obj: "prefix_{}".format(obj.unmapped_property1)})

        # when
        mapped_object = mapper.map(TestClassSomePropertyEmptyInit1(
            some_property="some_value", some_property_02="some_value_02", unmapped_property1="unmapped_value"))

        assert_that(mapped_object).is_instance_of(TestClassMappedPropertyEmptyInit)
        assert_that(mapped_object.mapped_property).is_equal_to("some_valuesome_value_02")
        assert_that(mapped_object.unmapped_property2).is_equal_to("prefix_unmapped_value")

    def test_map_with_option_fail_on_get_attr(self):
        # given
        mapper = ObjectMapper(TestClassSomeProperty1, TestEmptyClass1).custom_mappings(
            {"some_property": "non_existing_property"}).options(MapperOptions.fail_on_get_attr == False)

        # when
        mapped_object = mapper.map(TestEmptyClass1())

        # then
        assert_that(mapped_object).is_instance_of(TestClassSomeProperty1)
        assert_that(mapped_object.some_property).is_none()

        # given
        mapper_rev = ObjectMapper(TestEmptyClass1, TestClassSomeProperty1).custom_mappings(
            {"non_existing_property": "some_property"}).options(MapperOptions.fail_on_get_attr == False)

        # when
        mapped_object_rev = mapper_rev.map(TestEmptyClass1())

        # then
        assert_that(mapped_object_rev).is_instance_of(TestClassSomeProperty1)
        assert_that(mapped_object_rev.some_property).is_none()

        # given
        mapper_strict = ObjectMapper(TestClassSomeProperty1, TestEmptyClass1).custom_mappings(
            {"some_property": "non_existing_property"}).options(MapperOptions.fail_on_get_attr == True)

        try:
            # when
            mapper_strict.map(TestEmptyClass1())
            self.fail("Should raise AttributeError")
        except AttributeError as er:
            assert_that(er.message).contains("non_existing_property")

    def test_map_attr_name_for_empty_classes_should_raise_exception(self):
        # given
        mapper = ObjectMapper(TestEmptyClass1, TestEmptyClass1)

        with self.assertRaises(ValueError) as context:
            # when
            mapper.map_attr_name("unmapped_property")

        # then
        assert_that(context.exception.message).contains("unmapped_property")

    def test_map_attr_name_for_unmapped_explicit_property_should_raise_exception(self):
        # given
        mapper = ObjectMapper(TestClassSomeProperty1, TestClassMappedProperty).custom_mappings(
            {"some_property": "mapped_property"})

        with self.assertRaises(ValueError) as context:
            # when
            mapper.map_attr_name("unmapped_property")

        # then
        assert_that(context.exception.message).contains("unmapped_property")

    def test_map_attr_name_for_explicit_mapping(self):
        # given
        mapper = ObjectMapper(TestClassSomeProperty1, TestClassMappedProperty).custom_mappings(
            {"some_property": "mapped_property"})

        # then
        assert_that(mapper.map_attr_name("some_property")).is_equal_to("mapped_property")

        # then
        assert_that(mapper.map_attr_name("mapped_property")).is_equal_to("some_property")

    def test_map_attr_name_for_implicit_mapping(self):
        # given
        mapper = ObjectMapper(TestClassSomePropertyEmptyInit1, TestClassSomePropertyEmptyInit2)

        # then
        assert_that(mapper.map_attr_name("some_property")).is_equal_to("some_property")
        assert_that(mapper.map_attr_name("some_property_02")).is_equal_to("some_property_02")
        assert_that(mapper.map_attr_name("some_property_03")).is_equal_to("some_property_03")

        with self.assertRaises(ValueError) as context:
            # when
            mapper.map_attr_name("unmapped_property1")

        # then
        assert_that(context.exception.message).contains("unmapped_property1")

        with self.assertRaises(ValueError) as context:
            # when
            mapper.map_attr_name("unmapped_property2")

        # then
        assert_that(context.exception.message).contains("unmapped_property2")