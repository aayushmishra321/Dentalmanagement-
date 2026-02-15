# PyMySQL import removed - using SQLite3 for deployment
# import pymysql 
# pymysql.install_as_MySQLdb()

# Celery initialization
from .celery import app as celery_app

__all__ = ('celery_app',)