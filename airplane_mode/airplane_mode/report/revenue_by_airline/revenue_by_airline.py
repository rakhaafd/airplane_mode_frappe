import frappe


def execute(filters=None):
	columns = get_columns()
	data = get_data()
	chart = get_chart(data)
	report_summary = get_report_summary(data)

	return columns, data, None, chart, report_summary


def get_columns():
	return [
		{
			"label": "Airline",
			"fieldname": "airline",
			"fieldtype": "Link",
			"options": "Airline",
			"width": 250,
		},
		{
			"label": "Revenue",
			"fieldname": "revenue",
			"fieldtype": "Currency",
			"width": 180,
		},
	]


def get_data():
	airlines = frappe.get_all(
		"Airline",
		fields=["name"],
		order_by="name asc",
	)

	data = []

	for airline in airlines:
		revenue = get_airline_revenue(airline.name)

		data.append({
			"airline": airline.name,
			"revenue": revenue,
		})

	return data


def get_airline_revenue(airline):
	airplanes = frappe.get_all(
		"Airplane",
		filters={"airline": airline},
		pluck="name",
	)

	if not airplanes:
		return 0

	flights = frappe.get_all(
		"Airplane Flight",
		filters={
			"airplane": ["in", airplanes],
		},
		pluck="name",
	)

	if not flights:
		return 0

	tickets = frappe.get_all(
		"Airplane Ticket",
		filters={
			"flight": ["in", flights],
			"docstatus": 1,
		},
		fields=["total_amount"],
	)

	return sum(ticket.total_amount or 0 for ticket in tickets)
	flights = frappe.get_all(
		"Airplane Flight",
		filters={
			"docstatus": 1,
		},
		fields=["name", "airplane"],
	)

	airplane_names = frappe.get_all(
		"Airplane",
		filters={
			"airline": airline,
		},
		pluck="name",
	)

	flight_names = [
		flight.name for flight in flights
		if flight.airplane in airplane_names
	]

	if not flight_names:
		return 0

	tickets = frappe.get_all(
		"Airplane Ticket",
		filters={
			"flight": ["in", flight_names],
			"docstatus": 1,
		},
		fields=["total_amount"],
	)

	return sum(ticket.total_amount or 0 for ticket in tickets)


def get_chart(data):
	return {
		"data": {
			"labels": [row["airline"] for row in data],
			"datasets": [
				{
					"name": "Revenue",
					"values": [row["revenue"] for row in data],
				}
			],
		},
		"type": "donut",
	}


def get_report_summary(data):
	total_revenue = sum(row["revenue"] for row in data)

	return [
		{
			"value": total_revenue,
			"indicator": "Green",
			"label": "Total Revenue",
			"datatype": "Currency",
		}
	]