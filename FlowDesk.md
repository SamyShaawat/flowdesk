# FlowDesk - Odoo Practice Tasks for General Business Operations

*"The connected backbone for growing businesses."*

These are practice tasks for building a general business operations module in Odoo 19. I wrote every task the way a real client would ask for it, so don't expect a click-by-click tutorial. Figuring out what the client actually needs is part of the work.

The tasks come in two parts:

- **Part 1 - Core Business Flows (C1-C11):** set up and connect what standard Odoo already offers, with some automation and custom logic on top.
- **Part 2 - Real Business Gaps (N1-N11):** **none of these features exist in standard Odoo**. Every task is a real problem that real companies complain about, and that clients pay developers to solve.

Build it, test it, and if you're making a portfolio video, record it.

## Before you start

- Create a custom module called `flowdesk` and put all your work inside it.
- Even when a task is mostly setup (tags, templates, rules), try to save that setup in your module as XML or CSV data files. My test is simple: I install your module on a new, empty database and your work should be there. Anything you only clicked in the UI is gone with the database.
- Each task has an **Apps** line. Install those apps before you start the task.
- If you don't see an app called **Accounting**, use **Invoicing**. It covers everything these tasks need.
- Menu names and settings move around a bit between Odoo versions. If a hint points to something you can't find in your version, look for the same feature under a different name.
- For Part 2, before you build, spend 10 minutes checking that Odoo really doesn't do it already. If you find something close, extend it instead of rebuilding it, and write down what you found.
- Create some test data before testing: some customers and vendors, a few products, and 2 or 3 employees (salespeople and managers).

## How to read each task

- **Why this task** (Part 2 only) - what's missing in standard Odoo and why companies need it.
- **Scenario** - the problem, the way the client explains it to you. Read it like the client is sitting in front of you.
- **What to build** - what I expect you to deliver.
- **Done when** - the checklist I'll use to test your work. If every point works, the task is done.
- **Hints** - where to look in Odoo. Only read them if you're stuck.
- **Goal** - what the client gets out of it. If your solution works but doesn't reach the goal, it's not finished.
- **Depends on** - finish that task first, because this one builds on it.

If something is not clear, make a reasonable decision, write it down in a short note, and keep going. That's what you'd do with a real client too.

## Difficulty

- 🟢 **Easy** - one app, mostly configuration, or a few new fields with a simple rule or scheduled action. Good for warming up.
- 🟡 **Medium** - one or two apps, with blocking rules, automation, or custom logic. Most real client work looks like this.
- 🔴 **Hard** - three or more apps, real business logic (a full approval or money workflow, accounting entries), and reporting across departments.

## Suggested order

Finish Part 1 first, then Part 2.

- **Part 1:** C1 → C2 → C3 → C8 → C4 → C5 → C9 → C7 → C6 → C10 → C11
- **Part 2:** N1 → N2 → N3 → N4 → N5 → N6 → N7 → N8 → N9 → N10 → N11

## Progress

Tick a box when every **Done when** point of that task works.

**Part 1 - Core Business Flows**

- [x] C1. Clean Customer Database
- [x] C2. Professional Quotation Template
- [ ] C3. Purchase to Stock Flow
- [ ] C8. Vendor Bill 3-Way Match
- [ ] C4. Employee Onboarding Checklist
- [ ] C5. Expense Approval Workflow
- [ ] C9. Fleet and Driver Assignment
- [ ] C7. Paid Helpdesk Ticket
- [ ] C6. Sales Commission Feeding into Payroll
- [ ] C10. Full Cycle - Lead to Paid Invoice with Commission
- [ ] C11. Discount Limits with Manager Approval

**Part 2 - Real Business Gaps**

