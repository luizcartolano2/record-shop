""" Docstring for the views.py module.

"""
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from .models import Disc


@api_view(['POST'])
def create_disc(request):
    """
    Function to create a new disc.
    """
    if request.method == 'POST':
        request = request.data
        try:
            obj = Disc(name=request['name'],
                       artist=request['artist'],
                       release_year=request['release_year'],
                       style=request['style'],
                       amount=int(request['amount']))
        except Exception as e:
            print(e)
            return HttpResponse('JSON with bad format.', status=400)

        try:
            obj.save()
        except:
            return HttpResponse('Fail to create object.', status=500)

        return HttpResponse("New disc created.", status=201)


@api_view(['GET'])
def get_disc(request):
    """
    Function to get a new disc.
    """
    filters = request.data
    try:
        data = list(Disc.objects.filter(**filters).values())
        return JsonResponse(data, safe=False)
    except:
        return JsonResponse({}, safe=False)


@api_view(['DELETE'])
def delete_disc(request, id_):
    """
    Function to delete a disc.
    """
    try:
        Disc.objects.filter(id=id_).delete()
        return HttpResponse('Disc deleted.', status=200)
    except:
        return HttpResponse('Fail to delete disc.', status=500)
