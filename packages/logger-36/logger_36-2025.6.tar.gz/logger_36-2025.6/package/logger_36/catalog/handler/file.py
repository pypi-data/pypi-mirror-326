"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2023
SEE COPYRIGHT NOTICE BELOW
"""

import dataclasses as d
import logging as l
import textwrap as txt_
import typing as h
from pathlib import Path as path_t

from logger_36.constant.message import LINE_INDENT
from logger_36.constant.record import SHOW_W_RULE_ATTR
from logger_36.task.format.rule import RuleAsText
from logger_36.type.handler import handler_extension_t
from logger_36.type.handler import message_from_record_raw_p as message_from_record_p


@d.dataclass(slots=True, repr=False, eq=False)
class file_handler_t(l.FileHandler):
    """
    kind: See logger_36.constant.handler.handler_codes_h.
    """

    kind: h.ClassVar[str] = "f"

    extension: handler_extension_t = d.field(init=False)
    MessageFromRecord: message_from_record_p = d.field(init=False)

    name: d.InitVar[str | None] = None
    level: d.InitVar[int] = l.NOTSET
    should_store_memory_usage: d.InitVar[bool] = False
    message_width: d.InitVar[int] = -1
    formatter: d.InitVar[l.Formatter | None] = None

    path: d.InitVar[path_t | None] = None
    handler_args: d.InitVar[tuple[h.Any, ...] | None] = None
    handler_kwargs: d.InitVar[dict[str, h.Any] | None] = None

    def __post_init__(
        self,
        name: str | None,
        level: int,
        should_store_memory_usage: bool,
        message_width: int,
        formatter: l.Formatter | None,
        path: path_t | None,
        handler_args: tuple[h.Any, ...] | None,
        handler_kwargs: dict[str, h.Any] | None,
    ) -> None:
        """"""
        l.FileHandler.__init__(self, path, *handler_args, **handler_kwargs)

        self.extension = handler_extension_t(
            name=name,
            should_store_memory_usage=should_store_memory_usage,
            handler=self,
            level=level,
            message_width=message_width,
            formatter=formatter,
        )

        self.MessageFromRecord = self.extension.MessageFromRecord

    def emit(self, record: l.LogRecord, /) -> None:
        """"""
        if hasattr(record, SHOW_W_RULE_ATTR):
            message = RuleAsText(record.msg)
        else:
            message = self.MessageFromRecord(record)
        print(message, file=self.stream)
        self.stream.flush()

    def ShowMessage(self, message: str, /, *, indented: bool = False) -> None:
        """
        See documentation of
        logger_36.catalog.handler.generic.generic_handler_t.ShowMessage.
        """
        if indented:
            message = txt_.indent(message, LINE_INDENT)
        print(message, file=self.stream)
        self.stream.flush()

    def DisplayRule(self, /, *, text: str | None = None, color: str = "white") -> None:
        """"""
        self.ShowMessage(RuleAsText(text))


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
