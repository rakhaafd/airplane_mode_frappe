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
			"label": "Available Shops",
			"fieldname": "available_shops",
			"fieldtype": "Int",
			"width": 160,
		},
		{
			"label": "Occupied Shops",
			"fieldname": "occupied_shops",
			"fieldtype": "Int",
			"width": 160,
		},
	]

	airports = frappe.get_all("Airport", pluck="name")
	data = []

	for airport in airports:
		available = frappe.db.count(
			"Airport Shop",
			{
				"airport": airport,
				"status": "Available",
			}
		)

		occupied = frappe.db.count(
			"Airport Shop",
			{
				"airport": airport,
				"status": "Occupied",
			}
		)

		data.append({
			"airport": airport,
			"available_shops": available,
			"occupied_shops": occupied,
		})

	return columns, data