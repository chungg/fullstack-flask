from flask_migrate import Migrate
from flask_security import Security
from flask_wtf import CSRFProtect


migrate = Migrate()
security = Security()
csrf = CSRFProtect()
