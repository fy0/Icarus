import os
import math
import random
import string
import config
from slim.retcode import RETCODE
from .request import *

misc_info = misc()


def random_str_en(n, accept_digit_first_letter=False):
    if n < 0:
        raise ValueError("n < 0 !!!")
    ret = os.urandom(int(math.ceil(n / 2))).hex()[:n]
    if n and (not accept_digit_first_letter):
        if ret[0] not in string.ascii_letters:
            ret = random.choice(string.ascii_letters) + ret[1:]
    return ret


def random_str_cn(n):
    ret = []
    for i in range(n):
        ret.append(chr(random.randint(0x4e00, 0x9fa5)))
    return ''.join(ret)


def test_signup():
    assert config.USER_ALLOW_SIGNUP, '不开放注册时不测试'
    assert len(random_str_en(35)) == 35
    assert len(random_str_en(32)) == 32
    assert len(random_str_en(1)) == 1
    assert len(random_str_en(0)) == 0
    assert isinstance(random_str_en(35), str)

    ret = user.new(None)
    assert ret['code'] == RETCODE.INVALID_POSTDATA, '空提交'

    ret = user.new({})
    assert ret['code'] == RETCODE.INVALID_POSTDATA, '空提交'

    info = {
        'email': random_str_en(40),
        'nickname': random_str_en(30),
        'password': '111111',
        'password2': '111111'
    }

    ret = user.new(info)
    assert ret['code'] == RETCODE.FAILED
    assert ret['data']['email'], '无效的 Email 地址。'

    info['nickname'] = random_str_en(config.NICKNAME_FOR_REG_MAX),
    ret = user.new(info)
    assert 'nickname' not in ret['data'], 'nickname 边界情况（32字符）'

    info['nickname'] = random_str_en(config.NICKNAME_FOR_REG_MAX+1),
    ret = user.new(info)
    assert 'nickname' in ret['data'], 'nickname 越界（33字符）'

    info['nickname'] = '1' + random_str_en(config.NICKNAME_FOR_REG_MAX - 1)
    ret = user.new(info)
    assert 'nickname' in ret['data'], 'nickname 不能以数字开头'

    info['nickname'] = random_str_en(config.NICKNAME_FOR_REG_MIN),
    ret = user.new(info)
    assert 'nickname' not in ret['data'], 'nickname 边界情况（4字符）'

    info['nickname'] = random_str_en(config.NICKNAME_FOR_REG_MIN-1),
    ret = user.new(info)
    assert 'nickname' in ret['data'], 'nickname 越界（3字符）'

    info['nickname'] = random_str_cn(config.NICKNAME_CN_FOR_REG_MIN)
    ret = user.new(info)
    assert 'nickname' not in ret['data'], 'nickname 中文名称'

    info['nickname'] = random_str_cn(config.NICKNAME_FOR_REG_MAX)
    ret = user.new(info)
    assert 'nickname' not in ret['data'], 'nickname 中文名称最大长度'

    info['nickname'] = random_str_cn(config.NICKNAME_FOR_REG_MAX+1)
    ret = user.new(info)
    assert 'nickname' in ret['data'], 'nickname 中文名称越界'

    info['nickname'] = random_str_cn(config.NICKNAME_FOR_REG_MAX) + random.choice(string.ascii_letters)
    ret = user.new(info)
    assert 'nickname' in ret['data'], 'nickname 中文名称越界2'

    if config.NICKNAME_CN_FOR_REG_MIN < config.NICKNAME_FOR_REG_MIN:
        info['nickname'] = random_str_cn(config.NICKNAME_CN_FOR_REG_MIN)[:-1] + random.choice(string.ascii_letters)
        ret = user.new(info)
        assert 'nickname' in ret['data'], 'nickname 达到中文最短长度，但其中含有英文，且不及英文最短长度'

    if config.NICKNAME_FOR_REG_MIN - config.NICKNAME_CN_FOR_REG_MIN > 1:
        info['nickname'] = random_str_cn(config.NICKNAME_CN_FOR_REG_MIN) + random.choice(string.ascii_letters)
        ret = user.new(info)
        assert 'nickname' not in ret['data'], 'nickname 达到中文最短长度，但不及英文最短长度'

    # TODO: 反向的就暂不测试了，后面再写

    info['email'] = random_str_en(config.EMAIL_MAX - 7) + '@' + random_str_en(3) + '.com'
    assert len(info['email']) == config.EMAIL_MAX + 1
    info['nickname'] = random_str_en(config.NICKNAME_FOR_REG_MAX)
    ret = user.new(info)
    assert ret['code'] == RETCODE.FAILED
    assert 'email' in ret['data'], '邮箱长度越界'

    info['email'] = random_str_en(config.EMAIL_MAX - 8) + '@' + random_str_en(3) + '.com'
    assert len(info['email']) == config.EMAIL_MAX
    info['nickname'] = random_str_en(config.NICKNAME_FOR_REG_MAX)
    ret = user.new(info)
    assert ret['code'] == RETCODE.SUCCESS, '创建成功'

    info['email'] = info['email'].upper()
    ret = user.new(info)
    assert ret['code'] == RETCODE.FAILED, '邮箱大小写不同认为是不同账号'

    info['email'] = random_str_en(config.EMAIL_MAX - 8) + '@' + random_str_en(3) + '.com'
    info['nickname'] = info['nickname'].upper()
    ret = user.new(info)
    assert ret['code'] == RETCODE.FAILED, '帐号大小写不同不认为是不同账号'


def test_signin():
    pass
