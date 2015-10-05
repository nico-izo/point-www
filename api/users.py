from point.app import users, tags
from point.util.env import env
from point.util.www import check_referer
from geweb.http import Response
from geweb.exceptions import Forbidden, NotFound
from geweb.template import render
from point.core.user import User, SubscribeError, check_auth, \
                            AlreadySubscribed, AlreadyRequested, \
                            UserNotFound, NotAuthorized
from geweb.util import csrf
import json

from api import api


@api
def info(login):
    print '**** LOGIN: ****'
    print login
    try:
        user = User('login', login)
        # !!!
        print '**** user form API by login ****'
        print user
    except UserNotFound:
        raise NotFound

    try:
        data = users.info(user)
        print '*'*20
        print data
        print '*'*20
    except SubscribeError:
        raise Forbidden
    data['id'] = user.id
    data['login'] = user.login
    try:
        data['created'] = data['created']
    except (KeyError, AttributeError):
        pass
    try:
        data['birthdate'] = data['birthdate']
    except (KeyError, AttributeError):
        pass
    if env.user.id:
        data['subscribed'] = user.check_subscriber(env.user)
        data['rec_sub'] = user.check_rec_subscriber(env.user)
        if not data['subscribed']:
            data['bl'] = env.user.check_blacklist(user)
            if not data['bl']:
                data['wl'] = env.user.check_blacklist(user)
    return data


@api
def user_info_byid(uid):
    """Return user info by given user id"""
    if uid and uid.isdigit():
        try:
            user = User(int(uid))
            # !!!
            print '**** user from API by id ****'
            print user
        except (UserNotFound, ValueError):
            raise NotFound
        else:
            print '**** user LOGIN from by-id ****'
            print(user.login)
            data = users.info(user)
            print '**** DATA: ****'
            print data
            return data
    raise NotFound


# get user info via settings.domain/api/me
@api
def my_info():
    login = env.user.login
    if not login:
        raise NotAuthorized
    return users.info(login)


@csrf
@check_auth
@check_referer
def subscribe():
    if not env.owner or not env.owner.id:
        raise NotFound

    try:
        res = users.subscribe(env.owner)
    except SubscribeError:
        raise Forbidden
    except (AlreadySubscribed, AlreadyRequested):
        res = False

    # TODO: notify user if subscription request is sent

    if env.request.is_xhr:
        return Response(json.dumps({'ok': bool(res)}),
                        mimetype='application/json')

    return Response(redirect=env.request.referer)

@csrf
@check_auth
@check_referer
def unsubscribe():
    if not env.owner or not env.owner.id:
        raise NotFound

    users.unsubscribe(env.owner)

    if env.request.is_xhr:
        return Response(json.dumps({'ok': True}), mimetype='application/json')

    return Response(redirect=env.request.referer)

@csrf
@check_auth
@check_referer
def subscribe_rec():
    if not env.owner or not env.owner.id:
        raise NotFound

    try:
        res = users.subscribe_rec(env.owner)
    except SubscribeError:
        raise Forbidden
    except (AlreadySubscribed, AlreadyRequested):
        res = False

    if env.request.is_xhr:
        return Response(json.dumps({'ok': bool(res)}),
                        mimetype='application/json')

    return Response(redirect=env.request.referer)

@csrf
@check_auth
@check_referer
def unsubscribe_rec():
    if not env.owner or not env.owner.id:
        raise NotFound

    users.unsubscribe_rec(env.owner)

    if env.request.is_xhr:
        return Response(json.dumps({'ok': True}), mimetype='application/json')

    return Response(redirect=env.request.referer)

@csrf
@check_auth
@check_referer
def add_to_whitelist():
    if not env.owner or not env.owner.id:
        raise NotFound

    try:
        res = users.add_to_whitelist(env.owner)
    except SubscribeError:
        raise Forbidden
    except AlreadySubscribed:
        raise Forbidden

    if env.request.is_xhr:
        return Response(json.dumps({'ok': bool(res)}),
                        mimetype='application/json')

    return Response(redirect=env.request.referer)

@csrf
@check_auth
@check_referer
def del_from_whitelist():
    if not env.owner or not env.owner.id:
        raise NotFound

    try:
        res = users.del_from_whitelist(env.owner)
    except SubscribeError:
        raise Forbidden

    if env.request.is_xhr:
        return Response(json.dumps({'ok': bool(res)}),
                        mimetype='application/json')

    return Response(redirect=env.request.referer)

@csrf
@check_auth
@check_referer
def add_to_blacklist():
    if not env.owner or not env.owner.id:
        raise NotFound

    try:
        res = users.add_to_blacklist(env.owner)
    except SubscribeError:
        raise Forbidden

    if env.request.is_xhr:
        return Response(json.dumps({'ok': bool(res)}),
                        mimetype='application/json')

    return Response(redirect=env.request.referer)

@csrf
@check_auth
@check_referer
def del_from_blacklist():
    if not env.owner or not env.owner.id:
        raise NotFound

    try:
        res = users.del_from_blacklist(env.owner)
    except SubscribeError:
        raise Forbidden

    if env.request.is_xhr:
        return Response(json.dumps({'ok': bool(res)}),
                        mimetype='application/json')

    return Response(redirect=env.request.referer)

@csrf
@check_auth
@check_referer
def tag_subscribe():
    tag = env.request.args('tag', '').strip()
    if not tag:
        raise Forbidden
    try:
        tags.subscribe(tag, env.owner.login)
    except SubscribeError:
        raise Forbidden

    return Response(redirect=env.request.referer)

@csrf
@check_auth
@check_referer
def tag_unsubscribe():
    tag = env.request.args('tag', '').strip()
    if not tag:
        raise Forbidden
    tags.unsubscribe(tag, env.owner.login)
    return Response(redirect=env.request.referer)

@csrf
@check_auth
@check_referer
def tag_add_to_blacklist():
    tag = env.request.args('tag', '').strip()
    if not tag:
        raise Forbidden
    try:
        tags.add_to_blacklist(tag, env.owner.login)
    except SubscribeError:
        raise Forbidden
    return Response(redirect=env.request.referer)

@csrf
@check_auth
@check_referer
def tag_del_from_blacklist():
    tag = env.request.args('tag', '').strip()
    if not tag:
        raise Forbidden
    tags.del_from_blacklist(tag, env.owner.login)
    return Response(redirect=env.request.referer)

@api
def subscriptions(login):
    env.owner = User("login", login)
    if not env.owner or not env.owner.id:
        raise NotFound
    return env.owner.subscriptions()

@api
def subscriptions_byid(uid):
    """Return user's subscriptions by given user id"""
    uid = int(uid)
    env.owner = User(int(uid))
    if not env.owner or not env.owner.id:
        raise NotFound
    return env.owner.subscriptions()

@api
def subscribers(login):
    env.owner = User("login", login)
    if not env.owner or not env.owner.id:
        raise NotFound
    return env.owner.subscribers()

@api
def subscribers_byid(uid):
    """Return user's subscribers by given user id"""
    uid = int(uid)
    env.owner = User(int(uid))
    if not env.owner or not env.owner.id:
        raise NotFound
    return env.owner.subscribers()

@api
@check_auth
def blacklist():
    env.owner = env.user
    if not env.owner or not env.owner.id:
        raise NotFound
    return env.owner.blacklist()

@api
@check_auth
def whitelist():
    env.owner = env.user
    if not env.owner or not env.owner.id:
        raise NotFound
    return env.owner.whitelist()

