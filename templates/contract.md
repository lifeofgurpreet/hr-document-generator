# EMPLOYMENT CONTRACT

This Contract of Services ("the Contract") is made and entered into effective as of {{ contract_date }} between 
{{ employee_name }} (NRIC/Passport No: {{ employee_id }}) ("the Employee"), and {{ company.name }} ({{ company.registration_number }}) ("the Employer") ("the Organization"). 

WHEREAS, the Employee desires to perform such services by the Employer as {{ job_title }} pursuant to the terms and conditions set forth in the Contract.

WHEREAS, the Employer desires to have a need from the Employee in such capacity pursuant to the terms and conditions set forth in the Contract.

IT IS HEREBY AGREED as follows: 

## Job Specification

| Field | Value |
|-------|-------|
| Job Title | {{ job_title }} |
| Team | {{ team }} |
| Career Level | {{ career_level }} |
| Contract Term | {{ contract_term }} |
| Contract Start Date | {{ start_date }} |
| Contract End Date | {{ end_date }} |
| Reporting To | {{ reporting_to }} |
| Work Location | {{ work_location }} |

## Job Description & Organization Strategic Area KPI

{{ job_description }}

The Employee is required to attend regular meetings with the project team regarding the strategy and growth of the project. The Employee is also required to manage the project by:
- Facilitating communication between the relevant teams, partners, and stakeholders;
- Reporting potential problems or issues timely; or solving them where possible; and
- Ensuring the relevant teams, partners and stakeholders are aware of all processes and policies that apply to them.

## Role Expectations

As a/an {{ career_level }}, the Employee is expected to perform the following:
{% for responsibility in role_responsibilities %}
- {{ responsibility }}
{% endfor %}

## Strategic Area KPI Breakdown

The Employee is responsible to oversee and execute the roles according to the organization strategic areas KPI, including but not limited to:

| Strategic Area | KPI (%) | Role Focus |
|----------------|---------|------------|
{% for area, details in kpi_breakdown.items() %}
| {{ area }} | {{ details.percentage }}% | {{ details.description }} |
{% endfor %}

## Media Consent

By signing this Contract, you hereby consent for {{ company.name }}, and/or its partners to take your photographs, digital images and/or audio and/or video footage (the images) of and to store the images, make copies of the images and publish the images in any form, in whole or in part, and distribute them in any medium including, but not limited to, print media, the Internet, CD-ROM, other multimedia uses or graphic representation, cinematography or video.

## Working Hours

The Organization general hours of operation are {{ working_hours.general }}.
The Employee may work flexible hours on a weekly basis as long as the weekly hours amount to {{ working_hours.weekly_hours }} hours.

However, there might be occasions where project work requires the Employee to work more than {{ working_hours.weekly_hours }} hours ("Overtime"). In such a situation, the Employee will be informed beforehand and could apply for Replacement Leave. The Employee will need to inform the Manager. (see section J. Leave Entitlements).

### Overtime Replacement Leave
| Overtime Hours | Replacement Leave |
|----------------|-------------------|
{% for hours, leave in overtime_policy.replacement_leave.items() %}
| {{ hours }} | {{ leave }} |
{% endfor %}

The Employee is expected to start work by {{ working_hours.start_time }} daily or earlier if required. If the Employee has obligations outstation (meetings, site visits, etc.), the Employee has to inform his or her manager in advance at all times.

## The Contract Terms & Organization's Policies

The Employee is required to comply with the Organization's policy at all times as enlisted in, but not limited to, the Code of Conduct and Standard Operating Procedures. Failure to do so may result in immediate termination of employment.

The Contract extension term and salary increment are to be determined by the manager and to be approved by the Board, based on the Employee's scope of work (responsibility), overall performance and the Organization's performance.

## Remuneration & Payment Terms

The Employee's fee will be paid in the fourth week of the month and/or first week of the following month. Pro-rata if the Employee starts or ends in the middle of the month.

Salary increment is to be determined by the Employee's manager and to be approved by the Board, based on the Employee's services, overall performance and the Organization's performance. 

The salary (after EPF, PCB, SOCSO and EIS deduction) will be paid monthly.

As proposed, the salary is as follows:
- **Salary**: {{ salary }}; and
- Your salary of {{ salary }} per month is inclusive of payment for every statutory and general Public Holiday in Malaysia.

However, such benefit policies are subject to management's annual review.

## Termination Clause

The Employee shall be required to give {{ termination.notice_period }} written notice to the Organization for termination of this Contract.

The Organization may terminate the Employee's employment by giving a {{ termination.notice_period }} notice period (or payment in lieu) depending on service. 

Following the termination of your employment, the Employee will be required to return all organization and {{ company.name }} property.

Any violation of the Organization's Code of Conduct (refer to Appendix A) policies and procedures will result in an immediate termination of this Contract.

## Leave Entitlement

