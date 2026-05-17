// Copyright (c) 2026, rakha and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airplane Ticket", {
    refresh(frm) {
        frm.add_custom_button("Assign Seat", () => {
            let dialog = new frappe.ui.Dialog({
                title: "Assign Seat",
                fields: [
                    {
                        label: "Seat",
                        fieldname: "seat",
                        fieldtype: "Data",
                        reqd: 1
                    }
                ],
                primary_action_label: "Assign",
                primary_action(values) {
                    frm.set_value("seat", values.seat);
                    frm.save();

                    dialog.hide();
                }
            });

            dialog.show();
        });
    }
});