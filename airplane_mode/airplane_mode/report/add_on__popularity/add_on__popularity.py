# Copyright (c) 2026, rakha and contributors
# For license information, please see license.txt

# import frappe
from frappe import _


import frappe


def execute(filters=None):

    columns = [
        {
            "label": "Add-On Type",
            "fieldname": "item",
            "fieldtype": "Data",
            "width": 300,
        },
        {
            "label": "Sold Count",
            "fieldname": "count",
            "fieldtype": "Int",
            "width": 150,
        },
    ]

    data = frappe.db.sql("""
        SELECT
            item,
            COUNT(*) as count
        FROM `tabAirplane Ticket Add-on Item`
        GROUP BY item
        ORDER BY count DESC
    """, as_dict=True)

    return columns, data


