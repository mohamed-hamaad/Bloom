import os
import sys
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Bloom.settings')

application = get_wsgi_application()

# 🚀 الحيلة السحرية: تشغيل الـ Migrations أوتوماتيك أول ما السيرفر يشتغل
try:
    from django.core.management import call_command
    print("Running live migrations to Neon...")
    call_command('migrate', interactive=False)
    print("Migrations completed successfully!")
except Exception as e:
    print(sys.stderr, f"Migration failed: {e}")
