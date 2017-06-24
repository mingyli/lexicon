## Text compression using tries.

Consider a vocabulary consisting of only `dog` and `cat`. Then its trie consists of a root node with two children and other nodes each with zero children or one child. `dog` can be uniquely determined by the strings `d`, `do`, and `dog`, and similarly with `cat`. Then the text

`dog dog cat dog cat`

can be shortened to

`d d c d c`.

TODO: memoize in compressor and decompressor for speed. do not memoize by changing Trie
