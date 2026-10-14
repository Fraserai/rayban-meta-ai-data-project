from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK, WD_LINE_SPACING, WD_TAB_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor


OUT = Path(__file__).with_name("PROJECT_STATUS_WHERE_WE_ARE_2026-08-26.docx")

# decision_memo preset (standard_business_brief base) resolved token map
FONT = "Arial"
INK = "1F2937"
BLACK = "000000"
BLUE = "2E74B5"
DARK_BLUE = "1F4D78"
NAVY = "16324F"
MUTED = "667085"
PALE_BLUE = "EAF2F8"
LIGHT_GRAY = "F2F4F7"
PALE_GREEN = "E9F5EC"
GREEN = "236B3C"
PALE_AMBER = "FFF4D6"
AMBER = "7A5A00"
PALE_RED = "FDECEC"
RED = "9B1C1C"
WHITE = "FFFFFF"


def set_run_font(run, size=11, color=INK, bold=False, italic=False, all_caps=False):
    run.font.name = FONT
    run._element.get_or_add_rPr().rFonts.set(qn("w:ascii"), FONT)
    run._element.get_or_add_rPr().rFonts.set(qn("w:hAnsi"), FONT)
    run.font.size = Pt(size)
    run.font.color.rgb = RGBColor.from_string(color)
    run.bold = bold
    run.italic = italic
    if all_caps:
        run.font.all_caps = True
    return run


def set_cell_shading(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = tc_pr.find(qn("w:shd"))
    if shd is None:
        shd = OxmlElement("w:shd")
        tc_pr.append(shd)
    shd.set(qn("w:fill"), fill)


def set_cell_margins(cell, top=80, start=120, bottom=80, end=120):
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_mar = tc_pr.first_child_found_in("w:tcMar")
    if tc_mar is None:
        tc_mar = OxmlElement("w:tcMar")
        tc_pr.append(tc_mar)
    for side, value in (("top", top), ("start", start), ("bottom", bottom), ("end", end)):
        node = tc_mar.find(qn(f"w:{side}"))
        if node is None:
            node = OxmlElement(f"w:{side}")
            tc_mar.append(node)
        node.set(qn("w:w"), str(value))
        node.set(qn("w:type"), "dxa")


def set_table_borders(table, color="D0D5DD", size=6, inside=True):
    tbl_pr = table._tbl.tblPr
    borders = tbl_pr.first_child_found_in("w:tblBorders")
    if borders is None:
        borders = OxmlElement("w:tblBorders")
        tbl_pr.append(borders)
    edges = ["top", "left", "bottom", "right"]
    if inside:
        edges += ["insideH", "insideV"]
    for edge in edges:
        tag = borders.find(qn(f"w:{edge}"))
        if tag is None:
            tag = OxmlElement(f"w:{edge}")
            borders.append(tag)
        tag.set(qn("w:val"), "single")
        tag.set(qn("w:sz"), str(size))
        tag.set(qn("w:space"), "0")
        tag.set(qn("w:color"), color)


def set_table_geometry(table, widths, indent=120):
    assert sum(widths) == 9360, widths
    table.autofit = False
    table.alignment = WD_TABLE_ALIGNMENT.LEFT
    tbl_pr = table._tbl.tblPr
    tbl_w = tbl_pr.first_child_found_in("w:tblW")
    if tbl_w is None:
        tbl_w = OxmlElement("w:tblW")
        tbl_pr.append(tbl_w)
    tbl_w.set(qn("w:w"), "9360")
    tbl_w.set(qn("w:type"), "dxa")

    tbl_ind = tbl_pr.first_child_found_in("w:tblInd")
    if tbl_ind is None:
        tbl_ind = OxmlElement("w:tblInd")
        tbl_pr.append(tbl_ind)
    tbl_ind.set(qn("w:w"), str(indent))
    tbl_ind.set(qn("w:type"), "dxa")

    grid = table._tbl.tblGrid
    for child in list(grid):
        grid.remove(child)
    for width in widths:
        col = OxmlElement("w:gridCol")
        col.set(qn("w:w"), str(width))
        grid.append(col)

    for row in table.rows:
        tr_pr = row._tr.get_or_add_trPr()
        cant_split = OxmlElement("w:cantSplit")
        tr_pr.append(cant_split)
        for idx, cell in enumerate(row.cells):
            cell.width = Inches(widths[idx] / 1440)
            tc_pr = cell._tc.get_or_add_tcPr()
            tc_w = tc_pr.find(qn("w:tcW"))
            if tc_w is None:
                tc_w = OxmlElement("w:tcW")
                tc_pr.append(tc_w)
            tc_w.set(qn("w:w"), str(widths[idx]))
            tc_w.set(qn("w:type"), "dxa")
            set_cell_margins(cell)
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER


def set_repeat_table_header(row):
    tr_pr = row._tr.get_or_add_trPr()
    tbl_header = OxmlElement("w:tblHeader")
    tbl_header.set(qn("w:val"), "true")
    tr_pr.append(tbl_header)


def set_paragraph_border_bottom(paragraph, color="98A2B3", size=10, space=6):
    p_pr = paragraph._p.get_or_add_pPr()
    p_bdr = p_pr.find(qn("w:pBdr"))
    if p_bdr is None:
        p_bdr = OxmlElement("w:pBdr")
        p_pr.append(p_bdr)
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), str(size))
    bottom.set(qn("w:space"), str(space))
    bottom.set(qn("w:color"), color)
    p_bdr.append(bottom)


