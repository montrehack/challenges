__author__ = 'Gabriel Tremblay - initnull@gmail.com'

def get_cosmetic_url(request):
    return request.protocol + "://" + request.host

