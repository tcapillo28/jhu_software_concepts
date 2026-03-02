Operational Notes
=================

Busy-State Policy
-----------------
The application prevents overlapping pulls by using a busy flag stored in memory.

Idempotency Strategy
--------------------
Duplicate rows are prevented by checking unique keys before insertion.

Uniqueness Keys
---------------
Rows are uniquely identified by a combination of fields extracted from Grad Café posts.