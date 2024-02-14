from flask_restful import reqparse

feed_req_parser = reqparse.RequestParser()
feed_req_parser.add_argument(
    'page',
    type=int,
    location=['Args', 'headers'],
    required=False
)