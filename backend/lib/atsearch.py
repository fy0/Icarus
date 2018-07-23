import re
from typing import List, Tuple, Set

from slim.utils import to_hex

re_at = re.compile(r'(?:^|(?<=\s))@([\u4e00-\u9fa5a-zA-Z][\u4e00-\u9fa5a-zA-Z0-9]{1,32})(?=\s|$)')
re_at2 = re.compile('\x01[a-zA-Z0-9]-(.+?)\x01')


def at_replace(text: str, find_by_nicknames_func) -> Tuple[str, Set[str], Set[str]]:
    new_text, times = re_at.subn('\x01\\1\x01', text)
    old_matched = set(re_at2.findall(text))  # 已经标注过的
    matched = set(re_at2.findall(new_text)) - old_matched  # 新增的

    if find_by_nicknames_func:
        data = {}
        for i in find_by_nicknames_func(matched):
            data[i.nickname] = i

        new_matched = data.keys()
        for i in matched - new_matched:
            new_text = new_text.replace('\x01%s\x01' % i, '@%s' % i)

        for i in data.values():
            new_text = new_text.replace('\x01%s\x01' % i.nickname, '\x01%s-%s\x01' % (to_hex(i.id), i.nickname))

        matched = new_matched

    return new_text, old_matched, matched


if __name__ == '__main__':
    print(at_replace('@asd ,   @测试 , test@qq.com @end', None))
    print(at_replace('标准文本 test@qq.com', None))
    print(at_replace('@asd \x01测试\x01', None))

    def the_filter(input):
        class A: pass
        _ = A()
        _.id = b'\xAB\xCD'
        _.nickname = 'end'
        return [_]
    print(at_replace('@asd ,   @测试 , test@qq.com @end', the_filter))

    def the_filter(input):
        return []
    print(at_replace('@asd ,   @测试 , test@qq.com @end', the_filter))
