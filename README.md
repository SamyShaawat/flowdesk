# FlowDesk

*"The connected backbone for growing businesses."*

FlowDesk is a custom Odoo 19 module that I build one practice task at a time. The tasks are written like real client requests and cover everyday business operations, from lead to paid invoice: CRM, Sales, Purchase, Inventory, Accounting, HR, Expenses, Helpdesk, Fleet, and Project.

All the work is saved in the module as code and XML/CSV data, so installing the module on a new, empty database brings everything back. Nothing is set up only through the UI.

## Tasks

The full task list, with scenarios, acceptance checks, and hints, is in [FlowDesk.md](FlowDesk.md).

- **Part 1 - Core Business Flows (C1-C11):** set up and connect standard Odoo features, with some automation and custom logic on top.
- **Part 2 - Real Business Gaps (N1-N11):** features that standard Odoo doesn't have, such as a credit limit that really blocks orders, multi-level purchase approvals, and post-dated cheque management.

The **Progress** section in [FlowDesk.md](FlowDesk.md) shows which tasks are done.


## Requirements

- Odoo 19.0 **Enterprise** (the module depends on `helpdesk` and `website_enterprise`)
- Apps it depends on: Contacts, CRM, Sales, Purchase, Inventory, Employees, Expenses, Accounting/Invoicing, Helpdesk, Fleet, Project, Website

## Installation

1. Put the `flowdesk` folder in a directory listed in your `addons_path`.
2. Restart Odoo and update the apps list.
3. Install **FlowDesk** from Apps, or from the command line:

   ```bash
   ./odoo-bin -c odoo.conf -d <database> -i flowdesk
   ```

4. After pulling new changes, upgrade the module:

   ```bash
   ./odoo-bin -c odoo.conf -d <database> -u flowdesk
   ```

Install with demo data to get the sample duplicate customers used in C1.

## Module structure

```
flowdesk/
├── data/        # configuration saved as data (tags, templates, pricelists, settings)
├── demo/        # sample records for testing
├── models/      # model extensions
├── views/       # form, list, and search view changes, menus
├── report/      # QWeb report changes (e.g. the quotation PDF)
├── security/    # groups and access rights
├── controllers/
├── wizard/
└── FlowDesk.md  # the task list
```
