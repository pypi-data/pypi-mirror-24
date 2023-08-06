from ..ifuzzable import IFuzzable
import abc


class BasePrimitive(IFuzzable):
    """
    The primitive base class implements common functionality shared across most primitives.
    """
    __metaclass__ = abc.ABCMeta

    @property
    def mutant_index(self):
        return self._mutant_index

    @property
    def fuzzable(self):
        return self._fuzzable

    @property
    def original_value(self):
        return self._render(self._original_value)

    def __init__(self):
        self._fuzzable = True  # flag controlling whether or not the given primitive is to be fuzzed.
        self._mutant_index = 0  # current mutation index into the fuzz library.
        self._original_value = None  # original value of primitive.
        self._original_value_rendered = None # original value as rendered

        self._fuzz_complete = False  # this flag is raised when the mutations are exhausted.
        self._fuzz_library = []  # library of static fuzz heuristics to cycle through.
        self._rendered = ""  # rendered value of primitive.
        self._value = None  # current value of primitive.

    def mutate(self):
        """
        Mutate the primitive by stepping through the fuzz library, return False on completion.

        @rtype:  bool
        @return: True on success, False otherwise.
        """
        fuzz_complete = False
        # if we've ran out of mutations, raise the completion flag.
        if self._mutant_index == self.num_mutations():
            self._fuzz_complete = True
            fuzz_complete = True

        # if fuzzing was disabled or complete, and mutate() is called, ensure the original value is restored.
        if not self._fuzzable or fuzz_complete:
            self._value = self._original_value
            return False

        # update the current value from the fuzz library.
        self._value = self._fuzz_library[self._mutant_index]

        # increment the mutation count.
        self._mutant_index += 1

        return True

    def num_mutations(self):
        """
        Calculate and return the total number of mutations for this individual primitive.

        @rtype:  int
        @return: Number of mutated forms this primitive can take
        """

        return len(self._fuzz_library)

    def render(self):
        """
        Nothing fancy on render, simply return the value.
        """

        self._rendered = self._render(self._value)
        return self._rendered

    def _render(self, value):
        """
        Render an arbitrary value.

        :param value Value to render.
        :return: Rendered value
        :rtype: bytes
        """
        return value

    def reset(self):
        """
        Reset this primitive to the starting mutation state.
        """

        self._fuzz_complete = False
        self._mutant_index = 0
        self._value = self._original_value

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, repr(self._value))

    def __len__(self):
        return len(self._value)

    def __nonzero__(self):
        """
        Make sure instances evaluate to True even if __len__ is zero.

        :return: True
        """
        return True