def add_hyperlink(paragraph, text, url, color=BLUE):
    part = paragraph.part
    r_id = part.relate_to(url, "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink", is_external=True)
    hyperlink = OxmlElement("w:hyperlink")
    hyperlink.set(qn("r:id"), r_id)
    run = OxmlElement("w:r")
    r_pr = OxmlElement("w:rPr")
    r_fonts = OxmlElement("w:rFonts")
    r_fonts.set(qn("w:ascii"), FONT)
    r_fonts.set(qn("w:hAnsi"), FONT)
    r_pr.append(r_fonts)
    c = OxmlElement("w:color")
    c.set(qn("w:val"), color)
    r_pr.append(c)
    u = OxmlElement("w:u")
    u.set(qn("w:val"), "single")
    r_pr.append(u)
    sz = OxmlElement("w:sz")
    sz.set(qn("w:val"), "20")
    r_pr.append(sz)
    run.append(r_pr)
    t = OxmlElement("w:t")
    t.text = text
    run.append(t)
    hyperlink.append(run)
    paragraph._p.append(hyperlink)


def next_abstract_num_id(numbering):
    ids = [int(x.get(qn("w:abstractNumId"))) for x in numbering.findall(qn("w:abstractNum"))]
    return max(ids, default=-1) + 1


def next_num_id(numbering):
    ids = [int(x.get(qn("w:numId"))) for x in numbering.findall(qn("w:num"))]
    return max(ids, default=0) + 1


def create_num_style(doc, kind):
    numbering = doc.part.numbering_part.element
    abstract_id = next_abstract_num_id(numbering)
    num_id = next_num_id(numbering)

    abstract = OxmlElement("w:abstractNum")
    abstract.set(qn("w:abstractNumId"), str(abstract_id))
    multi = OxmlElement("w:multiLevelType")
    multi.set(qn("w:val"), "singleLevel")
    abstract.append(multi)
    lvl = OxmlElement("w:lvl")
    lvl.set(qn("w:ilvl"), "0")
    start = OxmlElement("w:start")
    start.set(qn("w:val"), "1")
    lvl.append(start)
    num_fmt = OxmlElement("w:numFmt")
    num_fmt.set(qn("w:val"), "bullet" if kind == "bullet" else "decimal")
    lvl.append(num_fmt)
    lvl_text = OxmlElement("w:lvlText")
    lvl_text.set(qn("w:val"), "•" if kind == "bullet" else "%1.")
    lvl.append(lvl_text)
    suff = OxmlElement("w:suff")
    suff.set(qn("w:val"), "tab")
    lvl.append(suff)
    p_pr = OxmlElement("w:pPr")
    tabs = OxmlElement("w:tabs")
    tab = OxmlElement("w:tab")
    tab.set(qn("w:val"), "num")
    tab.set(qn("w:pos"), "720")
    tabs.append(tab)
    p_pr.append(tabs)
    ind = OxmlElement("w:ind")
    ind.set(qn("w:left"), "720")
    ind.set(qn("w:hanging"), "360")
    p_pr.append(ind)
    spacing = OxmlElement("w:spacing")
    spacing.set(qn("w:after"), "160")
    spacing.set(qn("w:line"), "280")
    spacing.set(qn("w:lineRule"), "auto")
    p_pr.append(spacing)
    lvl.append(p_pr)
    abstract.append(lvl)
    numbering.append(abstract)

    num = OxmlElement("w:num")
    num.set(qn("w:numId"), str(num_id))
    abstract_num_id = OxmlElement("w:abstractNumId")
    abstract_num_id.set(qn("w:val"), str(abstract_id))
    num.append(abstract_num_id)
    numbering.append(num)
    return num_id


