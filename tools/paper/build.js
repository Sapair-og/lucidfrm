// Build docs/LucidForm_Paper_Draft.docx from docs/paper-draft.md in IEEE conference layout:
// A4, one-column title + author block, then two columns; Times New Roman.
//
//   node tools/paper/build.js
//
// The markdown is the source of truth; this script only typesets it. It understands the
// subset the draft uses: #/##/### headings, paragraphs with **bold**, *italic* and `code`,
// numbered lists, pipe tables, fenced code blocks, and the title/author preamble.

const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, AlignmentType, SectionType, Table, TableRow,
  TableCell, WidthType, BorderStyle, ShadingType, LevelFormat,
} = require("docx");

const ROOT = path.resolve(__dirname, "..", "..");
const SRC = path.join(ROOT, "docs", "paper-draft.md");
const OUT = path.join(ROOT, "docs", "LucidForm_Paper_Draft.docx");

const FONT = "Times New Roman";
const PAGE = { width: 11909, height: 16834 };
const MARGIN = { top: 1080, bottom: 1440, left: 900, right: 900 };
const GAP = 360;
const COL_W = Math.floor((PAGE.width - MARGIN.left - MARGIN.right - GAP) / 2);
const PT = (n) => n * 2; // docx sizes are half-points

// ---------------------------------------------------------------- inline markup

function runs(text, base = {}) {
  const out = [];
  const re = /(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`)/g;
  let last = 0;
  let m;
  while ((m = re.exec(text))) {
    if (m.index > last) out.push(new TextRun({ text: text.slice(last, m.index), font: FONT, ...base }));
    const tok = m[0];
    if (tok.startsWith("**")) out.push(new TextRun({ text: tok.slice(2, -2), bold: true, font: FONT, ...base }));
    else if (tok.startsWith("`")) out.push(new TextRun({ text: tok.slice(1, -1), font: "Courier New", ...base, size: (base.size || PT(10)) - 2 }));
    else out.push(new TextRun({ text: tok.slice(1, -1), italics: true, font: FONT, ...base }));
    last = m.index + tok.length;
  }
  if (last < text.length) out.push(new TextRun({ text: text.slice(last), font: FONT, ...base }));
  return out;
}

const body = (text, extra = {}) =>
  new Paragraph({
    children: runs(text, { size: PT(10) }),
    alignment: AlignmentType.JUSTIFIED,
    spacing: { after: 80, line: 240 },
    indent: { firstLine: 202 },
    ...extra,
  });

// ---------------------------------------------------------------- headings

function sectionHeading(text) {
  // "I. Introduction" -> "I. INTRODUCTION", centred small caps (IEEE level 1)
  return new Paragraph({
    children: [new TextRun({ text: text.toUpperCase(), font: FONT, size: PT(10), smallCaps: false })],
    alignment: AlignmentType.CENTER,
    spacing: { before: 200, after: 100 },
  });
}

function subHeading(text) {
  return new Paragraph({
    children: [new TextRun({ text, italics: true, font: FONT, size: PT(10) })],
    spacing: { before: 120, after: 60 },
  });
}

// ---------------------------------------------------------------- tables

function table(lines) {
  const rows = lines
    .filter((l) => !/^\|\s*-/.test(l))
    .map((l) => l.trim().replace(/^\||\|$/g, "").split("|").map((c) => c.trim()));
  const n = rows[0].length;
  const widths = Array(n).fill(Math.floor(COL_W / n));
  widths[n - 1] += COL_W - widths.reduce((a, b) => a + b, 0);
  const border = { style: BorderStyle.SINGLE, size: 4, color: "000000" };
  const borders = { top: border, bottom: border, left: border, right: border };
  return new Table({
    width: { size: COL_W, type: WidthType.DXA },
    columnWidths: widths,
    rows: rows.map(
      (cells, i) =>
        new TableRow({
          tableHeader: i === 0,
          children: cells.map(
            (c, j) =>
              new TableCell({
                width: { size: widths[j], type: WidthType.DXA },
                borders,
                shading: i === 0 ? { type: ShadingType.CLEAR, fill: "E7E6E6", color: "auto" } : undefined,
                margins: { top: 30, bottom: 30, left: 60, right: 60 },
                children: [new Paragraph({ children: runs(c, { size: PT(8), bold: i === 0 || undefined }) })],
              })
          ),
        })
    ),
  });
}

// ---------------------------------------------------------------- the document

function parse(md) {
  const lines = md.split(/\r?\n/);
  const hr = lines.map((l, i) => (l.trim() === "---" ? i : -1)).filter((i) => i >= 0);

  // Title: the default option in the preamble ("1. **...**").
  const titleLine = lines.slice(0, hr[0]).find((l) => /^1\.\s+\*\*/.test(l));
  const title = titleLine.match(/\*\*(.+?)\*\*/)[1];

  // Authors: blocks of lines between the first two rules.
  const authorBlocks = lines
    .slice(hr[0] + 1, hr[1])
    .join("\n")
    .trim()
    .split(/\n\s*\n/)
    .map((b) => b.split("\n").map((s) => s.trim()));

  const rest = lines.slice(hr[1] + 1);
  return { title, authorBlocks, rest };
}

