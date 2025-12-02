from app import create_app
from app.services.user_service import UserService
from app.models.user import User

app = create_app()
client = app.test_client()
with app.app_context():
    print('DB URI:', app.config['SQLALCHEMY_DATABASE_URI'])
    users_before = UserService.get_all()
    print('Before users:', len(users_before))

# GET form and pick csrf
resp = client.get('/users/create')
html = resp.data.decode('utf-8')
import re
m = re.search(r'name="csrf_token" type="hidden" value="([^"]+)"', html)
csrf = m.group(1) if m else None
print('csrf token found:', csrf is not None)

# Post a new user
post_resp = client.post('/users/create', data={
    'username': 'testuser-0',
    'email': 'testuser-0@example.com',
    'full_name': 'Test User 0',
    'is_active': 'y',
    'password': 'Aa!11111x',
    'confirm_password': 'Aa!11111x',
    'csrf_token': csrf,
}, follow_redirects=True)
print('POST status code:', post_resp.status_code)

with app.app_context():
    users_after = UserService.get_all()
    print('After users:', len(users_after))
    if users_after:
        u = users_after[0]
        print('Most recent:', u.id, u.username, u.email, u.full_name, u.is_active)
