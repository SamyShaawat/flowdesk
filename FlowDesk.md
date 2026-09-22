# FlowDesk — Odoo Practice Tasks for General Business Operations

*"The connected backbone for growing businesses."*

A set of practice tasks for building a general business operations module in Odoo. Each task is written like a real client request, not a coding exercise. Build it, then record it if you're making a portfolio video.

## How to use this file

1. Start from Easy, move to Medium, then try Hard once you're comfortable.
2. Read the "Scenario" like it's an actual client sitting in front of you. That's the real skill — turning a vague request into a working system.
3. Some tasks say **Depends on** — do that task first, since the next one builds on it.
4. Tasks marked **Full Cycle** need 3-4 modules working together. These are the best ones to show in a video because they prove you understand how Odoo modules connect, not just isolated fixes.

## Difficulty guide

- 🟢 **Easy** — one module, basic configuration, good for warming up
- 🟡 **Medium** — one or two modules, some automation or logic, this is where most real work lives
- 🔴 **Hard** — three or more modules, real business logic, reporting across departments

---

### 🟢 C1. Clean Customer Database
**Modules:** Contacts

**Scenario:** A company's customer list has duplicate entries and no way to tell a wholesale customer from a retail one.

**What to build:** Find and merge duplicate contacts. Add tags for customer type (Wholesale, Retail, VIP).

**Goal:** Sales team can filter customers by type instead of guessing.

---

### 🟢 C2. Professional Quotation Template
**Modules:** Sales

**Scenario:** The current quotation looks generic and customers keep asking about payment terms that aren't even mentioned on it.

**What to build:** Build a quotation template with company terms, validity date, and a standard discount rule for bulk orders.

**Goal:** Every quotation sent out looks professional and answers common customer questions before they're asked.

---

### 🟡 C3. Purchase to Stock Flow
**Modules:** Purchase, Inventory

**Scenario:** The warehouse keeps running out of fast-moving items because nobody notices stock is low until it's already zero.

**What to build:** Set a minimum stock rule per product so a purchase request is created automatically when stock drops below it. Match the vendor bill against what was actually received.

**Goal:** Reordering happens automatically, and finance never pays for more than what physically arrived.

---

### 🟡 C4. Employee Onboarding Checklist
**Modules:** Employees

**Scenario:** New hires get a laptop on day 3 instead of day 1 because nobody has a clear onboarding checklist.

**What to build:** Build an onboarding plan with a checklist of activities (ID badge, laptop request, account setup, orientation meeting) that gets created automatically for every new hire.

**Goal:** Every new employee gets the exact same, complete onboarding — nothing forgotten.

---

### 🟡 C5. Expense Approval Workflow
**Modules:** Expenses, Accounting

**Scenario:** Employees submit expense receipts on paper and reimbursement takes weeks because approvals get lost.

**What to build:** Employee submits an expense digitally → manager approves or rejects → approved expense is reimbursed and logged in accounting automatically.

**Goal:** Reimbursement time drops from weeks to days, with a clear approval trail.

---

### 🟡 C6. Sales Commission Feeding into Payroll
**Modules:** Sales, Accounting, Employees

**Scenario:** Salespeople get a commission on invoices that are actually paid, but finance currently calculates this manually every payroll cycle.

**What to build:** Calculate commission based on paid invoices linked to each salesperson, and feed the result into their payslip as an input automatically.

**Goal:** Commission on the payslip is always accurate and needs no manual calculation.

---

### 🟡 C7. Paid Helpdesk Ticket
**Modules:** Helpdesk, Sales, Accounting

**Scenario:** The company offers paid premium support, but tickets and payments are tracked in two disconnected systems.

**What to build:** A support ticket that requires payment before being marked "In Progress" — ticket links to a sale order, which links to an invoice.

**Goal:** Support staff can see, right on the ticket, whether the customer has actually paid.

---

### 🟡 C8. Vendor Bill 3-Way Match
**Modules:** Purchase, Inventory, Accounting

**Scenario:** The company was once billed for more items than were actually delivered, and nobody caught it until later.

**What to build:** Match the purchase order quantity, the goods actually received, and the vendor bill quantity — flag any mismatch before payment is approved.

**Goal:** No vendor bill gets paid unless what was ordered, received, and billed all match.

**Depends on:** C3

---

### 🟡 C9. Fleet and Driver Assignment
**Modules:** Fleet, Employees

**Scenario:** Company cars are assigned informally and nobody tracks service costs per car or per driver.

**What to build:** Assign company vehicles to specific employees. Log service and repair costs per vehicle. Build a report of cost per driver.

**Goal:** Management can see exactly which car (and which driver) is costing the most to maintain.

---

### 🔴 C10. Full Cycle — Lead to Paid Invoice with Commission
**Modules:** CRM, Sales, Inventory, Accounting, Employees

**Scenario:** Ownership wants to see the complete life of a deal — from the first lead contact, through delivery, to getting paid, to the salesperson's commission — instead of piecing it together from five different reports.

**What to build:** Lead enters CRM → quotation becomes a sale order → stock is reserved and delivered → invoice is generated and paid → the paid invoice automatically calculates the salesperson's commission for payroll.

**Goal:** One deal, fully traceable from first contact to the salesperson getting paid their commission — proof that every module in Odoo can work as one connected system.

**Depends on:** C6

---

## Best task for your portfolio video

**C10 — Full Cycle: Lead to Paid Invoice with Commission** is the strongest pick for FlowDesk. It proves you can connect CRM, Sales, Inventory, Accounting, and HR into one working deal — not just fix one isolated bug.
