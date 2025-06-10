import json

import nts
import requests
from nts import _
from lxml import etree

URL_PREFIXES = ("http://", "https://")


@nts.whitelist()
def import_genericode():
	doctype = "Code List"
	docname = nts.form_dict.docname
	content = nts.local.uploaded_file

	# recover the content, if it's a link
	if (file_url := nts.local.uploaded_file_url) and file_url.startswith(URL_PREFIXES):
		try:
			# If it's a URL, fetch the content and make it a local file (for durable audit)
			response = requests.get(nts.local.uploaded_file_url)
			response.raise_for_status()
			nts.local.uploaded_file = content = response.content
			nts.local.uploaded_filename = nts.local.uploaded_file_url.split("/")[-1]
			nts.local.uploaded_file_url = None
		except Exception as e:
			nts.throw(f"<pre>{e!s}</pre>", title=_("Fetching Error"))

	if file_url := nts.local.uploaded_file_url:
		file_path = nts.utils.file_manager.get_file_path(file_url)
		with open(file_path.encode(), mode="rb") as f:
			content = f.read()

	# Parse the xml content
	parser = etree.XMLParser(remove_blank_text=True)
	try:
		root = etree.fromstring(content, parser=parser)
	except Exception as e:
		nts.throw(f"<pre>{e!s}</pre>", title=_("Parsing Error"))

	# Extract the name (CanonicalVersionUri) from the parsed XML
	name = root.find(".//CanonicalVersionUri").text
	docname = docname or name

	if nts.db.exists(doctype, docname):
		code_list = nts.get_doc(doctype, docname)
		if code_list.name != name:
			nts.throw(_("The uploaded file does not match the selected Code List."))
	else:
		# Create a new Code List document with the extracted name
		code_list = nts.new_doc(doctype)
		code_list.name = name

	code_list.from_genericode(root)
	code_list.save()

	# Attach the file and provide a recoverable identifier
	file_doc = nts.get_doc(
		{
			"doctype": "File",
			"attached_to_doctype": "Code List",
			"attached_to_name": code_list.name,
			"folder": "Home/Attachments",
			"file_name": nts.local.uploaded_filename,
			"file_url": nts.local.uploaded_file_url,
			"is_private": 1,
			"content": content,
		}
	).save()

	# Get available columns and example values
	columns, example_values, filterable_columns = get_genericode_columns_and_examples(root)

	return {
		"code_list": code_list.name,
		"code_list_title": code_list.title,
		"file": file_doc.name,
		"columns": columns,
		"example_values": example_values,
		"filterable_columns": filterable_columns,
	}


@nts.whitelist()
def process_genericode_import(
	code_list_name: str,
	file_name: str,
	code_column: str,
	title_column: str | None = None,
	description_column: str | None = None,
	filters: str | None = None,
):
	from prodman.edi.doctype.common_code.common_code import import_genericode

	column_map = {"code": code_column, "title": title_column, "description": description_column}

	return import_genericode(code_list_name, file_name, column_map, json.loads(filters) if filters else None)


def get_genericode_columns_and_examples(root):
	columns = []
	example_values = {}
	filterable_columns = {}

	# Get column names
	for column in root.findall(".//Column"):
		column_id = column.get("Id")
		columns.append(column_id)
		example_values[column_id] = []
		filterable_columns[column_id] = set()

	# Get all values and count unique occurrences
	for row in root.findall(".//SimpleCodeList/Row"):
		for value in row.findall("Value"):
			column_id = value.get("ColumnRef")
			if column_id not in columns:
				# Handle undeclared column
				columns.append(column_id)
				example_values[column_id] = []
				filterable_columns[column_id] = set()

			simple_value = value.find("./SimpleValue")
			if simple_value is None:
				continue

			filterable_columns[column_id].add(simple_value.text)

	# Get example values (up to 3) and filter columns with cardinality <= 5
	for row in root.findall(".//SimpleCodeList/Row")[:3]:
		for value in row.findall("Value"):
			column_id = value.get("ColumnRef")
			simple_value = value.find("./SimpleValue")
			if simple_value is None:
				continue

			example_values[column_id].append(simple_value.text)

	filterable_columns = {k: list(v) for k, v in filterable_columns.items() if len(v) <= 5}

	return columns, example_values, filterable_columns
