"""Module implements the web ui"""
from __future__ import annotations
from typing import TYPE_CHECKING

import importlib

import base64
import threading
import time
import os
import sys
import uuid
import logging
from flask_bootstrap import Bootstrap5
import flask
import flask_login

from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import Length

from werkzeug.serving import make_server

from carconnectivity_connectors.base.ui.connector_ui import BaseConnectorUI

from carconnectivity_plugins.base.ui.plugin_ui import BasePluginUI
from carconnectivity_plugins.webui.ui.cache import cache
from carconnectivity_plugins.webui.ui.plugins import bp_plugins
from carconnectivity_plugins.webui.ui.connectors import bp_connectors
from carconnectivity_plugins.webui.ui.garage import blueprint as bp_garage


if TYPE_CHECKING:
    from typing import Dict, Optional, Literal
    from types import ModuleType

    from carconnectivity.carconnectivity import CarConnectivity
    from werkzeug.serving import BaseWSGIServer

LOG: logging.Logger = logging.getLogger("carconnectivity.plugins.webui")

csrf = CSRFProtect()


class LoginForm(FlaskForm):
    """
    LoginForm class represents a form for user login.

    Attributes:
        username (StringField): Field for entering the username with a length validator.
        password (PasswordField): Field for entering the password.
        remember_me (BooleanField): Checkbox to remember the user's login session.
        submit (SubmitField): Button to submit the login form.
    """
    username = StringField('User', validators=[Length(min=1, max=255)])
    password = PasswordField('Password')
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Submit')


