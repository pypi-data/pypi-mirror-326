"""Reimplementation of PLAYA 0.2 `page.layout` in a more appropriate location.

Creates dictionaries appropriate for feeding to bears of different
sorts (pandas or polars, your choice).
"""

from functools import singledispatch
from multiprocessing.context import BaseContext
from pathlib import Path
import logging
import multiprocessing

from typing import cast, Iterator, List, Union
from playa.page import (
    Page,
    ContentObject,
    PathObject,
    ImageObject,
    TextObject,
    XObjectObject,
)
from playa.utils import (
    apply_matrix_norm,
    apply_matrix_pt,
    Point,
    get_bound,
)
import playa
from playa import DeviceSpace, LayoutDict, fieldnames as FIELDNAMES, schema as SCHEMA  # noqa: F401

LOG = logging.getLogger(__name__)


@singledispatch
def process_object(obj: ContentObject) -> Iterator[LayoutDict]:
    """Handle obj according to its type"""
    yield from ()


def make_path(
    obj: PathObject,
    *,
    object_type: str,
    x0: float,
    y0: float,
    x1: float,
    y1: float,
    path_ops: str,
    pts: List[Point],
) -> LayoutDict:
    """Make a `LayoutDict` for a path."""
    return LayoutDict(
        object_type=object_type,
        x0=x0,
        y0=y0,
        x1=x1,
        y1=y1,
        mcid=None if obj.mcs is None else obj.mcs.mcid,
        tag=None if obj.mcs is None else obj.mcs.tag,
        path_ops=path_ops,
        pts_x=[x for x, y in pts],
        pts_y=[y for x, y in pts],
        stroke=obj.stroke,
        fill=obj.fill,
        evenodd=obj.evenodd,
        linewidth=obj.gstate.linewidth,
        dash_pattern=obj.gstate.dash.dash,
        dash_phase=obj.gstate.dash.phase,
        stroking_colorspace=obj.gstate.scs.name,
        stroking_color=obj.gstate.scolor.values,
        stroking_pattern=obj.gstate.scolor.pattern,
        non_stroking_colorspace=obj.gstate.ncs.name,
        non_stroking_color=obj.gstate.ncolor.values,
        non_stroking_pattern=obj.gstate.ncolor.pattern,
        page_index=0,
        page_label="0",
    )


@process_object.register
def _(obj: PathObject) -> Iterator[LayoutDict]:
    for path in obj:
        ops = []
        pts: List[Point] = []
        for seg in path.raw_segments:
            ops.append(seg.operator)
            if seg.operator == "h":
                pts.append(pts[0])
            else:
                pts.append(apply_matrix_pt(obj.ctm, seg.points[-1]))
        # Drop a redundant "l" on a path closed with "h"
        shape = "".join(ops)
        if len(ops) > 3 and shape[-2:] == "lh" and pts[-2] == pts[0]:
            shape = shape[:-2] + "h"
            pts.pop()
        if shape in {"mlh", "ml"}:
            # single line segment ("ml" is a frequent anomaly)
            (x0, y0), (x1, y1) = pts[0:2]
            if x0 > x1:
                (x1, x0) = (x0, x1)
            if y0 > y1:
                (y1, y0) = (y0, y1)
            yield make_path(
                obj,
                object_type="line",
                x0=x0,
                y0=y0,
                x1=x1,
                y1=y1,
                path_ops=shape,
                pts=pts,
            )
        elif shape in {"mlllh", "mllll"}:
            (x0, y0), (x1, y1), (x2, y2), (x3, y3), _ = pts
            is_closed_loop = pts[0] == pts[4]
            has_square_coordinates = (
                x0 == x1 and y1 == y2 and x2 == x3 and y3 == y0
            ) or (y0 == y1 and x1 == x2 and y2 == y3 and x3 == x0)
            if is_closed_loop and has_square_coordinates:
                if x0 > x2:
                    (x2, x0) = (x0, x2)
                if y0 > y2:
                    (y2, y0) = (y0, y2)
                yield make_path(
                    obj,
                    object_type="rect",
                    x0=x0,
                    y0=y0,
                    x1=x2,
                    y1=y2,
                    path_ops=shape,
                    pts=pts,
                )
            else:
                x0, y0, x1, y1 = get_bound(pts)
                yield make_path(
                    obj,
                    object_type="curve",
                    x0=x0,
                    y0=y0,
                    x1=x1,
                    y1=y1,
                    path_ops=shape,
                    pts=pts,
                )
        else:
            x0, y0, x1, y1 = get_bound(pts)
            yield make_path(
                obj,
                object_type="curve",
                x0=x0,
                y0=y0,
                x1=x1,
                y1=y1,
                path_ops=shape,
                pts=pts,
            )