You are entitled to {{ leave_entitlements.annual_leave }} days of Annual Leave per year if you start to work full-time in January. If the employment period starts at any other month, the annual leave will be automatically prorated.

During the first year of employment, you will acquire leave entitlement on an accrual basis.

In the second year of employment, you will be awarded full leave permission at the beginning of each year and may carry forward 10 days of leave per year.

You are entitled to {{ leave_entitlements.medical_leave }} days of Medical Leave, {{ leave_entitlements.hospitalization_leave }} days of Hospitalization leave (non-maternal), {{ leave_entitlements.paternity_leave }} days of paternity leave, {{ leave_entitlements.maternity_leave }} days of maternity leave, {{ leave_entitlements.compassionate_leave }} days of compassionate leave, and {{ leave_entitlements.study_leave }} days of study leave. However, such leave policies are subject to annual review.

For maternity leave, please provide a 2-month notice to notify the pregnancy to the Supervisor and/or Direct Leader and/or Employer.

If you worked overtime and on Public Holidays, you may, with your manager's approval, apply for Replacement Leave on the Organizations platform. You may utilize all Replacement Leaves in the same month or the following week and do not accumulate after 2-month.

## Benefits

During the Employment Term, the Executive will be entitled to participate in the Holistic Wellness benefit plans. The Employee may have the option to participate in the: 
- {{ benefits.wellness_claim }} wellness claim annually

The Organization is liable to contribute to the Employees Provident Fund (EPF), Social Security Organization (SOCSO) and Employment Insurance System (EIS), for the Organization contribution portion.

## Performance Management

The Employee to jointly agree on the yearly strategic plan and KPIs with the Organization.

The Employee shall deliver the above set KPIs whilst being guided by the Core Values of the Organization. The core values are as follows:

| Item | Core Values | Description |
|------|-------------|-------------|
{% for value in core_values %}
| {{ loop.index }}. | {{ value.name }} | {{ value.description }} |
{% endfor %}

## Confidentiality

All confidential and proprietary information relating to the business or operations of the Organization or off its affiliates shall be kept and treated as confidential both during and after the employment.

---

*** This part is intentionally left blank. ***

The Organization and the Employee hereby declare that they understand thoroughly the above provisions and agree to sign to abide by such provisions. They shall each retain a copy of this contract for future reference.

**Signature of Employee**: _________________

**NRIC / Passport Number**: {{ employee_id }}

**Date**: _________________

**Organization's Initial**: {{ company.name }} ({{ company.registration_number }})

**Date**: _________________

---

## APPENDIX A: CODE OF CONDUCT

Between {{ company.name }} (hereinafter referred to as the "Organization" and "We")

and {{ employee_name }} (hereinafter referred to as "the Employee" and "You")

### Sustainable Working Environment

We maintain an inclusive work environment and achieve excellence by attracting and retaining people of all backgrounds in our workforce.

We have identified mutual respect, honest communication and professional conduct as essential pillars in the culture.

We prohibit sexual, physical, emotional or any other kind of harassment by any person in the workplace or while conducting business.

We strive to avoid favouritism or the appearance of favouritism in the workplace in accordance with the policies and procedures adopted.

We comply with all policies and procedures at all times.

We comply with Malaysian and international law at all times.

We strive to be a contributing member of the global community. We support the human rights movement and aim to maximize positive social impact on our projects.

We are committed to doing our part to help preserve the Earth's finite resources and maintain the wellbeing of our planet for generations to come.

### Equal Employment Opportunities

We provide employment opportunities to all qualified persons on an equal basis. This includes, but is not limited to, recruitment, hiring, promotion, transfer, compensation, training, demotion or layoff. We will not discriminate against any Contractor, Employee or applicant for employment because of:
- Gender or Gender Identity
- Race, Ethnicity or National Origin
- Religion
- Age
- Sexual Orientation
- Disability
- Marital Status

We do not use child labour. Child labour is defined as employing any person younger than the minimum age allowed by law in the jurisdiction in question. However, in no event will we knowingly employ or hire anyone younger than sixteen (16) years of age.

### Health & Safety

We strive to eliminate potential hazards from the workplace and to comply with all applicable occupational safety and health laws and standards.

We help maintain a safe, healthy and productive work environment for all team members and others, by:
- prohibiting any acts that could be perceived as violent, threatening, degrading or intimidating.
- prohibiting the spreading of unconfirmed information, gossip or information that has no other purpose than damaging morale.
- prohibiting bullying
- prohibiting the possession, use, sale or transfer of illegal drugs or drug paraphernalia
- prohibiting the conduct of business while under the influence of alcohol
- prohibiting the possession or use of weapons/firearms, explosive devices or ammunition.

All Contractors/Employees/Interns are required to comply with and understand the importance to follow the Health and Safety guidelines and requirements, including the use of PPE set by the Organization.

☐ I have read and understood the code of conduct and I agree to adhere to its contents for the duration of my affiliation with {{ company.name }}. I understand that failure to do so may result in the immediate termination of my professional relationship with the Organization.

