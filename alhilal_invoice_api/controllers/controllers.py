# -*- coding: utf-8 -*-
import odoo

from odoo import http, api, fields
from odoo.http import request, Response, route
from odoo.exceptions import UserError
import functools
import json
import base64
import logging

_logger = logging.getLogger(__name__)


def validate_token(func):
    @functools.wraps(func)
    def wrap(self, *args, **kwargs):
        access_token = request.httprequest.headers.get("Authorization")
        if not access_token:
            return Response(
                json.dumps({"msg": "Missing access token in request header"}, indent=4),
                content_type="application/json;charset=utf-8",
                status=400,
            )
        if not access_token.lower().startswith("bearer "):
            return Response(
                json.dumps({"msg": "Invalid access token format"}, indent=4),
                content_type="application/json;charset=utf-8",
                status=400,
            )
        if access_token.lower().startswith("bearer "):
            key = access_token[7:]
        api_key_data = (
            request.env["res.users.apikeys"]
            .sudo()
            ._get_apikey_name(scope="web", key=key)
        )

        user_id = api_key_data["user_id"] if api_key_data else None
        user = request.env["res.users"].sudo().browse(user_id) if user_id else None
        if not user:
            return Response(
                json.dumps({"msg": "Token is invalid or expired"}, indent=4),
                content_type="application/json;charset=utf-8",
                status=401,
            )

        request.session.uid = user.id
        request.update_env(user=user.id)

        return func(self, *args, **kwargs)

    return wrap