- [ ] N1. Mandatory Reason for Cancelled Quotations
- [ ] N2. Automatic Follow-up on Silent Quotations
- [ ] N3. Vendor Document Expiry Tracking
- [ ] N4. Customer Credit Limit That Actually Blocks
- [ ] N5. Return Reasons and Return Analysis
- [ ] N6. Inventory Count Approval for Big Differences
- [ ] N7. Customer Promise-to-Pay Tracking
- [ ] N8. Fleet Service Reminders by Kilometers
- [ ] N9. Multi-Level Purchase Approval by Amount and Department
- [ ] N10. Employee Cash Advances Settled by Expenses
- [ ] N11. Post-Dated Cheque Management

---

## Part 1 - Core Business Flows

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

## Part 2 - Real Business Gaps

### 🟢 N1. Mandatory Reason for Cancelled Quotations
**Apps:** Sales

**Why this task:** CRM has lost reasons for opportunities, but a quotation in Sales can be cancelled with no reason at all. Companies that quote directly from Sales (without CRM) have no idea why they lose deals.

**Scenario:** "Half our quotations get cancelled and I don't know why. Was it the price? The delivery time? Did we just forget to follow up? I want to know where we're losing money."

**What to build:**
1. A list of cancel reasons the sales manager can manage: **Price too high**, **Delivery too slow**, **Went to competitor**, **Customer changed mind**, **No response**.
2. Cancelling a quotation asks for a reason (required) and an optional note.
3. A report of cancelled quotations by reason, by salesperson, and by month, with the lost amount.

**Done when:**
- Clicking Cancel on a quotation opens a small popup. You can't cancel without picking a reason.
- The reason and note are shown on the cancelled quotation and in the chatter.
- The manager can add a new reason without a developer.
- The report shows, for example, "Price too high: 12 quotations, 85,000 lost" and can be grouped by salesperson.
- Cancelling a confirmed sale order asks for a reason too.

**Hints:**
- Find the method behind the Cancel button and route it through your wizard. Other code also cancels orders (for example, merging or reset flows), so don't break those.
- A pivot or graph view on sale orders filtered by the cancelled state is enough for the report.

**Goal:** The company knows exactly why it loses deals, and can fix the biggest reason first.

---

### 🟢 N2. Automatic Follow-up on Silent Quotations
**Apps:** Sales

**Why this task:** Odoo shows a quotation as **Quotation Sent**, and then nothing happens. There's no reminder when the customer goes silent, so quotations just die in the list.

**Scenario:** "My salespeople send a quote and forget about it. Two weeks later the customer bought from someone else, and nobody even called them."

**What to build:**
1. A setting for the number of days without an answer before a follow-up is needed (for example 3 days).
2. Every day, sent quotations with no reply after that many days get a **Follow up** activity for their salesperson.
3. A second reminder after a longer delay (for example 7 days), sent to the sales manager this time.
4. A **Days waiting** field on the quotation, visible in the list.

**Done when:**
- A quotation sent 4 days ago with a 3-day setting gets one follow-up activity for its salesperson.
- Running the scheduled job again the same day doesn't create a second activity.
- A quotation that was confirmed, cancelled, or already has an open follow-up activity gets nothing.
- After 7 days the sales manager gets the escalation activity.
- The quotation list can be sorted by Days waiting.

**Hints:**
- A scheduled action (cron) running once a day is the right tool.
- Decide what "no reply" means: no new customer message in the chatter? No change of state? Write it down.

**Goal:** No quotation is forgotten. Every customer gets a follow-up call before they go to a competitor.

---

### 🟢 N3. Vendor Document Expiry Tracking
**Apps:** Contacts, Purchase

**Why this task:** Many companies must only buy from vendors with a valid commercial registration, tax certificate, or insurance. Odoo stores attachments on a contact, but it has no idea when a document expires.

**Scenario:** "Our auditor found we had paid a vendor whose tax certificate expired 8 months ago. We got fined. I need to know before a document expires, not after."

