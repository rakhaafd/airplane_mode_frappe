import frappe


def get_context(context):
	if frappe.session.user == "Guest":
		frappe.local.flags.redirect_location = "/login?redirect-to=/my_shops"
		raise frappe.Redirect

	context.shop_leads = frappe.get_all(
		"Airport Shop Lead",
		filters={
			"owner": frappe.session.user
		},
		fields=[
			"name",
			"shop",
			"username",
			"email",
			"phone",
			"creation"
		],
		order_by="creation desc"
	)

	context.rent_payments = frappe.get_all(
	"Airport Shop Rent Payment",
	filters={
		"tenant_email": frappe.session.user
	},
	fields=[
		"name",
		"airport_shop",
		"payment_month",
		"payment_year",
		"rent_amount",
		"paid_amount",
		"status",
	],
	order_by="creation desc",
)