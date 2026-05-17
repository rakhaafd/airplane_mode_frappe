# Copyright (c) 2026, rakha and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class FlightCrewMember(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		first_name: DF.Data
		full_name: DF.Data | None
		last_name: DF.Data
		role: DF.Literal["Pilot", "Co-Pilot", "Cabin Crew", "Flight Attendant", "Engineer"]
	# end: auto-generated types

	def validate(self):
		self.set_full_name()

	def set_full_name(self):
		first = self.first_name or ""
		last = self.last_name or ""

		self.full_name = f"{first} {last}".strip()