**What to build:**
1. On each vendor, a list of documents: document type, number, expiry date, and the file.
2. A status for each document: **Valid**, **Expiring soon** (within 30 days), **Expired**.
3. A daily reminder to the purchase team for documents expiring soon.
4. A warning on the purchase order when the vendor has an expired document.

**Done when:**
- You can add a tax certificate to a vendor with its expiry date and a scanned file.
- A document expiring in 20 days shows Expiring soon, and the purchase team gets an activity or email about it.
- Creating a purchase order for a vendor with an expired document shows a clear warning.
- The purchase team can list every vendor with an expired or expiring document in one click.

**Hints:**
- A new model linked to the contact, with a computed status field. Remember that "today" changes every day, so think about how the status stays correct (stored or not stored).
- Start with a warning. Blocking the purchase order is a business decision, so ask yourself whether the client wants that and write it down.

**Goal:** The company never buys from a vendor whose papers are out of date, and the auditor finds nothing.

---

### 🟡 N4. Customer Credit Limit That Actually Blocks
**Apps:** Sales, Accounting

**Why this task:** Odoo 19 lets you set a credit limit on a customer, but it only shows a warning. The salesperson can still confirm the order, and the warehouse still ships it.

**Scenario:** "We have customers who owe us 200,000 and still get new deliveries every week, because the salesperson just clicks past the warning. I want a hard stop, and only finance can let it through."

**What to build:**
1. When a sale order would push the customer over their credit limit (unpaid invoices + open orders + this order), it can't be confirmed.
2. The same block when the customer has any invoice overdue by more than X days (for example 60), even if they're under the limit.
3. A **Request Credit Approval** button. Finance gets notified and can approve this one order with a comment.
4. Finance can also put a customer **On Hold** manually, which blocks every new order.

**Done when:**
- Customer with a 50,000 limit and 45,000 unpaid: an order of 3,000 goes through, an order of 10,000 is blocked with a message showing the numbers.
- Customer with an invoice 70 days overdue is blocked even for a small order.
- Finance approves the blocked order, and now the salesperson can confirm it. Changing the order total after approval needs approval again.
- A customer On Hold can't have any order confirmed until finance removes the hold.
- Finance can see a list of every approval they gave, by customer.

**Hints:**
- Look at how Odoo computes the credit limit warning (`partner_id.credit` and the setting in Accounting). Reuse that number instead of calculating debt from scratch.
- Only users in a finance group should be able to approve or change the hold. Salespeople shouldn't be able to edit the limit either.

**Goal:** No more goods go out to customers who already owe too much, unless finance decided it on purpose.

---

### 🟡 N5. Return Reasons and Return Analysis
**Apps:** Inventory, Sales

**Why this task:** Odoo can create a return from a delivery, but it never asks why. The company can't tell a damaged product from a wrong delivery from a customer who changed their mind.

**Scenario:** "We have a lot of returns and I have no idea if it's the supplier's quality, our packing, or the warehouse picking the wrong item. Every reason needs a different fix."

**What to build:**
1. A list of return reasons, each with a **responsible** side: **Supplier** (defective), **Warehouse** (wrong item, bad packing), **Customer** (changed mind), **Transport** (damaged in transit).
2. Creating a return asks for a reason for each returned line.
3. Returned items with reason Defective go to a **Quarantine** location, not back to sellable stock.
4. A report of returns by product, reason, responsible side, and customer.

**Done when:**
- You can't validate a return without a reason on every line.
- A product returned as Defective ends up in Quarantine and isn't available for new sales.
- A product returned as Changed mind goes back to normal stock.
- The report shows, for example, that one product has 15 returns and 12 of them are Defective (a supplier problem).
- From a return you can open the original delivery and sale order.

**Hints:**
- Look at the return wizard in Inventory (`stock.return.picking`) and add the reason there.
- The quarantine location can be a normal internal location that isn't part of the warehouse's sellable stock.

**Goal:** Every return has a known cause, and management can fix the source of the problem instead of paying for it again.

