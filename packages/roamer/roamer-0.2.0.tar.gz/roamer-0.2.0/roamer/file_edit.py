"""
This module handles the temp file creation, processing it's output and hand off to the editor
"""

import sys
import tempfile
import os
from subprocess import call

ROAMER_EDITOR = os.environ.get('ROAMER_EDITOR')

if ROAMER_EDITOR:
    EDITOR = ROAMER_EDITOR
else:
    EDITOR = os.environ.get('EDITOR')
    if not EDITOR:
        EDITOR = 'vi'

if EDITOR in ['vim', 'nvim', 'vi']:
    EXTRA_EDITOR_COMMAND = '+set backupcopy=yes'
else:
    # nano and emacs work without any extra commands
    EXTRA_EDITOR_COMMAND = None


def file_editor(content):
    with tempfile.NamedTemporaryFile(suffix=".roamer") as temp:
        if sys.version_info[0] == 3:
            content = content.encode('utf-8')
        temp.write(content)
        temp.flush()
        if EXTRA_EDITOR_COMMAND:
            call([EDITOR, EXTRA_EDITOR_COMMAND, temp.name])
        else:
            call([EDITOR, temp.name])
        temp.seek(0)
        output = temp.read()
        if sys.version_info[0] == 3:
            output = output.decode('UTF-8')
        return output
