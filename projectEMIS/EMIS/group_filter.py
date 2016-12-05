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