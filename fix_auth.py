import re

# Read the file
with open(r'c:\Users\Virakyuth Pc\OneDrive\Desktop\Flask_SQLITE\app\routes\auth_routes.py', 'r') as f:
    content = f.read()

# Replace the incorrect line
content = content.replace(
    'return render_template(url_for("auth/register.html"))',
    'return render_template("auth/register.html")'
)

# Write back
with open(r'c:\Users\Virakyuth Pc\OneDrive\Desktop\Flask_SQLITE\app\routes\auth_routes.py', 'w') as f:
    f.write(content)

print("Fixed!")