class WebUI:
    """
    WebUI class for the Car Connectivity application.
    """
    def __init__(self, car_connectivity: CarConnectivity, host: str, port: int, username: Optional[str] = None, password: Optional[str] = None) -> None:
        self.car_connectivity: CarConnectivity = car_connectivity
        self.app = flask.Flask('CarConnectivity', template_folder=os.path.dirname(__file__) + '/templates', static_folder=os.path.dirname(__file__) + '/static')
        self.app.debug = True
        self.app.config.from_mapping(
            SECRET_KEY=uuid.uuid4().hex,
        )
        csrf.init_app(self.app)

        cache.init_app(self.app)

        bootstrap = Bootstrap5(self.app)

        login_manager = flask_login.LoginManager()
        login_manager.login_view = "login"
        login_manager.login_message = "You have to login to see this page"
        login_manager.login_message_category = "info"
        if username is not None and password is not None:
            login_manager.init_app(self.app)

            self.users = {}
            self.users[username] = {'password': password}

        class NoHealth(logging.Filter):
            def filter(self, record):
                return 'GET /healthcheck' not in record.getMessage()

        #  Disable logging for healthcheck
        logging.getLogger("werkzeug").addFilter(NoHealth())

        with self.app.app_context():
            if 'carconnectivity' not in flask.current_app.extensions:
                flask.current_app.extensions['car_connectivity'] = car_connectivity

        self.server: BaseWSGIServer = make_server(host, port, self.app, threaded=True)

        self.plugin_uis: Dict[str, BasePluginUI] = {}
        self.connector_uis: Dict[str, BaseConnectorUI] = {}

        @self.app.context_processor
        def inject_dict_for_all_templates() -> Dict:
            """ Build the navbar and pass this to Jinja for every route
            """
            plugins_sublinks = []
            connectors_sublinks = []
            # Build the Navigation Bar
            nav = [
                {"text": "Garage", "url": flask.url_for('garage.garage')},
                {
                    "text": "Connectors",
                    "sublinks": connectors_sublinks,
                    "url": flask.url_for('connectors.status')
                },
                {
                    "text": "Plugins",
                    "sublinks": plugins_sublinks,
                    "url": flask.url_for('plugins.status')
                },
            ]
            if 'carconnectivity_connectors_uis' in flask.current_app.extensions and flask.current_app.extensions['carconnectivity_connectors_uis'] is not None:
                connector_uis: Dict = flask.current_app.extensions['carconnectivity_connectors_uis']
                for connector_ui in connector_uis.values():
                    connector_nav = [
                        {
                            "text": connector_ui.get_title(),
                            "sublinks": connector_ui.get_nav_items(),
                            "url": flask.url_for('connectors.status')
                        }
                    ]
                    connectors_sublinks.append({"text": "Status", "url": flask.url_for('connectors.status')})
                    connectors_sublinks.append({"divider": True})
                    connectors_sublinks.extend(connector_nav)
            if 'carconnectivity_plugin_uis' in flask.current_app.extensions and flask.current_app.extensions['carconnectivity_plugin_uis'] is not None:
                plugin_uis: Dict = flask.current_app.extensions['carconnectivity_plugin_uis']
                for plugin_ui in plugin_uis.values():
                    plugin_nav = [
                        {
                            "text": plugin_ui.get_title(),
                            "sublinks": plugin_ui.get_nav_items(),
                            "url": flask.url_for('plugins.status')
                        }
                    ]
                    plugins_sublinks.append({"text": "Status", "url": flask.url_for('plugins.status')})
                    plugins_sublinks.append({"divider": True})
                    plugins_sublinks.extend(plugin_nav)
            return dict(navbar=nav)

        @self.app.before_request
        def before_request_callback():
            pass
            # flask.g.versions = dict()
            # flask.g.versions['VWsFriend'] = __vwsfriend_version__
            # flask.g.versions['WeConnect Python Library'] = __weconnect_version__

        @self.app.route('/', methods=['GET'])
        def root():
            return flask.redirect(flask.url_for('garage.garage'))

        @self.app.route('/healthcheck', methods=['GET'])
        def healthcheck() -> Literal['ok', 'unhealthy']:
            if 'car_connectivity' not in flask.current_app.extensions:
                flask.abort(500, "car_connectivity instance not connected")
            car_connectivity: Optional[CarConnectivity] = flask.current_app.extensions['car_connectivity']
            if car_connectivity is not None:
                if car_connectivity.is_healthy():
                    return 'ok'
            return 'unhealthy'

        @self.app.route('/restart', methods=['GET'])
        @flask_login.login_required
        def restart():
            def delayed_restart():
                time.sleep(10)
                python = sys.executable
                os.execl(python, python, * sys.argv)  # nosec

            t = threading.Thread(target=delayed_restart)
            t.start()
            return flask.redirect(flask.url_for('restartrefresh'))

        @self.app.route('/restartrefresh', methods=['GET'])
        def restartrefresh():
            return flask.render_template('restart.html', current_app=flask.current_app)

        @login_manager.user_loader
        def user_loader(username):
            if username not in self.users:
                return

            user = flask_login.UserMixin()
            user.id = username
            return user

        @login_manager.request_loader
        def load_user_from_request(request):
            auth = request.headers.get('Authorization')
            if auth and 'Basic ' in auth:
                auth = auth.replace('Basic ', '', 1)
                try:
                    auth = base64.b64decode(auth).decode("utf-8")
                except TypeError:
                    return None
                if ':' in auth:
                    user_pass = auth.split(":", 1)
                    if user_pass[0] in self.users and 'password' in self.users[user_pass[0]] and user_pass[1] == self.users[user_pass[0]]['password']:
                        user = flask_login.UserMixin()
                        user.id = user_pass[0]
                        return user
            # finally, return None if both methods did not login the user
            return None

        @self.app.route('/login', methods=['GET', 'POST'])
        def login():
            form = LoginForm()

            if form.validate_on_submit():
                username = form.username.data
                if username in self.users and 'password' in self.users[username] and form.password.data == self.users[username]['password']:
                    user = flask_login.UserMixin()
                    user.id = username
                    remember = form.remember_me.data
                    flask_login.login_user(user, remember=remember)

                    next_page = flask.request.args.get('next', default='garage')
                    return flask.redirect(next_page)
                else:
                    form.password.data = ''
                    flask.flash('User unknown or password is wrong', 'danger')

            return flask.render_template('login/login.html', form=form, current_app=self.app)

        @self.app.route("/logout")
        @flask_login.login_required
        def logout():
            flask_login.logout_user()
            return flask.redirect('login')

        @self.app.route('/about', methods=['GET'])
        def about():
            if 'car_connectivity' not in flask.current_app.extensions:
                flask.abort(500, "car_connectivity instance not connected")
            car_connectivity: Optional[CarConnectivity] = flask.current_app.extensions['car_connectivity']
            versions = dict()
            if car_connectivity is not None:
                versions['CarConnectivity'] = car_connectivity.version
                if car_connectivity.connectors is not None and car_connectivity.connectors.enabled:
                    for connector in car_connectivity.connectors.connectors.values():
                        versions[connector.get_type()] = connector.get_version()
                if car_connectivity.plugins is not None and car_connectivity.plugins.enabled:
                    for plugin in car_connectivity.plugins.plugins.values():
                        versions[plugin.get_type()] = plugin.get_version()
            return flask.render_template('about.html', current_app=flask.current_app, versions=versions)

    def load_blueprints(self) -> None:
        """
        Load and register blueprints for plugins and connectors.

        This method iterates over all plugins and connectors in the car connectivity system,
        attempts to import their respective UI modules, and registers their blueprints with
        the Flask application. If a UI module or class is not found, it continues to the next
        plugin or connector.

        Raises:
            ModuleNotFoundError: If the UI module for a plugin or connector is not found.
            AttributeError: If the UI class for a plugin or connector is not found.
        """
        for plugin in self.car_connectivity.plugins.plugins.values():
            parent_name = '.'.join(plugin.__module__.split('.')[:-1])
            try:
                plugin_ui_module: ModuleType = importlib.import_module('.ui.plugin_ui', parent_name)
                plugin_ui_class = getattr(plugin_ui_module, 'PluginUI')
                plugin_ui_instance: BasePluginUI = plugin_ui_class(plugin)
                self.plugin_uis[plugin.get_type()] = plugin_ui_instance
                if plugin_ui_instance.blueprint is not None:
                    bp_plugins.register_blueprint(plugin_ui_instance.blueprint)
            except ModuleNotFoundError:
                continue
            except AttributeError:
                continue
        for connector in self.car_connectivity.connectors.connectors.values():
            parent_name = '.'.join(connector.__module__.split('.')[:-1])
            try:
                conenctor_ui_module: ModuleType = importlib.import_module('.ui.conenctor_ui', parent_name)
                connector_ui_class = getattr(conenctor_ui_module, 'ConnectorUI')
                connector_ui_instance: BaseConnectorUI = connector_ui_class(connector)
                self.connector_uis[connector.get_type()] = connector_ui_instance
                if connector_ui_instance.blueprint is not None:
                    bp_connectors.register_blueprint(connector_ui_instance.blueprint)
            except ModuleNotFoundError:
                continue
            except AttributeError:
                continue
        with self.app.app_context():
            flask.current_app.register_blueprint(bp_plugins)
            flask.current_app.register_blueprint(bp_connectors)
            flask.current_app.register_blueprint(bp_garage)
            flask.current_app.extensions['carconnectivity_plugin_uis'] = self.plugin_uis
            flask.current_app.extensions['carconnectivity_connector_uis'] = self.connector_uis
