import io
import sys
from unittest import TestCase
from unittest.mock import call, ANY

from unittest.mock import MagicMock

from notif import notification_on_fail


class CaptureOutputTestCase(TestCase):
    def _capture_output(self):
        self.test_out = io.StringIO()
        self.original_output = sys.stdout
        sys.stdout = self.test_out


class FailDecoratorTest(CaptureOutputTestCase):
    def setUp(self) -> None:
        self.a_low_verbose_level = 1
        self.a_mid_verbose_level = 2
        self.a_high_level_verbose = 3
        self.a_verbose_level = 3
        self.notif = MagicMock()

    def test_givenAFailDecorator_whenRunFun_thenNotifWorkNormal(self):
        self._capture_output()

        expected_fun_message = "A message"

        @notification_on_fail(self.notif, verbose_level=self.a_verbose_level)
        def fail_test():
            print(expected_fun_message)

        fail_test()

        actual = self.test_out.getvalue().strip()
        self.assertEqual(expected_fun_message, actual)

    def test_givenAFailDecoratorWithStrVerbose_whenRunFun_thenNotifWorkNormal(self):
        self._capture_output()

        expected_fun_message = "A message"

        @notification_on_fail(self.notif, verbose_level=str(self.a_verbose_level))
        def fail_test():
            print(expected_fun_message)

        fail_test()

        actual = self.test_out.getvalue().strip()
        self.assertEqual(expected_fun_message, actual)

    def test_givenAFailDecoratorWithIntVerbose_whenRunFun_thenNotifWorkNormal(self):
        self._capture_output()

        expected_fun_message = "A message"

        @notification_on_fail(self.notif, verbose_level=self.a_verbose_level)
        def fail_test():
            print(expected_fun_message)

        fail_test()

        actual = self.test_out.getvalue().strip()
        self.assertEqual(expected_fun_message, actual)

    def test_givenAFailDecorator_whenRunFunRaiseAnyError_thenRaiseError(self):
        expected_error = ValueError

        @notification_on_fail(self.notif, verbose_level=self.a_verbose_level)
        def fail_test_value_error():
            raise expected_error

        with self.assertRaises(expected_error):
            fail_test_value_error()

        expected_error = ImportError

        @notification_on_fail(self.notif, verbose_level=self.a_verbose_level)
        def fail_test_import_error():
            raise expected_error

        with self.assertRaises(expected_error):
            fail_test_import_error()

        expected_error = Exception

        @notification_on_fail(self.notif, verbose_level=self.a_verbose_level)
        def fail_test_exception():
            raise expected_error

        with self.assertRaises(expected_error):
            fail_test_exception()

    def test_givenAFailDecorator_whenRunFunRaiseAnyError_thenSendNotificatorErrorMessage(
        self,
    ):
        self._capture_output()

        expected_error = ValueError

        @notification_on_fail(self.notif, verbose_level=self.a_verbose_level)
        def fail_test():
            raise expected_error

        with self.assertRaises(expected_error):
            fail_test()

        self.notif.assert_has_calls([call.send_notification(message=ANY)])

    def test_givenAFailDecorator_whenRunFunRaiseAnyErrorVerbose1_thenSendNotificatorErrorMessageAccordingVerboseLevel(
        self,
    ):
        expected_error_message = "An error message"
        expected_type = ValueError
        expected_error = expected_type(expected_error_message)

        @notification_on_fail(self.notif, verbose_level=self.a_low_verbose_level)
        def fail_test():
            raise expected_error

        with self.assertRaises(ValueError):
            fail_test()

        expected_message = f"An error occurred of type {expected_type} when running the script."
        self.notif.assert_has_calls([call.send_notification(message=expected_message)])

    def test_givenAFailDecorator_whenRunFunRaiseAnyErrorVerbose2_thenSendNotificatorErrorMessageAccordingVerboseLevel(
        self,
    ):
        expected_error_message = "An error message"
        expected_type = ValueError
        expected_error = expected_type(expected_error_message)

        @notification_on_fail(self.notif, verbose_level=self.a_mid_verbose_level)
        def fail_test():
            raise expected_error

        with self.assertRaises(ValueError):
            fail_test()

        expected_message = f"An error occurred when running the script. The error message is: {expected_error_message}"
        self.notif.assert_has_calls([call.send_notification(message=expected_message)])

    def test_givenAFailDecorator_whenRunFunRaiseAnyErrorVerbose3_thenSendNotificatorErrorMessageAccordingVerboseLevel(
        self,
    ):
        expected_error_message = "An error message"
        expected_type = ValueError
        expected_error = expected_type(expected_error_message)

        @notification_on_fail(self.notif, verbose_level=self.a_high_level_verbose)
        def fail_test():
            raise expected_error

        with self.assertRaises(ValueError):
            fail_test()

        self.notif.assert_has_calls([call.send_notification(message=ANY)])
