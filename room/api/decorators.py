from rest_framework.response import Response


def role_required(allowed_roles=[]):
    def decorator(func):
        def validate_role(request, *args, **kwargs):
            if request.user.role in allowed_roles:
                return func(request, *args, **kwargs)
            else:
                return Response({
                    'response': 'You Cannot Perform This Action - Only Room Manager Can Do That',
                })
        return validate_role
    return decorator


def validate_room_manager(func):
    def wrapper(request, *args, **kwargs):
        if request.user.role == 1:
            return func(request, *args, **kwargs)
        else:
            return Response({
                'response': 'You Cannot Perform This Action - Only Room Manager Can Do That',
            })
    return wrapper
