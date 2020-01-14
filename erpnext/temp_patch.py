import watchdog
import csv
import frappe
from frappe.core.doctype.communication import email

def test():
	print 'testing watchdog'

def send_email(recipients, msg_body, custid=None,custcode=None):
	msg_subject = "Request to clear dues against your Web and Domain Services"
	msg_header  = "Dear Customer,"
	msg_footer = "Yours Sincerely"

	cc = []
	bcc= []

	email.make(
		doctype = 'Customers',
		name = custid,
		content = "{msg_header}<br/><br/>{msg_body}<br/><br/>Customer ID: {custid}<br/>Customer Code: {custcode}<br/><br/>{msg_footer}".format(
				custid=custid,
				custcode=custcode,
				msg_header=msg_header,
				msg_body=msg_body,
				msg_footer=msg_footer
			  ),
		subject = msg_subject,
		recipients=",".join(recipients),
		cc = ",".join(cc),
		bcc = ",".join(bcc),
		communication_medium='Email',
		send_email=True,
		send_me_a_copy=True,            #Sends a copy to bia@bt.bt
		#print_html=email_body          #Sends the print_html content as html attachment
	)

def bulk_email():
	counter = 0
	not_exist = 0
	total_due = 0
	file_path = "/home/frappe/erp/apps/erpnext/erpnext/domain_due_listt20191126.csv"
	with open(file_path) as src:
		data = csv.reader(src, delimiter=',')
		for row in data:
			counter += 1
			cust = None
			#if counter>10:
			#	break
			msg_body = "Your domain <b>{domain}</b> has total outstanding dues {dues}. Please clear the pending dues before 6th Dec 2019 to avoid service disconnection."

			if not frappe.db.exists("Customers", {"customer_code": str(row[1]).strip()}):
				not_exist += 1
				print "|".join([str(counter), str(row[1]), str(row[6]), str(row[8]), str(row[11]),str("ERROR")])
			else:
				cust = frappe.db.get_value("Customers", {"customer_code": str(row[1]).strip()}, "name")
				print "|".join([str(counter), str(row[1]), str(row[6]), str(row[8]), str(row[11]),cust,str("SUCCESS")])

			if row[11] != "TOTAL_AMOUNT":
				total_due += float(row[11])
				try:
					msg_body = msg_body.format(domain=str(row[8]).strip(),dues='Nu. {:,.2f}/-'.format(float(str(row[11]).strip())))
					send_email([str(row[6]).strip()], msg_body, cust, str(row[1]).strip())
				except Exception, e:
					print 'ERROR: ', str(e)
				

	print "Total records: {0}".format(counter)
	print "Total no.of customers not found: {0}".format(not_exist)
	print "Total Due Amount: {0}".format(total_due)

# bench execute erpnext.temp_patch.bulk_email_20190113 --args "1,"
def bulk_email_20190113(debug=1):
	counter = 0
	not_exist = 0
	test = 0
	file_path = "/home/frappe/erp/apps/erpnext/erpnext/Copy of dues 2020-workout.csv"
	with open(file_path) as src:
		data = csv.reader(src, delimiter=',')
		for row in data:
			counter += 1
			cust = None
			#if counter>10:
			#	break
			msg_body = "Your domain <b>{domain}</b> has outstanding dues for bill period(01-JAN-2018 to 01-JAN-2019). Please clear the pending dues before 15th January, 2020 to avoid permanent disconnection of the service."

			# ignore first row
			if counter == 1:
				continue

			if test and counter > 5:
				break

			if not frappe.db.exists("Customers", row[0].strip()):
				not_exist += 1
				print "|".join([str(counter), str(row[0]), str(row[1]), str(row[2]), str(row[3]),str(row[4]),str("ERROR")])
			else:
				cust = frappe.db.get_value("Customers", row[0].strip(), ["name", "customer_code"])
				print "|".join([str(counter), str(row[0]), str(row[1]), str(row[2]), str(row[3]),str(row[4]),str("SUCCESS")])

			if not debug:
				try:
					msg_body = msg_body.format(domain=str(row[4]).strip())
					send_email([str(row[2]).strip()], msg_body, cust[0] if cust else None, cust[1] if cust else None)
				except Exception, e:
					print 'ERROR: ', str(e)

	print "Total records: {0}".format(counter)
	print "Total no.of customers not found: {0}".format(not_exist)
