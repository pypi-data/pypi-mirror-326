"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2023
SEE COPYRIGHT NOTICE BELOW
"""

import dataclasses as d
import logging as l
import textwrap as txt_
import typing as h

from logger_36.catalog.config.console_rich import (
    ACTUAL_COLOR,
    ALTERNATIVE_BACKGROUND_FOR_DARK,
    ALTERNATIVE_BACKGROUND_FOR_LIGHT,
    DATE_TIME_COLOR,
    EXPECTED_COLOR,
    GRAY_COLOR,
    LEVEL_COLOR,
    WHITE_COLOR,
)
from logger_36.config.message import ACTUAL_PATTERNS, EXPECTED_PATTERNS, WHERE_SEPARATOR
from logger_36.constant.message import CONTEXT_LENGTH, LINE_INDENT
from logger_36.constant.record import SHOW_W_RULE_ATTR
from logger_36.task.format.rule import Rule, rule_t
from logger_36.type.handler import handler_extension_t
from logger_36.type.handler import (
    message_from_record_preprocessed_p as message_from_record_p,
)
from rich.console import Console as console_t  # noqa
from rich.console import RenderableType as renderable_t  # noqa
from rich.markup import escape as EscapedVersion  # noqa
from rich.text import Text as text_t  # noqa
from rich.traceback import install as InstallTracebackHandler  # noqa

_COMMON_TRACEBACK_ARGUMENTS = ("theme", "width")
_EXCLUSIVE_TRACEBACK_ARGUMENTS = (
    "extra_lines",
    "indent_guides",
    "locals_hide_dunder",
    "locals_hide_sunder",
    "locals_max_length",
    "locals_max_string",
    "max_frames" "show_locals",
    "suppress",
    "word_wrap",
)


@d.dataclass(slots=True, repr=False, eq=False)
class console_rich_handler_t(l.Handler):
    """
    kind: See logger_36.constant.handler.handler_codes_h.

    alternating_lines:
    - Initial value:
        - 1: enabled for dark background
        - 2: enabled for light background
        - anything else: disabled
    - Runtime value: 0/1=do not/do highlight next time.
    """

    kind: h.ClassVar[str] = "c"

    extension: handler_extension_t = d.field(init=False)
    console: console_t = d.field(init=False)
    MessageFromRecord: message_from_record_p = d.field(init=False)
    alternating_lines: int = 0
    background_is_light: bool = True

    name: d.InitVar[str | None] = None
    level: d.InitVar[int] = l.NOTSET
    should_store_memory_usage: d.InitVar[bool] = False
    message_width: d.InitVar[int] = -1
    formatter: d.InitVar[l.Formatter | None] = None
    should_install_traceback: d.InitVar[bool] = False
    should_record: d.InitVar[bool] = False

    rich_kwargs: d.InitVar[dict[str, h.Any] | None] = None

    def __post_init__(
        self,
        name: str | None,
        level: int,
        should_store_memory_usage: bool,
        message_width: int,
        formatter: l.Formatter | None,
        should_install_traceback: bool,
        should_record: bool,
        rich_kwargs: dict[str, h.Any] | None,
    ) -> None:
        """"""
        l.Handler.__init__(self)

        self.extension = handler_extension_t(
            name=name,
            should_store_memory_usage=should_store_memory_usage,
            handler=self,
            level=level,
            message_width=message_width,
            formatter=formatter,
        )

        if rich_kwargs is None:
            rich_console_kwargs = {}
        else:
            rich_console_kwargs = rich_kwargs
        rich_traceback_kwargs = {}
        if should_install_traceback:
            for key in rich_console_kwargs:
                if key in _COMMON_TRACEBACK_ARGUMENTS:
                    rich_traceback_kwargs[key] = rich_console_kwargs[key]
                elif key in _EXCLUSIVE_TRACEBACK_ARGUMENTS:
                    rich_traceback_kwargs[key] = rich_console_kwargs[key]
                    del rich_console_kwargs[key]

        self.console = console_t(
            highlight=False,
            force_terminal=True,
            record=should_record,
            **rich_console_kwargs,
        )
        if should_install_traceback:
            rich_traceback_kwargs["console"] = self.console
            InstallTracebackHandler(**rich_traceback_kwargs)

        self.MessageFromRecord = self.extension.MessageFromRecord
        if self.alternating_lines == 1:
            self.alternating_lines = 0
            self.background_is_light = False
        elif self.alternating_lines == 2:
            self.alternating_lines = 0
            self.background_is_light = True
        else:
            self.alternating_lines = -1

    def emit(self, record: l.LogRecord, /) -> None:
        """"""
        if hasattr(record, SHOW_W_RULE_ATTR):
            richer = Rule(record.msg, DATE_TIME_COLOR)
        else:
            message = self.MessageFromRecord(record, PreProcessed=EscapedVersion)
            should_highlight_back = self.alternating_lines == 1
            if self.alternating_lines >= 0:
                self.alternating_lines = (self.alternating_lines + 1) % 2
            richer = HighlightedVersion(
                self.console,
                message,
                record.levelno,
                should_highlight_back=should_highlight_back,
                background_is_light=self.background_is_light,
            )
        self.console.print(richer, crop=False, overflow="ignore")

    def ShowMessage(self, message: str | rule_t, /, *, indented: bool = False) -> None:
        """
        See documentation of
        logger_36.catalog.handler.generic.generic_handler_t.ShowMessage.
        """
        if isinstance(message, str) and indented:
            message = txt_.indent(message, LINE_INDENT)
        self.console.print(message, crop=False, overflow="ignore")

    def DisplayRule(self, /, *, text: str | None = None, color: str = "white") -> None:
        """"""
        self.ShowMessage(Rule(text, color))


def HighlightedVersion(
    _: console_t,
    message: str,
    log_level: int,
    /,
    *,
    should_highlight_back: bool = False,
    background_is_light: bool = True,
) -> renderable_t:
    """"""
    output = text_t(message, WHITE_COLOR)

    output.stylize(LEVEL_COLOR[log_level], end=CONTEXT_LENGTH)
    where = message.rfind(WHERE_SEPARATOR)
    if (where >= 0) and ("\n" not in message[where:]):
        output.stylize(GRAY_COLOR, start=where)
    _ = output.highlight_words(ACTUAL_PATTERNS, style=ACTUAL_COLOR)
    _ = output.highlight_regex(EXPECTED_PATTERNS, style=EXPECTED_COLOR)

    if should_highlight_back:
        if background_is_light:
            style = ALTERNATIVE_BACKGROUND_FOR_LIGHT
        else:
            style = ALTERNATIVE_BACKGROUND_FOR_DARK
        output.stylize(style)

    return output


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