---

### 🟡 N6. Inventory Count Approval for Big Differences
**Apps:** Inventory

**Why this task:** In Odoo, anyone with inventory access can count a product and apply the new quantity right away. A 500-unit "correction" posts straight to stock and accounting with nobody checking it.

**Scenario:** "Someone in the warehouse 'fixed' the count of an expensive item from 120 to 20. That's 100 units gone, and it hit the books without anyone asking why. Small differences are fine, big ones need me."

**What to build:**
1. An approval threshold, by value (for example 1,000) and by percentage (for example 10%).
2. Counted quantities with a difference below the threshold are applied normally.
3. Counts above the threshold need a reason and go to **Waiting Approval** instead of being applied.
4. The inventory manager approves or rejects. Approved counts are applied, rejected ones are reset.
5. A log of every approved adjustment: product, old quantity, new quantity, value, who counted, who approved.

**Done when:**
- Counting a cheap product 2 units off applies immediately.
- Counting an expensive product 100 units off can't be applied. It shows Waiting Approval and the manager is notified.
- A warehouse user can't approve their own count.
- The manager approves and the stock (and the stock valuation) update. Rejecting leaves stock unchanged.
- The owner can list all big adjustments of the last month with their total value.

**Hints:**
- Look at `stock.quant` and the method that applies counted quantities. Every way to apply a count must go through your check, not only the button you see first.
- Use the product cost for the value.

**Goal:** Stock can still be corrected quickly, but nobody can make valuable stock disappear without a manager signing it off.

---

### 🟡 N7. Customer Promise-to-Pay Tracking
**Apps:** Accounting, Contacts
**Depends on:** N4

**Why this task:** Odoo follow-ups send reminders, but when a customer calls and says "I'll pay on the 15th", there's nowhere to record that promise, and nothing happens if the 15th passes and no money comes.

**Scenario:** "My collections person spends all day on the phone. Customers promise dates and amounts, they get written in a notebook, and half the promises are broken without anyone noticing."

**What to build:**
1. A **Promise to Pay** on a customer: date, amount, which invoices, and a note from the call.
2. When a payment comes in, the promise is marked **Kept** (fully or partly).
3. The day after the promise date, if the amount wasn't paid, it becomes **Broken** and the collections person gets an activity.
4. A customer with 2 broken promises in 90 days is put **On Hold** automatically (using the hold from N4).
5. A report of promises by customer: kept, broken, and the total amount still promised.

**Done when:**
- The collections person records "10,000 on the 15th" for a customer in under a minute, from the customer or the invoice.
- The customer pays 10,000 before the 15th: the promise shows Kept.
- The customer pays 4,000: the promise shows Partly kept with 6,000 missing.
- The 16th arrives with no payment: the promise shows Broken and an activity is created.
- A second broken promise puts the customer on hold, and new sale orders are blocked.

**Hints:**
- A daily scheduled action checks the due promises.
- Decide which payments count toward a promise: only payments on the promised invoices, or any payment from that customer. Write it down.

**Goal:** Collections knows which customers keep their word, and the ones who don't stop getting new goods.

---

### 🟡 N8. Fleet Service Reminders by Kilometers
**Apps:** Fleet

**Why this task:** Odoo Fleet records odometer readings and services, and it reminds you about contracts that expire. It doesn't know that a car needs an oil change every 10,000 km, so services get missed until the car breaks down.

**Scenario:** "One of our delivery vans ran 25,000 km past its oil change and the engine died. The odometer was logged every week, and nobody connected the dots."

**What to build:**
1. Service plans per vehicle model: service type and interval in km and/or months (for example oil change every 10,000 km or 6 months, whichever comes first).
2. Each vehicle shows its next due service with the km and date it's due.
3. When a new odometer reading gets within X km of a due service (for example 500 km), the fleet manager gets an activity.
4. Logging the service resets the counter for that service type.
5. An **Overdue services** list across the whole fleet.

