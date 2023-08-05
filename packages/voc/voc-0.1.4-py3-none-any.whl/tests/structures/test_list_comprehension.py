from ..utils import TranspileTestCase


class ListComprehensionTests(TranspileTestCase):
    def test_syntax(self):
        self.assertCodeExecution("""
            x = [1, 2, 3, 4, 5]
            print([v**2 for v in x])
            """)

        self.assertCodeExecution("""
            x = [1, 2, 3, 4, 5]
            print([v for v in x])
            """)

    def test_method(self):
        self.assertCodeExecution("""
            x = [1, 2, 3, 4, 5]
            print(list(v**2 for v in x))
            """)
