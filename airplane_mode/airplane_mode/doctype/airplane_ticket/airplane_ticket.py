# Copyright (c) 2026, rakha and contributors
# For license information, please see license.txt

import frappe
import random
import string
from frappe.model.document import Document
from frappe import _


class AirplaneTicket(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from airplane_mode.airplane_mode.doctype.airplane_ticket_add_on_item.airplane_ticket_add_on_item import AirplaneTicketAddonItem
		from frappe.types import DF

		add_ons: DF.Table[AirplaneTicketAddonItem]
		amended_from: DF.Link | None
		departure_date: DF.Date
		departure_time: DF.Time
		destination_airport_code: DF.Data
		duration_of_flight: DF.Duration
		flight: DF.Link
		flight_price: DF.Currency
		gate_number: DF.Data | None
		passenger: DF.Data
		seat: DF.Data | None
		source_airport_code: DF.Data
		ticket_status: DF.Literal["Booked", "Checked-In", "Boarded"]
		total_amount: DF.Currency
	# end: auto-generated types

	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from airplane_mode.airplane_mode.doctype.airplane_ticket_add_on_item.airplane_ticket_add_on_item import AirplaneTicketAddonItem
		from frappe.types import DF

		add_ons: DF.Table[AirplaneTicketAddonItem]
		amended_from: DF.Link | None
		departure_date: DF.Date
		departure_time: DF.Time
		destination_airport_code: DF.Data
		duration_of_flight: DF.Duration
		flight: DF.Link
		flight_price: DF.Currency
		passenger: DF.Link
		seat: DF.Data | None
		source_airport_code: DF.Data
		ticket_status: DF.Literal["Booked", "Checked-In", "Boarded"]
		total_amount: DF.Currency

	def before_insert(self):
		if not self.seat:
			self.assign_seat()

	def assign_seat(self):
		rows = 99
		cols = ["A", "B", "C", "D", "E"]

		all_seats = [
			f"{row}{col}"
			for row in range(1, rows + 1)
			for col in cols
		]

		booked_seats = frappe.get_all(
			"Airplane Ticket",
			filters={
				"flight": self.flight,
				"docstatus": ["!=", 2],
			},
			pluck="seat",
		)

		for seat in all_seats:
			if seat not in booked_seats:
				self.seat = seat
				return

		frappe.throw("No seats available for this flight.")

	def validate(self):
		self.check_flight_capacity()
		self.set_flight_price()
		self.set_add_on_amounts()
		self.validate_unique_add_ons()
		self.calculate_total_amount()

	def check_flight_capacity(self):
		if not self.flight:
			return

		airplane = frappe.db.get_value(
			"Airplane Flight",
			self.flight,
			"airplane"
		)

		if not airplane:
			return

		capacity = frappe.db.get_value(
			"Airplane",
			airplane,
			"capacity"
		) or 0

		if not capacity:
			return

		total_tickets = frappe.db.count(
			"Airplane Ticket",
			{
				"flight": self.flight,
				"docstatus": ["!=", 2],
				"name": ["!=", self.name],
			}
		)

		if total_tickets >= capacity:
			frappe.throw(_("Flight is fully booked."))

	def set_flight_price(self):
		if self.flight:
			self.flight_price = frappe.db.get_value(
				"Airplane Flight",
				self.flight,
				"price"
			) or 0

	def set_add_on_amounts(self):
		for row in self.add_ons:
			if row.item:
				row.amount = frappe.db.get_value(
					"Airplane Ticket Add-on Type",
					row.item,
					"amount"
				) or 0

	def validate_unique_add_ons(self):
		items = []

		for row in self.add_ons:
			if row.item in items:
				frappe.throw(f"Add-on {row.item} is already selected.")

			items.append(row.item)

	def calculate_total_amount(self):
		add_on_total = 0

		for row in self.add_ons:
			add_on_total += row.amount or 0

		self.total_amount = (self.flight_price or 0) + add_on_total

	def before_submit(self):
		if self.ticket_status != "Boarded":
			frappe.throw("Only tickets with status Boarded can be submitted.")