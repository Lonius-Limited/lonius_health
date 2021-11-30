import frappe
import datetime
from frappe import _ 
from frappe.model.workflow import get_workflow_name
from frappe.utils import get_fullname

#UPDATE THE QUEUE LOG ON WORKFLOW STATE CHANGE
def update_queue_state(doc, handler=None):
    if doc.get("queue_log") is None: return
    logged_in_user = frappe.session.user
    queue_log_table = frappe.new_doc("Queue Log")
    action_user = get_fullname(logged_in_user)
    workflow_state = doc.get('workflow_state')
    if not workflow_state: workflow_state = 'Checked In'
    if workflow_state == 'Consultation': workflow_state = 'Start Consult'
    if not frappe.db.exists({"doctype": "Queue Log", "parenttype": doc.get("doctype"), "parent": doc.get("name"), "action": workflow_state}):
        queue_log_table.update(
            {
                "doctype": "Queue Log",
                "parenttype": doc.get("doctype"),
                "parent": doc.get("name"),
                "parentfield": "queue_log",
                "action": workflow_state,
                "timestamp": frappe.utils.data.now_datetime(),
                "user": action_user,
                "idx": len(doc.queue_log) + 1,
            }
        )
        doc.queue_log.append(queue_log_table)
    return

#UPDATE THE WORKFLOW STATE OF THE ENCOUNTER DIRECTLY
def change_encounter_workflow_state(encounter_document_name, proposed_workflow_state):
    workflow_name = get_workflow_name('Patient Encounter')
    if not workflow_name: return
    current_workflow_state = frappe.db.get_value('Patient Encounter', encounter_document_name, "workflow_state")
    if current_workflow_state == proposed_workflow_state: return
    if is_valid_encounter_workflow_state(proposed_workflow_state):
        encounter_doc = frappe.get_doc('Patient Encounter', encounter_document_name)
        encounter_doc.set('workflow_state', proposed_workflow_state)
        encounter_doc.save()
        encounter_doc.notify_update()
    else:
        frappe.msgprint('The workflow state is not valid')
    return

def is_valid_encounter_workflow_state(workflow_state):
    return workflow_state in ('Checked In', 'Vitals Taken', 'Consultation', 'Consult Ended', 'Reviewed', 'Visit Aborted')

def vitals_submitted_update_encounter(doc, handler=None):
    encounter_workflow_state = 'Vitals Taken'
    #GET CURRENT ACTIVE ENCOUNTER
    patient = doc.get('patient')
    encounter = get_checked_in_encounter(patient)
    if encounter:
        change_encounter_workflow_state(encounter[0].get('name'), encounter_workflow_state)


def get_checked_in_encounter(patient):
    checked_in_encounter = frappe.get_list('Patient Encounter', filters={
        'workflow_state':'Checked In',
        'patient': patient
    })
    if len(checked_in_encounter) > 0:
        return checked_in_encounter
    return False

@frappe.whitelist()
def get_lab_profile_tests(docname=None):
    if not docname or docname == '': return []
    return frappe.get_list('Lab Profile Templates', filters={
        'parent': docname
    }, fields=["*"])