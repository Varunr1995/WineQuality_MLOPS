# The main reason to use test_config.py file is that when we deploy the project in to a page, the user will provide inputs.
# If the values provided by the user is too low or too high which we call it as outlier's then the output generated will be false.
# In order to overcome the issue we will specify a range of values that the user need to provide as input.
# If the value doesn't reside in that range, then the error will popup stating that the value is out off range please change it.
# By getting this notification the user will change the values.

class NotInRange(Exception):
    def __init__(self, message = "Value is not in the range"):
        self.message = message
        super().__init__(self.message)


def test_generic():
    a = 5
    with pytest.raises(NotInRange):
        if a not in range(10,20):
            raise NotInRange

