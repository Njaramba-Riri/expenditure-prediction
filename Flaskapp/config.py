import os 

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    TWITTER_API_KEY = "xKUXD2Yt4pik6ALkbiLWHVT5c"
    TWITTER_API_SECRET = "S5RENJDqdhDWk0BIhYJzy4uPRaafRk7GtDsSlPurS0oa2TmFlJ"
    FACEBOOK_CLIENT_ID = "215492924842506"
    FACEBOOK_CLIENT_SECRET = "06da42a59c27057d7fc08d32aec87f45"
    GOOGLE_CLIENT_ID = "1025272602399-l3tjk1mj4srctlpuun9vkk2clu2veiiv.apps.googleusercontent.com"
    GOOGLE_CLIENT_SECRET = "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"
    RECAPTCHA_PUBLIC_KEY = "6Ldktp8nAAAAAF-DPrnyjnLQyIElSlfKHICIeeNL"

    @staticmethod
    def init_app(app):
        pass

class ProdConfig(object):
    SECRET_KEY = 'b}Q\xeb\xdb\x16\xd7E\x1a\xcc\xc3\x96\xbc\xbbP]\xb0'

class DevConfig(object):
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'Riri'
    MYSQL_PASSWORD = '$Shadowalker'
    MYSQL_DATABASE = 'MLDB'
    MYSQL_HOST = 3306 
    SECRET_KEY = 'b\xbcN~\xe3Zhw\x19\x18\xdf\x86\xa4@\x05\x0b\xdc'
    DEBUG = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    CACHE_TYPE = 'simple'
    BABEL_TRANSLATION_DIRECTORIES='/desktop/expenditure/flaskapp/webapp/translations'
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://Riri:$Shadowalker1@localhost:3306/dev"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_ECHO = True
    GOOGLE_CLIENT_ID = "282277803958-91kd492opdubeh1oaqohm1bde2bqvb3o.apps.googleusercontent.com"
    GOOGLE_CLIENT_SECRET = "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" 
    GOOGLE_DISCOVERY_URL = 'https://acccounts.google.com/.well-known/openid-configuration'
    FACEBOOK_CLIENT_ID = "215492924842506"
    FACEBOOK_CLIENT_SECRET = "06da42a59c27057d7fc08d32aec87f45"
    TWITTER_API_KEY = "xKUXD2Yt4pik6ALkbiLWHVT5c"
    TWITTER_API_SECRET = "S5RENJDqdhDWk0BIhYJzy4uPRaafRk7GtDsSlPurS0oa2TmFlJ"
    RECAPTCHA_PUBLIC_KEY = "6LdNVKAnAAAAAIgHqZUIphIbyyOg1LAyR_s5Y1FI"
    RECAPTCHA_PRIVATE_KEY = "6LdNVKAnAAAAAF141xe4jFzhdL4e0t0KE_q1nGpA"
    RECAPTCHA_SECRET_KEY = "6LeWlaUnAAAAAMvvOCaUrPpMXDPcAlAwrLv2qs3t"
    RECAPTCHA_SITE_KEY = "6LeWlaUnAAAAAGSb_qHpWBsaYLMOGLW-UtLf9kg8"
    FOURSQUARE_API = "fsq3Sll2608N709M9WHvfWWQSFgKSCgSJVLr1FW3wMHhWJg="
    OAUTHLIB_INSECURE_TRANSPORT = '1'
    OAUTHLIB_RELAX_TOKEN_SCOPE = '1'
    MAIL_DEFAULT_SENDER = 'jamesnjaramba132@gmail.com'
    MAIL_SUBJECT_PREFIX = "Confirm account."
    MAIL_SERVER  ='smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_DEBUG = False
    MAIL_USERNAME = 'jamesnjaramba132@gmail.com'
    MAIL_PASSWORD = 'nyaguthii'
    LETSGO_ADMIN = 'james.letsgo@gmail.com'
    WORKSPACE = "expenditure"
    YOUR_PROJECT_NAME = "Tourist Expenditure Prediction"
    YOUR_PROJECT_DESCRIPTION = "Leveraging the power of ML to uncover the underlying patterns that influence tourist spending."


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')