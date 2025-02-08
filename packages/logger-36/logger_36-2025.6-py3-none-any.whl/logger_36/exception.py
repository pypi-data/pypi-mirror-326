"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2023
SEE COPYRIGHT NOTICE BELOW
"""

import re as r
import sys as s
import tempfile as tmpf
import traceback as tcbk
import types as t
from pathlib import Path as path_t

_ORIGINAL_EXCEPTION_HANDLER = s.excepthook


def OverrideExceptionFormat() -> None:
    """"""
    s.excepthook = _HandleException


def ResetExceptionFormat() -> None:
    """"""
    s.excepthook = _ORIGINAL_EXCEPTION_HANDLER


def _HandleException(
    stripe: type[Exception], exception: Exception, trace: t.TracebackType, /
) -> None:
    """"""
    while trace.tb_next is not None:
        trace = trace.tb_next
    frame = trace.tb_frame
    code = frame.f_code
    module = path_t(code.co_filename)
    function = code.co_name
    line_number = frame.f_lineno
    line_content = module.read_text().splitlines()[line_number - 1].strip()

    # Format module.
    home = path_t.home()
    if module.is_relative_to(home):
        module = path_t("~") / module.relative_to(home)

    # Format line content.
    if line_content.startswith("raise "):
        # Do not display code of explicit exception raising.
        line_content = None

    # Find variables appearing in the line.
    if line_content is None:
        line_content = variables = ""
    else:
        all_variables = frame.f_locals
        found_names = []
        for match in r.finditer(r"[^\d\W]\w*", line_content):
            name = match.group()
            if name in all_variables:
                found_names.append(name)
        if found_names.__len__() > 0:
            longest = max(map(len, found_names))
            variables = map(
                lambda _: f"{_:{longest}} = {all_variables[_]}", sorted(found_names)
            )
            variables = "        " + "\n        ".join(variables) + "\n"
        else:
            variables = ""

        line_content = f"    {line_content}\n"

    # Format message.
    message = str(exception).strip()
    if message.__len__() > 0:
        message = f"    {message[0].title()}{message[1:]}\n"

    document = tmpf.NamedTemporaryFile(delete=False)

    print(
        f"{stripe.__name__}\n"
        f"    {module}:{function}@{line_number}\n"
        f"{line_content}"
        f"{variables}"
        f"{message}"
        f"    Full report at: {document.name}",
        file=s.stderr,
    )

    lines = tcbk.format_exception(exception)
    message = "".join(lines)

    document.write(message.encode())
    document.close()


"""
COPYRIGHT NOTICE

This software is governed by the CeCILL  license under French law and
abiding by the rules of distribution of free software.  You can  use,
modify and/ or redistribute the software under the terms of the CeCILL
license as circulated by CEA, CNRS and INRIA at the following URL
"http://www.cecill.info".

As a counterpart to the access to the source code and  rights to copy,
modify and redistribute granted by the license, users are provided only
with a limited warranty  and the software's author,  the holder of the
economic rights,  and the successive licensors  have only  limited
liability.

In this respect, the user's attention is drawn to the risks associated
with loading,  using,  modifying and/or developing or reproducing the
software by the user in light of its specific status of free software,
that may mean  that it is complicated to manipulate,  and  that  also
therefore means  that it is reserved for developers  and  experienced
professionals having in-depth computer knowledge. Users are therefore
encouraged to load and test the software's suitability as regards their
requirements in conditions enabling the security of their systems and/or
data to be ensured and,  more generally, to use and operate it in the
same conditions as regards security.

The fact that you are presently reading this means that you have had
knowledge of the CeCILL license and that you accept its terms.

SEE LICENCE NOTICE: file README-LICENCE-utf8.txt at project source root.

This software is being developed by Eric Debreuve, a CNRS employee and
member of team Morpheme.
Team Morpheme is a joint team between Inria, CNRS, and UniCA.
It is hosted by the Centre Inria d'Université Côte d'Azur, Laboratory
I3S, and Laboratory iBV.

CNRS: https://www.cnrs.fr/index.php/en
Inria: https://www.inria.fr/en/
UniCA: https://univ-cotedazur.eu/
Centre Inria d'Université Côte d'Azur: https://www.inria.fr/en/centre/sophia/
I3S: https://www.i3s.unice.fr/en/
iBV: http://ibv.unice.fr/
Team Morpheme: https://team.inria.fr/morpheme/
"""
