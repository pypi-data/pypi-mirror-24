# edith

Edith: an edit-distance implementation with edit-path retrieval.

This implementation relays not on string-edition. It is intended to work on *lists* of objects.

It is based on:
 * https://en.wikipedia.org/wiki/Levenshtein_distance
 * https://en.wikipedia.org/wiki/Wagner-Fischer_algorithm

## Usage

    import edith
    dst = edith.Distance(src, tgt)
    length = dst.calc()
    e_path = dst.editpath()

## Samples

    >>> import edith
    
    >>> dst = edith.Distance("Saturday", "Sunday")
    >>> dst.calc()
    3
    
    >>> print [str(x) for x in dst.editpath()]
    ['del-2', 'del-3', 'sust-3-n']

    >>> edith.Edition.Apply("Saturday", dst.editpath(), debug=True)
    del-3 : Saturday -> Saurday
    del-2 : Saurday -> Surday
    sust-3-n : Surday -> Sunday
    'Sunday'

Showing calculation matrix:
    
    >>> dst = edith.Distance("kitten", "sitting")
    >>> dst.calc()
    3

    >>> print [str(x) for x in dst.editpath()]
    ['sust-1-s', 'sust-5-i', 'inst-6-g']
        
    >>> dst.editpath()
    [\S1s, \S5i, |I6g]

    >>> dst.dump()

                k     i     t     t     e     n
          0*[-] 1-D1  2-D2  3-D3  4-D4  5-D5  6-D6
        s 1|I0s 1\S1s 2-D2  3-D3  4-D4  5-D5  6-D6
        i 2|I1i 2|I1i 1\S1s 2-D3  3-D4  4-D5  5-D6
        t 3|I2t 3|I2t 2|I2t 1\S1s 2-D3  3-D5  4-D6
        t 4|I3t 4|I3t 3|I3t 2|I2t 1\S1s 2-D5  3-D6  
        i 5|I4i 5|I4i 4|I3t 3|I4i 2|I4i 2\S5i 3-D6
        n 6|I5n 6|I5n 5|I5n 4|I5n 3|I5n 3|I5n 2\S5i
        g 7|I6g 7|I6g 6|I6g 5|I6g 4|I6g 4|I6g 3|I6g
