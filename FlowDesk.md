# FlowDesk - Odoo Practice Tasks for General Business Operations

*"The connected backbone for growing businesses."*

These are practice tasks for building a general business operations module in Odoo. I wrote every task the way a real client would ask for it, so don't expect a click-by-click tutorial. Figuring out what the client actually needs is part of the work.

Build it, test it, and if you're making a portfolio video, record it.

## Before you start

- Create a custom module called `flowdesk` and put all your work inside it.
- Even when a task is mostly setup (tags, templates, rules), try to save that setup in your module as XML or CSV data files. My test is simple: I install your module on a new, empty database and your work should be there. Anything you only clicked in the UI is gone with the database.
- Each task has an **Apps** line. Install those apps before you start the task.
- If you don't see an app called **Accounting**, use **Invoicing**. It covers everything these tasks need.
- Menu names and settings move around a bit between Odoo versions. If a hint points to something you can't find in your version, look for the same feature under a different name.
- Create some test data before testing: some customers and vendors, a few products, and 2 or 3 employees (salespeople and managers).

## How to read each task

- **Scenario** - the problem, the way the client explains it to you. Read it like the client is sitting in front of you.
- **What to build** - what I expect you to deliver.
- **Done when** - the checklist I'll use to test your work. If every point works, the task is done.
- **Hints** - where to look in Odoo. Only read them if you're stuck.
- **Goal** - what the client gets out of it. If your solution works but doesn't reach the goal, it's not finished.
- **Depends on** - finish that task first, because this one builds on it.

If something is not clear, make a reasonable decision, write it down in a short note, and keep going. That's what you'd do with a real client too.

## Difficulty

- 🟢 **Easy** - one app, mostly configuration. Good for warming up.
- 🟡 **Medium** - one or two apps, with some automation or custom logic. Most real client work looks like this.
- 🔴 **Hard** - three or more apps, real business logic, and reporting across departments.

## Suggested order

C1 → C2 → C3 → C8 → C4 → C5 → C9 → C7 → C6 → C10 → C11

---

### 🟢 C1. Clean Customer Database
**Apps:** Contacts

**Scenario:** A company's customer list is full of duplicates, and there's no way to tell a wholesale customer from a retail one.

**What to build:**
1. Find the duplicate contacts and merge them.
2. Add tags for customer type: **Wholesale**, **Retail**, and **VIP**.

**Done when:**
- Create a few duplicates on purpose (same company typed twice, slightly different names). After merging, each customer exists only once, and their past quotations and invoices are still attached.
- Every customer has a type tag.
- The sales team can filter customers by Wholesale, Retail, or VIP in one click.

**Hints:**
- Odoo already has a merge tool for contacts. Select the duplicates in the list view and look in the Actions menu.

**Goal:** The sales team filters customers by type instead of guessing.

---

### 🟢 C2. Professional Quotation Template
**Apps:** Sales

**Scenario:** The current quotation looks generic, and customers keep asking about payment terms that aren't even on it.

**What to build:** A quotation template with:
1. The company's terms and conditions.
2. A validity date (for example, 30 days from the quotation date).
3. The payment terms.
4. A standard discount rule for bulk orders. Pick the rule (for example, 10% off when ordering 100 units or more) and write it down.

**Done when:**
- A new quotation made from the template already has the terms, validity date, and payment terms filled in.
- The bulk discount applies automatically when the quantity is high enough, and not below it.
- The printed/PDF quotation shows the terms, validity date, and payment terms clearly.

**Hints:**
- Turn on **Quotation Templates** in Sales settings.
- A pricelist rule with a minimum quantity can handle the bulk discount.

**Goal:** Every quotation looks professional and answers the usual customer questions before they're asked.

---

### 🟡 C3. Purchase to Stock Flow
**Apps:** Purchase, Inventory

**Scenario:** The warehouse keeps running out of fast-moving items because nobody notices stock is low until it hits zero.

**What to build:**
1. A minimum stock rule for each product, so a purchase request is created automatically when stock drops below the minimum.
2. Vendor bills that are checked against what was actually received.

**Done when:**
- When stock of a product drops below its minimum, a purchase request (RFQ) for that product is created without anyone asking for it.
- If you order 100 units and only 80 arrive, the vendor bill is for 80, not 100.
- Nobody has to check stock levels by hand.

**Hints:**
- Look at reordering rules in Inventory.
- Look at the bill control setting in Purchase (ordered quantities vs received quantities).

