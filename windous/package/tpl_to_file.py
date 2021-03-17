import os
import re
import sys

import yaml


class MyRenderClass:

    charref = re.compile(r'\{\{(.+?)\}\}')

    def __init__(self, content):
        self.content = content

    def render(self, context):
        rs = []
        last_start = 0
        for r in re. finditer(self.charref, self.content):
            key = r.groups()[0].strip()

            rs.append(self.content[last_start:r.start()])
            rs.append(context.get(key, '{{ %s }}' % key))
            last_start = r.end()

        rs.append(self.content[last_start:])
        new_content = ''.join(rs)
        return new_content


class TemplateToFile:

    tpl_suffix = '.template'
    # render_class = Engine().from_string
    render_class = MyRenderClass

    def __init__(self, tpl_dir, tgt_dir, tpl_suffix=None):
        self.tpl_dir = tpl_dir
        self.tgt_dir = tgt_dir

        if tpl_suffix:
            self.tpl_suffix = tpl_suffix

    def render(self, context):
        prefix_length = len(self.tpl_dir) + 1
        for root, dirs, files in os.walk(self.tpl_dir):
            for file in files:
                tgt_path = os.path.join(self.tgt_dir, root[prefix_length:], file[:-len(self.tpl_suffix)])
                tpl_path = os.path.join(root, file)

                if not file.endswith(self.tpl_suffix):
                    continue

                with open(tpl_path, 'r', encoding='utf-8') as template_file:
                    content = template_file.read()
                    template = self.render_class(content)
                    content = template.render(context)
                    old_content = ''
                    if os.path.exists(tgt_path):
                        with open(tgt_path, 'r', encoding='utf-8') as f:
                            old_content = f.read()
                    if content != old_content:
                        with open(tgt_path, 'w', encoding='utf-8') as new_file:
                            new_file.write(content)

    def clear(self, context):
        prefix_length = len(self.tpl_dir) + 1
        for root, dirs, files in os.walk(self.tpl_dir):
            for file in files:
                tgt_path = os.path.join(self.tgt_dir, root[prefix_length:], file[:-len(self.tpl_suffix)])
                if not file.endswith(self.tpl_suffix):
                    continue

                if os.path.exists(tgt_path):
                    os.remove(tgt_path)


def main():
    context = {}
    data = {}

    context_context = {
        'CURRENT_PATH': os.path.dirname(os.path.abspath(__file__))
    }

    with open('config-prod.yaml', 'r', encoding='utf-8') as f:
        data = yaml.load(f.read(), Loader=yaml.FullLoader)
    for key in data:
        context.update(data[key])
    for key in context:
        template = MyRenderClass(str(context[key]))
        context[key] = template.render(context_context)

    tpl_dir = context.get('TPL_DIR', './template')
    tgt_dir = context.get('TGT_DIR', '.')

    t2f = TemplateToFile(tpl_dir=tpl_dir, tgt_dir=tgt_dir)
    if 'clear' in sys.argv:
        t2f.clear(context)
    else:
        t2f.render(context)


if __name__ == '__main__':
    main()
