from rest_framework.response import Response


def role_required(allowed_roles=[]):
    def decorator(func):
        def validate_role(request, *args, **kwargs):
            if request.user.role in allowed_roles:
                return func(request, *args, **kwargs)
            else:
                return Response({
                    'response': 'You Cannot Perform This Action - Only Customer Manager Can Do That',
                })
        return validate_role
    return decorator


def validate_customer_manager(func):
    def wrapper(request, *args, **kwargs):
        if request.user.role == 3:
            return func(request, *args, **kwargs)
        else:
            return Response({
                'response': 'You Cannot Perform This Action - Only Customer Manager Can Do That',
            })
    return wrapper


def validate_user_hotel(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_superuser:
            return func(request, *args, **kwargs)
        else:
            return Response({
                'response': 'You Cannot Perform This Action - Only Users Related To This Hotel Can',
            })
    return wrapper