**Name**: {{ employee_name }}

**Date**: _________________

**Signature**: _________________

---

## APPENDIX B: THE NON-DISCLOSURE AGREEMENT

The NON-DISCLOSURE AGREEMENT, (hereinafter known as "the Agreement", is entered into between {{ employee_name }} (hereinafter known as "the Contractor/Intern/Employee") and {{ company.name }} (hereinafter known as "the Organization"), (collectively known as "the Parties"), as of this {{ contract_date }}.

### (A) Scope of the Agreement

The Agreement acknowledges that certain information, trade secrets, and proprietary data (hereinafter known as "Confidential Information") of or regarding the Organization and/or the Organization's business may be discussed between the Contractor/Intern/Employee and the Organization.

### (B) Confidential Information

For the purpose of this clause, Confidential Information includes (but shall not be limited to) trade secrets, technical know-how, any information relating to customers, operations and financial information and commercial methods of the Organization, any material, knowledge, and data (verbal, electronic, written and/or in any other form) concerning the Organization or the Organization's businesses, not generally known to the public.

Except in carrying out your duties for the Organization, you must keep confidential and must not either during the course of your employment or at any time thereafter directly or indirectly disclose, publish or use for your own benefit or for the benefit of others either:
(i) Any of the Organization's and/or Organization's businesses Confidential Information or that of its customers without first having obtained the Organization's written consent to such disclosure, publication or use; or
(ii) Any information which has been disclosed to the Organization and/or the Organization's business by others under an agreement which requires the Organization and/or the Organization's business to keep such information confidential.

### (C) Previous Agreements

The Agreement constitutes the entirety of the Agreement and the signing thereof by both the Parties nullifies any and all previous agreements made between the Organization and the Contractor/Intern/Employee.

### (D) Modifications and Amendments

No modifications, amendments, rectifications, changes and/or alterations shall be made to the Agreement by either party unless in writing and signed by authorized representatives of both the Parties.

### (E) Successors and Assigns

The Agreement shall be binding upon the successors, subsidiaries, assigns and/or corporations controlling or controlled by the Parties. The Organization may assign the Agreement to any party at any time, whereas the Contractor/Intern/Employee is prohibited from assigning any of his/her rights or obligations in the Agreement without prior written consent from the Organization.

### (F) Nature of Contractual Relationship between the Parties

The Agreement:-
(i) does not constitute a contract of employment, nor does it guarantee the Contractor's/Intern's/Employees continuation of employment with the Organization; and
(ii) does not create a partnership or joint venture between the Organization and the Contractor/Intern/Employee.

### (G) Severability

Any provision within the Agreement (or any portion thereof) deemed invalid, unlawful or otherwise unusable by a court of law shall be dissolved from the Agreement and the remainder of the Agreement shall continue to be enforceable.

### (H) Governing Law

The Agreement shall be governed by the Malaysian laws.

### (I) Immunity

Disclosing Confidential Information to an attorney, government representative or court official in confidence while assisting or taking part in a case involving a suspected violation of law connected or related to the Organization and/or Organization's business is considered as a breach of the Agreement unless the Contractor/Intern/Employee is required to disclose Confidential Information by law.

### (J) Cause of Action

The Contractor/Intern/Employee understands that the use or disclosure of any Confidential Information may be cause for an action at law in an appropriate forum or in any court of law, and that the Organization shall be entitled to an injunction prohibiting the use or disclosure of the Confidential Information.

### (K) Indemnification

The Contractor/Intern/Employee understands and agrees that if the use or disclosure of Confidential Information by him/her or any affiliate, or representative of the Contractor/Intern/Employee causes damage, loss, cost or expense to the Organization and/or the Organization's business, the Contractor/Intern/Employee shall be held responsible and shall indemnify the Organization.

### (L) Injunctive Relief

The Contractor/Intern/Employee understands and agrees that the use or disclosure of Confidential Information could cause the Organization irreparable harm and the Organization has the right to pursue legal action beyond remedies of a monetary nature in the form of an injunctive or equitable relief.

### (M) Notice of Unauthorized Use or Disclosure

The Contractor/Intern/Employee is bound by the Agreement to notify the Organization in the event of a breach of the Agreement involving the dissemination of Confidential Information, either by the Contractor/Intern/Employee or a third party, the Contractor/Intern/Employee will do everything possible to help the Organization regains possession of the Confidential Information.

### (N) Costs and Expenses

In a dispute arising out of or in relation to the Agreement, if either party brings an action to enforce their rights under the Agreement, the winning party shall recover its costs and expenses (including reasonable attorney's fees) incurred in connection with the action and/or any appeal, from the losing party.

IN WITNESS WHEREOF, the Contractor/Intern/Employee hereto agrees to the terms of the Agreement and signed on the date written below.

**By**: _________________

**Name**: {{ employee_name }}

**Date**: _________________
