# Load API

import oswald
from loguru import logger
from waitress import serve


oswald_load = oswald.Oswald("endpoints")

api = oswald_load.api

serve(api)