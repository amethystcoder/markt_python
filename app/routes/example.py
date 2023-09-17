from flask_smorest import Blueprint
from flask.views import MethodView

from app.schemas import ExampleSchema  # Import the ExampleSchema

example_blp = Blueprint("Example", "example", description="Example Endpoint")


@example_blp.route("/example")
class ExampleResource(MethodView):
    @example_blp.response(200, ExampleSchema)
    def get(self):
        """
        Get an example response.

        Returns:
            dict: Example response data.
        """
        return {"message": "This is an example endpoint response"}
