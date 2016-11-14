"""
In ussd airflow ussd customer journey is created and defined by
yaml

Each section in yaml is a ussd screen. Each section must have an
key of value pair of screen_type: screen_type

The screen type defines the logic and how the screen is going to be
rendered.

The following are the  supported screen types:

"""

from ussd.core import UssdHandlerAbstract, UssdResponse
import datetime


class InputScreen(UssdHandlerAbstract):
    """

    **Input Screen**

    This screen prompts the user to enter an input

    Fields required:
        - text: this the text to display to the user.
        - input_identifier: input amount entered by users will be saved
                            with this key. To access this in the input
                            anywhere {{ input_identifier }}
        - next_handler: The next screen to go after the user enters
                        input
        - validators:
            - error_message: This is the message to display when the validation fails
              regex: regex used to validate ussd input. Its mutually exclusive with expression
            - expression: if regex is not enough you can use a jinja expression will be called ussd request object
              error_message: This the message thats going to be displayed if expression returns False

    Example:
        .. literalinclude:: ../../ussd/tests/sample_screen_definition/valid_input_screen_conf.yml
    """

    screen_type = "input_screen"

    @staticmethod
    def validate_schema(ussd_content):
        pass

    def handle(self):
        if not self.ussd_request.input:
            response_text = self.get_text()
            ussd_screen = dict(
                name=self.handler,
                start=datetime.datetime.now(),
                screen_text=response_text
            )
            self.ussd_request.session['steps'].append(ussd_screen)

            return UssdResponse(response_text)
        else:
            session_key = self.screen_content['input_identifier']
            next_handler = self.screen_content['next_screen']
            self.ussd_request.session[session_key] = \
                self.ussd_request.input

            self.ussd_request.session['steps'][-1].update(
                end=datetime.datetime.now(),
                selection=self.ussd_request.input
            )
            return self.ussd_request.forward(next_handler)
