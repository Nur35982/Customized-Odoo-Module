from odoo import fields, models, api

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    # Custom fields for Harnest Label Industries
    fabric_quality = fields.Char(string='Fabric Quality')
    quantity = fields.Integer(string='Quantity')
    delivery_lead_time = fields.Integer(string='Delivery Lead Time (Days)')
    inquiry_source = fields.Selection(
        [('email', 'Email'), ('whatsapp', 'WhatsApp'), ('phone', 'Phone')],
        string='Inquiry Source'
    )
    sample_status = fields.Selection(
        [
            ('inquiry', 'Inquiry'),
            ('sample_development', 'Sample Development'),
            ('sample_delivered', 'Sample Delivered'),
            ('customer_approval', 'Customer Approval'),
            ('customer_rejection', 'Customer Rejection'),
            ('re_sampling', 'Re-sampling'),
            ('sample_approved', 'Sample Approved'),
            ('order_finalized', 'Order Finalized')
        ],
        string='Sample Status', default='inquiry', tracking=True
    )
    original_sample_verified = fields.Boolean(string='Original Sample Verified', default=False)
    quality_control_passed = fields.Boolean(string='Quality Control Passed', default=False)

    @api.model_create_multi
    def create(self, vals_list):
        # Set default inquiry stage if not specified
        for vals in vals_list:
            if 'sample_status' not in vals:
                vals['sample_status'] = 'inquiry'
        return super(CrmLead, self).create(vals_list)

    def action_verify_sample(self):
        """Mark the original sample as verified."""
        for lead in self:
            lead.original_sample_verified = True

    def action_quality_control_pass(self):
        """Mark quality control as passed."""
        for lead in self:
            lead.quality_control_passed = True

    def action_advance_sample_status(self):
        """Advance the sample status to the next stage."""
        status_sequence = [
            'inquiry', 'sample_development', 'sample_delivered',
            'customer_approval', 'sample_approved', 'order_finalized'
        ]
        for lead in self:
            current_status = lead.sample_status
            if current_status == 'customer_rejection':
                lead.sample_status = 're_sampling'
            elif current_status == 're_sampling':
                lead.sample_status = 'sample_development'
            elif current_status in status_sequence:
                current_index = status_sequence.index(current_status)
                if current_index < len(status_sequence) - 1:
                    lead.sample_status = status_sequence[current_index + 1]
            # If approved, create a sales order
            if lead.sample_status == 'order_finalized':
                self._create_sales_order(lead)

    def action_reject_sample(self):
        """Mark the sample as rejected by the customer."""
        for lead in self:
            lead.sample_status = 'customer_rejection'

    def _create_sales_order(self, lead):
        """Create a sales order from the lead."""
        product = self.env['product.product'].search([('name', '=', 'Sample Product')], limit=1)
        if not product:
            product_template = self.env['product.template'].search([('name', '=', 'Sample Product')], limit=1)
            product = self.env['product.product'].create({
                'product_tmpl_id': product_template.id,
                'name': product_template.name,
            })
        sale_order = self.env['sale.order'].create({
            'partner_id': lead.partner_id.id,
            'opportunity_id': lead.id,
            'order_line': [(0, 0, {
                'product_id': product.id,
                'product_uom_qty': lead.quantity or 1,
            })]
        })
        return sale_order