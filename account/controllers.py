from django.contrib.auth import get_user_model, authenticate
from django.shortcuts import get_object_or_404
from ninja import Router

from account.authorization import GlobalAuth, get_tokens_for_user
from account.schemas import AccountCreate, AuthOut, SigninSchema, AccountOut, AccountUpdate, ChangePasswordSchema
from config.utils.schemas import MessageOut

User = get_user_model()

account_controller = Router(tags=['auth'])


@account_controller.post('signup', response={
    400: MessageOut,
    201: AuthOut,
})
def signup(request, account_in: AccountCreate):
    if account_in.password1 != account_in.password2:
        return 400, {'detail': 'الرمز غير مطابق'}

    try:
        User.objects.get(username=account_in.username)
    except:
        new_user = User.objects.create_user(

            name=account_in.name,
            username=account_in.username,
            password=account_in.password1,
            address1=account_in.address1,
            phone_number=account_in.phone_number
        )

        token = get_tokens_for_user(new_user)

        return 201, {
            'token': token,
            'account': new_user,
        }

    return 400, {'detail': 'المستخدم مسجل بالفعل'}


@account_controller.post('signin', response={
    200: AuthOut,
    404: MessageOut,
})
def signin(request, signin_in: SigninSchema):
    user = authenticate(username=signin_in.username, password=signin_in.password)

    if not user:
        return 404, {'detail': 'المستخدم غير مسجل'}

    token = get_tokens_for_user(user)

    return {
        'token': token,
        'account': user
    }


@account_controller.get('', auth=GlobalAuth(), response=AccountOut)
def me(request):
    return get_object_or_404(User, id=request.auth['pk'])


@account_controller.put('', auth=GlobalAuth(), response={
    200: AccountOut,
})
def update_account(request, update_in: AccountUpdate):
    User.objects.filter(id=request.auth['pk']).update(**update_in.dict())
    return get_object_or_404(User, id=request.auth['pk'])


@account_controller.post('change-password', auth=GlobalAuth(), response={
    200: MessageOut,
    400: MessageOut
})
def change_password(request, password_update_in: ChangePasswordSchema):
    # user = authenticate(get_object_or_404(User, id=request.auth['pk']).email, password_update_in.old_password)
    if password_update_in.new_password1 != password_update_in.new_password2:
        return 400, {'detail': 'passwords do not match'}
    user = get_object_or_404(User, id=request.auth['pk'])
    is_it_him = user.check_password(password_update_in.old_password)

    if not is_it_him:
        return 400, {'detail': 'Dude, make sure you are him!'}

    user.set_password(password_update_in.new_password1)
    user.save()
    return {'detail': 'password updated successfully'}
