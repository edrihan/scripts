# scripts
Random utilities

## remove_glyphs.py

A small CLI to strip out glyphs from a font before merging or repackaging.
Leverages fontTools.subset to handle all the nitty-gritty of GSUB/GPOS, mark lookups, etc.

Usage examples:
  remove named glyphs
  ```remove_glyphs.py -i source.ttf -o cleaned.ttf -g A B C```

  # remove glyphs for every character in a text file
  remove_glyphs.py -i source.ttf -o cleaned.ttf -f chars.txt

  # remove all glyphs found in another font
  remove_glyphs.py -i source.ttf -o cleaned.ttf -r otherFont.otf
