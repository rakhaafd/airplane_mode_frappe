import frappe


def get_context(context):
	if frappe.session.user == "Guest":
		frappe.local.flags.redirect_location = "/login?redirect-to=/my_tickets"
		raise frappe.Redirect

	context.tickets = frappe.get_all(
		"Airplane Ticket",
		filters={
			"owner": frappe.session.user
		},
		fields=[
			"name",
			"flight",
			"passenger",
			"seat",
			"flight_price",
			"total_amount",
			"ticket_status",
			"creation"
		],
		order_by="creation desc"
	)