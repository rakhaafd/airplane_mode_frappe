import frappe
from frappe.model.document import Document
from frappe.utils import today, getdate


class AirportShopLead(Document):

	def after_insert(self):
		self.convert_lead_to_tenant()

	def convert_lead_to_tenant(self):
		if not self.shop:
			return

		shop = frappe.get_doc("Airport Shop", self.shop)

		if shop.status == "Occupied":
			frappe.throw("This shop is already occupied.")

		shop.status = "Occupied"
		shop.tenant_name = self.name
		shop.tenant_email = self.email
		shop.tenant_phone = self.phone
		shop.save(ignore_permissions=True)

		self.create_rent_payment(shop)

	def create_rent_payment(self, shop):
		current_date = getdate(today())
		month = current_date.strftime("%B")
		year = current_date.year

		exists = frappe.db.exists(
			"Airport Shop Rent Payment",
			{
				"airport_shop": shop.name,
				"payment_month": month,
				"payment_year": year,
			}
		)

		if exists:
			return

		payment = frappe.new_doc("Airport Shop Rent Payment")
		payment.airport_shop = shop.name
		payment.payment_month = month
		payment.payment_year = year
		payment.rent_amount = shop.rent_amount or 0
		payment.paid_amount = 0
		payment.status = "Unpaid"
		payment.insert(ignore_permissions=True)