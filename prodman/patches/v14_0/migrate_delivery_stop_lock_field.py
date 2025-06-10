import nts
from nts.model.utils.rename_field import rename_field


def execute():
	if nts.db.has_column("Delivery Stop", "lock"):
		rename_field("Delivery Stop", "lock", "locked")
