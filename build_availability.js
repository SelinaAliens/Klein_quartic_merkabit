const { Document, Packer, Paragraph, TextRun, ExternalHyperlink, AlignmentType, LevelFormat } = require("docx");
const fs = require("fs");

const TNR = { font: "Times New Roman" };

const doc = new Document({
  numbering: {
    config: [
      {
        reference: "bullets",
        levels: [
          {
            level: 0,
            format: LevelFormat.BULLET,
            text: "\u2022",
            alignment: AlignmentType.LEFT,
            style: {
              paragraph: { indent: { left: 720, hanging: 360 } },
            },
          },
        ],
      },
    ],
  },
  sections: [
    {
      properties: {
        page: {
          size: { width: 12240, height: 15840 },
          margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 },
        },
      },
      children: [
        // Section heading
        new Paragraph({
          spacing: { after: 200 },
          children: [
            new TextRun({ ...TNR, size: 24, bold: true, text: "Code and Data Availability" }),
          ],
        }),

        // Paragraph 1
        new Paragraph({
          spacing: { after: 120 },
          children: [
            new TextRun({
              ...TNR,
              size: 24,
              text: "All computational proofs, analysis scripts, and figure-generation code supporting this paper are publicly available at:",
            }),
          ],
        }),

        // URL line - centered, bold, hyperlinked
        new Paragraph({
          spacing: { before: 80, after: 200 },
          alignment: AlignmentType.CENTER,
          children: [
            new ExternalHyperlink({
              children: [
                new TextRun({
                  ...TNR,
                  size: 24,
                  bold: true,
                  style: "Hyperlink",
                  text: "https://github.com/selinaserephina-star/Klein_quartic_merkabit",
                }),
              ],
              link: "https://github.com/selinaserephina-star/Klein_quartic_merkabit",
            }),
          ],
        }),

        // Paragraph 2
        new Paragraph({
          spacing: { after: 120 },
          children: [
            new TextRun({
              ...TNR,
              size: 24,
              text: "The repository contains the following components:",
            }),
          ],
        }),

        // Bullet items
        ...[
          "klein_quartic_analysis.py \u2014 Core PSL(2,7) \u2245 GL(3,\uD835\uDD3D\u2082) realization and Klein quartic structural analysis",
          "azygetic_graph.py \u2014 Theta characteristic enumeration, symplectic pairing, srg(28, 12, 6, 4) verification, and T(8) isomorphism proof (Theorem 2)",
          "vertex_bijection.py \u2014 Equivariant bijection construction between 56-element coset spaces with full 9,408-pair verification (Theorem 1)",
          "route_b_justification.py \u2014 Exhaustive Eisenstein prime enumeration over norm 109, proving (12, 5) uniquely forced by E\u2086 architecture (Theorem 3)",
          "cyclotomic_analysis.py \u2014 \u211A(\u03B6\u2082\u2081) subfield lattice computation and Golay code embedding (Theorem 4)",
          "theta_analysis.py \u2014 Symplectic inner product computation and azygetic/syzygetic classification of all 64 theta characteristics",
          "generate_figures.py \u2014 Reproduction of all six figures at 300 DPI",
          "build_paper8.js \u2014 Node.js script (requires the docx package) that assembles the complete paper with embedded figures",
        ].map(
          (item) =>
            new Paragraph({
              numbering: { reference: "bullets", level: 0 },
              spacing: { after: 60 },
              children: [
                new TextRun({
                  ...TNR,
                  size: 24,
                  bold: true,
                  text: item.split(" \u2014 ")[0],
                }),
                new TextRun({
                  ...TNR,
                  size: 24,
                  text: " \u2014 " + item.split(" \u2014 ")[1],
                }),
              ],
            })
        ),

        // Paragraph 3
        new Paragraph({
          spacing: { before: 200, after: 120 },
          children: [
            new TextRun({
              ...TNR,
              size: 24,
              text: "Every theorem in this paper is accompanied by a self-contained computational verification. The scripts require only standard open-source libraries (NumPy, SciPy, SymPy, Matplotlib, NetworkX) and can be executed independently to reproduce all stated results.",
            }),
          ],
        }),

        // Paragraph 4
        new Paragraph({
          spacing: { after: 120 },
          children: [
            new TextRun({
              ...TNR,
              size: 24,
              text: "No external datasets are required. All mathematical objects \u2014 the Klein quartic, PSL(2,7), theta characteristics, Eisenstein integers, and E\u2086 Coxeter invariants \u2014 are constructed from first principles within the scripts.",
            }),
          ],
        }),
      ],
    },
  ],
});

Packer.toBuffer(doc).then((buffer) => {
  const outPath = "C:\\Users\\selin\\OneDrive\\Desktop\\KleinsQuartic\\Code_Data_Availability.docx";
  fs.writeFileSync(outPath, buffer);
  console.log("Written to " + outPath + " (" + buffer.length + " bytes)");
});
