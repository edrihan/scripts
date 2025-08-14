#!/usr/bin/env python3
"""
remove_glyphs.py

A small CLI to strip out glyphs from a font before merging or repackaging.
Leverages fontTools.subset to handle all the nitty-gritty of GSUB/GPOS, mark lookups, etc.

Usage examples:
  # remove named glyphs
  remove_glyphs.py -i source.ttf -o cleaned.ttf -g A B C

  # remove glyphs for every character in a text file
  remove_glyphs.py -i source.ttf -o cleaned.ttf -f chars.txt

  # remove all glyphs found in another font
  remove_glyphs.py -i source.ttf -o cleaned.ttf -r otherFont.otf
"""

import argparse
from fontTools.ttLib import TTFont
from fontTools.subset import Subsetter, Options


def remove_glyphs_via_subset(font_path, glyphs_to_remove, output_path):
    # Load the font
    font = TTFont(font_path)

    # Build the set of all original glyphs, then subtract the ones to remove
    all_glyphs = set(font.getGlyphOrder())
    keep_glyphs = sorted(all_glyphs - set(glyphs_to_remove))

    # Configure subsetter: keep glyph names, all layout features, ignore missing glyphs
    opts = Options()
    opts.glyph_names = True
    opts.layout_features = ["*"]
    opts.ignore_missing_glyphs = True

    subsetter = Subsetter(opts)
    subsetter.populate(glyphs=keep_glyphs)
    subsetter.subset(font)

    font.save(output_path)
    print(f"✅ Cleaned font saved to: {output_path}")


def extract_glyphs_from_font(font_path):
    """Return the set of all glyph names in the given font."""
    ft = TTFont(font_path)
    return set(ft.getGlyphOrder())


def extract_glyphs_from_chars(font_path, chars):
    """
    Map each Unicode character in 'chars' to its glyph name(s)
    in the font's cmap, return the resulting set of glyph names.
    """
    ft = TTFont(font_path)
    glyphs = set()
    for table in ft["cmap"].tables:
        for codepoint, name in table.cmap.items():
            if chr(codepoint) in chars:
                glyphs.add(name)
    return glyphs


def parse_args():
    p = argparse.ArgumentParser(
        description="Strip glyphs from a font before merging or repackaging.",
        epilog="""
Examples:
  remove_glyphs.py -i src.ttf -o out.ttf -g uni0041 uni0042
  remove_glyphs.py -i src.ttf -o out.ttf -f chars.txt
  remove_glyphs.py -i src.ttf -o out.ttf -r otherFont.otf
""",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    p.add_argument("-i", "--input", required=True, help="Source font path (.ttf/.otf)")
    p.add_argument("-o", "--output", required=True, help="Destination for cleaned font")
    p.add_argument("-g", "--glyphs", nargs="*", help="Glyph names to remove (space-separated)")
    p.add_argument("-f", "--glyph-file",
                   help="Text file: every character in it will be mapped to glyphs to remove")
    p.add_argument("-r", "--remove-from-font",
                   help="Another font: all its glyphs will be removed from the input")
    return p.parse_args()


def main():
    args = parse_args()
    to_remove = set(args.glyphs or [])

    # If user gave a text file of characters, map chars → glyph names.
    if args.glyph_file:
        try:
            text = open(args.glyph_file, encoding="utf-8").read()
            chars_glyphs = extract_glyphs_from_chars(args.input, text)
            to_remove.update(chars_glyphs)
        except Exception as e:
            print(f"❌ Failed to read glyph-file '{args.glyph_file}': {e}")
            return

    # If user gave another font, drop all its glyph names.
    if args.remove_from_font:
        try:
            other_glyphs = extract_glyphs_from_font(args.remove_from_font)
            to_remove.update(other_glyphs)
        except Exception as e:
            print(f"❌ Failed to read font for removal '{args.remove_from_font}': {e}")
            return

    if not to_remove:
        print("⚠️  No glyphs specified for removal. Use -g, -f, or -r.")
        return

    remove_glyphs_via_subset(args.input, to_remove, args.output)


if __name__ == "__main__":
    main()
