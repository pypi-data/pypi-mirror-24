"""
policy_api module includes policy-aware (vs. low-level database) interface
to policy's databases (contracts, sessions, etc).

  - Current consumer of policy_api is policy_server rest apis, which handle http-specific request logic and hand off to policy_api to take care of the policy-specific request logic.
  - These APIs could in theory also be used as an importable library for other components with an interest in the policy databases, e.g. a read-only interest. As the policy databases are stored in a distributed database such as mongo_db, those clients could share the database, not just the functionality.
"""
