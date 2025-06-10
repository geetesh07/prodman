import click
import nts


def execute():
	table = "tabStock Ledger Entry"
	index_list = ["posting_datetime_creation_index", "item_warehouse"]

	for index in index_list:
		if not nts.db.has_index(table, index):
			continue

		try:
			nts.db.sql_ddl(f"ALTER TABLE `{table}` DROP INDEX `{index}`")
			click.echo(f"✓ dropped {index} index from {table}")
		except Exception:
			nts.log_error("Failed to drop index")
