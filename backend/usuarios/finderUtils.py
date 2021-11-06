from .models import Case


def query_all_avaible():
    querySet = Case.objects.filter(status= 'D')
    return querySet

def query_by_status(status):
    querySet = Case.objects.filter(status=status)
    return querySet

def query_by_type(type):
    querySet = Case.objects.filter(type_status=type).filter(status='D')
    return querySet

def query_by_type_status(type,status):
    querySet = Case.objects.filter(type_status=type).filter(status=status)
    return querySet