""" _ """


class Maybe:
    #
    # (
    class Nothing:
        #
        # (
        __instance_nothing = None

        def __new__(cls, *args):
            # Create a Singleton to make Nothing objects unique and same.
            # (
            if cls.__instance_nothing is None:
                #
                # (
                cls.__instance_nothing = object.__new__(cls, *args)
            # )

            return cls.__instance_nothing
        # )

        def is_nothing(self):
            #
            # (
            return True
        # )

        def is_something(self):
            #
            # (
            return False
        # )

        def get_value(self):
            #
            # (
            raise TypeError(f"{self.__class__} type can't contain values.")
        # )

    # ) Class 'Nothing' END

    class Something:
        #
        # (
        __value = None

        def __init__(self, arg):
            #
            # (
            self.__value = arg
        # )

        def is_nothing(self):
            #
            # (
            return False
        # )

        def is_something(self):
            #
            # (
            return True
        # )

        def get_value(self):
            #
            # (
            return self.__value
        # )

    # ) Class 'Something' END
# ) Class 'Maybe' END


if __name__ == "__main__":
    # (
    def test_nothing():
        # ( 'Nothing' tests:
        PASSED = True

        x1 = Maybe.Nothing()
        x2 = Maybe.Nothing()

        assert (x1 is x2)

        # print(x1)
        # print(x2)

        assert (x1.is_nothing() == True)

        assert (x2.is_something() == False)

        try:
            # (
            print(x2.get_value())
        # )
        except TypeError as TErr:
            # (
            PASSED = True
        # )

        print(f"test_nothing(), PASSED ==", PASSED)

    # )

    def test_something():
        # ( Something tests:

        PASSED = True

        x1 = Maybe.Something(1)
        x2 = Maybe.Something(2)

        assert (x1 is not x2)

        # print(x1)
        # print(x2)

        assert (x1.is_nothing() == False)

        assert (x2.is_something() == True)

        try:
            # (
            print(f"x2 something value == ", x2.get_value())
        # )
        except Exception as Err:
            # (
            print("[ ERROR ] |", Err)
            PASSED = False
        # )

        print(f"test_something(), PASSED ==", PASSED)
    # )

    test_nothing()

    test_something()
# )
