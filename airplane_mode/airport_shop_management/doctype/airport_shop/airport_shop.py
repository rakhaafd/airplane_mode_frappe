# Copyright (c) 2026, rakha and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator
from frappe import scrub
from frappe.utils import today, getdate


def get_shop_settings():
	settings = frappe.get_all(
		"Airport Shop Settings",
		fields=[
			"default_rent_amount",
			"enable_rent_reminders",
		],
		limit=1,
	)

	return settings[0] if settings else None


class AirportShop(WebsiteGenerator):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		airport: DF.Link
		area_sqm: DF.Float
		contract_end_date: DF.Date
		contract_start_date: DF.Date
		is_published: DF.Check
		rent_amount: DF.Currency
		route: DF.Data | None
		shop_name: DF.Data
		shop_number: DF.Data
		shop_type: DF.Link | None
		status: DF.Literal["Available", "Occupied"]
		tenant_email: DF.Data | None
		tenant_name: DF.Data
		tenant_phone: DF.Data | None
	# end: auto-generated types

	def validate(self):
		self.set_default_rent()
		self.set_route()

	def set_default_rent(self):
		settings = get_shop_settings()

		if not settings:
			return

		if not self.rent_amount:
			self.rent_amount = settings.default_rent_amount or 0

	def set_route(self):
		if self.shop_name:
			self.route = f"shops/{scrub(self.shop_name).replace('_', '-')}"

def create_monthly_rent_payments():
	shops = frappe.get_all(
		"Airport Shop",
		filters={"status": "Occupied"},
		fields=[
			"name",
			"rent_amount",
		],
	)

	current_date = getdate(today())
	month = current_date.strftime("%B")
	year = current_date.year

	for shop in shops:
		exists = frappe.db.exists(
			"Airport Shop Rent Payment",
			{
				"airport_shop": shop.name,
				"payment_month": month,
				"payment_year": year,
			},
		)

		if exists:
			continue

		payment = frappe.new_doc("Airport Shop Rent Payment")
		payment.airport_shop = shop.name
		payment.payment_month = month
		payment.payment_year = year
		payment.rent_amount = shop.rent_amount or 0
		payment.status = "Unpaid"
		payment.insert(ignore_permissions=True)


def send_rent_reminders():
	settings = get_shop_settings()

	if not settings:
		return

	if not settings.enable_rent_reminders:
		return

	payments = frappe.get_all(
		"Airport Shop Rent Payment",
		filters={"status": "Unpaid"},
		fields=[
			"name",
			"airport_shop",
			"tenant_name",
			"tenant_email",
			"rent_amount",
			"payment_month",
			"payment_year",
		],
	)

	for payment in payments:
		if not payment.tenant_email:
			continue

		frappe.sendmail(
			recipients=[payment.tenant_email],
			subject="Monthly Rent Payment Reminder",
			message=f"""
				<p>Hello {payment.tenant_name},</p>

				<p>
					This is a reminder that your rent payment
					for <b>{payment.payment_month} {payment.payment_year}</b>
					is due.
				</p>

				<p>
					Shop: <b>{payment.airport_shop}</b><br>
					Rent Amount: <b>{payment.rent_amount}</b>
				</p>
			""",
		)