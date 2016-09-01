import os
import os.path
import click
import textwrap

HEADER_TEMPLATE ="""\
/* Auto-generated by the pyresource tool. Do not edit */
const uint8_t {varname}_data[{len}] = {{
{data_hex}
}};

const HTTPResource {varname}({varname}_data, {len});
"""

RESOURCE_H_TEMPLATE = """\
#ifndef _{guard_name}_H_
#define _{guard_name}_H_

/* Auto-generated by the pyresource tool. Do not edit */

#include "http_common.h"
{includes}

#endif /* ifndef _{guard_name}_H_ */
"""

@click.command(short_help='Convert HTTP resource file into a C header.')
@click.argument('dirs', type=click.Path(True, False, True), nargs=-1)
def pyresouce(dirs):
    """Adafruit Python Resource Tool

    This is a tool to convert a HTTP resouce folder into a C header format
    that can be imported into WICED board sketches.

    Example of converting myresources folder:

      pyresource resources_dir
    """
    includes = ''
    for d in dirs:
        for f in os.listdir(d):
            varname = f.replace('.', '_')
            params = {}
            params['varname'] = varname
            with open(d + '/' + f, "rb") as fin:
                data = fin.read()
                data_hex = ', '.join(['0x{0:02X}'.format(ord(x)) for x in data])
                # Set data to hex string (wrapped nicely on 80 character boundary).
                data_hex = textwrap.fill(data_hex, width=80, break_long_words=False,
                                         break_on_hyphens=False, initial_indent='  ', subsequent_indent='  ')
                params['len'] = len(data)
                params['data_hex'] = data_hex
            with open(varname + '.h', "w") as fout:
                fout.write(HEADER_TEMPLATE.format(**params))
            includes += '#include "' + varname + '.h"\n'

    with open('resources.h', "w") as fout:
        params = {}
        params['guard_name'] = 'RESOURCE'
        params['includes'] = includes
        fout.write(RESOURCE_H_TEMPLATE.format(**params))

if __name__ == '__main__':
    pyresouce()