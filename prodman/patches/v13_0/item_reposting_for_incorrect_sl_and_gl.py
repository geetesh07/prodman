import nts
from nts.utils import get_time, getdate, today

from prodman.accounts.utils import update_gl_entries_after
from prodman.stock.stock_ledger import update_entries_after


def execute():
	doctypes_to_reload = [
		("setup", "company"),
		("stock", "repost_item_valuation"),
		("stock", "stock_entry_detail"),
		("stock", "purchase_receipt_item"),
		("stock", "delivery_note_item"),
		("stock", "packed_item"),
		("accounts", "sales_invoice_item"),
		("accounts", "purchase_invoice_item"),
		("buying", "purchase_receipt_item_supplied"),
		("subcontracting", "subcontracting_receipt_item"),
		("subcontracting", "subcontracting_receipt_supplied_item"),
	]

	for module, doctype in doctypes_to_reload:
		nts.reload_doc(module, "doctype", doctype)

	reposting_project_deployed_on = get_creation_time()
	posting_date = getdate(reposting_project_deployed_on)
	posting_time = get_time(reposting_project_deployed_on)

	if posting_date == today():
		return

	nts.clear_cache()
	nts.flags.warehouse_account_map = {}

	company_list = []

	data = nts.db.sql(
		"""
		SELECT
			name, item_code, warehouse, voucher_type, voucher_no, posting_date, posting_time, company, creation
		FROM
			`tabStock Ledger Entry`
		WHERE
			creation > %s
			and is_cancelled = 0
		ORDER BY timestamp(posting_date, posting_time) asc, creation asc
	""",
		reposting_project_deployed_on,
		as_dict=1,
	)

	nts.db.auto_commit_on_many_writes = 1
	print("Reposting Stock Ledger Entries...")
	total_sle = len(data)
	i = 0
	for d in data:
		if d.company not in company_list:
			company_list.append(d.company)

		update_entries_after(
			{
				"item_code": d.item_code,
				"warehouse": d.warehouse,
				"posting_date": d.posting_date,
				"posting_time": d.posting_time,
				"voucher_type": d.voucher_type,
				"voucher_no": d.voucher_no,
				"sle_id": d.name,
				"creation": d.creation,
			},
			allow_negative_stock=True,
		)

		i += 1
		if i % 100 == 0:
			print(i, "/", total_sle)

	print("Reposting General Ledger Entries...")

	if data:
		for row in nts.get_all("Company", filters={"enable_perpetual_inventory": 1}):
			if row.name in company_list:
				update_gl_entries_after(posting_date, posting_time, company=row.name)

	nts.db.auto_commit_on_many_writes = 0


def get_creation_time():
	return nts.db.sql(
		""" SELECT create_time FROM
		INFORMATION_SCHEMA.TABLES where TABLE_NAME = "tabRepost Item Valuation" """,
		as_list=1,
	)[0][0]
