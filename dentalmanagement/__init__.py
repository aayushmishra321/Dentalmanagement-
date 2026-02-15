# PyMySQL import removed - using SQLite3 for deployment
# import pymysql 
# pymysql.install_as_MySQLdb()

# Celery initialization - optional
try:
    from .celery import app as celery_app
    __all__ = ('celery_app',)
except ImportError:
    # Celery not available, continue without it
    celery_app = None
    __all__ = ()
