from contextlib import contextmanager

import nts


@contextmanager
def temporary_flag(flag_name, value):
	flags = nts.local.flags
	flags[flag_name] = value
	try:
		yield
	finally:
		flags.pop(flag_name, None)
