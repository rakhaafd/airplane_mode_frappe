# Copyright (c) 2026, rakha and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import today


class AirportShopRentPayment(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		airport: DF.Link
		airport_shop: DF.Link
		paid_amount: DF.Currency
		payment_date: DF.Date | None
		payment_month: DF.Literal["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
		payment_year: DF.Int
		rent_amount: DF.Currency
		status: DF.Literal["Unpaid", "Paid", "Overdue"]
		tenant_email: DF.Data | None
		tenant_name: DF.Data
	# end: auto-generated types

	def validate(self):
		self.set_paid_status()

	def set_paid_status(self):
		if self.paid_amount and self.rent_amount:
			if self.paid_amount >= self.rent_amount:
				self.status = "Paid"
				if not self.payment_date:
					self.payment_date = today()
			else:
				self.status = "Unpaid"
