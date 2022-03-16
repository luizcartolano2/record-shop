""" Docstring for the views.py module.

"""
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from rest_framework.decorators import api_view
from .models import Disc, User, Request


@api_view(['POST'])
def create_disc(request):
    """
    Function to create a new disc.

    :param request: An object representing the request made.
    :return: An http response informing request result.
    """
    if request.method == 'POST':
        request = request.data
        try:
            obj = Disc(name=request['name'],
                       artist=request['artist'],
                       release_year=request['release_year'],
                       style=request['style'],
                       amount=int(request['amount']))
        except:
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

    :param request: An object representing the request made.
    :return: An http response informing request result.
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

    :param request: An object representing the request made.
    :param id_: The object identifier.
    :return: An http response informing request result.
    """
    try:
        Disc.objects.filter(id=id_).delete()
        return HttpResponse('Disc deleted.', status=200)
    except:
        return HttpResponse('Fail to delete disc.', status=500)


@api_view(['PUT'])
def put_disc(request, id_):
    """
    Method to update a total disc object.

    :param request: An object representing the request made.
    :param id_: The object identifier.
    :return: An http response informing request result.
    """
    request = request.data
    try:
        # make sure no other thread will update same object
        obj = Disc.objects.get(id=id_)
    except:
        return HttpResponse('Disc does not exist on DB.', status=400)

    try:
        obj.name = request['name']
        obj.artist = request['artist']
        obj.release_year = request['release_year']
        obj.style = request['style']
        obj.save()
        obj.add_disc(amount=int(request['amount']))
    except:
        return HttpResponse('Problem updating object.', status=500)

    return HttpResponse('Update completed.', status=200)


@api_view(['POST'])
def create_client(request):
    """
    Function to create a new client.

    :param request: An object representing the request made.
    :return: An http response informing request result.
    """
    request = request.data
    # get the subscription moment
    time_now = timezone.now()
    try:
        # creates an default User object
        user = User(
            name=request['name'],
            email=request['email'],
            is_staff=False,
            is_superuser=False,
            is_active=True,
            date_joined=time_now,
            phone_number=request['phone_number'],
            identity=request['identity'],
            birth_day=request['birth_day']
        )
        user.set_password(request['password'])
        user.save()

        return HttpResponse('User created.', status=201)
    except:
        return HttpResponse('Fail to create user.', status=400)


@api_view(['GET'])
def get_clients(request):
    """
    Function to get the users from database.

    :param request: An object representing the request made.
    :return: An http response informing request result.
    """
    filters = request.data
    try:
        data = list(User.objects.filter(**filters).values())
        return JsonResponse(data, safe=False)
    except:
        return JsonResponse({}, safe=False)


@api_view(['PUT'])
def put_client(request, id_):
    """
    Function to update a client.

    :param request: An object representing the request made.
    :param id_: The object identifier.
    :return: An http response informing request result.
    """
    request = request.data
    try:
        # make sure no other thread will update same object
        obj = User.objects.get(id=id_)
    except:
        return HttpResponse('User does not exist on DB.', status=400)

    try:
        obj.name = request['name']
        obj.phone_number = request['phone_number']
        obj.birth_day = request['birth_day']
        obj.save()
    except:
        return HttpResponse('Problem updating object.', status=500)

    return HttpResponse('Update completed.', status=200)


@api_view(['DELETE'])
def delete_client(request, id_):
    """
    Function to delete a client (set as inactive).

    :param request: An object representing the request made.
    :param id_: The object identifier.
    :return: An http response informing request result.
    """
    try:
        # make sure no other thread will update same object
        obj = User.objects.get(id=id_)
        obj.is_active = False
        obj.save()

        return HttpResponse('User deleted.', status=200)
    except:
        return HttpResponse('User does not exist on DB.', status=400)


@api_view(['POST'])
def create_request(request):
    """
    Function to create a new request in database.

    :param request: An object representing the request made.
    :return: An http response informing request result.
    """
    request = request.data

    try:
        client_id = request['client']
        # get the client object
        client_obj = User.objects.get(id=client_id)
    except:
        return HttpResponse('Client does not exist on DB.', status=400)

    # we check if user is active, otherwise he can't make a request
    if not client_obj.is_active:
        return HttpResponse('Client is inactive and cant make a request.', status=401)

    try:
        # get id of disc and client
        disc_id = request['disc']
        # get the disc object
        disc_obj = Disc.objects.get(id=disc_id)
    except:
        return HttpResponse('Disc does not exist on DB.', status=400)

    # check if the amount requested is valid
    try:
        amount_requested = request['amount']
        disc_obj.remove_disc(amount=amount_requested)
    except:
        return HttpResponse('The amounted requested is more than the amount available.',
                            status=401)

    # if we got here user is active and the amount of disc's requested is valid
    try:
        request_obj = Request(client=client_obj,
                              Disc=disc_obj,
                              amount=amount_requested)
        request_obj.save()

        return HttpResponse('Request created.', status=201)
    except:
        return HttpResponse('Could not create request object.', status=500)


@api_view(['GET'])
def get_requests(request):
    """
    Function to retrieve the requests from database.

    :param request: An object representing the request made.
    :return:
    """
    filters = request.data
    try:
        data = list(Request.objects.filter(**filters).values())
        return JsonResponse(data, safe=False)
    except:
        return JsonResponse({}, safe=False)