**Done when:**
- A van with 9,600 km since its last oil change and a 10,000 km plan gets a reminder after its next odometer reading.
- A car that barely drives still gets its oil change reminder after 6 months.
- Logging the oil change moves the next due km forward by 10,000.
- The fleet manager sees every overdue vehicle in one list, sorted by how late it is.

**Hints:**
- Fleet already has vehicle models, odometer logs (`fleet.vehicle.odometer`), and service logs. Build on them.
- Trigger the check when an odometer reading is saved, and also daily for the month-based part.

**Goal:** Vehicles are serviced on time, and the company stops paying for engines that died of neglect.

---

### 🔴 N9. Multi-Level Purchase Approval by Amount and Department
**Apps:** Purchase, Employees, Accounting

**Why this task:** Odoo Purchase has one approval level: orders above one amount need a manager. Real companies have a chain: department head, then finance, then the general manager, depending on the amount and the department.

**Scenario:** "Our IT head approves their own team's laptops, finance checks anything above 20,000, and I sign everything above 100,000. Right now we do it on paper and WhatsApp, and orders get placed before anyone signs."

**What to build:**
1. Approval rules: department, amount range, and the ordered list of approvers (a person or a role like "Department manager").
   - Up to 5,000: department manager.
   - 5,000 to 20,000: department manager, then finance manager.
   - Above 20,000: department manager, then finance manager, then general manager.
2. Each purchase order belongs to a department (from the employee who requested it).
3. The order can't be confirmed until every required approver has approved, **in order**. Each approver is notified only when it's their turn.
4. Any approver can reject with a reason. The order goes back to the requester.
5. Changing the amount or lines after an approval restarts the approvals.
6. A **Pending my approval** menu for each approver, and a report of how long approvals take.

**Done when:**
- A 3,000 order from IT needs only the IT manager. A 50,000 order needs all three, one after the other.
- The finance manager can't approve before the department manager did.
- Nobody can approve their own purchase order.
- Adding a line after the first approval sends the order back to the start of the chain.
- Each approval (who, when, comment) is shown on the order.
- The general manager sees the average approval time per department.

**Hints:**
- Odoo's own "Order Approval" setting uses the `to approve` state. See how it works, then decide whether to extend it or replace it.
- Store each approval step as a line on the order. That gives you the history and the report almost for free.

**Goal:** No purchase is placed without the right signatures, and management can see where approvals get stuck.

---

### 🔴 N10. Employee Cash Advances Settled by Expenses
**Apps:** Expenses, Accounting, Employees

**Why this task:** Odoo Expenses handles "employee paid, company reimburses". It has no clean flow for the opposite, very common case: the company gives the employee cash first (for a trip or site purchases), and the employee then justifies it with receipts.

**Scenario:** "Our site engineers get 5,000 cash before each project visit. Months later, nobody knows who still holds company cash, who handed in receipts, and who owes us money back."

**What to build:**
1. An **advance request**: employee, amount, purpose, and expected settlement date. It's approved by the employee's manager, then paid by finance.
2. Paying the advance posts an accounting entry to an **Employee Advances** account (money the employee owes the company), not to an expense.
3. The employee settles the advance with their expenses. The expenses reduce the advance balance instead of being reimbursed.
4. When the advance is closed:
   - Expenses less than the advance: the employee returns the difference (cash back or payroll deduction, you choose).
   - Expenses more than the advance: the company pays the difference.
5. An advances report per employee: given, justified, still open, and overdue.
6. An employee with an overdue open advance can't request a new one.

**Done when:**
- Advance of 5,000 approved and paid: the Employee Advances account shows 5,000 for that employee.
- Employee submits 4,200 in expenses against it: the balance shows 800 still to return. The expenses aren't paid out a second time.
- Employee returns 800: the advance is closed and the account balance for that employee is 0.
- A second case with 5,600 in expenses: the company pays the extra 600.
- Finance sees every employee still holding company cash, and for how long.
- Every step has an accounting entry that an accountant would agree with.