**Goal:** Reordering happens automatically, and finance never pays for more than what physically arrived.

---

### 🟡 C4. Employee Onboarding Checklist
**Apps:** Employees

**Scenario:** New hires get their laptop on day 3 instead of day 1, because nobody has a clear onboarding checklist.

**What to build:**
1. An onboarding plan with this checklist of activities:
   - ID badge
   - Laptop request
   - Account setup
   - Orientation meeting
2. The plan is created **automatically** for every new hire.

**Done when:**
- Creating a new employee creates all 4 activities right away, with nobody starting the plan by hand.
- Each activity is assigned to the right person (for example IT for the laptop, HR for the badge) and has a due date.
- The activities show up in the assigned people's activity lists.

**Hints:**
- Look for onboarding or activity plans in the Employees configuration. If your version doesn't have them, activities created by an automated action do the same job.
- Odoo lets you launch a plan by hand. Making it automatic is the part you need to build.

**Goal:** Every new employee gets the same complete onboarding, with nothing forgotten.

---

### 🟡 C5. Expense Approval Workflow
**Apps:** Expenses, Accounting

**Scenario:** Employees hand in paper receipts, and reimbursement takes weeks because approvals get lost.

**What to build:** This flow:
1. The employee submits an expense in Odoo, with a photo of the receipt.
2. Their manager approves or rejects it.
3. The approved expense is reimbursed and recorded in accounting automatically.

**Done when:**
- An employee can submit an expense with a receipt attached.
- Their manager gets notified and can approve or reject.
- A rejected expense goes back to the employee with the reason.
- An approved expense creates the accounting entry and can be paid.
- Anyone can look at an expense and see who approved it and when.

**Goal:** Reimbursement time drops from weeks to days, with a clear approval trail.

---

### 🟡 C6. Sales Commission Feeding into Payroll
**Apps:** Sales, Accounting, Employees (plus Payroll)

**Scenario:** Salespeople earn a commission on invoices that are actually paid. Right now finance works it out by hand every payroll cycle.

**What to build:**
1. Calculate each salesperson's commission from the **paid** invoices linked to them.
2. Put that amount on their payslip automatically, as an input.

**Done when:**
- Only paid invoices count. An invoice that isn't paid yet adds nothing.
- The commission is calculated for the right salesperson and the right payroll period.
- When the payslip is generated, the commission line is already there with the right amount. Nobody types it in.
- A salesperson with no paid invoices gets no commission (or 0).

**Hints:**
- Payslips come from a Payroll app. Any payroll module works. If your Odoo doesn't have one, there are free payroll modules on the Odoo Apps store and from the OCA.
- You decide the commission rate and whether partially paid invoices count. Write down what you chose.

**Goal:** Commission on the payslip is always right and never needs manual calculation.

---

### 🟡 C7. Paid Helpdesk Ticket
**Apps:** Helpdesk, Sales, Accounting

**Scenario:** The company sells paid premium support, but tickets and payments are tracked in two separate systems.

**What to build:**
1. A support ticket linked to a sale order, which is linked to an invoice.
2. The ticket can't move to **In Progress** until the invoice is paid.
3. The payment status is visible right on the ticket.

**Done when:**
- From the ticket you can open its sale order and invoice.
- Trying to move an unpaid ticket to In Progress is blocked, with a clear message.
- Once the invoice is paid, the ticket can move to In Progress.
- Support staff can see on the ticket (and in the ticket list) whether the customer has paid.

**Hints:**
- Check what your Helpdesk app already links to Sales before building links yourself.
- If you don't have a Helpdesk app, a simple ticket model of your own with stages works fine.

**Goal:** Support staff can see, right on the ticket, whether the customer actually paid.

---

### 🟡 C8. Vendor Bill 3-Way Match
**Apps:** Purchase, Inventory, Accounting
**Depends on:** C3

**Scenario:** Once, the company was billed for more items than were actually delivered, and nobody caught it until much later.

**What to build:**
1. Compare three quantities for each purchase: **ordered** (purchase order), **received** (goods receipt), and **billed** (vendor bill).
2. Flag any mismatch before the bill can be paid.

**Done when:**
- Order 100, receive 100, bill 100: the bill is fine and can be paid.
- Order 100, receive 80, bill 100: the bill is flagged and can't be paid until someone deals with the difference.
- The mismatch is easy to spot (a status, a filter, or a warning), without opening every bill one by one.

