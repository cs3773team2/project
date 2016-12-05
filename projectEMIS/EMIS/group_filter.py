from django.contrib.auth.decorators import login_required, user_passes_test


def patient(function=None):
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated() and u.groups.filter(name='Patient').exists(),
        login_url='/user_not_auth/'
    )
    return actual_decorator(function)


def doctor(function=None):
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated() and u.groups.filter(name='Doctor').exists(),
        login_url='/user_not_auth/'
    )
    return actual_decorator(function)


def clinical_staff(function=None):
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated() and u.groups.filter(name='Clinical_Staff').exists(),
        login_url='/user_not_auth/'
    )
    return actual_decorator(function)


def nurse(function=None):
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated() and u.groups.filter(name='Nurse').exists(),
        login_url='/user_not_auth/'
    )
    return actual_decorator(function)


def lab(function=None):
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated() and u.groups.filter(name='Lab').exists(),
        login_url='/user_not_auth/'
    )
    return actual_decorator(function)


def pharmacy(function=None):
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated() and u.groups.filter(name='Pharmacy').exists(),
        login_url='/user_not_auth/'
    )
    return actual_decorator(function)


def insurance(function=None):
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated() and u.groups.filter(name='Insurance').exists(),
        login_url='/user_not_auth/'
    )
    return actual_decorator(function)