class AlhilalInvoiceApi(http.Controller):

    def check_user_permissions(self):
        user = request.env.user
        if not user.has_group("account.group_account_invoice"):
            return False
        return True

    @validate_token
    @http.route(
        "/v1/api/create_invoice",
        auth="none",
        type="http",
        methods=["POST"],
        csrf=False,
    )
    def api_create_invoice(self):
        """Create a new invoice with the given partner ID, date, and product lines.
        Also, create a payment for the invoice if the payment method is 'wallet'.
        Returns a success message with the invoice details or an error message
        if required fields are missing or the product lines format is invalid."""
        try:
            data = json.loads(request.httprequest.data)

            # Validate required fields
            if not all(
                field in data
                for field in [
                    "date",
                    "branch",
                    "subscription_type",
                    "invoice_lines",
                ]
            ):
                return Response(
                    json.dumps(
                        {"error": "Missing required fields", "status_code": 400},
                        sort_keys=True,
                        indent=4,
                    ),
                    content_type="application/json;charset=utf-8",
                    status=400,
                )
            date = data.get("date")
            try:
                date = fields.Date.from_string(date)
            except ValueError:
                return Response(
                    json.dumps(
                        {
                            "error": "Invalid date format. Expected YYYY-MM-DD",
                            "status_code": 400,
                        },
                        sort_keys=True,
                        indent=4,
                    ),
                    content_type="application/json;charset=utf-8",
                    status=400,
                )

                # TODO update company_id to existing company
            company_id = 2
            company = request.env["res.company"].browse(company_id)
            if not company:
                return Response(
                    json.dumps(
                        {"error": "Company not found", "status_code": 404},
                        sort_keys=True,
                        indent=4,
                    ),
                    content_type="application/json;charset=utf-8",
                    status=404,
                )
            company_tax = request.env["account.tax"].search(
                [
                    ("company_id", "=", company.id),
                    ("type_tax_use", "=", "sale"),
                    ("amount_type", "=", "percent"),
                    ("amount", "=", 15),
                ],
                limit=1,
            )
            if not company_tax:
                return Response(
                    json.dumps(
                        {"error": "Tax not found", "status_code": 404},
                        sort_keys=True,
                        indent=4,
                    ),
                    content_type="application/json;charset=utf-8",
                    status=404,
                )
            branch = request.env["res.branch"].search(
                [("company_id", "=", company.id), ("name", "=", data["branch"])],
                limit=1,
            )
            if not branch:
                return Response(
                    json.dumps(
                        {"error": "Branch not found", "status_code": 404},
                        sort_keys=True,
                        indent=4,
                    ),
                    content_type="application/json;charset=utf-8",
                    status=404,
                )
            analytic_accounts = branch.sales_analytic_distributions
            if not analytic_accounts:
                return Response(
                    json.dumps(
                        {"error": "Analytic account not found", "status_code": 404},
                        sort_keys=True,
                        indent=4,
                    ),
                    content_type="application/json;charset=utf-8",
                    status=404,
                )

            if not isinstance(data["invoice_lines"], list):
                return Response(
                    json.dumps(
                        {
                            "error": "invoice_lines must be a list of objects",
                            "status_code": 400,
                        },
                        sort_keys=True,
                        indent=4,
                    ),
                    content_type="application/json;charset=utf-8",
                    status=400,
                )
            membership_plan = False
            lines = []
            for line in data["invoice_lines"]:
                if not isinstance(line, dict):
                    return Response(
                        json.dumps(
                            {
                                "error": "Each invoice line must be an object",
                                "status_code": 400,
                            },
                            sort_keys=True,
                            indent=4,
                        ),
                        content_type="application/json;charset=utf-8",
                        status=400,
                    )
                if (
                    "product" not in line
                    or "quantity" not in line
                    or "price_unit" not in line
                ):
                    return Response(
                        json.dumps(
                            {
                                "error": "Each invoice line must contain 'product', 'quantity', and 'price_unit'",
                                "status_code": 400,
                            },
                            sort_keys=True,
                            indent=4,
                        ),
                        content_type="application/json;charset=utf-8",
                        status=400,
                    )
                if (
                    not isinstance(line["quantity"], (int, float))
                    or line["quantity"] <= 0
                ):
                    return Response(
                        json.dumps(
                            {
                                "error": "The 'quantity' in each invoice line must be a positive number",
                                "status_code": 400,
                            },
                            sort_keys=True,
                            indent=4,
                        ),
                        content_type="application/json;charset=utf-8",
                        status=400,
                    )
                if (
                    not isinstance(line["price_unit"], (int, float))
                    or line["price_unit"] <= 0
                ):
                    return Response(
                        json.dumps(
                            {
                                "error": "The 'price_unit' in each invoice line must be a positive number",
                                "status_code": 400,
                            },
                            sort_keys=True,
                            indent=4,
                        ),
                        content_type="application/json;charset=utf-8",
                        status=400,
                    )

                if line.get("product") == "subscription":
                    if not "start_date" in line or not "end_date" in line:
                        return Response(
                            json.dumps(
                                {
                                    "error": "Missing required fields for subscription",
                                    "status_code": 400,
                                },
                                sort_keys=True,
                                indent=4,
                            ),
                            content_type="application/json;charset=utf-8",
                            status=400,
                        )
                    start_date = line.get("start_date")
                    end_date = line.get("end_date")
                    try:
                        start_date = fields.Date.from_string(start_date)
                        end_date = fields.Date.from_string(end_date)
                    except ValueError:
                        return Response(
                            json.dumps(
                                {
                                    "error": "Invalid date format. Expected YYYY-MM-DD",
                                    "status_code": 400,
                                },
                                sort_keys=True,
                                indent=4,
                            ),
                            content_type="application/json;charset=utf-8",
                            status=400,
                        )
                    if start_date > end_date:
                        return Response(
                            json.dumps(
                                {
                                    "error": "Start date must be before end date",
                                    "status_code": 400,
                                },
                                sort_keys=True,
                                indent=4,
                            ),
                            content_type="application/json;charset=utf-8",
                            status=400,
                        )
                    period = (end_date - start_date).days
                    if period <= 0:
                        return Response(
                            json.dumps(
                                {
                                    "error": "Subscription period must be greater than 0 days",
                                    "status_code": 400,
                                },
                                sort_keys=True,
                                indent=4,
                            ),
                            content_type="application/json;charset=utf-8",
                            status=400,
                        )
                    moths = period // 30
                    if moths == 1:
                        # product_id = 45  # Example product ID for subscription
                        product_id = 228
                    elif moths == 2:
                        # product_id = 46  # Example product ID for subscription
                        product_id = 229
                    elif moths == 3:
                        product_id = 47  # Example product ID for subscription
                        # product_id = 47
                    elif moths == 6:
                        product_id = 48  # Example product ID for subscription
                        # product_id = 48
                    elif moths == 9:
                        product_id = 49  # Example product ID for subscription
                        # product_id = 49
                    else:
                        return Response(
                            json.dumps(
                                {
                                    "error": "Invalid subscription period",
                                    "status_code": 400,
                                },
                                sort_keys=True,
                                indent=4,
                            ),
                            content_type="application/json;charset=utf-8",
                            status=400,
                        )
                    print("moths", moths)
                    membership_plan = request.env["sale.subscription.plan"].search(
                        [
                            ("billing_period_value", "=", moths),
                            ("billing_period_unit", "=", "month"),
                            # ("company_id", "=", company.id),
                        ],
                        limit=1,
                    )
                    if not membership_plan:
                        return Response(
                            json.dumps(
                                {
                                    "error": "Membership plan not found",
                                    "status_code": 404,
                                },
                                sort_keys=True,
                                indent=4,
                            ),
                            content_type="application/json;charset=utf-8",
                            status=404,
                        )
                    product = request.env["product.product"].browse(product_id)
                    if not product:
                        return Response(
                            json.dumps(
                                {
                                    "error": f"Product with ID {product_id} not found",
                                    "status_code": 404,
                                },
                                sort_keys=True,
                                indent=4,
                            ),
                            content_type="application/json;charset=utf-8",
                            status=404,
                        )

                elif line.get("product") == "clothes":

                    # product_id = 44  # Example product ID for clothes
                    product_id = 293
                    product = request.env["product.product"].search(
                        [("id", "=", product_id)]
                    )
                    if not product:
                        return Response(
                            json.dumps(
                                {
                                    "error": f"Product with ID {product_id} not found",
                                    "status_code": 404,
                                },
                                sort_keys=True,
                                indent=4,
                            ),
                            content_type="application/json;charset=utf-8",
                            status=404,
                        )
                else:
                    return Response(
                        json.dumps(
                            {
                                "error": "Invalid product type. Expected 'subscription' or 'clothes'",
                                "status_code": 400,
                            },
                            sort_keys=True,
                            indent=4,
                        ),
                        content_type="application/json;charset=utf-8",
                        status=400,
                    )
                analytic_distribution = (
                    {acc.id: 100.0 for acc in analytic_accounts if hasattr(acc, "id")}
                    if analytic_accounts
                    else {}
                )
                line_data = {  # Use (0, 0, {values}) format for creating new records
                    "product_id": product.id,
                    "quantity": line["quantity"],
                    "price_unit": line["price_unit"],
                    "discount": line.get("discount", 0.0),
                    "analytic_distribution": analytic_distribution,
                    "name": line.get("label", product.name),
                    "tax_ids": [(6, 0, company_tax.ids)],
                }
                if line.get("product") == "subscription":
                    line_data["start_date"] = line["start_date"]
                    line_data["end_date"] = line["end_date"]
                lines.append(
                    (
                        0,
                        0,
                        line_data,
                    )
                )

            # TODO update partner_id to existing partner
            partner_id = 24803  # Example partner ID
            partner = request.env["res.partner"].browse(partner_id)
            if not partner:
                return Response(
                    json.dumps(
                        {"error": "Partner not found", "status_code": 404},
                        sort_keys=True,
                        indent=4,
                    ),
                    content_type="application/json;charset=utf-8",
                    status=404,
                )
            if len(lines) == 0:
                return Response(
                    json.dumps(
                        {"error": "No invoice lines provided", "status_code": 400},
                        sort_keys=True,
                        indent=4,
                    ),
                    content_type="application/json;charset=utf-8",
                    status=400,
                )
            journal_id = (
                request.env["account.journal"]
                .search(
                    [
                        ("type", "=", "sale"),
                        ("company_id", "=", company.id),
                        ("name", "=", "Customer Invoices"),
                    ],
                    limit=1,
                )
                .id
            )
            if not journal_id:
                return Response(
                    json.dumps(
                        {"error": "Journal not found", "status_code": 404},
                        sort_keys=True,
                        indent=4,
                    ),
                    content_type="application/json;charset=utf-8",
                    status=404,
                )

            invoice_values = {
                "invoice_date": data["date"],
                "partner_id": partner.id,
                "move_type": "out_invoice",
                "journal_id": journal_id,
                "branch_id": branch.id,
                "membership_plan_id": membership_plan.id if membership_plan else False,
                "subscription_type": (
                    data["subscription_type"] if data["subscription_type"] else False
                ),
                "invoice_line_ids": lines,
                "company_id": company.id,
            }

            # Create the invoice
            invoice = request.env["account.move"].create(invoice_values)

            if not invoice:
                return Response(
                    json.dumps(
                        {"error": "Failed to create invoice", "status_code": 500},
                        sort_keys=True,
                        indent=4,
                    ),
                    content_type="application/json;charset=utf-8",
                    status=500,
                )
            invoice.action_post()

            invoice_details = {
                "invoice_id": invoice.id,
                "invoice_number": invoice.name,
            }
            res = {
                "msg": "Your invoice was created successfully",
                "invoice": invoice_details,
            }

            return Response(
                json.dumps(res, sort_keys=True, indent=4),
                content_type="application/json;charset=utf-8",
                status=200,
            )
        except Exception as e:
            return Response(
                json.dumps(
                    {"error": str(e), "status_code": 500}, sort_keys=True, indent=4
                ),
                content_type="application/json;charset=utf-8",
                status=500,
            )
