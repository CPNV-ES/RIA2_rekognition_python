from http import HTTPStatus
from flask import Blueprint, request
from flasgger import swag_from
from pypika import MySQLQuery as Query, Table, CustomFunction
from flaskr.constants.AttributeType import AttributeType

generate_api = Blueprint('api', __name__)


@generate_api.route('/sql', methods=['POST'])
async def generate_sql():
    content = request.get_json(silent=True)

    message = ""

    sql_text = ""

    try:
        if (not content):
            raise Exception('No content')
        if (not "bucket_url" in content or not content["bucket_url"]):
            raise Exception(
                r'No bucket url given, try to add "bucket_url": "s3://kfc.kentuky.com/nugget.jpg" ')
        if (not "name" in content or not content["name"]):
            raise Exception(
                r'No name given, try to add "name": "example_1"')
        if (not "hash" in content or not content["hash"]):
            raise Exception(
                r'No hash given, try to add "hash": "5683b32d9da3fe83cef1e284dc210e768d02b7cf"')
        if (not "ip" in content or not content["ip"]):
            raise Exception(r'No ip given, try to add "ip": "8.8.8.8"')
        if (not "created_at" in content or not content["created_at"]):
            raise Exception(
                r'No created_at given, try to add "created_at": "2018-12-25 09:27:53"')

        image = Table('image')
        analysis = Table('analysis')
        object = Table('object')
        attribute = Table('attribute')

        q = Query.into(image).columns('url', 'name', 'hash').insert(
            content["bucket_url"], content["name"], content["hash"])

        sql_text = str(q) + ";"

        sql_text += "SET @IMAGE = LAST_INSERT_ID();"

        ip_sql_function = CustomFunction('INET_ATON', ['ip'])
        apocalypse_now_sql_function = CustomFunction('NOW')

        q = Query.into(analysis).columns('image_id', 'ip', 'created_at', 'updated_at').insert('@IMAGE',
                                                                                              ip_sql_function(content["ip"]), content["created_at"], apocalypse_now_sql_function())
        # workaround to remove default quote wrapper to use @IMAGE variable
        sql_text += str(q).replace("'@IMAGE'", "@IMAGE") + ";"

        sql_text += "SET @ANALYSIS = LAST_INSERT_ID();"

        for analyzed_item in content["analysis_content"]:
            q = Query.into(object).columns('analysis_id', 'name', 'category').insert(
                '@ANALYSIS', 'face_object', 'face')
            sql_text += str(q).replace("'@ANALYSIS'", "@ANALYSIS") + ";"
            sql_text += "SET @OBJECT = LAST_INSERT_ID();"

            for object_key, object_value in analyzed_item.items():

                object_value_type = type(object_value)

                def get_attribute_insert_query(name, type: AttributeType, value):
                    value_array = [None] * 3
                    value_array[type.value] = str(
                        value) if value is not None else None
                    q = Query.into(attribute).columns('object_id', 'name', 'value_type', 'value_string', 'value_number', 'value_boolean').insert(
                        '@OBJECT', name, type.name.lower(), value_array[0], value_array[1], value_array[2])
                    return str(q).replace("'@OBJECT'", "@OBJECT") + ";"

                if (object_value_type is dict):
                    for attribute_key, attribute_value in object_value.items():
                        attribute_value_type = AttributeType.type(
                            type(attribute_value))

                        name = object_key + '.' + attribute_key
                        sql_text += get_attribute_insert_query(
                            name, attribute_value_type, attribute_value)
                elif object_value_type is list:
                    for subobject_key in range(0, len(object_value)):
                        if type(object_value[subobject_key]) is dict:
                            for attribute_key, attribute_value in object_value[subobject_key].items():
                                attribute_value_type = AttributeType.type(
                                    type(attribute_value))

                                name = object_key + '.' + \
                                    str(subobject_key) + \
                                    '.' + attribute_key
                                sql_text += get_attribute_insert_query(
                                    name, attribute_value_type, attribute_value)
                        else:
                            attribute_value_type = AttributeType.type(
                                type(object_value[subobject_key]))

                            name = object_key
                            sql_text += get_attribute_insert_query(
                                name, attribute_value_type, object_value[subobject_key])
                else:

                    attribute_value_type = AttributeType.type(
                        object_value_type)
                    name = object_key
                    sql_text += get_attribute_insert_query(
                        name, attribute_value_type, object_value)
        message = sql_text

    except Exception as e:
        message = str(e)

    return message
