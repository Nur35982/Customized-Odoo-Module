# Harnest Label Industries Odoo Module

Custom Odoo 18.0 module for Harnest Label Industries to manage CRM and sales processes, including inquiries, sample development, and order finalization.

## Features
- Manage leads with custom fields (fabric quality, quantity, delivery lead time).
- Workflow: Inquiry → Sample Development → Sample Delivery → Customer Approval/Rejection → Re-sampling → Order Finalization.
- Supports Bengali and English languages.
- Integrates with Odoo CRM and Sales modules.

## Installation
1. Place the module in your Odoo `addons` or `custom` directory.
2. Update the Odoo module list: `python odoo-bin -c odoo.conf -u harnest_label_industries`.
3. Install via Odoo Apps menu.

## Dependencies
- `crm`
- `sale_management`

## License
MIT