def apply_num(paragraph, num_id):
    p_pr = paragraph._p.get_or_add_pPr()
    num_pr = p_pr.find(qn("w:numPr"))
    if num_pr is None:
        num_pr = OxmlElement("w:numPr")
        p_pr.append(num_pr)
    ilvl = OxmlElement("w:ilvl")
    ilvl.set(qn("w:val"), "0")
    num_id_el = OxmlElement("w:numId")
    num_id_el.set(qn("w:val"), str(num_id))
    num_pr.append(ilvl)
    num_pr.append(num_id_el)


def add_bullet(doc, num_id, text, bold_lead=None):
    p = doc.add_paragraph()
    apply_num(p, num_id)
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.line_spacing = 1.167
    if bold_lead and text.startswith(bold_lead):
        set_run_font(p.add_run(bold_lead), bold=True)
        set_run_font(p.add_run(text[len(bold_lead):]))
    else:
        set_run_font(p.add_run(text))
    return p


def add_numbered(doc, num_id, lead, body):
    p = doc.add_paragraph()
    apply_num(p, num_id)
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.line_spacing = 1.167
    set_run_font(p.add_run(lead), bold=True, color=NAVY)
    set_run_font(p.add_run(body))
    return p


def add_body(doc, text, bold_lead=None, color=INK, italic=False, after=6):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(after)
    p.paragraph_format.line_spacing = 1.10
    if bold_lead and text.startswith(bold_lead):
        set_run_font(p.add_run(bold_lead), bold=True, color=color)
        set_run_font(p.add_run(text[len(bold_lead):]), color=color, italic=italic)
    else:
        set_run_font(p.add_run(text), color=color, italic=italic)
    return p


def add_heading(doc, text, level=1):
    p = doc.add_paragraph(style=f"Heading {level}")
    p.paragraph_format.keep_with_next = True
    set_run_font(p.add_run(text), size={1: 16, 2: 13, 3: 12}[level], color={1: BLUE, 2: BLUE, 3: DARK_BLUE}[level], bold=True)
    return p


def add_callout(doc, label, text, fill=PALE_BLUE, label_color=NAVY, border="B6CCE2"):
    table = doc.add_table(rows=1, cols=1)
    set_table_geometry(table, [9360])
    set_table_borders(table, color=border, size=8, inside=False)
    cell = table.cell(0, 0)
    set_cell_shading(cell, fill)
    set_cell_margins(cell, top=150, bottom=150, start=180, end=180)
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.10
    set_run_font(p.add_run(f"{label}: "), size=11, color=label_color, bold=True)
    set_run_font(p.add_run(text), size=11, color=INK)
    doc.add_paragraph().paragraph_format.space_after = Pt(0)
    return table


