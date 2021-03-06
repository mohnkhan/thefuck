# -*- encoding: utf-8 -*-
from thefuck.utils import memoize, get_alias

target_layout = '''qwertyuiop[]asdfghjkl;'zxcvbnm,./QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?'''

source_layouts = [u'''йцукенгшщзхъфывапролджэячсмитьбю.ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,''',
                  u'''йцукенгшщзхїфівапролджєячсмитьбю.ЙЦУКЕНГШЩЗХЇФІВАПРОЛДЖЄЯЧСМИТЬБЮ,''',
                  u'''ضصثقفغعهخحجچشسیبلاتنمکگظطزرذدپو./ًٌٍَُِّْ][}{ؤئيإأآة»«:؛كٓژٰ‌ٔء><؟''',
                  u''';ςερτυθιοπ[]ασδφγηξκλ΄ζχψωβνμ,./:΅ΕΡΤΥΘΙΟΠ{}ΑΣΔΦΓΗΞΚΛ¨"ΖΧΨΩΒΝΜ<>?''',
                  u'''/'קראטוןםפ][שדגכעיחלךף,זסבהנמצתץ.QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?''']


@memoize
def _get_matched_layout(command):
    # don't use command.split_script here because a layout mismatch will likely
    # result in a non-splitable sript as per shlex
    cmd = command.script.split(' ')
    for source_layout in source_layouts:
        is_all_match = True

        for cmd_part in cmd:
            if not all([ch in source_layout or ch in '-_' for ch in cmd_part]):
                is_all_match = False
                break

        if is_all_match:
            return source_layout


def _switch(ch, layout):
    if ch in layout:
        return target_layout[layout.index(ch)]
    else:
        return ch


def _switch_command(command, layout):
    return ''.join(_switch(ch, layout) for ch in command.script)


def match(command):
    if 'not found' not in command.output:
        return False
    matched_layout = _get_matched_layout(command)
    return (matched_layout and
            _switch_command(command, matched_layout) != get_alias())


def get_new_command(command):
    matched_layout = _get_matched_layout(command)
    return _switch_command(command, matched_layout)