**Hints:**
- Use a receivable-type account for employee advances, with the employee's contact as the partner, so balances per employee come from the accounting itself.
- Look at how an expense's payment mode ("paid by employee" vs "paid by company") changes its accounting entry, before you design yours.
- Write down the journal entries for each step on paper before you code anything.

**Goal:** The company always knows who holds its cash, and every advance ends with receipts or money back.

---

### 🔴 N11. Post-Dated Cheque Management
**Apps:** Accounting, Sales, Purchase

**Why this task:** In many markets (Middle East, Africa, Asia) customers pay with post-dated cheques: you receive the cheque today, but you can only deposit it on a future date. Odoo has no cheque life cycle. Companies track hundreds of cheques in Excel, and bounced cheques get lost.

**Scenario:** "We have 300 customer cheques in the safe right now. I don't know which ones are due this week, which ones are at the bank, and which ones bounced. Last month a 40,000 cheque bounced and we kept delivering to that customer for three weeks."

**What to build:**
1. A **cheque** record for received (customer) and issued (vendor) cheques: number, bank, amount, cheque date (due date), partner, and the invoices it pays.
2. A life cycle with states and matching accounting entries:
   - **Received** (in the safe): the customer's debt moves to a **Cheques Under Collection** account.
   - **Deposited** at the bank.
   - **Cleared**: money reaches the bank account.
   - **Bounced**: the debt goes back to the customer, with an optional bank fee charged to them.
   - **Returned** to the customer or **Replaced** by a new cheque.
3. Issued cheques to vendors with the same idea (Issued → Cleared or Cancelled), using a **Cheques Payable** account.
4. A dashboard: cheques due this week, cheques at the bank, bounced cheques, and total amount per state.
5. A bounced cheque puts the customer on hold (reuse N4 if you did it) and creates an activity for collections.

**Done when:**
- A customer gives a 10,000 cheque dated next month. The invoice shows as paid by cheque, but the money isn't in the bank account yet.
- On its date, the cheque shows in "due this week" and can be deposited in one click. Several cheques can be deposited together.
- Clearing moves the money to the bank. Bouncing brings the 10,000 back to the customer balance and the invoice is unpaid again.
- A bounced cheque blocks new sale orders for that customer.
- Every state change has its accounting entry and is visible in the cheque's chatter.
- The owner sees in one screen how much money is sitting in cheques and when it will come in.

**Hints:**
- Look at how Odoo payments use an outstanding receipts account before reconciliation with the bank statement. Your Cheques Under Collection account plays a similar role.
- Don't let a user jump states (for example Received straight to Cleared without Deposited) unless you decide that's allowed, and write it down.
- Write down the journal entry for every state change on paper before coding. If the entries are wrong, nothing else matters.

**Goal:** The company knows at any moment where every cheque is and how much cash is coming, and a bounced cheque is caught the same day, not three weeks later.

---

## Best tasks for your portfolio video

- **Part 1:** pick **C10 - Full Cycle: Lead to Paid Invoice with Commission**. It shows CRM, Sales, Inventory, Accounting, and HR working together on one deal, which is exactly what clients hire an Odoo developer for.
- **Part 2:** pick **N11 - Post-Dated Cheque Management**. It solves a problem that thousands of companies have and standard Odoo doesn't cover, and it shows you understand accounting, not only forms and buttons. **N9 - Multi-Level Purchase Approval** is a strong second choice: every mid-size company asks for it.

## What to hand in

- Your `flowdesk` module (it should install on a new database without errors).
- A short note with any decisions you made where the task left the choice to you.
- For each Part 2 task, one line saying what you checked in standard Odoo before building it.
- Optional: a short video of the task working.