@process_object.register
def _(obj: ImageObject) -> Iterator[LayoutDict]:
    x0, y0, x1, y1 = obj.bbox
    if (
        obj.stream is not None
        and obj.stream.objid is not None
        and obj.stream.genno is not None
    ):
        stream_id = (obj.stream.objid, obj.stream.genno)
    else:
        stream_id = None
    yield LayoutDict(
        object_type="image",
        x0=x0,
        y0=y0,
        x1=x1,
        y1=y1,
        xobjid=obj.xobjid,
        mcid=None if obj.mcs is None else obj.mcs.mcid,
        tag=None if obj.mcs is None else obj.mcs.tag,
        srcsize=obj.srcsize,
        imagemask=obj.imagemask,
        bits=obj.bits,
        image_colorspace=obj.colorspace,
        stream=stream_id,
        page_index=0,
        page_label="0",
    )


@process_object.register
def _(obj: TextObject) -> Iterator[LayoutDict]:
    for glyph in obj:
        x0, y0, x1, y1 = glyph.bbox
        tstate = glyph.textstate
        gstate = glyph.gstate
        # apparently we can assert this?
        font = tstate.font
        assert font is not None
        glyph_x, glyph_y = apply_matrix_norm(glyph.ctm, tstate.glyph_offset)
        (a, b, c, d, e, f) = glyph.matrix
        if font.vertical:
            size = abs(tstate.fontsize * a)
        else:
            size = abs(tstate.fontsize * d)
        scaling = tstate.scaling * 0.01  # FIXME: unnecessary?
        upright = a * d * scaling > 0 and b * c <= 0

        yield LayoutDict(
            object_type="char",
            x0=x0,
            y0=y0,
            x1=x1,
            y1=y1,
            size=size,
            upright=upright,
            text=glyph.text,
            cid=glyph.cid,
            fontname=font.fontname,
            glyph_offset_x=glyph_x,
            glyph_offset_y=glyph_y,
            render_mode=tstate.render_mode,
            dash_pattern=gstate.dash.dash,
            dash_phase=gstate.dash.phase,
            stroking_colorspace=gstate.scs.name,
            stroking_color=gstate.scolor.values,
            stroking_pattern=gstate.scolor.pattern,
            non_stroking_colorspace=gstate.ncs.name,
            non_stroking_color=gstate.ncolor.values,
            non_stroking_pattern=gstate.ncolor.pattern,
            mcid=None if obj.mcs is None else obj.mcs.mcid,
            tag=None if obj.mcs is None else obj.mcs.tag,
            page_index=0,
            page_label="0",
        )


@process_object.register
def _(obj: XObjectObject) -> Iterator[LayoutDict]:
    for child in obj:
        for layout in process_object(child):
            layout["xobjid"] = obj.xobjid
            yield layout


def extract_page(page: Page) -> List[LayoutDict]:
    """Extract LayoutDict items from a Page."""
    page_layout = []
    for obj in page:
        for dic in process_object(obj):
            dic = cast(LayoutDict, dic)  # ugh
            dic["page_index"] = page.page_idx
            dic["page_label"] = page.label
            page_layout.append(dic)
    return page_layout


def extract(
    path: Path,
    space: DeviceSpace = "screen",
    max_workers: Union[int, None] = 1,
    mp_context: Union[BaseContext, None] = None,
) -> Iterator[LayoutDict]:
    """Extract LayoutDict items from a document."""
    if max_workers is None:
        max_workers = multiprocessing.cpu_count()
    with playa.open(
        path,
        max_workers=max_workers,
        mp_context=mp_context,
    ) as pdf:
        for page in pdf.pages.map(extract_page):
            yield from page
