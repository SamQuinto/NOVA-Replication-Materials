# Exercise materials

| Folder | Contents |
| --- | --- |
| [job](job/) | Flexible and fixed nine-issue role materials in Word and PDF |
| [tutorial](tutorial/) | Venue-hire practice exercise in Word and PDF |
| [scoring_tables](scoring_tables/) | Exact JSON definitions and readable scoring-table workbook |
| [questionnaires](questionnaires/) | Main-study and role-feedback questions in Word, PDF and YAML; analysis schema in JSON |

Role documents contain both private roles for research use. During a study, give each negotiator only their assigned role. Do not expose both parties' scoring values in the flexible exercise.

JSON files preserve historical snapshots. `fixed-9.json` retains other definitions internally, but its active table has nine issues and at most five representative options per issue. Continuous domains and interpolation rules are authoritative in JSON; the workbook is a readable index, not a replacement scoring engine.

The analysis schema supplies historical question labels. The deployment YAML also includes interface/payment information. Candidate and recruiter feedback questionnaires differ. Response data are in section 3, not inside the questionnaire files.
