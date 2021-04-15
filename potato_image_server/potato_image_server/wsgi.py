import os
import sys

from django.core.wsgi import get_wsgi_application

sys.path.append('/home/victor/web/potato-image-server')
sys.path.append('/home/victor/coding/web/potato-image-server')
sys.path.append('/home/victor/coding/web/potato-image-server/potato_image_server')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'potato_image_server.settings')

application = get_wsgi_application()