def add_status_table(doc):
    table = doc.add_table(rows=1, cols=3)
    set_table_geometry(table, [2200, 1900, 5260])
    set_table_borders(table)
    headers = ["Workstream", "Current status", "What it means"]
    for idx, text in enumerate(headers):
        cell = table.rows[0].cells[idx]
        set_cell_shading(cell, NAVY)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        set_run_font(p.add_run(text), size=9.5, color=WHITE, bold=True)
    set_repeat_table_header(table.rows[0])
    rows = [
        ("Phase 1 due diligence", "COMPLETE", "The technical, platform, commercial, privacy and competitive questions were researched and documented."),
        ("Production application", "NOT STARTED", "No production code, application scaffold or irreversible architecture decision has been made."),
        ("Meta commercial rights", "UNRESOLVED — CRITICAL", "The reviewed public terms appear incompatible with selling or licensing SDK-derived datasets; written Meta and legal clearance is required."),
        ("Real-device reliability", "PLAUSIBLE — UNTESTED", "Live video and wearer narration are exposed, but useful-duration capture, A/V drift, thermal load and dropouts have not been measured."),
        ("Buyer value", "NOT VALIDATED", "No qualified buyer has yet defined an evaluation task or demonstrated that enriched human demonstrations improve its model or workflow."),
        ("Architecture and procurement", "DEFERRED", "The project remains hardware-agnostic and avoids committing spend until the rights and demand gates have a credible path."),
    ]
    status_styles = {
        "COMPLETE": (PALE_GREEN, GREEN),
        "NOT STARTED": (LIGHT_GRAY, MUTED),
        "UNRESOLVED — CRITICAL": (PALE_RED, RED),
        "PLAUSIBLE — UNTESTED": (PALE_AMBER, AMBER),
        "NOT VALIDATED": (PALE_RED, RED),
        "DEFERRED": (LIGHT_GRAY, MUTED),
    }
    for row_idx, (area, status, meaning) in enumerate(rows, 1):
        cells = table.add_row().cells
        for cell in cells:
            set_cell_margins(cell, top=110, bottom=110, start=120, end=120)
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        set_cell_shading(cells[1], status_styles[status][0])
        for idx, text in enumerate((area, status, meaning)):
            p = cells[idx].paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.05
            set_run_font(
                p.add_run(text),
                size=9.2 if idx != 1 else 8.8,
                color=status_styles[status][1] if idx == 1 else INK,
                bold=idx in (0, 1),
            )
        if row_idx % 2 == 0:
            set_cell_shading(cells[0], "FAFBFC")
            set_cell_shading(cells[2], "FAFBFC")
    set_table_geometry(table, [2200, 1900, 5260])
    return table


def add_comparison_table(doc):
    table = doc.add_table(rows=1, cols=2)
    set_table_geometry(table, [4680, 4680])
    set_table_borders(table)
    for idx, text in enumerate(("Framing to avoid", "More defensible product thesis")):
        cell = table.rows[0].cells[idx]
        set_cell_shading(cell, PALE_RED if idx == 0 else PALE_GREEN)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        set_run_font(p.add_run(text), size=10, color=RED if idx == 0 else GREEN, bold=True)
    pairs = [
        ("“Ray-Ban footage for robots.”", "A rights-cleared, hardware-agnostic demonstration-data and enrichment system."),
        ("Raw first-person hours as the product.", "Buyer-designed task packs with provenance, annotations, review and measurable downstream utility."),
        ("RGB video as direct robot supervision.", "Video-language and task-understanding data, augmented with exocentric, pose, contact or robot telemetry where required."),
        ("Scale contributors before proving demand.", "Secure one design buyer, one task and one acceptance test before scaling collection."),
    ]
    for left, right in pairs:
        cells = table.add_row().cells
        for idx, text in enumerate((left, right)):
            p = cells[idx].paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.05
            set_run_font(p.add_run(text), size=9.5, color=INK)
    set_table_geometry(table, [4680, 4680])
    return table


def add_action_table(doc):
    table = doc.add_table(rows=1, cols=3)
    set_table_geometry(table, [950, 4700, 3710])
    set_table_borders(table)
    for idx, text in enumerate(("Order", "Action", "Exit evidence")):
        cell = table.rows[0].cells[idx]
        set_cell_shading(cell, NAVY)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if idx == 0 else WD_ALIGN_PARAGRAPH.LEFT
        set_run_font(p.add_run(text), size=9.5, color=WHITE, bold=True)
    actions = [
        ("1", "Prepare a one-page data-flow and revenue-model brief for Meta and Australian counsel.", "Written answer on commercial AI-training use, sale/licensing, derived artefacts, third-party delivery, retention/deletion and distribution scale."),
        ("2", "Recruit one qualified robotics or embodied-AI buyer to define one task, schema and evaluation.", "Named design partner, agreed acceptance criteria and a commitment to assess a blinded sample."),
        ("3", "Refresh the SDK, repositories, release notes and authenticated platform terms immediately before any build decision.", "Dated change log showing whether DAT 0.8.0 conclusions still hold."),
        ("4", "Only after Gates 0 and buyer discovery show a credible path, approve the controlled iOS capture experiment.", "A signed experiment brief, consent protocol, hardware list, metrics and stop conditions."),
    ]
    for idx_row, (order, action, evidence) in enumerate(actions, 1):
        cells = table.add_row().cells
        if idx_row % 2 == 0:
            for cell in cells:
                set_cell_shading(cell, "FAFBFC")
        for idx, text in enumerate((order, action, evidence)):
            p = cells[idx].paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.05
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if idx == 0 else WD_ALIGN_PARAGRAPH.LEFT
            set_run_font(p.add_run(text), size=9.2, color=INK, bold=idx == 0)
    set_table_geometry(table, [950, 4700, 3710])
    return table


