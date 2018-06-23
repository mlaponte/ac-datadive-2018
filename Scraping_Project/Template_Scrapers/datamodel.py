from enum import Enum

class Fields(Enum):
	# part 1: General Project information
	IAM = "IAM"
	IAM_ID = "IAM_id"
	YEAR = "year"
	COUNTRY = "country"
	PROJECT_NAME = "project_name"
	PROJECT_ID = "project_id"
	PROJECT_NUMBER = "project_number"
	# comma separated list of values
	RELATED_PROJECT_NUMBER = "related_project_number"
	PROJECT_TYPE = "project_type"
	PROJECT_LOAN_AMOUNT = "project_loan_amount"
	SECTOR = "sector"
	ISSUES = "issues"
	FILERS = "filers"
	FILING_DATE = "filing_date"
	ENVIRONMENTAL_CATEGORY = "enviromental_category"
	COMPLAINT_STATUS = "complaint_status"
	DATE_CLOSED = "date_closed"
	# link to the project
	HYPERLINK = "hyperlink"

	# part 2 : project life cycle stage information
	REGISTRATION_START_DATE = "registration_start_date"
	REGISTRATION_END_DATE = "registration_end_date"
	ELIGIBILITY_START_DATE = "eligibility_start_date"
	ELIGIBILITY_END_DATE = "eligibility_end_date"
	DISPUTE_RESOLUTION_START_DATE = "dispute_resolution_start_date"
	DISPUTE_RESOLUTION_END_DATE = "dispute_resolution_end_date"
	COMPLIANCE_REVIEW_START_DATE = "compliance_review_start_date"
	COMPLIANCE_REVIEW_END_DATE = "compliance_review_end_date"
	MONITORING_START_DATE = "monitoring_start_date"
	MONITORING_END_DATE = "monitoring_end_date"
	IS_COMPLIANCE_REPORT_ISSUED = "is_compliance_report_issued"
	
	# part 3: comma separate list of links to documents
	DOCUMENTS = "documents"


