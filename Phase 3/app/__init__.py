from flask import Flask
from config import Config
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config.from_object(Config)

# leave the following import at the bottom of this file

from app import routes, managerRoutes, holidayRoutes, stateVolumeRoutes, manufacturerRoutes, \
    homeRoute, assignmentsRoute, populationRoute, store_revenue
