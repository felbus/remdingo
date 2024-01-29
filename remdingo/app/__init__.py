import logging

from flask import g
from flask import Flask, render_template, request
# from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists, create_database, drop_database
# from flask_session import Session
from flask.logging import create_logger

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object("remdingo.config.config.Config")

    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True

    db.init_app(app)

    log = create_logger(app)

    log.info("Starting Remdingo App")

    from remdingo.app.controllers.dashboard_controller import dashboard_bp

    app.register_blueprint(dashboard_bp)

    @app.cli.command('resetdb')
    def reset_db_command():
        from remdingo.db.models.reminders import Reminders

        if database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
            db.drop_all()
            drop_database(app.config['SQLALCHEMY_DATABASE_URI'])

        if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
            create_database(app.config['SQLALCHEMY_DATABASE_URI'])

        db.create_all()
        print('remdingo postgres schema all done..')

    @app.errorhandler(404)
    def page_not_found(_):
        return render_template("errors/404.html"), 404

    @app.errorhandler(Exception)
    def handle_error(e):
        print(e)
        return render_template(
            "errors/exception.html",
            error=e,
        ), 500

    if not app.debug:
        @app.errorhandler(Exception)
        def handle_error(e):
            print(e)
            return render_template(
                "errors/exception.html",
                error=e,
            ), 500

        @app.teardown_appcontext
        def shutdown_session(exception=None):
            if exception:
                logging.error("DB teardown")
                logging.error(exception)
            db.session.remove()

    return app
