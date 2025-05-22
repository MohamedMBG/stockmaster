from django.contrib.auth.decorators import user_passes_test

def admin_required(function):
    """
    Decorator for views that checks if the user is an admin.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and u.is_admin(),
    )
    return actual_decorator(function)

def supervisor_required(function):
    """
    Decorator for views that checks if the user is a supervisor or admin.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and (u.is_supervisor() or u.is_admin()),
    )
    return actual_decorator(function)

def client_required(function):
    """
    Decorator for views that checks if the user is a client.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and u.is_client(),
    )
    return actual_decorator(function)
