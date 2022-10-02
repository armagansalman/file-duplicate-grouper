"""

    ~~~ WHY ~~~
To be able to represent nothing and separate it from something (useable values).

"""


"""
MIT License

Copyright (c) (2022) (Armağan Salman)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


class NothingType():
#(
    pass
#)


class SomethingType():
#(
    pass
#)


def make_nothing():
#(
    return tuple( [NothingType] )
#)


def make_something(thing):
#(
    return tuple( [SomethingType, thing] )
#)


def is_nothing(maybe_val):
#(
    return maybe_val[0] == NothingType
#)


def is_something(maybe_val):
#(
    return maybe_val[0] == SomethingType
#)


def get_something(maybe_val):
#(
    if is_something(maybe_val):
    #(
        return maybe_val[1]
    #)
    
    else:
    #(
        raise Exception(f"{str(maybe_val)} is not something. Given argument must be created with make_something.")
    #)
#)


def get_or_default(maybe_val, default_val):
#(
    try:
    #(
        return get_something(maybe_val)
    #)
    except:
    #(
        return default_val
    #)
#)



def main():
#(
    s = make_something([1,2,3])
    n = make_nothing()
    
    
    assert(is_nothing(s) == False)
    
    assert(is_nothing(n) == True)
    
    assert(is_something(s) == True)
    assert(is_something(n) == False)
    
    assert(get_something(s) == [1,2,3])
    
    assert(get_or_default(n, "default") == "default")
    
    try:
    #(
        assert(get_something([1,2,3])) # Should raise an Exception.
    #)
    except:
    #(
        pass
    #)
    
    try:
    #(
        assert(get_something(n)) # Should raise an Exception.
    #)
    except:
    #(
        pass
    #)
    
    print(f"[ INFO ] All assertions passed for {__name__}.")
#)


if __name__ == "__main__":
#(
    main()
#)