def style_document(doc):
    section = doc.sections[0]
    section.page_width = Inches(8.5)
    section.page_height = Inches(11)
    section.top_margin = Inches(1)
    section.right_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1)
    section.header_distance = Inches(0.492)
    section.footer_distance = Inches(0.492)

    normal = doc.styles["Normal"]
    normal.font.name = FONT
    normal._element.rPr.rFonts.set(qn("w:ascii"), FONT)
    normal._element.rPr.rFonts.set(qn("w:hAnsi"), FONT)
    normal.font.size = Pt(11)
    normal.font.color.rgb = RGBColor.from_string(INK)
    normal.paragraph_format.space_before = Pt(0)
    normal.paragraph_format.space_after = Pt(6)
    normal.paragraph_format.line_spacing = 1.10

    for level, size, color, before, after in (
        (1, 16, BLUE, 12, 6),
        (2, 13, BLUE, 10, 5),
        (3, 12, DARK_BLUE, 8, 4),
    ):
        style = doc.styles[f"Heading {level}"]
        style.font.name = FONT
        style._element.rPr.rFonts.set(qn("w:ascii"), FONT)
        style._element.rPr.rFonts.set(qn("w:hAnsi"), FONT)
        style.font.size = Pt(size)
        style.font.bold = True
        style.font.color.rgb = RGBColor.from_string(color)
        style.paragraph_format.space_before = Pt(before)
        style.paragraph_format.space_after = Pt(after)
        style.paragraph_format.keep_with_next = True


def add_header_footer(section):
    header_p = section.header.paragraphs[0]
    header_p.paragraph_format.space_after = Pt(0)
    header_p.paragraph_format.tab_stops.add_tab_stop(Inches(6.5), WD_TAB_ALIGNMENT.RIGHT)
    set_run_font(header_p.add_run("RAY-BAN META AI DATA PROJECT"), size=8.5, color=MUTED, bold=True, all_caps=True)
    header_p.add_run("\t")
    set_run_font(header_p.add_run("STATUS BRIEF | 26 AUG 2026"), size=8.5, color=MUTED, bold=True)

    footer_p = section.footer.paragraphs[0]
    footer_p.paragraph_format.space_before = Pt(0)
    footer_p.paragraph_format.space_after = Pt(0)
    footer_p.paragraph_format.tab_stops.add_tab_stop(Inches(6.5), WD_TAB_ALIGNMENT.RIGHT)
    set_run_font(footer_p.add_run("Internal working document — evidence baseline 31 July 2026"), size=8, color=MUTED)
    footer_p.add_run("\t")
    set_run_font(footer_p.add_run("|  Page "), size=8, color=MUTED)
    fld_char1 = OxmlElement("w:fldChar")
    fld_char1.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = " PAGE "
    fld_char2 = OxmlElement("w:fldChar")
    fld_char2.set(qn("w:fldCharType"), "end")
    run = OxmlElement("w:r")
    run.append(fld_char1)
    run.append(instr)
    run.append(fld_char2)
    footer_p._p.append(run)


def add_page_break(doc):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(0)
    p.add_run().add_break(WD_BREAK.PAGE)


