# scripts
Random utilities

### remove_glyphs.py

CLI tool to strip out glyphs from a font. Uses fontTools.subset to handle GSUB/GPOS, mark lookups, etc.

  remove named glyphs: ```remove_glyphs.py -i source.ttf -o cleaned.ttf -g A B C```

  remove glyphs for every character in a text file: ```remove_glyphs.py -i source.ttf -o cleaned.ttf -f chars.txt```

  remove all glyphs found in another font: ```remove_glyphs.py -i source.ttf -o cleaned.ttf -r otherFont.otf```

  ```options:
  -h, --help            show this help message and exit
  -i, --input INPUT     Source font path (.ttf/.otf)
  -o, --output OUTPUT   Destination for cleaned font
  -g, --glyphs [GLYPHS ...]
                        Glyph names to remove (space-separated)
  -f, --glyph-file GLYPH_FILE
                        Text file: every character in it will be mapped to glyphs to remove
  -r, --remove-from-font REMOVE_FROM_FONT
                        Another font: all its glyphs will be removed from the input

Examples:
  remove_glyphs.py -i src.ttf -o out.ttf -g uni0041 uni0042
  remove_glyphs.py -i src.ttf -o out.ttf -f chars.txt
  remove_glyphs.py -i src.ttf -o out.ttf -r otherFont.otf```
