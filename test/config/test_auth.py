from config.auth import AuthConfig


class TestAuthConfig(object):
    def test_default_secret_key(self):
        """
        Checks if the default SECRET_KEY is correct
        """
        assert AuthConfig.SECRET_KEY == 'dev_secret_key'

    def test_default_jwt_secret_key(self):
        """
        Checks if the default JWT_SECRET_KEY is correct
        """
        assert AuthConfig.JWT_SECRET_KEY == 'dev_jwt_secret_key'
