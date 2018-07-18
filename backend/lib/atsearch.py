import re
from typing import List, Tuple, Set

re_at = re.compile(r'(?:^|(?<=\s))@([\u4e00-\u9fa5a-zA-Z][\u4e00-\u9fa5a-zA-Z0-9]{1,32})(?=\s|$)')
re_at2 = re.compile('\x01(.+?)\x01')


def at_search(text: str, usernames_filter) -> Tuple[str, Set[str], Set[str]]:
    new_text, times = re_at.subn('\x01\\1\x01', text)
    old_matched = set(re_at2.findall(text))  # 已经标注过的
    matched = set(re_at2.findall(new_text)) - old_matched  # 新增的

    if usernames_filter:
        new_matched = usernames_filter(matched)
        for i in matched - new_matched:
            new_text = new_text.replace('\x01%s\x01' % i, '@%s' % i)
        matched = new_matched

    return new_text, old_matched, matched


if __name__ == '__main__':
    print(at_search('@asd ,   @测试 , test@qq.com @end', None))
    print(at_search('标准文本 test@qq.com', None))
    print(at_search('@asd \x01测试\x01', None))

    def the_filter(input):
        return {'end'}
    print(at_search('@asd ,   @测试 , test@qq.com @end', the_filter))

    def the_filter(input):
        return set()
    print(at_search('@asd ,   @测试 , test@qq.com @end', the_filter))
