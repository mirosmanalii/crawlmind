# CRAWLMIND
A thinking crawler, not a scraper.

Crawlmind is a production-grade system that: 
  - Autonomously navigates complex web applications using a real browser (e.g. Playwright)
  - Handles login flows, pagination, and multi-step user workflows
  - Classifies page types based on DOM/control composition

Captures signals such as:
  - Broken links
  - Form validation failures
  - Console/runtime errors
  - Layout overlaps and UI issues
  - Performance bottlenecks
  - Classifies defects into: Functional, UI, Performance, Accessibility, Content, Security
  - Scores and prioritizes defects using severity, frequency, reproducibility, and impact
  - Produces structured, machine-readable outputs for downstream systems

## Page types:
## 1. ERROR
### Semantic Meaning
The page represents a system failure or runtime crash.

### Must Satisfy At Least One
* `status_code >= 500`
* `400 <= status_code < 500`
* `console_errors present AND status_code == 200`

### Must Override All Other Types
* ERROR is terminal and highest priority.

### Must NOT Require
* DOM structure
* Forms
* Tables

## 2. LOGIN
### Semantic Meaning
Primary purpose is authentication via credentials.

### Must Satisfy One of:

### Strong structural condition
* `has_password_input == True`
* `has_username_input == True`
* `submit_button_count > 0`

### OR Strong URL intent
* URL contains login / signin

### Must NOT Be
* Multi-field registration form (unless it has password + username combo)

### Must Override
* FORM
* DASHBOARD
* DETAIL

## 3. AUTH_CHALLENGE
### Semantic Meaning
Secondary authentication step (OTP, MFA, SSO challenge).

### Must Satisfy One of:
* URL contains OTP / verify / challenge / two-factor
* Small form (≤2 inputs)
* No password field
* Redirect detected

### Must NOT Be
* Full login page
* Multi-field data form

## 4. EMPTY
### Semantic Meaning
Page has no data to display.

### Must Satisfy
* `empty_state_detected == True`

### Must Override
* LISTING
* DETAIL
* DASHBOARD

## 5. LISTING
### Semantic Meaning
Page displays multiple records of similar structure.

### Must Satisfy One of:
* `table_count > 0 AND pagination_controls == True`
* `table_count > 1`

### Must NOT Be
* Single record
* Pure dashboard
* Form page

### Structural Traits
* Repeating rows
* Page navigation

## 6. DETAIL
### Semantic Meaning
Single-record structured view.

### Must Satisfy
* `table_count == 1`
* `pagination_controls == False`
* `has_form == False`

### Must NOT Be
* Listing
* Form
* Dashboard

## 7. FORM
### Semantic Meaning
Primary purpose is structured data entry.

### Must Satisfy
* `has_form == True`
* `input_count >= threshold`
* `not has_password_input`

### Must NOT Be
* LOGIN
* AUTH_CHALLENGE
* Minor search form embedded in landing page

### Key Requirement (To Be Refined Later)
* Form must dominate page content
* Not just a utility widget

## 8. PAGINATION
### Semantic Meaning
Explicit navigation-only page.

### Must Satisfy
* `pagination_controls == True`
* `table_count == 0`

### Must NOT Be
* Listing with content
* Dashboard

## 9. DASHBOARD
### Semantic Meaning
Landing page aggregating multiple content blocks.

### Must Satisfy
* `content_block_count >= threshold`
* No dominant form
* No pagination
* `table_count == 0`
* Not empty

### Must NOT Be
* Login
* Listing
* Detail
* Form

## 10. UNKNOWN
### Semantic Meaning
No deterministic classification matched.

### Must Occur When
* No rule fires
* Confidence < threshold
* Ambiguous structure

## Current Severity Mapping (v1)
* 5xx Server Error = 9
* 4xx Client Error = 7
* Console Error	= 6
* Network Failure	= 6
* Slow Page Load = 6
* Long Tasks = 5
* Layout Overlap = 5
