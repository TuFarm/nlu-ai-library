# Admin Web

Admin Web is the staff interface, separate from the public kiosk. It keeps the sidebar layout for dashboard metrics, knowledge sources, conversation logs, user views, survey management, reports and feature status.

Phase 2 data is illustrative. Upload does not store or parse files; tables do not mutate records; authentication and role checks are not implemented. Before deployment, protect every `/admin` page and `/api/v1/admin` route with staff authentication, authorization and audit logging.
