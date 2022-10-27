"""
    ~~~ WHY ~~~
    To be able to represent nothing and separate it from something (usable values).

"""

class Maybe():
#(
        pass
#)

class NothingType(Maybe):
    # (
    pass
# )


class SomethingType(Maybe):
    # (
    pass
# )


def make_nothing():
    # (
    return (NothingType, ) # One element tuple.
# )


def make_something(thing):
    # (
    return (SomethingType, thing)
# )


def is_nothing(maybe_val):
    # (
    return type(maybe_val) == tuple and maybe_val[0] == NothingType
# )


def is_something(maybe_val):
    # (
    return type(maybe_val) == tuple and maybe_val[0] == SomethingType
# )


def get_something(maybe_val):
    # (
    if is_something(maybe_val):
        # (
        return maybe_val[1]
    # )

    else:
        # (
        raise Exception(
            f"{str(maybe_val)} is not something. Given argument must be created with make_something.")
    # )
# )


def get_or_default(maybe_val, default_val):
    # (
    try:
        # (
        return get_something(maybe_val)
    # )
    except:
        # (
        return default_val
    # )
# )


def main():
    # (
    s = make_something([1, 2, 3])
    n = make_nothing()

    assert (is_nothing("abc") == False)
    assert (is_something("abc") == False)
    
    assert (is_nothing(s) == False)

    assert (is_nothing(n) == True)

    assert (is_something(s) == True)
    assert (is_something(n) == False)

    assert (get_something(s) == [1, 2, 3])

    assert (get_or_default(n, "default") == "default")

    try:
        # (
        assert (get_something([1, 2, 3]))  # Should raise an Exception.
    # )
    except:
        # (
        pass
    # )

    try:
        # (
        assert (get_something(n))  # Should raise an Exception.
    # )
    except:
        # (
        pass
    # )

    print(f"[ INFO ] All assertions passed for {__name__}.")
# )


if __name__ == "__main__":
    # (
    main()
# )