function authorsTable(blocks) {
  const perRow = 3;
  const w = Math.floor((PAGE.width - MARGIN.left - MARGIN.right) / perRow);
  const none = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
  const borders = { top: none, bottom: none, left: none, right: none, insideHorizontal: none, insideVertical: none };
  const rows = [];
  for (let i = 0; i < blocks.length; i += perRow) {
    const slice = blocks.slice(i, i + perRow);
    while (slice.length < perRow) slice.push([]);
    rows.push(
      new TableRow({
        children: slice.map(
          (b) =>
            new TableCell({
              width: { size: w, type: WidthType.DXA },
              borders,
              children: (b.length ? b : [""]).map(
                (line, k) =>
                  new Paragraph({
                    alignment: AlignmentType.CENTER,
                    spacing: { after: k === b.length - 1 ? 160 : 0 },
                    children: [new TextRun({ text: line, font: FONT, size: PT(k === 0 ? 11 : 9), italics: k > 0 && k < b.length - 1 })],
                  })
              ),
            })
        ),
      })
    );
  }
  return new Table({ width: { size: w * perRow, type: WidthType.DXA }, columnWidths: Array(perRow).fill(w), borders, rows });
}

let listInstance = 0;

function bodyBlocks(rest) {
  const out = [];
  let i = 0;
  let inRefs = false;
  while (i < rest.length) {
    const line = rest[i];
    const t = line.trim();
    if (!t || t === "---") { i++; continue; }

    if (t.startsWith("```")) {
      const code = [];
      i++;
      while (i < rest.length && !rest[i].trim().startsWith("```")) code.push(rest[i++]);
      i++;
      code.forEach((c, k) =>
        out.push(new Paragraph({
          children: [new TextRun({ text: c.replace(/\t/g, "    ") || " ", font: "Courier New", size: PT(7) })],
          spacing: { after: k === code.length - 1 ? 120 : 0 },
        }))
      );
      continue;
    }
    if (t.startsWith("|")) {
      const tl = [];
      while (i < rest.length && rest[i].trim().startsWith("|")) tl.push(rest[i++]);
      out.push(table(tl));
      out.push(new Paragraph({ children: [], spacing: { after: 80 } }));
      continue;
    }
    if (t.startsWith("## ")) {
      const h = t.slice(3);
      inRefs = /^references$/i.test(h);
      out.push(sectionHeading(h));
      i++;
      continue;
    }
    if (t.startsWith("### ")) { out.push(subHeading(t.slice(4))); i++; continue; }

    if (t.startsWith("**Abstract**")) {
      out.push(new Paragraph({
        children: runs(t.replace(/^\*\*Abstract\*\*/, "Abstract"), { size: PT(9), bold: true, italics: true }),
        alignment: AlignmentType.JUSTIFIED, spacing: { after: 100 },
      }));
      i++;
      continue;
    }
    if (t.startsWith("**Keywords**")) {
      out.push(new Paragraph({
        children: runs(t.replace(/^\*\*Keywords\*\*/, "Keywords"), { size: PT(9), bold: true, italics: true }),
        alignment: AlignmentType.JUSTIFIED, spacing: { after: 160 },
      }));
      i++;
      continue;
    }
    if (/^\*\*(Table|Algorithm|Figure)\s/.test(t)) {
      // keepNext: a caption must not be stranded at the foot of a column away from its table.
      out.push(new Paragraph({ children: runs(t.replace(/\*\*/g, ""), { size: PT(8) }), alignment: AlignmentType.CENTER, spacing: { before: 80, after: 60 }, keepNext: true, keepLines: true }));
      i++;
      continue;
    }
    if (/^\d+\.\s/.test(t) && !inRefs) {
      listInstance += 1; // each list restarts at 1)
      while (i < rest.length && /^\d+\.\s/.test(rest[i].trim())) {
        out.push(new Paragraph({
          numbering: { reference: "numbered", level: 0, instance: listInstance },
          children: runs(rest[i].trim().replace(/^\d+\.\s+/, ""), { size: PT(10) }),
          alignment: AlignmentType.JUSTIFIED, spacing: { after: 40 },
        }));
        i++;
      }
      continue;
    }
    if (inRefs) {
      out.push(new Paragraph({ children: runs(t, { size: PT(8) }), alignment: AlignmentType.JUSTIFIED, spacing: { after: 40 }, indent: { left: 360, hanging: 360 } }));
      i++;
      continue;
    }
    // A paragraph may wrap across source lines.
    const para = [t];
    i++;
    while (i < rest.length && rest[i].trim() && !/^(#|\||```|\d+\.\s|\*\*(Table|Algorithm|Figure)|---)/.test(rest[i].trim())) para.push(rest[i++].trim());
    out.push(body(para.join(" ")));
  }
  return out;
}

const { title, authorBlocks, rest } = parse(fs.readFileSync(SRC, "utf8"));

const doc = new Document({
  styles: { default: { document: { run: { font: FONT, size: PT(10) } } } },
  numbering: {
    config: [{
      reference: "numbered",
      levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1)", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 360, hanging: 260 } } } }],
    }],
  },
  sections: [
    {
      properties: { page: { size: PAGE, margin: MARGIN } },
      children: [
        new Paragraph({ children: [new TextRun({ text: title, font: FONT, size: PT(22) })], alignment: AlignmentType.CENTER, spacing: { after: 240 } }),
        authorsTable(authorBlocks),
      ],
    },
    {
      properties: { type: SectionType.CONTINUOUS, page: { size: PAGE, margin: MARGIN }, column: { count: 2, space: GAP } },
      children: bodyBlocks(rest),
    },
  ],
});

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync(OUT, buf);
  console.log(`wrote ${OUT} (${buf.length} bytes)`);
});
