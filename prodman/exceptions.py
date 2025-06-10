import nts


# accounts
class PartyFrozen(nts.ValidationError):
	pass


class InvalidAccountCurrency(nts.ValidationError):
	pass


class InvalidCurrency(nts.ValidationError):
	pass


class PartyDisabled(nts.ValidationError):
	pass


class InvalidAccountDimensionError(nts.ValidationError):
	pass


class MandatoryAccountDimensionError(nts.ValidationError):
	pass