def build():
    doc = Document()
    doc.settings.odd_and_even_pages_header_footer = False
    style_document(doc)
    add_header_footer(doc.sections[0])
    bullet_id = create_num_style(doc, "bullet")
    decimal_id = create_num_style(doc, "decimal")

    # Page 1: memo masthead and status readout
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(3)
    set_run_font(p.add_run("PROJECT STATUS BRIEF"), size=10, color=BLUE, bold=True, all_caps=True)

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(3)
    set_run_font(p.add_run("Ray-Ban Meta AI Data Project"), size=25, color=BLACK, bold=True)

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(14)
    set_run_font(p.add_run("Where we are now, what is blocked, and what should happen next"), size=13.5, color=MUTED)

    metadata = [
        ("To", "Founding team"),
        ("Date", "26 August 2026, Australia/Brisbane"),
        ("Phase", "Phase 1 complete — Phase 2 not authorised"),
        ("Evidence baseline", "31 July 2026; Meta Wearables DAT 0.8.0"),
        ("Decision posture", "Hold production build pending platform/legal clearance and buyer validation"),
    ]
    for label, value in metadata:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.0
        set_run_font(p.add_run(f"{label}: "), size=10.2, color=BLACK, bold=True)
        set_run_font(p.add_run(value), size=10.2, color=BLACK)
    rule = doc.add_paragraph()
    rule.paragraph_format.space_before = Pt(2)
    rule.paragraph_format.space_after = Pt(10)
    set_paragraph_border_bottom(rule, color="98A2B3", size=10, space=6)

    add_callout(
        doc,
        "Bottom line",
        "The capture concept is technically plausible in a controlled prototype, but the business is not yet cleared to operate on Meta’s public developer platform and buyer value has not been demonstrated. The correct status is ‘research complete, build on hold’ — not ‘ready to develop.’",
        fill=PALE_BLUE,
    )

    add_heading(doc, "1. Current project position", 1)
    add_status_table(doc)
    add_body(
        doc,
        "This is a deliberate pause, not lost momentum. Phase 1 did its job: it found the two questions that could invalidate the business before we spent meaningfully — rights to commercialise the data and evidence that a buyer benefits from it.",
        after=0,
    )

    add_page_break(doc)

    # Page 2: established evidence
    add_heading(doc, "2. What Phase 1 established", 1)
    add_heading(doc, "The hardware and SDK are narrower than the consumer marketing", 2)
    add_bullet(doc, bullet_id, "DAT 0.8.0 is a Developer Preview mobile SDK. The third-party application runs on the paired iPhone or Android phone; public evidence did not establish a general on-glasses application runtime or supported post-hoc import of consumer-stored recordings. [1–4]")
    add_bullet(doc, bullet_id, "Developer video is documented up to portrait 720 × 1280 at a requested maximum 30 fps, with adaptive degradation. This must not be presented as the consumer 3K recording mode. [1, 2, 3, 8]")
    add_bullet(doc, bullet_id, "Wearer audio is beamformed Bluetooth HFP at 8 kHz mono. It may support narration and transcription, but it is not full-fidelity environmental audio or raw access to the consumer microphone array. [1, 5]")
    add_bullet(doc, bullet_id, "The SDK exposes live camera/still capture plus session, stream, permission, thermal and critical power/error events. The reviewed public surface did not establish battery percentage, depth, gaze, calibrated pose, IMU, raw microphone channels or robot telemetry. [1–3]")
    add_bullet(doc, bullet_id, "Current release paths in the reviewed material were invite-only; iOS App Store distribution was explicitly unsupported. A general public Android route was not established. [1, 6]")

    add_heading(doc, "The data can be useful — but it is not direct robot-action supervision", 2)
    add_body(doc, "First-person RGB/audio can support transcription, procedural segmentation, object/tool recognition, hand-object events, action labels, narration alignment, error/recovery examples, outcome labels, privacy filtering and human-reviewed quality scores.")
    add_body(doc, "However, the capture lacks the embodiment signals used for robot behaviour learning: joint state, commanded actions, gripper state, force, tactile feedback, calibrated 3D pose and contact. Its most defensible initial uses are video-language pretraining, task understanding, procedural reasoning and error/recovery enrichment — unless supplementary sensors or robot data are added.")

    add_heading(doc, "The highest-priority problem is commercial permission", 2)
    add_callout(
        doc,
        "Critical inference — not legal advice",
        "The reviewed Meta Wearables Developer Terms define Technology Data broadly, including derived data, and prohibit selling or licensing it. On an ordinary reading, commercial delivery of DAT-captured video, annotations or training packages is likely outside the public licence. Contributor consent alone cannot be assumed to override that restriction. Written Meta clarification and qualified legal advice are required. [1, 7]",
        fill=PALE_RED,
        label_color=RED,
        border="E6A5A5",
    )

    add_page_break(doc)

    # Page 3: what is not yet proven and cofounder challenge
    add_heading(doc, "3. What remains unknown or unvalidated", 1)
    add_numbered(doc, decimal_id, "Commercial rights. ", "Will Meta provide written permission or a separate agreement for commercial AI training, sale/licensing of raw and derived artefacts, third-party delivery and the required tester/distribution scale?")
    add_numbered(doc, decimal_id, "Capture reliability. ", "Can the glasses and phone deliver useful-duration recordings with bounded A/V offset and drift, acceptable compression, stable HFP audio, manageable heat/battery use and recoverable interruptions?")
    add_numbered(doc, decimal_id, "Buyer value. ", "Which specific robotics or embodied-AI task benefits from this data, what schema is required, and can a blinded evaluation show model lift or material labelling/time savings?")
    add_numbered(doc, decimal_id, "Rights operations. ", "Can contributor, bystander, workplace, site, privacy, deletion and cross-border obligations be met without making collection uneconomic?")
    add_numbered(doc, decimal_id, "Embodiment bridge. ", "What minimum supplementary signals — exocentric video, 6-DoF tool pose, gripper/contact data, environment sensors or paired robot episodes — are required for the buyer’s intended use?")

    add_heading(doc, "4. Cofounder assessment: refine the thesis before building", 1)
    add_comparison_table(doc)
    add_body(
        doc,
        "The moat cannot be the glasses. Hardware access is vendor-controlled, capture quality is constrained, and competitors already collect egocentric demonstrations. A defensible moat would be the rights and provenance layer, task design, error/recovery coverage, cross-sensor alignment, review quality and a buyer-facing evaluation that proves utility.",
        after=0,
    )

    add_page_break(doc)

    # Page 4: gated validation path
    add_heading(doc, "5. The gated path from research to a real project", 1)
    add_heading(doc, "Gate 0 — Platform and legal clearance", 2)
    add_body(doc, "Send Meta the exact data flow and revenue model, then obtain Australian privacy, recording and workplace advice. The written response must cover commercial AI-training use, derived annotations/models, buyer delivery, retention/deletion, service providers and release-channel scale.")
    add_callout(doc, "Stop condition", "If there is no written path to commercial use, do not build around DAT. Test the broader thesis with a different, rights-cleared capture endpoint.", fill=PALE_RED, label_color=RED, border="E6A5A5")

    add_heading(doc, "Gate 1 — Controlled capture reliability", 2)
    add_body(doc, "Only after Phase 2 approval: one Ray-Ban Meta Gen 2, one current iPhone, a bystander-free room, approximately 30 episodes across five visible tabletop tasks, and successful, mistake and recovery conditions. Run 5-, 10- and 20-minute sessions at more than one stream setting.")
    add_bullet(doc, bullet_id, "Measure delivered video quality, frame gaps, hand/tool visibility, start latency, storage, battery, thermal state and interruption recovery.")
    add_bullet(doc, bullet_id, "Use visible/audible sync events at the beginning and end; measure initial A/V offset and drift rather than assuming synchronisation.")
    add_bullet(doc, bullet_id, "Treat ≥95% completed episodes, no unexplained gaps in accepted episodes and corrected median A/V alignment within 100 ms as provisional engineering gates only; the buyer must approve final acceptance criteria.")

    add_heading(doc, "Gate 2 — Enrichment and buyer value", 2)
    add_body(doc, "For one buyer-defined task, create a small package containing transcript, atomic actions, objects/tools, hand-object events, a mistake/recovery branch, outcome evidence, technical quality scores and provenance. Double-annotate a subset and expose disagreement.")
    add_callout(doc, "Pass condition", "A qualified buyer confirms the schema is usable and demonstrates, or commits to an agreed test showing, measurable downstream lift or meaningful cost/time reduction.", fill=PALE_GREEN, label_color=GREEN, border="A7D2B1")

    add_page_break(doc)

    # Page 5: operating plan and decision
    add_heading(doc, "6. Immediate operating plan", 1)
    add_action_table(doc)

    add_heading(doc, "7. What we should not do yet", 1)
    add_bullet(doc, bullet_id, "Do not write a production capture application, contributor marketplace or large annotation platform.")
    add_bullet(doc, bullet_id, "Do not purchase a fleet of glasses or recruit contributors before permission, distribution scale and buyer demand are credible.")
    add_bullet(doc, bullet_id, "Do not describe consumer 3K recording, multi-microphone audio or native device features as developer-accessible SDK capabilities.")
    add_bullet(doc, bullet_id, "Do not sell first-person RGB/audio as robot control data; label the missing depth, pose, force, tactile and robot-state signals explicitly.")
    add_bullet(doc, bullet_id, "Do not treat face/voice redaction as a substitute for lawful collection, site permission or informed consent.")

    add_heading(doc, "8. Decision requested", 1)
    add_callout(
        doc,
        "Recommended decision",
        "Keep the project in Phase 1 close-out. Authorise only the Meta/legal clarification brief and buyer discovery. Do not authorise a production build. Prepare the controlled iOS experiment on paper, but execute it only when Gate 0 and buyer discovery establish a credible path.",
        fill=PALE_BLUE,
    )

    add_page_break(doc)

    add_heading(doc, "Evidence basis and freshness", 1)
    add_body(doc, "This memo summarises the detailed Phase 1 report prepared on 31 July 2026. It is a project-status document, not a live 26 August re-review of Meta’s SDK, repositories or terms. Because DAT was a fast-moving Developer Preview, all time-sensitive platform claims must be rechecked before procurement or Phase 2.")
    add_body(doc, "Workspace note: the original project folder is currently on the Desktop, while the saved workspace configuration still references its former Documents location. This brief is saved beside the source report.", italic=True, color=MUTED)

    add_heading(doc, "Key sources", 2)
    sources = [
        ("[1] Detailed Phase 1 technical research and feasibility assessment — local project report, prepared 31 July 2026.", None),
        ("[2] Meta Wearables DAT for iOS — official repository", "https://github.com/facebook/meta-wearables-dat-ios"),
        ("[3] Meta Wearables DAT for Android — official repository", "https://github.com/facebook/meta-wearables-dat-android"),
        ("[4] Meta staff discussion on app execution and stored media", "https://github.com/facebook/meta-wearables-dat-android/discussions/20"),
        ("[5] Meta developer documentation — microphones and speakers", "https://wearables.developer.meta.com/docs/develop/dat/microphones-and-speakers/"),
        ("[6] Meta developer documentation — release channels", "https://wearables.developer.meta.com/docs/develop/dat/set-up-release-channels/"),
        ("[7] Meta Wearables Developer Terms", "https://wearables.developer.meta.com/terms"),
        ("[8] Meta developer documentation — iOS/Android integration guides", "https://wearables.developer.meta.com/docs/develop/dat/build-integration-ios/"),
    ]
    for text, url in sources:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.0
        if url:
            set_run_font(p.add_run(text + ": "), size=9.5, color=INK)
            add_hyperlink(p, url, url)
        else:
            set_run_font(p.add_run(text), size=9.5, color=INK)
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(0)
    set_run_font(p.add_run("Access date for linked sources used in the underlying report: 31 July 2026, unless the report states otherwise."), size=9, color=MUTED, italic=True)

    add_page_break(doc)

    # Required closing classification
    add_heading(doc, "Verified facts", 1)
    add_bullet(doc, bullet_id, "Phase 1 research is complete and the full cited report exists; production code and irreversible architecture decisions have not been made.")
    add_bullet(doc, bullet_id, "The 31 July evidence established Developer Preview live video and wearer-audio access, but with materially narrower developer capabilities than consumer marketing implies.")
    add_bullet(doc, bullet_id, "No real-device reliability experiment or buyer-defined evaluation has yet been completed.")

    add_heading(doc, "Assumptions", 1)
    add_bullet(doc, bullet_id, "DAT-captured media and its annotations would likely be treated as Technology Data; this remains a legal/platform inference requiring written confirmation.")
    add_bullet(doc, bullet_id, "The broader hardware-agnostic enrichment thesis may remain viable even if Meta’s public platform cannot support the commercial model.")

    add_heading(doc, "Open questions", 1)
    add_bullet(doc, bullet_id, "Will Meta grant permission or an appropriate agreement, and at what distribution scale?")
    add_bullet(doc, bullet_id, "Can one buyer-defined task show measurable value from enriched first-person demonstrations?")
    add_bullet(doc, bullet_id, "Can useful-duration A/V capture meet quality, thermal, battery, interruption and consent requirements?")

    add_heading(doc, "Recommended next step", 1)
    add_body(doc, "Prepare the one-page Meta/legal data-flow and revenue-model brief and secure one buyer discovery partner. Keep production coding on hold. If both paths are credible, explicitly approve Phase 2 and run the smallest controlled iOS experiment.", bold_lead="Prepare the one-page Meta/legal data-flow and revenue-model brief")

    core = doc.core_properties
    core.title = "Ray-Ban Meta AI Data Project — Where We Are Now"
    core.subject = "Phase 1 project status, risks and next decision gates"
    core.author = "Technical co-founder"
    core.keywords = "Ray-Ban Meta, wearables, DAT, technical due diligence, AI training data, robotics"
    core.comments = "Status brief based on the 31 July 2026 Phase 1 report."

    doc.save(OUT)
    print(OUT)


if __name__ == "__main__":
    build()