**Hints:**
- Check whether your Odoo already has a 3-way matching feature. If it does, see how far it gets you and fill the gaps. If not, build the check yourself.

**Goal:** No vendor bill gets paid unless what was ordered, received, and billed all match.

---

### 🟡 C9. Fleet and Driver Assignment
**Apps:** Fleet, Employees

**Scenario:** Company cars are handed out informally, and nobody tracks service costs per car or per driver.

**What to build:**
1. Assign each company vehicle to a specific employee (the driver).
2. Log service and repair costs for each vehicle.
3. A report of costs per driver.

**Done when:**
- Each vehicle shows its current driver.
- Every service or repair is logged on the vehicle with its cost and date.
- The report shows the total cost per vehicle and per driver, and you can sort it to find the most expensive.
- If a car changes driver, costs from before the change stay with the old driver.

**Hints:**
- Fleet already tracks drivers and services. Check what's there before building your own.

**Goal:** Management can see exactly which car, and which driver, costs the most to maintain.

---

### 🔴 C10. Full Cycle - Lead to Paid Invoice with Commission
**Apps:** CRM, Sales, Inventory, Accounting, Employees
**Depends on:** C6

**Scenario:** The owners want to see the full life of a deal (from the first lead contact, through delivery, to getting paid, to the salesperson's commission) instead of piecing it together from five different reports.

**What to build:** Connect these steps so each one comes from the one before it:
1. A lead comes into CRM.
2. The quotation becomes a sale order.
3. The stock is reserved and delivered.
4. The invoice is created and paid.
5. The paid invoice automatically calculates the salesperson's commission for payroll.

**Done when:**
- You can run one deal from first contact to commission without typing the same data twice.
- From the opportunity you can open the sale order, the delivery, the invoice, and the payment.
- Stock goes down when the delivery is done.
- The commission shows up on the salesperson's payslip only after the invoice is paid.

**Hints:**
- Most of these links already exist in Odoo. Your job is to make sure nothing breaks between the steps and to fill any gaps.
- This is a great one to record. Show one deal going through the whole flow.

**Goal:** One deal, fully traceable from first contact to the salesperson getting their commission, which shows every Odoo app working as one connected system.

---
### 🔴 C11. Discount Limits with Manager Approval
**Apps:** Sales, Employees
**Depends on:** C2

**Why this task:** Nearly every company that has salespeople wants a cap on how much discount they can give. Odoo lets anyone who can edit a quotation type any discount they like.

**Scenario:** Salespeople give big discounts to close deals fast. The owner found quotations going out at 35% off on products with a 30% margin, so the company was losing money on every unit. The rule should be: each salesperson can discount up to a limit, and anything above that needs the sales manager's OK before the customer sees it.

**What to build:**
1. A **maximum discount %** for each salesperson (for example junior 5%, senior 15%). Managers have no limit.
2. When a quotation has a line with a discount above the salesperson's limit, it can't be sent or confirmed. Instead it goes to **Waiting for Approval**.
3. The sales manager gets notified, sees the quotation with the lines over the limit highlighted, and approves or rejects it with a comment.
4. Approved: the salesperson can send and confirm it. Rejected: it goes back to the salesperson with the manager's comment.
5. Every approval is logged on the quotation: who approved, when, and what the discount was.

**Done when:**
- A junior salesperson with a 5% limit gives 4%: the quotation goes out normally.
- The same salesperson gives 12%: sending and confirming are blocked, and the quotation shows Waiting for Approval.
- The manager approves, and now the salesperson can send and confirm it.
- If the salesperson raises the discount again *after* approval, it needs approval again.
- The owner can list every approved discount over the limit, by salesperson.

**Hints:**
- Check the limit when the quotation is sent and when it's confirmed, not only when the line is saved. People find the other buttons.
- Think about discounts that come from a pricelist versus ones typed by hand. Decide whether both count, and write it down.

**Goal:** Salespeople can still negotiate, but no big discount goes out without the manager knowing, and the owner can see every exception.

---

## Best task for your portfolio video

Pick **C10 - Full Cycle: Lead to Paid Invoice with Commission**. It shows CRM, Sales, Inventory, Accounting, and HR working together on one deal, which is exactly what clients hire an Odoo developer for.

## What to hand in

- Your `flowdesk` module (it should install on a new database without errors).
- A short note with any decisions you made where the task left the choice to you.
- Optional: a short video of the task working.
