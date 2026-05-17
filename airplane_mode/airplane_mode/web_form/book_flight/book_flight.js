frappe.ready(() => {
	const flight = frappe.utils.get_url_arg("flight");

	if (!flight) return;

	frappe.web_form.set_value("flight", flight);

	frappe.call({
		method: "frappe.client.get_value",
		args: {
			doctype: "Airplane Flight",
			filters: {
				name: flight
			},
			fieldname: [
				"price",
				"source_airport_code",
				"destination_airport_code"
			]
		},
		callback: function (r) {
			if (!r.message) return;

			frappe.web_form.set_value("flight_price", r.message.price || 0);
			frappe.web_form.set_value("source_airport_code", r.message.source_airport_code || "");
			frappe.web_form.set_value("destination_airport_code", r.message.destination_airport_code || "");

			frappe.web_form.set_value("total_amount", r.message.price || 0);
		}
	});
});