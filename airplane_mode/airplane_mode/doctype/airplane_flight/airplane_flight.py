# Copyright (c) 2026, rakha and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator


class AirplaneFlight(WebsiteGenerator):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from airplane_mode.airplane_mode.doctype.airplane_flight_crew_member.airplane_flight_crew_member import AirplaneFlightCrewMember
		from frappe.types import DF

		airplane: DF.Link
		amended_from: DF.Link | None
		date_of_departure: DF.Date
		destination_airport: DF.Link
		destination_airport_code: DF.Data | None
		duration: DF.Duration
		gate_number: DF.Data | None
		is_published: DF.Check
		price: DF.Currency
		route: DF.Data | None
		source_airport: DF.Link
		source_airport_code: DF.Data | None
		status: DF.Literal["Scheduled", "Completed", "Cancelled"]
		table_icme: DF.Table[AirplaneFlightCrewMember]
		time_of_departure: DF.Time
	# end: auto-generated types

	def on_submit(self):
		tickets = frappe.get_all(
			"Airplane Ticket",
			filters={
				"flight": self.name,
				"ticket_status": "Boarded",
				"docstatus": 0,
			},
			pluck="name",
		)

		for ticket_name in tickets:
			ticket = frappe.get_doc("Airplane Ticket", ticket_name)
			ticket.submit()

	def on_update(self):
		if self.has_value_changed("gate_number"):
			frappe.enqueue(
				update_ticket_gate_numbers,
				flight=self.name,
				gate_number=self.gate_number,
				queue="short"
			)

def update_ticket_gate_numbers(flight, gate_number):
	tickets = frappe.get_all(
		"Airplane Ticket",
		filters={"flight": flight},
		pluck="name"
	)

	for ticket in tickets:
		frappe.db.set_value(
			"Airplane Ticket",
			ticket,
			"gate_number",
			gate_number
		)