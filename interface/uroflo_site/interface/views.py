from django.http import JsonResponse
import random
from scale_class import Scale

# define scale
scale = Scale(pd_sck_pin=2, dout_pin=3)


def get_hematuria(request):

    # replace value with the code needed to read the hematuria sensor
    # and get the percentage

    value = random.randint(0, 100) # re
    return JsonResponse({'value': value})


def get_saline_weight(request):

    weight = scale.read_weight()
    volume = weight / (1009)
    volume = round(volume, 1)
    percentage = int((volume/3)*100) # assuming 3 L bag

    return JsonResponse({'volume': volume, 'percentage': percentage})



