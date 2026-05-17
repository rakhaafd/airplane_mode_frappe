// Copyright (c) 2026, rakha and contributors
// For license information, please see license.txt

frappe.ui.form.on('Flight Passenger', {
    first_name(frm) {
        set_full_name(frm);
    },

    last_name(frm) {
        set_full_name(frm);
    }
});

function set_full_name(frm) {
    frm.set_value(
        'full_name',
        `${frm.doc.first_name || ''} ${frm.doc.last_name || ''}`.trim()
    );
}