from django.contrib import admin

from .models import Cent, Dist, Slice
from .models import Pin
from .models import User
from .models import Day
from .models import Cent
from .models import Dist_new
from .models import Slice
from .models import Time


admin.site.register(Dist)
admin.site.register(Pin)
admin.site.register(User)
admin.site.register(Day)
admin.site.register(Cent)
admin.site.register(Dist_new)
admin.site.register(Slice)
admin.site.register(Time)