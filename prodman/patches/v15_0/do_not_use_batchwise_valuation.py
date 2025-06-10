import nts


def execute():
	valuation_method = nts.db.get_single_value("Stock Settings", "valuation_method")
	if valuation_method in ["FIFO", "LIFO"]:
		return

	if nts.get_all("Batch", filters={"use_batchwise_valuation": 1}, limit=1):
		return

	if nts.get_all("Item", filters={"has_batch_no": 1, "valuation_method": "FIFO"}, limit=1):
		return

	nts.db.set_single_value("Stock Settings", "do_not_use_batchwise_valuation", 1)
