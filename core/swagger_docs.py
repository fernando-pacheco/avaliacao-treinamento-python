from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec


def config_swagger(app):
    spec = APISpec(
        title='Sample Project - APIs Documentation',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    )

    app.config.update({
        'APISPEC_SPEC': spec,
        'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON
        'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'  # URI to access UI of API Doc
    })
    return FlaskApiSpec(app)