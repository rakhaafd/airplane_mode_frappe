import frappe


def execute(filters=None):
	columns = [
		{
			"label": "Airport",
			"fieldname": "airport",
			"fieldtype": "Link",
			"options": "Airport",
			"width": 250,
		},
		{
			"label": "Total Shops",
			"fieldname": "total_shops",
			"fieldtype": "Int",
			"width": 150,
		},
	]

	airports = frappe.get_all("Airport", pluck="name")
	data = []

	for airport in airports:
		total_shops = frappe.db.count(
			"Airport Shop",
			{"airport": airport}
		)

		data.append({
			"airport": airport,
			"total_shops": total_shops,
		})

	return columns, data