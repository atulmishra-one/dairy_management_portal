import xlrd

from app.services.extension import task_server, sqlalchemy as db
from app.models.core.user import User
from app.application import initialize_app

try:
    from app.config.production import ProductionConfig as config_object
except ImportError:
    from app.config.local import LocalConfig as config_object


@task_server.task()
def upload_users(file_object):
    
    workbook = xlrd.open_workbook(file_object)
    worksheet = workbook.sheet_by_index(0)
        
    offset = 0
    rows = []
    for i, row in enumerate(range(worksheet.nrows)):
        if i <= offset:  # (Optionally) skip headers
            continue
        r = []
        for j, col in enumerate(range(worksheet.ncols)):
            r.append(worksheet.cell_value(i, j))
        rows.append(r)
    
    users = []
    for i, row in enumerate(rows):
        users.append({
            'initial_name': row[0],
            'first_name': row[1],
            'last_name': row[2],
            'username': row[3],
            'email': row[4],
            'password': row[5],
            'active': row[6]
        })
    
    app = initialize_app(config_object)
    with app.test_request_context():
        user_object = User()
        user_object.create_or_update(users)
        
    return "OK."